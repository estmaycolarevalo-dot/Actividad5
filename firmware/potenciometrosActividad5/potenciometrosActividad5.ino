// ======================================================
// CONTROL DE BRAZO ROBÓTICO URDF VÍA UART CON ESP32
// ======================================================

// Asignación de pines ADC (ADC1)
const int PIN_POT_BASE    = 34; // Joint 1 (Base - 10k)
const int PIN_POT_BRAZO   = 35; // Joint 2 (Brazo - 50k)
const int PIN_POT_PINZA   = 32; // Joint Gripper (Pinza - 50k)

void setup() {
  // Inicialización de la comunicación serial
  Serial.begin(115200);
  
  // Configurar la resolución del ADC del ESP32 a 12 bits (0 - 4095)
  analogReadResolution(12);
  
  // Pines de entrada analógica
  pinMode(PIN_POT_BASE, INPUT);
  pinMode(PIN_POT_BRAZO, INPUT);
  pinMode(PIN_POT_PINZA, INPUT);
}

void loop() {
  // 1. Lectura de valores analógicos en bruto (0 a 4095)
  int valBase  = analogRead(PIN_POT_BASE);
  int valBrazo = analogRead(PIN_POT_BRAZO);
  int valPinza = analogRead(PIN_POT_PINZA);

  // 2. Mapeo a las unidades reales de las articulaciones del URDF

  // Joint 1 (Base): Rotación de -PI a +PI rad (-3.1416 a 3.1416 rad)
  float j1_rad = map(valBase, 0, 4095, -314, 314) / 100.0;

  // Joint 2 (Brazo): Inclinación de -PI/2 a +PI/2 rad (-1.57 a 1.57 rad)
  float j2_rad = map(valBrazo, 0, 4095, -157, 157) / 100.0;

  // Joint Gripper (Pinza): Desplazamiento prismático de 0.0 a 0.03 metros
  float gripper_m = map(valPinza, 0, 4095, 0, 30) / 1000.0;

  // 3. Envío de datos por Serial en formato CSV (j1,j2,gripper)
  Serial.print(j1_rad, 2);
  Serial.print(",");
  Serial.print(j2_rad, 2);
  Serial.print(",");
  Serial.println(gripper_m, 3);

  // 4. Retardo de muestreo (~20 lecturas por segundo)
  delay(50);
}