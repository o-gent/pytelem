#include "tcp.h"

Packer packer;
int* message;
int a;

void setup() {
  Serial.begin(9600);
}


void loop() {
  message = packer.sensor_heartbeat();
  Serial.print(packer.serialise(message)); Serial.print("\n");
  packer.payload[2] = a;
  a++;
  delay(1000);
}
