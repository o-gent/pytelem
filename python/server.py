import socket

def serve():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(('0.0.0.0',5000))
    sock.listen()

    client, addr = sock.accept()
    print(addr, " connected!")
    # initialised message
    print(addr, client.recv(1024))
    
    return client

if __name__ == "__main__":
    import time

    while True:
        sock = serve()
        time.sleep(0.1)
        data,addr = sock.recvfrom(1024)
        print(data, addr)