import serial


class datalink():
    def __init__(self, port):
        self.conn = serial.Serial(port, 9600)
        self.packet_num = 1
        self.data = [0 for i in range(20)]

        #send initial ready packet
    

    def packet_handle(self):
        raw_message = self.conn.readline().decode("utf-8")
        datapacket = self.deserialise(raw_message)
        
        if datapacket:
            self.data = datapacket
            self.send("1")
            self.packet_num += 1
        else:
            print("packet not recieved sucessfully")
            self.send("0") # request new data packet
            # call packet_handle again..
            self.packet_handle() 

        return self.data 


    def deserialise(self, raw_message):
        # this is a bit messy..
        verified = False
        
        if raw_message.startswith("<") and raw_message.endswith(">\n"): 
            test1 = True
        else: 
            test1 = False

        try:
            datapacket = raw_message[1:-1].split("-")

            if int(datapacket[2]) == self.packet_num: 
                test2 = True
            else: 
                test2 = False
            
            print(test1, test2)
            if test1 and test2: verified = True

        except Exception:
            verified = False

        if verified:
            return datapacket
        else:
            return False


    def send(self, message):
        """ place holder """
        self.conn.write(bytes(message, "ascii"))