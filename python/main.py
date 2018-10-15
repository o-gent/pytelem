# resisting urges to semicolon
from serial_handle import datalink


def main():
    data = link.packet_handle()
    print(data)
    # do stuff


if __name__ == "__main__":
    port = "COM4"
    link = datalink(port)
    
    while True:
        main()