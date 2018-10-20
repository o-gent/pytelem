#include "tcp.h"

void Datalink::initialise(){
  // initial handshake - decide which side sends first
  int local;
  int remote;
  String remote_string = "";
  randomSeed(analogRead(0));

  while(true){
    remote_string = ""; // reset
    local = random(0,100);
    Serial.println(local);
    while(remote_string == ""){
      remote_string = Serial.readString();
    }
    remote = remote_string.toInt();
    if (local == remote){
    }
    else{
      break;
    }
  }
  if(local > remote){
    order = true;
  }
  else{
    order = false;
  }
}


void Datalink::send_payload(){
  /* co-ordinates functions - embeds payload in packet and sends over serial */
  this->message = this->packet_maker();
  Serial.print(this->serialise(this->message)); Serial.print("\n");
  this->received_check();
}


int* Datalink::packet_maker(){
  /* creates packet to be sent with header and footer data */
  
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


String Datalink::serialise(int input[20]){
  /* changes array to string, for sending over serial */
  
  String output;
  
  output = "<";
  for(unsigned int a = 1; a < 20; a++){
    output += input[a];
    output += "-";
  }
  output += ">";

  return output;
}


void Datalink::received_check(){
  ack_check = false;
  do { 
      //r = Serial.readString();
      r = Serial.read();

      while(r != '0' && r != '1'){
        r = Serial.read();
      }
      
      if(r == b){
        ack_check = true;
      }
      else{
        Serial.print(this->serialise(message)); Serial.print("\n");
      }
    } while(ack_check == false);
}


int Datalink::serial_handler(String message){
  //unimplimented
  String output;
}
