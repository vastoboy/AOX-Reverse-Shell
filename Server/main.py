import os
from aox_server import AOXServer



art = """
         █████╗  ██████╗ ██╗  ██╗     ███████╗██╗  ██╗███████╗██╗     ██╗     
        ██╔══██╗██╔═══██╗╚██╗██╔╝     ██╔════╝██║  ██║██╔════╝██║     ██║     
        ███████║██║   ██║ ╚███╔╝█████╗███████╗███████║█████╗  ██║     ██║     
        ██╔══██║██║   ██║ ██╔██╗╚════╝╚════██║██╔══██║██╔══╝  ██║     ██║     
        ██║  ██║╚██████╔╝██╔╝ ██╗     ███████║██║  ██║███████╗███████╗███████╗
        ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
"""

print(art)


client_folder = "ClientFolder"
aox_server = AOXServer("192.168.1.209", 4001, client_folder)


if not os.path.exists(client_folder):
    os.mkdir(client_folder)


aox_server.print_guide()
aox_server.start()


