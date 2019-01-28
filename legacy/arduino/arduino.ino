#include "datalink.h"


int example_data[10] = {0};
int ex2[10] = {2};
Datalink link;


void setup() {
  Serial.begin(115200);
  link.stream_start();
  // initial handshake (unimplimented)
}


void loop() {
  // example of data being injected to payload
  example_data[2]++;
  ex2[3]++;
  link.send(2, ex2);
  link.send(1,example_data);
  link.serial_handler();
}
