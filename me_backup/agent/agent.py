
import socket


class Agent:
    HOST = '127.0.0.1'
    PORT = 13123    
    
    def __init__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((Agent.HOST, Agent.PORT))
            s.sendall(b'Hello, world')
            data = s.recv(1024)

        print('Received', repr(data))

if __name__ == '__main__':
    Agent()