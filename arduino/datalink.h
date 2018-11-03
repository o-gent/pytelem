#ifndef datalink_H
#define datalink_H

#include <Arduino.h> 
#include "list.h"

class Datalink{
  private:
    // declare class variables
    bool order;
    int send_left;
    int receive_left;
    int temp_id;
    int current_packet[20] = {0}; // also a legacy variable
    int packets[20][13] = {{0}};
    List queue;
  
    // function names same as python
    void _send();
    void _id_register(int idnum, bool ACK);
    void _receive();
    void _failed();
    String _serialise(int* packet);
    bool _deserialise(String raw_message);
    void _serial_send(String message);
    String _serial_receive();

  public:
    // public function declarations (same as python)
    void stream_start(); // this is different to python
    void serial_handler();
    void send(int id_, int* message);
    int* get(int id_); 
};

String getValue(String data, char separator, int index);

#endif
