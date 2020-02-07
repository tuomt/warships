import socket
from threading import Thread
from queue import Queue
import time
from networking.packet import Packet

IP_ADDRESS = "127.0.0.1"
PORT = 7772
ENCODING = "utf-8"
BUFFER_SIZE = 24

class Server():
    def __init__(self):
        self.recv_queue = Queue()
        self.send_queue = Queue()
        self.interrupt_queue = Queue()
        self.is_running = False
        self.connected = False

    def create(self, ip, port):
        # Create a thread for establishing the connection
        establish_connection = Thread(target=self._start, args=[ip, port])
        # This thread is a daemon thread -> inherited threads will also be daemons
        establish_connection.daemon = True
        return establish_connection

    def _start(self, ip, port):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((ip, port))
        self.is_running = True
        self._socket.listen(5)
        print("Server started! Waiting for a client...")
        self._socket.settimeout(1.0)
        interrupt = False

        while True:
            if self.interrupt_queue.empty() == False:
                interrupt = self.interrupt_queue.get(False)
            try:
                if interrupt:
                    print("Server accept operation was interrupted. Closing the socket.")
                    self._socket.close()
                    self.is_running = False
                    return
                client, addr = self._socket.accept()
                break
            except socket.timeout as e:
                pass

        # Set timeout back to default so it doesn't interfere with receiving data
        self._socket.settimeout(None) 
        print(f"Client connected from {addr}")
        recv_thread = Thread(target=self.receive, args=[client])
        recv_thread.start()
        send_thread = Thread(target=self.send, args=[client])
        send_thread.start()
        self.connected = True
            
    def close(self):
        self.send_queue.put("close")
        self._socket.close()
        self.is_running = False
        self.connected = False

    def send(self, receiver):
        while True:
            if self.send_queue.empty() == False:
                packet = self.send_queue.get(False)
                if packet.msg == "close":
                    print("Closing send-thread.")
                    return False
                receiver.send(packet.data)
                
    def receive(self, sender):
        while True:
            data = sender.recv(BUFFER_SIZE)
            if len(data) > 0:
                print("recv data:", data)
                packet = Packet.from_bytes(data)
                self.recv_queue.put(packet)
                print(f"Received: {packet.msg}")
                if packet.msg == "close":
                    # Inform the send-thread that the connection is closing
                    self.send_queue.put(packet)
                    print("Closing receive-thread.")
                    return False
            # Check the send queue in case we are going to shut down the connection
            if self.send_queue.empty() == False:
                incoming_packet = self.send_queue.get(False)
                if incoming_packet.msg == "close":
                    return False
