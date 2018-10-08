#ifndef tcp_H
#define tcp_H

#include <Arduino.h> 

class Packer{
  public:
    int packet_count = 0;
    int payload[10] = {0};
    int current_packet[20] = {0};
    
    int* sensor_heartbeat();
    String serialise(int input[20]);
};

#endif


/*
struct packet{
  // header
  int data_type;
  double packet_number;
  // payload  
  double payload [10];
  // footer
  int checksum;
};
*/
