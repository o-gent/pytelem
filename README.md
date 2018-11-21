# Telemetry-over-serial

Allows telemerty communication between python devices - including specific support for micropython devices. 

Arduino support is no longer being worked on, however is compatible with an earlier version of the python implimentation. 

Packet interpreter checks validity of packets by keeping track of packet number, by checking packet begins with correct characters and checksum.

The main.py and arduino.ino are example usages - datalink.py and datalink.cpp include classes which are to integrate seemlessly with other projects making telemetry as easy as possible


### Current work:

- impliment checksum functionality if needed 

- impliment way to reset system when disconnected so can be reconnected without restarting the program


### Issues:

some random issues sometimes on startup - currently unknown


#### Notes:

Serial Handler
    Queues packets 
    Routes packets

Can different packet IDs

Handshake decides who is sending



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
