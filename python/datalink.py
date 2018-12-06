# any functions named _x are for internal use only.
import time

from utils import Logger, uLogger


# find device type
import sys
if sys.implementation.name == "cpython":
    from serial import Serial 
    import random as r
    l = Logger()

if sys.implementation.name == "micropython":
    # resolve implimentation difference between cpython and micropython.
    from machine import UART
    Serial = UART
    from uos import urandom
    r = lambda x: int(urandom(1)/256 * x) # only works for x less than 256. 
    l = uLogger()



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
        self.conn = Serial(port,  baudrate = 57000, timeout = 0.1)
        
        #initise class wide variables
        self.packets = {}
        self._idnum = 0 # makes sure each id made is unique
        self._queue = []
        self._order = 'unset'
        self.temp_id = 0

        # initialises data stream..
        self._stream_start()


    def _stream_start(self) -> None:
        
        # regester default id
        self._id_register(0,True)

        i = 0

        # ensure syncronisation
        self._serial_send("start")
        while self._serial_receive() != "start\n":
            self._serial_send("start")       

        # decides order of send receive
        def test():
            # could be anything as long as definitive result
            local = r.randint(0,100)
            self._serial_send(str(local))
            remote = self._serial_receive()
            return remote, local
        
        # checks if test is definitive
        while True:
            remote, local = test()
            
            i += 1
            if i > 5:
                self._stream_start()
            
            time.sleep(1)

            try: 
                remote = int(remote)
                if remote == local:
                    pass
                else:
                    break
            except: pass

        self._serial_send("end")
        while self._serial_receive() != "end\n":
            i += 1
            if i > 5:
                self._stream_start()
            self._serial_send("end")
        
        self._serial_receive()
        time.sleep(1)
        self._serial_receive()
        time.sleep(1)
        

        # evaluates results
        if remote > local:
            self.order = 'remote' # remote starts stream first
            self._serial_receive()
        else:
            self.order = 'local' # local starts stream first
            self._serial_send('<-1-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0>')
            self._serial_receive()
        
        l.log(self.order)
        l.log("syncronisation finished", 3)


    def _id_register(self, id_, ACK : bool) -> None:
        """needs work as could be conflict from each device creating same IDs"""

        self.packets[id_] = {}

        # setting attributes for id
        self.packets[id_]['packet_num'] = 0
        if ACK: self.packets[id_]['ACK'] = 1
        else: self.packets[id_]['ACK'] = 0
        self.packets[id_]['payload'] = [0]


    def _serialise(self, packet : list) -> str:
        """ 
        covert list to string using "-" to seperate values
        requires "-" to start to allow C++ to work...
        """
        output = "<"
        
        for i in packet:
            output += "-"
            output += str(i)
        output += ">"

        return output
    

    def _deserialise(self, raw_message: str):
        """ runs consistancy checks on packet, returns false if not consistent, else returns packet """
        
        # first check 
        if raw_message.startswith("<") and raw_message.endswith(">\n"): 
            # second check + try, except loop if no "-" exist
            try:
                datapacket = raw_message[1:-1].split("-")
                
                # convert datapacket string to list of integers
                for index, num in enumerate(datapacket):
                    try: datapacket[index] = int(num)
                    except: pass
                
                return datapacket[1:]
        
            except:
                l.log("packet could not be parsed (no - split)", 2)
                return False
        
        else:
            l.log("packet could not be parsed ( < > error)", 2)
            return False


    def _serial_send(self, message: str):
        """ place holder """
        self.conn.write(bytes(message + '\n', "utf-8"))
        l.log_root(message, 1)


    def _serial_receive(self) -> str:
        """ returns string from serial """
        r = ""

        i = 0
        # COULD BE ISSUE?
        while len(r) == 0:
            r = self.conn.readline().decode("utf-8")
            i += 1
            if i > 10:
                l.log("timeout!", 2)
                return "False"
        
        l.log_root(r, 1)
        return r


    def serial_handler(self) -> None:
        """ handles packets """
        # initialises scope variables for use in secondary functions
        self.send_left = len(self._queue)
        self.receive_left = 0
        self.temp_id = 0
        
        # keep sending/receiving while either side has packets left for cycle
        
        self._send()
        while self.send_left > 0:
            self._send()
        while self.receive_left > 0:
            self._send()
        
    
    def _send(self) -> None:
        """ calls _receive() each cycle """

        # see what data is currently wanted and adjust queue accordingly

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
                l.log("packet num = " + str(packet_num), 0)
                self.packets[id_num]['packet_num'] += 1
                ack = self.packets[id_num]['ACK']


                last_packet_received = 1
                checksum = 0
                
                
                # form packet
                packet = []
                packet.append(last_packet_received)
                packet.append(self.send_left)
                packet.append(id_num)
                packet.append(packet_num)
                for i in payload:
                    packet.append(i)
                packet.append(checksum)


                # store id incase failure
                self.temp_id = id_num

                # send
                self._serial_send(self._serialise(packet))
                
                # wait for error checking
                self._receive()
        
        else:
            # send default packet
            print('no packets queued')
            packet = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            self._serial_send(self._serialise(packet))
            self._receive()


    def _receive(self) -> None:
        raw_message = self._serial_receive()
        packet = self._deserialise(raw_message)
        
        # continue if packet was correct
        if packet:
            
            packet : list

            # check if packet is default no payload
            if packet[0] == 1 and packet[2] == 0:
                # end _receive()
                return None

            # catch failed send packets..
            if packet[0] == 0:
                l.log("caught failed packet", 2)
                
                # check if id_ 0 failure
                if self.temp_id == 0:
                    packet = [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                    self._serial_send(self._serialise(packet))

                # read failed id and go back to __send()
                self._queue.append(self.temp_id)
                # FUDGE: makes sure packet number is same as last time as it will be incremented
                self.packets[self.temp_id]['packet_num'] -= 1
                self._send()


            # if id not registered, register.
            try: self.packets[packet[2]]
            except: self._id_register(packet[2], True)
            

            # compare current packet_num with packet_num stored locally with id
            if int(packet[3]) != self.packets[packet[2]]['packet_num']:
                # if incosistent - failed..
                l.log("packet number comparision failed" + " actual: " + str(packet[3]) + " record: " + str(self.packets[packet[2]]['packet_num']), 2)
                self._failed()
            

            # fetch data from packet and store
            id_num = packet[2] # get id
            self.packets[id_num]['packet_num'] += 1         # increment packet num
            self.packets[id_num]['payload'] = packet[5:-1]  # store payload


            # update receive left 
            self.receive_left = packet[1]


        # if packet not correct.. 
        else:
            l.log(2, 2)
            self._failed()


    def _failed(self) -> None:
        l.log("incoming packet failed - requesting new", 2)
        time.sleep(0.1) # prevent recursion limit from happening too quickly
        # request new packet with special packet and recurse
        self._serial_send('<-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0>') # FUDGE
        self._receive()


    def send(self, id_ = 1, message = [0], ACK = True) -> None:
        """ send an array, specify id_str for multiple messages to different places """
        
        # check if exists, if not then register
        try: self.packets[id_]
        except: self._id_register(id_, ACK)
        
        # adds payload to ID dictionary
        self.packets[id_]['payload'] = message
        # adds ID to queue
        self._queue.append(id_)
    
    
    def get(self, id_ = 1):
        """ returns payload of id if exists, otherwise returns false """
        
        # gets payload of specified id from packets dict
        if type(id_) == int:
            try: self.packets[id_]
            except: return False
        
        return self.packets[id_]['payload']