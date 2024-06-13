import socket
import hashlib
class Client:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET,
                                        socket.SOCK_STREAM)  
        self.connection.connect((ip, port))  
        print(self.reliable_receive())


    def reliable_send(self, data):
        self.connection.send(data.encode())

    def reliable_receive(self):
        while True:
            try:
                return self.connection.recv(1024).decode()
            except ValueError:
                continue

    def Encrypt(self,data):
        key = b"B21DCAT099"
        hash_value = hashlib.sha256(data.encode()+key).hexdigest()
        return data + "|"+hash_value
        
    def start(self):
        check = False
        while True:
            message_out = input("Message to Server : ")
            if message_out == "exit":
                self.connection.close()
                break
            message_to_send = self.Encrypt(message_out)
            self.reliable_send(message_to_send)
            if not check:
                if self.reliable_receive() == "Hello, I am B21DCAT099 server":
                    print("Hello, I am B21DCAT099 server")
                    check = True
            elif not check and self.reliable_receive() != "Hello, I am B21DCAT099 server"  :
                self.connection.close()
                break
           
  
my_backdoor = Client("192.168.189.133", 4444)
my_backdoor.start()

