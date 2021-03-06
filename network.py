import socket
import pickle


# coded this class so we can re-use this class in the future
# initialising clients
class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.35"
        self.port = 8889
        self.addr = (self.server, self.port)
        self.symb = self.connect()

    def get_number(self):
        return self.symb

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048*16))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048*16))
        except socket.error as e:
            str(e)
