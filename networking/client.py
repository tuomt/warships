import socket
from threading import Thread
from queue import Queue
import time
from networking.packet import Packet

IP_ADDRESS = "127.0.0.1"
PORT = 7772
ENCODING = "utf-8"
BUFFER_SIZE = 2048

class Client():
    def __init__(self):
        self.connected = False
        self.recv_queue = Queue()
        self.send_queue = Queue()
        self.interrupt_queue = Queue()
        self._socket = None

    def create(self, ip, port):
        # Create a thread for establishing the connection
        establish_connection = Thread(target=self._start, args=[ip, port])
        # This thread is a daemon thread -> inherited threads will also be daemons
        establish_connection.daemon = True
        return establish_connection

    def _start(self, ip, port):
        interrupt = False
        print("Trying to connect to:", ip, port)
        while True:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(1.0)

            if self.interrupt_queue.empty() == False:
                interrupt = self.interrupt_queue.get(False)
            try:
                if interrupt:
                    print("Connecting operation was closed. Closing the socket.")
                    self._socket.close()
                    self._socket = None
                    return
                self._socket.connect((ip, port))
                break
            except socket.timeout as e:
                pass
            
        # Set timeout back to default so it doesn't interfere with receiving data
        self._socket.settimeout(None) 
        print(f"Connected to {ip}:{port}")
        recv_thread = Thread(target=self.receive, args=[self._socket])
        recv_thread.start()
        send_thread = Thread(target=self.send, args=[self._socket])
        send_thread.start()
        self.connected = True
            
    def close(self):
        self.interrupt_queue.put(True)
        self._socket.close()
        self._socket = None
        self.connected = False

    def send(self, receiver):
        while True:
            # Check the interrupt queue
            if self.interrupt_queue.empty() == False:
                interrupt = self.interrupt_queue.get()
                if interrupt:
                    print("Closing send-thread.")
                    return False

            if self.send_queue.empty() == False:
                packet = self.send_queue.get(False)
                data = packet.pack_data()
                receiver.send(data)
                            
    def receive(self, sender):
        while True:
            # Check the interrupt queue in case we are going to shut down the connection
            if self.interrupt_queue.empty() == False:
                interrupt = self.interrupt_queue.get(False)
                if interrupt:
                    return False

            data = sender.recv(BUFFER_SIZE)
            if len(data) > 0:
                packet = Packet(data)
                self.recv_queue.put(packet)
                if packet.type == Packet.T_CLOSE:
                    # Inform the send-thread that the connection is closing
                    self.interrupt_queue.put(True)
                    print("Closing receive-thread.")
                    return False

    def get_packet(self, packet_type=None):
        """
        Get a packet from the receive queue.
        If a packet with the specified type is not found in the queue, return None.
        If a packet_type is not provided, the first packet in the queue will be returned.
        If there are no packets in the queue, return None.

        :param int packet_type: one of the T_ prefixed constants of the Packet class
        :return: the first packet in the queue that is of the type packet_type
        :rtype: Packet or None
        """

        if self.recv_queue.empty() == False:
            if packet_type == None:
                packet = self.recv_queue.get(False)
                return packet
            else:
                packet = self.recv_queue.get(False)
                if packet.type == packet_type:
                    return packet
                else:
                    # The packet type is wrong so it will be put back in the queue
                    self.recv_queue.put(packet)
                    return None
        else:
            return None
