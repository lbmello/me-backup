
import socket
import subprocess


class Server:
    HOST = '127.0.0.1'
    PORT = 13123     

    def __init__(self):
        process = subprocess.call(self.wait_connection(), stdout=self.stdout, stderr=self.stderr, shell=True)
        print(self.stderr)


    def wait_connection(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((Server.HOST, Server.PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)