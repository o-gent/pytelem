#include "datalink.h"


int example_data[10] = {0};
Datalink link;


void setup() {
  Serial.begin(115200);
  link.stream_start();
  // initial handshake (unimplimented)
}


void loop() {
  // example of data being injected to payload
  example_data[2]++;
  link.send(1,example_data);
  link.serial_handler();
}
