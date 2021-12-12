import enum
from os import close, remove
import socket
import threading

class ClientType(enum.Enum):
    TESTING = -1
    BLENDER = 1
    HOUDINI = 2
    UNREAL = 3
    UNITY = 4

class CommandTypeToken(enum.Enum):
    CLIENT_TYPE = 1
    COMMAND = 2
    MESSAGE = 3
    BROADCAST = 4
    QUIT = 99

class Command(enum.Enum):
    VERBATIM = 1
    TRANSLATE = 2
    ROTATE = 3
    SCALE = 4

class CommandClient():
    def __init__(self, client_type, socket_connect, socket_address):
        self.client_type = client_type
        self.socket_connect = socket_connect
        self.socket_address = socket_address

class CommandServer():
    def __init__(self, auto_start=True):
        self.BUFFER_SIZE = 4096
        self.IP = socket.gethostbyname(socket.gethostname())
        self.PORT = 21111
        self.BACKLOG = 5
        self.is_running = False

        self.client_list = {}

        if auto_start:
            self.start_server()

    def broadcast_to_clients(self, message):
        for key, value in self.client_list.items():
            try:
                value.socket_connect.send(message.encode('utf-8'))
                print ('Broadcasting message to all clients')
            except:
                value.socket_connect.close()
                self.remove_client(value)
    
    def shutdown_all_clients(self):
        for key, value in self.client_list.items():
            value.socket_connect.shutdown(1)
            value.socket_connect.close()
        
        self.client_list.clear()

    def remove_client(self, client):
        print ('Removing Client: {0}'.format(client.client_type))
        del self.client_list[client.client_type]

    def wait_for_connections(self):
        while self.is_running: # Server poll
            try:
                client_socket, address = self.server_socket.accept()
                print ('New Client Connected: {0}'.format(address))
                send_cmd = 'Successfully connected to the Command Server. Waiting for [CLIENT_TYPE]'.encode('utf-8')
                client_socket.send(send_cmd)
                
                # Start get Client Type
                threading.Thread(target=self.wait_for_client_type, args=(client_socket, address)).start()
            except:
                break
    
    def wait_for_client_type(self, client, address):
        """Wait for client type input before actually handling commands"""
        client_type_msg = client.recv(self.BUFFER_SIZE)
        if client_type_msg:
            decode_client_type = client_type_msg.decode('utf-8')
            if decode_client_type.startswith('[{0}]'.format(CommandTypeToken.CLIENT_TYPE.name)):
                # Get client type from message
                client_type = decode_client_type[(len(CommandTypeToken.CLIENT_TYPE.name) + 2):].strip()
                self.client_list[client_type] = CommandClient(client_type, client, address)
                print ('Client [{0}] connected. Starting listen.'.format(client_type))

                # Start listening
                threading.Thread(target=self.wait_for_commands, args=(client,)).start()
            else:
                # If this is wrong then should just close connection
                client.send('Incorrect [CLIENT_TYPE]. Closing connection.'.encode('utf-8'))
                client.close()

    def wait_for_commands(self, client):
        while self.is_running:
            try:
                command = client.recv(self.BUFFER_SIZE)
                if command:
                    print ('Command recieved')
                    self.interpret_command(command.decode('utf-8'))
                else:
                    self.remove_client(client)
                    continue
            except:
                continue

    def interpret_command(self, command):
        if command.startswith('[{0}]'.format(CommandTypeToken.COMMAND.name)):
            print ('Run Command')
        elif command.startswith('[{0}]'.format(CommandTypeToken.MESSAGE.name)):
            print ('Printing')
            print (command[(len(CommandTypeToken.MESSAGE.name) + 2):].strip())
        elif command.startswith('[{0}]'.format(CommandTypeToken.BROADCAST.name)):
            print ('Broadcasting')
            self.broadcast_to_clients(command[(len(CommandTypeToken.BROADCAST.name) + 2):].strip())
        elif command.startswith('[{0}]'.format(CommandTypeToken.QUIT.name)):
            print ('Closing Server')
            self.close_server()
        else:
            print ('Why')

    def close_server(self):
        print ('Command Server Stopped: ({0}, {1})'.format(self.IP, self.PORT))
        self.is_running = False
        
        try:
            if len(self.client_list.items()) > 0:
                self.shutdown_all_clients()
                self.server_socket.shutdown(1)
            
            self.server_socket.close()
        except socket.error as msg:
            pass
            self.server_socket.close()

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.IP, self.PORT))
        self.server_socket.listen(self.BACKLOG)
        print ('Command Server Started: ({0}, {1})'.format(self.IP, self.PORT))
        self.is_running = True
        
        self.wait_for_connections()

if __name__ == '__main__':
    command_server = CommandServer()