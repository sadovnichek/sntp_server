import queue
import socket
import threading

from sntpmessage import SNTPMessage


class Server:
    def __init__(self, offset):
        self.server_port = 123
        self.offset = offset
        self.received = queue.Queue()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(('127.0.0.1', self.server_port))
        self.receiver = threading.Thread(target=self.get_request)
        self.handler = threading.Thread(target=self.send_reply)

    def start(self):
        print(f"server started with offset={self.offset} on {self.server_port} port")
        self.receiver.setDaemon(True)
        self.receiver.start()
        self.handler.start()

    def send_reply(self):
        while True:
            packet, address = self.received.get()
            if packet:
                self.server.sendto(bytes(packet), address)

    def get_request(self):
        while True:
            data, addr = self.server.recvfrom(1024)
            message = SNTPMessage(data, self.offset)
            self.received.put((message, addr))
            print(f"Request from IP: {addr[0]}\tPort: {addr[1]}\n")
