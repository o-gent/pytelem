#ifndef tcp_H
#define tcp_H

#include <Arduino.h> 

class Datalink{
  private:
    // packet structure
    typedef struct {
      bool ACK;
      int packets_left_in_round;

      int id;
      int data_type;
      int packet_number;

      int* payload;

      int check_sum
    } packet_structure;

    // declare class variables
    int* packets[10] = {0}; // store structs within this 
    int idnum;
    int* queue[10] = {0}; // need to make this act as a list
    bool order;

    // LEGACY declare variables for class
    int packet_count = 0;
    int current_packet[20] = {0};
    bool ack_check;
    char r;
    char b = '1';
  

  public:
    int payload[10] = {0};
    int* message;
    
    // function names same as python
    void _stream_start();
    void _id_register(String id_str, bool ACK);
    void _send();
    void _receive();
    String _serialise(int* packet);
    bool _deserialise(String raw_message);
    void _serial_send(String message);
    String _serial_receive();
    void serial_handler();
    void send(String id_str, int* message, bool ACK);


    //legacy
    int* packet_maker();
    String serialise(int input[20]);
    void received_check();
    int serial_handler(String message);
    void send_payload();
};

#endif
