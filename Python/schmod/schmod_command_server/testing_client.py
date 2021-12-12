import socket
import sys


class TestingClient():
    def __init__(self, auto_connect=True):
        self.BUFFER_SIZE = 4096
        self.IP = socket.gethostbyname(socket.gethostname())
        self.PORT = 21111
        self.is_connected = False

        if auto_connect:
            self.connect()
            self.listen()

    def connect(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.connect((self.IP, self.PORT))
            self.is_connected  = True
        except:
            print ('Could not establish a connection to the Command Server')

    def listen(self):
        while self.is_connected:
            command = self.server_socket.recv(self.BUFFER_SIZE)
            if command:
                decode = command.decode('utf-8')
                print (decode)
                if '[CLIENT_TYPE]' in decode:
                    client_type_msg = '[CLIENT_TYPE] TESTING'.encode('utf-8')
                    self.server_socket.send(client_type_msg)
                
            self.server_socket.send('[QUIT]'.encode('utf-8'))

if __name__ == '__main__':
    test_client = TestingClient()