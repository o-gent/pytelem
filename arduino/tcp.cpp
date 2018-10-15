#include "tcp.h"

Send::Send(){
  // start serial communication here

}


int* Send::sensor_heartbeat(){
  // creates packet to be sent with header and footer data

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
  
  //footer - checksum to be implimented
  current_packet[17] = 0;

  return current_packet;
}


String Send::serialise(int input[20]){
  // changes array to string, for sending over serial
  
  String output;
  
  output = "<";
  for(unsigned int a = 1; a < 20; a++){
    output += input[a];
    output += "-";
  }
  output += ">";

  return output;
}


void Send::recieved_check(){
  ack_check = false;
  do { 
      //r = Serial.readString();
      r = Serial.read();
      
      if(r == b){
        ack_check = true;
      }
      else{
        Serial.print(this->serialise(message)); Serial.print("\n");
      }
    } while(ack_check == false);
}


int Get::serial_handler(String message){
  //unimplimented
  String output;
}
