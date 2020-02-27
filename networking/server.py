import socket
from threading import Thread
from networking.connection import Connection

class Server(Connection):
    def __init__(self):
        Connection.__init__(self)

    def _start(self, ip, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind((ip, port))
        except OSError:
            print("Failed to bind the socket. The address/port might already be in use!")
            return
        self.socket.listen(5)
        print("Server started! Waiting for a client...")
        self.socket.settimeout(1.0)
        interrupt = False

        while True:
            if self._interrupt_queue.empty() == False:
                interrupt = self._interrupt_queue.get(False)
            try:
                if interrupt:
                    print("Server accept operation was interrupted. Closing the socket.")
                    self.socket.close()
                    return
                client, addr = self.socket.accept()
                print(f"Client connected from {addr}")
                break
            except socket.timeout:
                pass

        self.start_send_recv(client)
