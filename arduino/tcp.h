#ifndef tcp_H
#define tcp_H

#include <Arduino.h> 


class Send{
  public:
    int packet_count = 0;
    int payload[10] = {0};
    int current_packet[20] = {0};
    bool ack_check;
    char r;
    char b = '1';
    int* message;
    
    Send();
    int* sensor_heartbeat();
    String serialise(int input[20]);
    void received_check();
};


class Get{
  public:
    int serial_handler(String message);


};


#endif
