#include "tcp.h"


int example_data;
Datalink link;


void setup() {
  Serial.begin(115200);
  link.initialise();
  a = 0;
  // initial handshake (unimplimented)
}


void loop() {
  // example of data being injected to payload
  link.payload[2] = example_data;
  example_data++;

  link.send_payload();
}
