void setup() {
  Serial.begin(115200);
  Serial3.begin(115200);

}

void loop() {
  // read from port 0, send to port 3:
  if (Serial.available()) {
    int inByte = Serial.read();
    Serial3.print(inByte, BYTE); 

  }
  // read from port 1, send to port 0:
  if (Serial3.available()) {
    int inByte = Serial3.read();
    Serial.print(inByte, BYTE); 
  }
}
