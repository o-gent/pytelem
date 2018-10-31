#ifndef datalink_H
#define datalink_H

#include <Arduino.h> 
#include "list.h"

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

      int check_sum;
    } packet_structure;

    // declare class variables
    bool order;
    int send_left;
    int receive_left;
    int temp_id;
    int current_packet[20] = {0}; // also a legacy variable
    List packets;
    List queue;
  
    // function names same as python
    void _stream_start();
    void _id_register(String id_str, bool ACK);
    void _send();
    void _receive();
    void _failed();
    String _serialise(int* packet);
    int* _deserialise(String raw_message);
    void _serial_send(String message);
    String _serial_receive();

    
    // LEGACY declare variables for class
    int packet_count = 0;
    bool ack_check;
    char r;
    char b = '1';


  public:
    // public function declarations (same as python)
    void serial_handler();
    void send(int id_, int* message);
    int* get(int id_); 

    

    // LEGACY (required global variables to be changed)
    int payload[10] = {0};
    int* message;

    int* packet_maker();
    String serialise(int input[20]);
    void received_check();
    int serial_handler(String message);
    void send_payload();
};

#endif
