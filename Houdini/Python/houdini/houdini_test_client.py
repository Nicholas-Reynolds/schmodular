import socket

class HoudiniTestClient():
    def __init__(self, auto_connect=True):
        self.BUFFER_SIZE = 4096
        self.IP = socket.gethostbyname(socket.gethostname())
        self.PORT = 21111
        self.is_connected = False

        if auto_connect:
            self.connect()
            self.send()

    def connect(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.connect((self.IP, self.PORT))
            self.is_connected  = True
        except:
            print ('Could not establish a connection to the Command Server')
    
    def send(self):
        while True:
            msg = 'Test hello world'
            self.server_socket.send(msg.encode('utf-8'))
            self.server_socket.close()
            break

if __name__ == '__main__':
    test_client = HoudiniTestClient()