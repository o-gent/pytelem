#include "datalink.h"


void Datalink::stream_start(){
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
      delay(10);
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
    delay(10);
    this->_receive();
  }
}


void Datalink::_id_register(int idnum, bool ACK){
  // packets structure: [1] = packet_num, [2] = ACK, [3 onwards] = payload
  this->packets[idnum][0] = 1; // says this id exists for checks..
  this->packets[idnum][1] = 0;
  if(ACK){this->packets[idnum][2] = 1;}
  if(ACK){this->packets[idnum][2] = 0;}
}


void Datalink::serial_handler(){
  send_left = this->queue.len();
  
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
  int check_sum;
  String str_message; //serialised packet

  // check queue has something in it
  if(this->queue.len() > 0){
    //cycle through queue
    for(int i = this->queue.len(); i--; i > 0){
      // get id from queue
      cycle_idnum = this->queue.pop();
      
      send_left = this->queue.len();
      //form packet
      this->current_packet[0] = 1; // last packet received
      
      this->current_packet[1] = send_left;
      this->current_packet[2] = cycle_idnum;
      this->current_packet[3] = this->packets[cycle_idnum][1]; // packet_num
      
      this->packets[cycle_idnum][1]++; // incriment packet_num stored for ID
      
      // inject payload
      for(int i = 4, j = 3; i<=13, j<=12; i++, j++){
        this->current_packet[i] = this->packets[cycle_idnum][j];
      }

      //calculate checksum
      check_sum = 0;
      this->current_packet[19] = check_sum;

      //store current id incase packet failure
      this->temp_id = cycle_idnum;
      // serialise packet
      str_message = this->_serialise(current_packet);
      // send
      this->_serial_send(str_message);
      //wait for error checking
      this->_receive();
    }
  }
}


void Datalink::_receive(){
  // gets new message - stored in object variable
  if(this->_deserialise(this->_serial_receive())){
    
    // check if packet has no payload - id 0
    // is failed packet
    if(this->current_packet[0] == 1){
      // id
      if(this->current_packet[2] == 0){
        // end _receive()
        return void();
      } 
    }


    // catch failed send packets..
    if(this->current_packet[0] == 0){

      // read failed id and go back to send
      this->queue.add(this->temp_id);

      // FUDGe: reduces temp_id packet number to same as last time..
      this->packets[this->temp_id][1]--;
      
      this->_send();
    }


    // compare incoming packet_num with stored
    if(this->current_packet != this->packets[this->current_packet[2]][1]){
      this->_failed();
    }


    //if id not regestered, register.
    if(this->packets[current_packet[2]][0] == 0){
      this->_id_register(current_packet[2], true);
    }


    // fetch data from packet and store
    this->packets[this->current_packet[2]][1]++;
    for(int i = 4, j = 3; i<=13, j<=12; i++,j++){
    this->current_packet[i] = this->packets[this->current_packet[2]][j];
    }


    // update receive left 
    this->receive_left = current_packet[1]; 
  }

  else{
    this->_failed();
  }

}


void Datalink::_failed(){
  // request new packet with special packet and recurse   fUDGING
  this->_serial_send("<-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0>");
  this->_receive();
}


String Datalink::_serialise(int packet[20]){
/* changes array to string, for sending over serial */
  String output;
  
  output = "<";
  for(int a = 0; a < 20; a++){
    output += "-";
    output += packet[a];
  }
  output += ">";

  return output;
}


bool Datalink::_deserialise(String raw_message){
  // slightly different to python version
  // returns a bool and modifies this->current_packet variable instead
  //Serial.print("deserialise:");Serial.print(raw_message);
  // first check
  if(raw_message.startsWith("<") && raw_message.endsWith(">")){
    // second check
    // this will fail if packet isn't complete
    for(int i = 0; i<20; i++){
      this->current_packet[i] = getValue(raw_message, '-', (i+1)).toInt();
    }

    return true; 
  }
  
  else{
    Serial.print("check fail");
    return false;
  }
}


void Datalink::_serial_send(String message){
  Serial.print(message); Serial.print("\n");
}


String Datalink::_serial_receive(){
  /* returns String from serial */
  delay(10);
  String readString = "";
  
  while (true) {
    delay(2);
    char c = Serial.read();  //gets one byte from serial buffer
    
    if (c == '<'){
      readString += c;
      while (true) {
        delay(1);
        char c = Serial.read();  //gets one byte from serial buffer
        //Serial.print("CHAR: ");Serial.println(c);
        
        readString += c; //makes the string readString
        if(c == '>'){
          return readString; // stops reading once end of line reaches
        }
      }
    }
  //pass
  }
}


void Datalink::send(int id_, int message[10]){
  /* main user function - send an array with id */
  
  // check if exists, if not, register
  if(this->packets[id_][0] == 0){
    this->_id_register(id_, true);
  }
  
  // transfer message to packets[id_][payload]
  for(int i_ = 0, j_ = 3; i_<10, j_<13; i_++,j_++){
    this->packets[id_][j_] = message[i_];
  }
   
  // adds id_ to send queue
  this->queue.add(id_);
}


int* Datalink::get(int id_){
  /* returns payload of id_ NOTE: will return 0 array if not registered*/
  int return_packet[10];
  
  // copy payload from this->packets
  for(int i = 0, j = 3; i<=9, j<=12; i++, j++){
    return_packet[i] = this->packets[id_][j];
  }
  
  return return_packet;
}


String getValue(String data, char separator, int index)
{
    int found = 0;
    int strIndex[] = { 0, -1 };
    int maxIndex = data.length() - 1;

    for (int i = 0; i <= maxIndex && found <= index; i++) {
        if (data.charAt(i) == separator || i == maxIndex) {
            found++;
            strIndex[0] = strIndex[1] + 1;
            strIndex[1] = (i == maxIndex) ? i+1 : i;
        }
    }
    return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}
