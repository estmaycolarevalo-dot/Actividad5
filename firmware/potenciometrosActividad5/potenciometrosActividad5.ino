const int PIN_POT_BASE    = 34;
const int PIN_POT_BRAZO   = 35;
const int PIN_POT_PINZA   = 32;
void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  pinMode(PIN_POT_BASE, INPUT);
  pinMode(PIN_POT_BRAZO, INPUT);
  pinMode(PIN_POT_PINZA, INPUT);
}
void loop() {
  int valBase  = analogRead(PIN_POT_BASE);
  int valBrazo = analogRead(PIN_POT_BRAZO);
  int valPinza = analogRead(PIN_POT_PINZA);
  float j1_rad = map(valBase, 0, 4095, -314, 314) / 100.0;
  float j2_rad = map(valBrazo, 0, 4095, -157, 157) / 100.0;
  float gripper_m = map(valPinza, 0, 4095, 0, 30) / 1000.0;
  Serial.print(j1_rad, 2);
  Serial.print(",");
  Serial.print(j2_rad, 2);
  Serial.print(",");
  Serial.println(gripper_m, 3);
  delay(50);
}
