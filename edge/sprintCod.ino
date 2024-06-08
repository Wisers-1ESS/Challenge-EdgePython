const int pinShunt = A1;
const int pinTemp = A0;
const int pinIma = 2;
double Volts = 0;
float raioPneu = 22.86; // Raio em CM
unsigned long tempoDecorrido = 0, tempoIniciaVel = 0, tempoZeraVel = 0;
float veloKm = 0;
// Valor da resistência do shunt em ohms
const float shuntResistance = 204*0.1; // exemplo 0.1 ohms

// Função para calcular a corrente com base na leitura do pino do shunt
float calcularWatts() {
  int shuntVoltage = analogRead(pinShunt);
  
  // Converte a leitura analógica para tensão (assumindo Vref de 5V)
  float shuntVoltageVolts = shuntVoltage * (5.0 / 1024.0);
  
  // Calcula a corrente usando a lei de Ohm: I = V / R
  float corrente = shuntVoltageVolts / shuntResistance;
  return corrente * 5.0; // Corrente multiplicada pela tensão da bateria para obter potência
}

float tempCelsius(){
  double tempRead = analogRead(pinTemp);
  Volts = (tempRead / 1024.0) * 5000; // 5000 para obter em milivolts
  return (Volts - 500) * 0.1; // temperatura em Celsius
}

void velocidade(){
  unsigned long tempoAtual = millis();
  tempoDecorrido = tempoAtual - tempoIniciaVel;
  tempoIniciaVel = tempoAtual;
  float comprimento = 2 * 3.1415 * (raioPneu / 100.0); // comprimento da roda em metros
  veloKm = (3.6 * comprimento) / (tempoDecorrido / 1000.0); // converte para km/h
  Serial.print("Velocidade: ");
  Serial.print(veloKm);
  Serial.println(" KM/Hr");
  tempoZeraVel = tempoAtual; // Atualiza o tempo de referência para zerar a velocidade
}

void setup() {
  // Inicialização do monitor serial
  Serial.begin(9600);
  tempoIniciaVel = millis();
  attachInterrupt(digitalPinToInterrupt(pinIma), velocidade, RISING);
}

void loop() {
  // Ler a corrente
  float watts = calcularWatts();
  float temperatura = tempCelsius();
  
  // Envia a corrente para o monitor serial
  Serial.print("Temperatura: ");
  Serial.print(temperatura, 1);
  Serial.println(" °C");
  Serial.print("Uso da bateria: ");
  Serial.print(watts / 1000);
  Serial.println(" KW");
  
  if (millis() - tempoZeraVel > 5000) {
    veloKm = 0;
    Serial.println("Velocidade: 0 KM/Hr");
  }
  
  delay(1000);
}
