#include "tcp.h"

int a;
Datalink link;

void setup() {
  Serial.begin(115200);
  a = 0;
  // initial handshake (unimplimented)
}


void loop() {
  // example of data being injected to payload
  link.payload[2] = a;
  a++;

  link.send_payload();
}
