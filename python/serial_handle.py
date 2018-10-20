# any functions named __x are for internal use only. 
import serial
import random as r


# for reference
packet_structure = {
    'ACK' : bool,                   #0
    'packets_left_in_round' : int,  #1
    
    'id' : int,                     #2
    'data_type' : int,              #3  EC = 1
    'packet_number' : int,          #4
    
    'payload' : list,               #5:
    
    'check_sum' : int               #-1:
}


class datalink():
    def __init__(self, port):
        # start serial connection
        self.conn = serial.Serial(port, 115200)
        #initise class wide variables
        # next two are legacy
        self.packet_num = 1
        self.data = [0 for i in range(20)]
        # new vars
        self.packets = {}
        self.__idnum = 0 # makes sure each id made is unique
        self.__queue = []
        self.__order = 'unset'
        # initialises data stream..
        self.stream_start()


    def stream_start(self):
        # decides order of send receive
        def test():
            # could be anything as long as definitive result
            local = r.randint(0,100)
            self.__serial_send(str(local))
            remote = self.__serial_receive()
            self.__serial_send(str(local))
            return remote, local
        
        # checks if test is definitive
        while True:
            remote, local = test()
            try: 
                remote = int(remote)
                if remote == local:
                    pass
                else:
                    break
            except: pass
        
        # evaluates results
        if remote > local:
            self.order = 'remote' # remote starts stream first
        else:
            self.order = 'local' # local starts stream first
        print(self.order)


    def __id_register(self, id_str, ACK):
        'needs work as could be conflict from each device creating same IDs'
        
        # store packet information under unique numerical id
        self.packets[self.__idnum] = {}
        # save string name under numerical id for incoming messages
        self.packets[self.__idnum]['id'] = id_str
        
        # linking id_str to id_number for lookup during sending 
        self.packets[id_str] = self.__idnum

        self.__idnum += 1 # increment for next handshake
        
        # fetching numerical id again (fudging)
        id_num = self.packets[id_str]
        # setting attributes for id
        self.packets[id_num]['packet_num'] = 0
        if ACK: self.packets[id_num]['ACK'] = 1
        else: self.packets[id_num]['ACK'] = 0
        self.packets[id_num]['payload'] = [0]


    def serial_handler(self):
        """ handles packets """
        # initialises scope variables for use in secondary functions
        received_status = 0
        send_left = len(self.__queue)
        receive_left = 0
        
        # logic for send/receive order based on which platform started
        # keep sending/receiving while either side has packets left for cycle
        if self.order == 'local':
            __send()
            while send_left > 0:
                __send()
            while receive_left > 0:
                __send()
        if self.order == 'remote':
            __receive()
            __send()
            while send_left >0 :
                __send()
            while receive_left > 0:
                __send()

        # secondary function of serial_handler
        def __send():
            """ calls __receive() each cycle """
            # check if anything in queue
            if self.__queue:
                # cycle through queue
                for __ in self.__queue:
                    # get an id from queue
                    id_num = self.__queue.pop()

                    # fetch packet data
                    send_left = len(self.__queue)
                    payload = self.packets[id_num]['payload']
                    packet_num = self.packets[id_num]['packet_num']
                    self.packets[id_num]['packet_num'] += 1
                    ack = self.packets[id_num]['ACK']
                    last_packet_received = 1
                    checksum = 0
                    # form packet
                    packet = []
                    packet.append(last_packet_received)
                    packet.append(send_left)
                    packet.append(id_num)
                    packet.append(ack)
                    packet.append(packet_num)
                    for i in payload:
                        packet.append(i)
                    packet.append(checksum)

                    # store id incase failure
                    self.temp_id = id_num
                    # serialise packet
                    string = self.__serialise(packet)
                    # send
                    self.__serial_send(string)
                    # wait for error checking
                    __receive()
            else:
                # send default packet
                packet = [1,0]
                self.__serial_send(self.__serialise(packet))
                __receive()

        # secondary function of serial_handler
        def __receive():
            raw_message = self.__serial_receive()
            packet = self.deserialise(raw_message)
            # will continue if packet was correct
            if packet:
                # catch failed send packets..
                if packet[0] == 0:
                    # read failed id and go back to __send()
                    self.__queue.append(self.temp_id)
                    # FUDGE: makes sure packet number is same as last time as it will be incremented
                    self.packets[self.temp_id]['packet_num'] -= 1
                    __send()
                
                # continue if normal
                received_status = 1

                # if id not registered, register.
                if not self.packets[packet[2]]:
                    if packet[3] == 1:
                        ack = True
                    else: 
                        ack = False
                    self.__id_register(packet[2], ack)
                
                # fetch data from packet and store
                id_num = packet[2] # get id
                self.packets[id_num]['packet_num'] += 1         # increment packet num
                self.packets[id_num]['payload'] = packet[5:-1]  # store payload
            
            # if packet not correct.. 
            else:
                print("incoming packet failed - requesting new")
                received_status = 0
                # request new packet with special packet and recurse
                self.__serial_send('<0>') # FUDGE
                __receive()


    def get_packet(self):
        """ LEGACY: fetches raw serial data from buffer, returns payload as list """

        raw_message = self.__serial_receive()
        datapacket = self.deserialise(raw_message)
        
        if datapacket:
            self.data = datapacket
            self.__serial_send("1")
            self.packet_num += 1
        else:
            print("packet not recieved sucessfully")
            self.__serial_send("0") # request new data packet
            # call packet_handle again..
            self.get_packet() 

        #returns full packet for debugging for now.
        return self.data 


    def deserialise(self, raw_message):
        """ runs consistancy checks on packet, returns false if not consistent, else returns packet """

        # NEEDS CHANGING TO SUPPORT ID LOOKUP

        test1 = False
        test2 = False
        verified = False

        # first check 
        if raw_message.startswith("<") and raw_message.endswith(">\n"): test1 = True
        else: test1 = False

        # second check + try, except loop if no "-" exist
        try:
            datapacket = raw_message[1:-1].split("-")

            if int(datapacket[2]) == self.packet_num: test2 = True
            else: test2 = False

        except:
            verified = False

        if test1 and test2: verified = True

        if verified: return datapacket
        else: return False


    def __serial_send(self, message):
        """ place holder """
        self.conn.write(bytes(message, "utf-8"))
        print('sent: ', message)


    def __serial_receive(self):
        """ returns string from serial """
        r = ""
        # COULD BE ISSUE?
        while len(r) == 0:
            r = self.conn.readline().decode("utf-8")
        print('recieved: ', r)
        return r


    def send(self, id_str = 'default', message = [0], ACK = True):
        """ send an array, specify id_str for multiple messages to different places """
        
        # check if exists, if not then register
        if not self.packets[id_str]:
            self.__id_register(id_str, ACK)
        
        id_num = self.packets[id_str]
        # adds payload to ID dictionary
        self.packets[id_num]['payload'] = message
        # adds ID to queue
        self.__queue.append(id_num)


    def __serialise(self, packet : list) -> str:
        output = "<"
        for i in output:
            output += str(i)
            output += "-"
        output += ">"
        return output