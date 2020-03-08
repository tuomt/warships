import socket
from threading import Thread
from networking.connection import Connection

class Client(Connection):
    def __init__(self):
        Connection.__init__(self)

    def _start(self, ip, port):
        interrupt = False
        print("Trying to connect to:", ip, port)
        while True:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(1.0)

            if self._interrupt_queue.empty() == False:
                interrupt = self._interrupt_queue.get(block=False)
            try:
                if interrupt:
                    print("Connecting operation was closed. Closing the socket.")
                    self.socket.close()
                    self.socket = None
                    return
                self.socket.connect((ip, port))
                print(f"Connected to {ip}:{port}")
                break
            except socket.timeout:
                pass
            except ConnectionRefusedError:
                self._closure_queue.put(False)
                return
            
        self.start_send_recv(self.socket)
