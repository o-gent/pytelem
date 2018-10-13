#include "tcp.h"


int* Send::sensor_heartbeat(){
  packet_count += 1;

  //header
  current_packet[1] = 0;
  current_packet[2] = 1;   //packet type
  current_packet[3] = packet_count;
  current_packet[6] = 0;
  //payload
  for(unsigned int a = 1, b = 7; a<10; a++, b++){
    current_packet[b] = payload[a];
  }
  //footer
  current_packet[17] = 0;

  return current_packet;
}

String Send::serialise(int input[20]){
  String output;
  
  output = "<";
  for(unsigned int a = 1; a < 20; a++){
    output += input[a];
    output += "-";
  }
  output += ">";

  return output;
}


int Get::serial_handler(String message){
  String output;
  
}
