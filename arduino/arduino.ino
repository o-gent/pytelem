#include "tcp.h"

Send send;

int a;

void setup() {
  Serial.begin(9600);
  a = 0;
  // initial handshake (unimplimented)
}


void loop() {
  // example of data being injected to payload
  send.payload[2] = a;
  a++;

  // embeds payload in packet and sends over serial
  send.message = send.sensor_heartbeat();
  Serial.print(send.serialise(send.message)); Serial.print("\n");
  send.recieved_check();
}
