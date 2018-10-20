#ifndef tcp_H
#define tcp_H

#include <Arduino.h> 

class Datalink{
  // declare variables for class
  int packet_count = 0;
  int current_packet[20] = {0};
  bool ack_check;
  char r;
  char b = '1';
  bool order;
  
  public:
    int payload[10] = {0};
    int* message;
    
    void initialise();
    int* packet_maker();
    String serialise(int input[20]);
    void received_check();
    int serial_handler(String message);

    void send_payload();
};

#endif
