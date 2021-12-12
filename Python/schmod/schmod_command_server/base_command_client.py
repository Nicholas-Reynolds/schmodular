import threading
import socket
import uuid

class BaseCommandClient(threading.Thread):
    """Placeholder"""
    def __init__(self, client_type='', auto_start=True):
        super(BaseCommandClient, self).__init__()

        self.__IP = socket.gethostbyname(socket.gethostname())
        self.__PORT = 21111

        self.__thread_running = True
        self.__guid = uuid.uuid4()
        self.__associated_socket = None
        self.__is_connected = False
        self.__client_type = client_type

        # Start Thread
        self.daemon = True
        if auto_start:
            self.start()
    
    def stop(self):
        self.__thread_running = False
        self.__associated_socket.close()
    
    def run_command(self, message):
        raise NotImplementedError('Need to impliment method to pass python run')

    # Connect
    def run(self):
        self.__associated_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__associated_socket.connect((self.__IP, self.__PORT))
        except Exception as e:
            print ('Except: {0}'.format(e))
            self.__associated_socket.close()
            self.__associated_socket = None
            return -1

        while self.__thread_running:
            message = self.__associated_socket.recv(4096)
            if message:
                decoded = message.decode('utf-8')
                if '[CLIENT_TYPE]' in decoded:
                    client_type_msg = ('[CLIENT_TYPE] {0}'.format(self.__client_type)).encode('utf-8')
                    self.__associated_socket.send(client_type_msg)
                else:
                    self.run_command(decoded)
            else:
                break

def start_server():
    thread_name = 'TestServer'
    
    server_thread = None
    for thread in threading.enumerate():
        if thread.name == thread_name:
            server_thread = thread
    
    if server_thread is None:
        thread = BaseCommandClient()
        thread.name = thread_name
        
    return thread

def stop_server():
    thread_name = 'TestServer'
    server_thread = None
    for thread in threading.enumerate():
        if thread.name == thread_name:
            server_thread = thread
           
    if server_thread is not None:
        server_thread.stop()

if __name__ == '__main__':
    stop_server()
