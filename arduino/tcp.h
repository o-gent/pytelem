#ifndef tcp_H
#define tcp_H

#include <Arduino.h> 


class Send{
  public:
    int packet_count = 0;
    int payload[10] = {0};
    int current_packet[20] = {0};
    
    int* sensor_heartbeat();
    String serialise(int input[20]);
};


class Get{
  public:
    int serial_handler(String message);


};


#endif