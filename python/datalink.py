# any functions named _x are for internal use only. 
import serial
import random as r


# for reference
packet_structure = {
    'ACK' : bool,                   #0
    'packets_left_in_round' : int,  #1
    
    'id' : int,                     #2
    'packet_number' : int,          #4
    
    'payload' : list,               #5:
    
    'check_sum' : int               #-1:
}


class Datalink():
    def __init__(self, port):
        # start serial connection
        self.conn = serial.Serial(port, 115200)
        #initise class wide variables
        # next two are legacy
        self.packet_num = 1
        self.data = [0 for i in range(20)]
        # new vars
        self.packets = {}
        self._idnum = 0 # makes sure each id made is unique
        self._queue = []
        self._order = 'unset'
        # initialises data stream..
        self._stream_start()


    def _stream_start(self) -> None:
        # decides order of send receive
        def test():
            # could be anything as long as definitive result
            local = r.randint(0,100)
            self._serial_send(str(local))
            remote = self._serial_receive()
            self._serial_send(str(local))
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


    def _id_register(self, id_, ACK : bool) -> None:
        """needs work as could be conflict from each device creating same IDs"""
        
        # store packet information under unique numerical id
        self.packets[self._idnum] = {}

        if type(id_) == str:
            # save string name under numerical id for incoming messages
            self.packets[self._idnum]['id'] = id_
            # linking id_(str) to id_number for lookup during sending 
            self.packets[id_] = self._idnum
            # fetching numerical id again (fudging)
            id_num = self.packets[id_]
        else:
            # id_ assumed int
            id_num = id_

        self._idnum += 1 # increment for next handshake

        # setting attributes for id
        self.packets[id_num]['packet_num'] = 0
        if ACK: self.packets[id_num]['ACK'] = 1
        else: self.packets[id_num]['ACK'] = 0
        self.packets[id_num]['payload'] = [0]


    def _serialise(self, packet : list) -> str:
        """ 
        covert list to string using "-" to seperate values
        requires "-" to start to allow C++ to work...
        """
        output = "<"
        for i in output:
            output += "-"
            output += str(i)
        output += ">"
        return output
    

    def _deserialise(self, raw_message: str):
        """ runs consistancy checks on packet, returns false if not consistent, else returns packet """

        # if can't read packet - would need to resend anyway..
        # need to rethink packet reciept.. 
        
        # first check 
        if raw_message.startswith("<") and raw_message.endswith(">\n"): 

            # second check + try, except loop if no "-" exist
            try:
                datapacket = raw_message[1:-1].split("-")

                if int(datapacket[2]) == self.packet_num: 
                    return datapacket
                else: 
                    return False
            except:
                return False
        else: 
            return False


    def _serial_send(self, message: str):
        """ place holder """
        self.conn.write(bytes(message, "utf-8"))
        print('sent: ', message)


    def _serial_receive(self) -> str:
        """ returns string from serial """
        r = ""

        # COULD BE ISSUE?
        while len(r) == 0:
            r = self.conn.readline().decode("utf-8")
        
        print('recieved: ', r)
        return r


    def serial_handler(self) -> None:
        """ handles packets """
        # initialises scope variables for use in secondary functions
        self.send_left = len(self._queue)
        self.receive_left = 0
        
        # logic for send/receive order based on which platform started
        # keep sending/receiving while either side has packets left for cycle
        if self.order == 'remote':
            self._receive()
        
        self._send()
        while self.send_left > 0:
            self._send()
        while self.receive_left > 0:
            self._send()
        
    
    def _send(self) -> None:
        """ calls _receive() each cycle """
        # check if anything in queue
        if self._queue:
            # cycle through queue
            for __ in self._queue:
                # get an id from queue
                id_num = self._queue.pop()

                # fetch packet data
                self.send_left = len(self._queue)
                payload = self.packets[id_num]['payload']
                packet_num = self.packets[id_num]['packet_num']
                self.packets[id_num]['packet_num'] += 1
                ack = self.packets[id_num]['ACK']

                last_packet_received = 1
                
                checksum = 0
                # form packet
                packet = []
                packet.append(last_packet_received)
                packet.append(self.send_left)
                packet.append(id_num)
                packet.append(ack)
                packet.append(packet_num)
                for i in payload:
                    packet.append(i)
                packet.append(checksum)

                # store id incase failure
                self.temp_id = id_num
                # serialise packet
                string = self._serialise(packet)
                # send
                self._serial_send(string)
                # wait for error checking
                self._receive()
        else:
            # send default packet
            packet = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            self._serial_send(self._serialise(packet))
            self._receive()


    def _receive(self) -> None:
        raw_message = self._serial_receive()
        packet = self._deserialise(raw_message)
        # will continue if packet was correct
        if packet:
            packet : list
            # compare current packet_num with packet_num stored locally with id
            if int(packet[3]) != self.packets[packet[2]]['packet_num']:
                self._failed()

            # catch failed send packets..
            if packet[0] == 0:
                # read failed id and go back to __send()
                self._queue.append(self.temp_id)
                # FUDGE: makes sure packet number is same as last time as it will be incremented
                self.packets[self.temp_id]['packet_num'] -= 1
                self._send()

            # if id not registered, register.
            if not self.packets[packet[2]]:
                if packet[3] == 1:
                    ack = True
                else: 
                    ack = False
                self._id_register(packet[2], ack)
            
            # fetch data from packet and store
            id_num = packet[2] # get id
            self.packets[id_num]['packet_num'] += 1         # increment packet num
            self.packets[id_num]['payload'] = packet[5:-1]  # store payload

            # update receive left 
            self.receive_left = packet[1]

        # if packet not correct.. 
        else:
            self._failed()


    def _failed(self) -> None:
        print("incoming packet failed - requesting new")
        # request new packet with special packet and recurse
        self._serial_send('<-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0>') # FUDGE
        self._receive()


    def send(self, id_str = 'default', message = [0], ACK = True) -> None:
        """ send an array, specify id_str for multiple messages to different places """
        
        # check if exists, if not then register
        if not self.packets[id_str]:
            self._id_register(id_str, ACK)
        
        id_num = self.packets[id_str]
        # adds payload to ID dictionary
        self.packets[id_num]['payload'] = message
        # adds ID to queue
        self._queue.append(id_num)
    
    
    def get(self, id_ = 'default'):
        """ returns payload of id if exists, otherwise returns false """
        # gets payload of specified id from packets dict
        if type(id_) == str:
            if self.packets[id_]:
                id_num = self.packets[id_]
            else: 
                # id doesn't exist..
                return False
        elif type(id_) == int:
            if self.packets[id_]:
                id_num = id_
            else:
                # id doesn't exist..
                return False
        
        return self.packets[id_num]['payload']


    
    # LEGACY - LEGACY - LEGACY
    def get_packet(self):
        """ fetches raw serial data from buffer, returns payload as list """

        raw_message = self._serial_receive()
        datapacket = self._deserialise(raw_message)
        
        if datapacket:
            self.data = datapacket
            self._serial_send("1")
            self.packet_num += 1
        else:
            print("packet not recieved sucessfully")
            self._serial_send("0") # request new data packet
            # call packet_handle again..
            self.get_packet() 

        #returns full packet for debugging for now.
        return self.data 
