from socket import timeout
from threading import Thread
from queue import Queue
from time import sleep
from networking.packet import Packet

BUFFER_SIZE = 2048

class Connection():
    def __init__(self):
        """
        The constructor. 
        Derived classes have to implement self._start() and override self.socket with a local endpoint.

        :attr bool self.connected: is the connection established
        :attr socket.socket self.socket: local socket endpoint
        :attr queue.Queue self.recv_queue: queue for packets to be sent
        :attr queue.Queue self.send_queue: queue for received packets
        :attr queue.Queue self._interrupt_queue: queue for interrupting the connection
        :attr queue.Queue self._closure_queue: queue used when closing the connection
        """
        self.connected = False
        self.socket = None
        self.recv_queue = Queue()
        self.send_queue = Queue()
        self._interrupt_queue = Queue()
        self._closure_queue = Queue()
    
    def create(self, ip, port):
        """
        Create a daemon thread for establishing connection.
        Call start() on the thread when you want to start connecting.

        :param string ip: The IPv4 address
        :param int port: The port
        :return: The thread for establishing connection
        :rtype: threading.Thread
        """
        establish_connection = Thread(target=self._start, args=[ip, port])
        # This thread is a daemon thread -> child threads will also be daemons
        establish_connection.daemon = True
        return establish_connection

    def _start(self, ip, port):
        """
        Implement this method.
        Create a socket and establish connection.
        Then call start_send_recv().
        This method is called in create() when creating a new thread.
        """
        raise NotImplementedError

    def start_send_recv(self, socket):
        """
        Start the send and receive threads.
        Set connected status to True.

        :param socket.socket socket: The socket on which the send and receive operations will be processed
        """
        if self.socket == None:
            raise NotImplementedError("You must override self.socket")
        recv_thread = Thread(target=self._receive, args=[socket])
        recv_thread.start()
        send_thread = Thread(target=self._send, args=[socket])
        send_thread.start()
        self.connected = True

    def check_closure(self):
        """
        See if the connection was closed and how it was closed.

        :return: True if the closure was controlled, False if it was unexpected, None if the connection was not closed
        :rtype: bool or None
        """
        if not self._closure_queue.empty():
            if self._closure_queue.get() == True:
                return True
            else:
                return False
        else:
            return None

    def close(self):
        """
        Start closure procedure and inform the other end of the connection.
        The underlying socket and the threads will be closed when receiving and sending are halted.
        """
        self._interrupt_queue.put(True)

    def _controlled_closure(self, receiver, initiator):
        if initiator:
            try:
                data = [0]
                close_packet = Packet(data, Packet.T_CLOSE)
                receiver.send(close_packet.pack_data())
            except:
                print("Error in controlled closure: failed to send close packet.")
        self.connected = False
        self._closure_queue.put(True)

    def _uncontrolled_closure(self):
        self.connected = False
        self._closure_queue.put(False)

    def _send(self, receiver):
        while True:
            # Check the interrupt queue
            if self._interrupt_queue.empty() == False:
                controlled_interrupt = self._interrupt_queue.get(block=False)
                if controlled_interrupt:
                    self._controlled_closure(receiver, True)
                else:
                    self._uncontrolled_closure()
                print("Closing send-thread.")
                return

            if self.send_queue.empty() == False:
                packet = self.send_queue.get(False)
                data = packet.pack_data()
                try:
                    receiver.send(data)
                except OSError:
                    print("Error in sending data. Closing send-thread.")
                    self._uncontrolled_closure()
                    return

            sleep(0.001)

    def _receive(self, sender):
        sender.settimeout(0.1)

        while True:
            try:
                data = sender.recv(BUFFER_SIZE)
                if len(data) > 0:
                    packet = Packet(data)
                    if packet.type == Packet.T_CLOSE:
                        print("data:", packet.get_data(include_header=False))
                        if packet.get_data(include_header=False)[0] == 0:
                            # Initiator
                            initiator = False
                        else:
                            initiator = True
                        # Send the close packet back
                        self._controlled_closure(sender, initiator)
                        # Inform the send-thread that the connection is closing
                        self._interrupt_queue.put(True)
                        sleep(1)
                        self.socket.close()
                        print("Closing recv-thread")
                        return
                    self.recv_queue.put(packet)
            except timeout:
                pass
            except OSError:
                print("Error in receiving data. Closing recv-thread.")
                self._interrupt_queue.put(False)
                self._uncontrolled_closure()
                return

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
                packet = self.recv_queue.get(block=False)
                return packet
            else:
                packet = self.recv_queue.get(block=False)
                if packet.type == packet_type:
                    return packet
                else:
                    # The packet type is wrong so it will be put back in the queue
                    self.recv_queue.put(packet)
                    return None
        else:
            return None
