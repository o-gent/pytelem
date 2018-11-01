from datalink import Datalink


def main():
    # fetches and processes data, returns array with payload only
    link.send(message = [0,1,2,3,4,5,6,7,8,9])
    link.serial_handler()
    print(link.get(id_=1))
    # do stuff


if __name__ == "__main__":
    # start communication with Arduino and initilise datalink class
    port = "COM4"
    link = Datalink(port)
    
    while True:
        main()