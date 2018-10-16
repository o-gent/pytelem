# resisting urges to semicolon
from serial_handle import datalink


def main():
    # fetches and processes data, returns array with payload only
    data = link.get_packet()
    print(data)
    # do stuff


if __name__ == "__main__":
    # start communication with Arduino and initilise datalink class
    port = "COM4"
    link = datalink(port)
    
    while True:
        main()