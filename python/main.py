# resisting urges to semicolon
from serial_handle import datalink


def main():
    data = link.packet_handle()
    # do stuff


if __name__ == "__main__":
    port = "COM3"
    link = datalink(port)
    
    while True:
        main()