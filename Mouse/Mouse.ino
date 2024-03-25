#include <Mouse.h>

void setup() {
  Serial.begin(9600);
  Mouse.begin();
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    int x = data.substring(0, data.indexOf(',')).toInt();
    int y = data.substring(data.indexOf(',') + 1).toInt();
    Mouse.move(x, y);
  }
}
