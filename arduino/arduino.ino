#include "tcp.h"

Send send;

int* message;
int a;
char r;
char b = '1';
bool ack_check;

void setup() {
  Serial.begin(9600);
  a = 0;

  // initial handshake (unimplimented)
  r = Serial.read();
}


void loop() {
  // example of data being injected to payload
  send.payload[2] = a;
  a++;

  // embeds payload in packet and sends over serial
  message = send.sensor_heartbeat();
  Serial.print(send.serialise(message)); Serial.print("\n");
  

  // check if packet was validated, else, resend until validated
  // needs tidying into own function. 
  ack_check = true;
  while(ack_check) { 
    //r = Serial.readString();
    r = Serial.read();
    
    if(r == b){
      ack_check = false;
    }
    else{
      Serial.print(send.serialise(message)); Serial.print("\n");
    }
  }
}
