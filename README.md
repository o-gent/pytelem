# Telemetry-over-serial

Allows arduino sensor data to be sent over a serial device with some TCP-like features to ensure reliable transmission.
The interpretation program is written in python, each implementation can be found in their respective folders. 


Currently packets are arranged to have a header, payload and footer. Header contains data type and packet number and footer contains a checksum of the payload. 


Python packet interpreter checks validity of packets by keeping track of packet number, by checking packet begins with correct characters and checksum. 


Current work:


[ ] - implement checksum arduino functionality and validity check
[ ] - implement different packet types to allow for unchecked and checked packets (TCP/UDP)
[ ] - work out whether serial communication should be done within class or in main file.


Issues:


Currently only works on 9600 baud rate.. something to do with timings on dodgy reads and writes

Currently for every three packets, two fail due to packet number not being correct, arduino not updating fast enough or python not sending ACK byte fast enough. 