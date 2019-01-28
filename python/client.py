import time
import socket

def connect():
    sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM ) #socket.SOCK_DGRAM
    sock.connect(('192.168.4.1',5000))
    sock.send(b'initialise')
    return sock

if __name__ == "__main__":
    sock = connect()
    
    while True:
        sock.send(b'HI')
        print(sock.recv(1024))