import serial
import random as r


class datalink():
    def __init__(self, port):
        # for reference
        self.packet_structure = {
            'ACK' : bool,                   #0
            'packets_left_in_round' : int,  #1
            
            'id' : int,                     #2
            'data_type' : int,              #3  EC = 1
            'packet_number' : int,          #4
            
            'payload' : list,               #5:
            
            'check_sum' : int               #-1:
        }

        # start serial connection
        self.conn = serial.Serial(port, 115200)
        
        #initise class wide variables
        self.packet_num = 1
        self.data = [0 for i in range(20)]

        self.packets = {}
        self.__idnum = 0
        self.__queue = []

        self.__order = 'unset'
        
        # initialises data stream..
        self.stream_start()


    def stream_start(self):
        # decides order of send receive
        def test():
            local = r.randint(0,100)
            self.__serial_send(str(local))
            remote = self.__serial_receive()
            self.__serial_send(str(local))
            return remote, local
        
        while True:
            remote, local = test()
            try: 
                remote = int(remote)
                if remote == local:
                    pass
                else:
                    break
            except: pass
        
        if remote > local:
            # remote starts stream first
            self.order = 'remote'
        else:
            # local starts stream first
            self.order = 'local'
        print(self.order)

    def __id_register(self, id_str, ACK):
        # needs work as could be conflict from each device creating same IDs 
        self.packets[self.__idnum] = {}
        self.packets[self.__idnum]['id'] = id_str
        # fudge lookup table for id on recieved packets 
        self.packets[id_str] = self.__idnum
        self.__idnum += 1 # increment for next handshake

        id_num = self.packets[id_str]

        self.packets[id_num]['packet_num'] = 0
        if ACK: self.packets[id_num]['ACK'] = 1
        else: self.packets[id_num]['ACK'] = 0
        self.packets[id_num]['payload'] = [0]


    #def handshake(self, id_, error_checking = True):
        #self.__id_register(id_, ACK = error_checking)
        # queues handshake packet
        #self.__queue.append(id_)


    def serial_handler(self):
        """ handles packets """
        received_status = 0
        send_left = len(self.__queue)
        receive_left = 0
        
        # logic for send/receive order based on which platform started
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

        def __send():
            """ calls __receive() each cycle """
            if self.__queue:
                for __ in self.__queue:
                    id_num = self.__queue.pop()
                    send_left = len(self.__queue)

                    # form packet
                    payload = self.packets[id_num]['payload']
                    packet_num = self.packets[id_num]['packet_num']
                    self.packets[id_num]['packet_num'] += 1
                    ack = self.packets[id_num]['ACK']
                    last_packet_received = 1
                    checksum = 0

                    packet = []
                    packet.append(last_packet_received)
                    packet.append(send_left)
                    packet.append(id_num)
                    packet.append(ack)
                    packet.append(packet_num)
                    for i in payload:
                        packet.append(i)
                    packet.append(checksum)

                    # store string incase failure
                    self.temp_id = id_num

                    string = self.serialise(packet)
                    # send
                    self.__serial_send(string)
                    # wait for error checking
                    __receive()
            else:
                # send default packet
                packet = [1,0]
                self.__serial_send(self.serialise(packet))
                __receive()

        def __receive():
            raw_message = self.__serial_receive()
            packet = self.deserialise(raw_message)

            if packet:
                # catch failed send packets..
                if packet[0] == 0:
                    self.__queue.append(self.temp_id)
                    self.packets[self.temp_id]['packet_num'] -= 1
                    __send()
                
                # continue if normal
                received_status = 1
                # if id not registered, register.
                if self.packets[packet[2]]:
                    if packet[3] == 1:
                        ack = True
                    else: 
                        ack = False
                    self.__id_register(packet[2], ack)
                # get id
                id_num = packet[2]
                # increment packet num, store payload
                self.packets[id_num]['packet_num'] += 1
                self.packets[id_num]['payload'] = packet[5:-1]
            else:
                print("incoming packet failed - requesting new")
                received_status = 0
                # request new packet with special packet and recurse
                self.__serial_send('<0>')
                __receive()


    def get_packet(self):
        """ fetches raw serial data from buffer, returns payload as list """

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
        #while len(r) == 0:
        r = self.conn.readline().decode("utf-8")

        print('recieved: ', r)
        return r


    def send(self, id_str = 'default', message = [0], ACK = True):
        # check if exists, if not then register
        if not self.packets[id_str]:
            self.__id_register(id_str, ACK)
        
        id_num = self.packets[id_str]
        # adds payload to ID dictionary
        self.packets[id_num]['payload'] = message
        # adds ID to queue
        self.__queue.append(id_num)


    def serialise(self, packet : list) -> str:
        
        output = "<"
        for i in list:
            output.append(str(i))
            output.append("-")
        output.append(">")

        return output


    def received_check(self):
        pass