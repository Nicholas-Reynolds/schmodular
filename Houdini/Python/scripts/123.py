import threading
from houdini.houdini_command_client import *

# Start Server
server_thread = HoudiniCommandClient('HOUDINI')
print ('Started python sever in thread: {0}'.format(server_thread))