import ds
import sys
from .data import view

class Commands:
    def data_view(self, file: str):
        view(file)

def cli_runner():
    message = ds.cli_entry(sys.argv)
    method, params = message
    instance = Commands() 
    command = getattr(instance, method, None)
    if callable(command):
        command(**params)
    else:
        print(f"Command '{method}' not found.")