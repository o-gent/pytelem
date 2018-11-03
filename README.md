# Telemetry-over-serial

Allows arduino sensor data to be sent over a serial device with some TCP-like features to ensure reliable transmission.
The interpretation program is written in python, each implementation can be found in their respective folders. 


Currently packets are arranged to have a header, payload and footer. Header contains data type and packet number and footer contains a checksum of the payload. 


Python packet interpreter checks validity of packets by keeping track of packet number, by checking packet begins with correct characters and checksum.

The main.py and arduino.ino are example usages - datalink.py and datalink.cpp include classes which are to integrate seemlessly with other projects making telemetry as easy as possible


### Current work:

- [ ] implement checksum arduino functionality and validity check

- [ ] implement structure for sending commands to arduino

- [X] have some kind of packet identity so packets for different purposes can be requested


### Issues:

Undergoing major changes - LEGACY code still functional but new code is completely untested.

Relatively high dynamic memory usage - probably due to use of arduino Strings. Could be reduced by using char arrays. https://arduino.stackexchange.com/questions/1013/how-do-i-split-an-incoming-string


#### Notes:

Data requester decides if packets are error checked - during handshake

Serial Handler
    Queues packets 
    Routes packets

Can different types of packets - each requires a handshake

Handshake decides who is sending 

Beginning byte decides if conformation or not. 



###packet design - 

pre-header>
whether last packet was received correctly;
packets left in round;

header>
id;
packet number;

payload>
message;

footer>
checksum;
