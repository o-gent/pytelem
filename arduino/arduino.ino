#include "tcp.h"

Send send;
int* message;
int a;
//String r;
char r;
char b = '1';

bool check;

void setup() {
  Serial.begin(9600);
  //Serial.setTimeout(200);
  a = 0;
  // initial handshake
  r = Serial.read();
}


void loop() {
  message = send.sensor_heartbeat();
  
  Serial.print(send.serialise(message)); Serial.print("\n");
  
  check = true;
  while(check) { 
    //r = Serial.readString();
    if(Serial.available() > 0){
      r = Serial.read();
    }
    if(r == b){
      check = false;
    }
    else{
      Serial.print(send.serialise(message)); Serial.print("\n");
    }
  }
  
  send.payload[2] = a;
  a++;
}
