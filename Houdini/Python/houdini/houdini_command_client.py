import hou
from schmod.schmod_command_server.base_command_client import BaseCommandClient

class HoudiniCommandClient(BaseCommandClient):
    def __init__(self, client_type=''):
        super().__init__(client_type=client_type)
    
    def run_command(self, message):
        print (message)
        # TODO Eval