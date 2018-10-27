#include "datalink.h"
 

void Datalink::_stream_start(){
  // initial handshake - decide which side sends first
  // initialise function variables  
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


void Datalink::_id_register(int idnum, bool ACK){
  // packets structure: [0] = packet_num, [1] = ACK, [2 onwards] = payload
  packets[idnum][0] = 0
  if(ACK){packets[idnum][1] = 1}
  if(ACK){packets[idnum][1] = 0}

}

void Datalink::serial_handler(){
  
  send_left = queue.len();

  if(order == false){
    this->_receive();
  }
  this->_send();
  while(send_left > 0){
    this->_send();
  }
  while(receive_left > 0){
    this->_send();
  }

}


void Datalink::_send(){
  int cycle_idnum; //temporary variable
  int current_packet[20];
  int check_sum;
  String str_message; //serialised packet

  // check queue has something in it
  if(queue.len() > 0){
    //cycle through queue
    for(int i = queue.len(), i--, i > 0){
      // get id from queue
      cycle_idnum = queue.pop();

      send_left = queue.len();
      //form packet
      current_packet[0] = 1; // last packet received
      current_packet[1] = send_left;
      current_packet[2] = cycle_idnum;
      current_packet[3] = packets[cycle_idnum][0]; // packet_num
      packets[cycle_idnum][0]++;

      //calculate checksum
      check_sum = 0;
      current_packet[19] = check_sum;

      //store current id incase packet failure
      temp_id = cycle_idnum;
      // serialise packet
      str_message = this->_serialise(current_packet);
      // send
      this->_serial_send(str_message)
      //wait for error checking
      this->_receive();
    }
  }
}


void Datalink::_receive(){
  String raw_message;
  int current_packet[20];

}


String Datalink::_serialise(int* packet){
/* changes array to string, for sending over serial */
  
  String output;
  
  output = "<";
  for(int a = 1; a < 20; a++){
    output += input[a];
    output += "-";
  }
  output += ">";

  return output;
}


int* Datalink::_deserialise(String raw_message){

}


void Datalink::_serial_send(String message){
  Serial.print(message); Serial.print("\n");
}


String Datalink::_serial_receive(){
  // returns string from serial
}


void Datalink::send(String id_str, int* message, bool ACK){
  // main user function - send an array with id

  //check if exists, if not, register
}


// LEGACY

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
