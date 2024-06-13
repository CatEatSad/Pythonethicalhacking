import socket
import hashlib


class Server:
    def __init__(self, ip, port):
        # Create Socket object
        listener = socket.socket(socket.AF_INET,
                                 socket.SOCK_STREAM)
        # Bind Server ip and port to connection
        listener.bind((ip, port))
        # Waiting to connect
        listener.listen(1)
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        self.client_ip = str(address)[2:17]
        print("[+] Got a connection from " + str(address))
        self.reliable_send("You are now connecting to " + ip)

    # For sending data
    def reliable_send(self, data):
        self.connection.send(data.encode())

    # For receiving data
    def reliable_receive(self):
        while True:
            try:
                return self.connection.recv(1024).decode()
            except ValueError:
                continue

    # run
    def start(self):
        check = True
        while True:
            result = self.reliable_receive()
            if result == "exit" or result == "":
                self.connection.close()
                break
            message, hashkey = result.split("|")
            calculated_hash = hashlib.sha256(message.encode() + b"B21DCAT099").hexdigest()
            # Close connection
            if calculated_hash == hashkey and check:
                check = False
                self.reliable_send("Hello, I am B21DCAT099 server")
            elif calculated_hash != hashkey:
                print("The received message has lost its integrity.")
                self.connection.close()
                break
            print("Message from " + self.client_ip + ": " + message)


my_listener = Server("192.168.189.133", 4444)
my_listener.start()
