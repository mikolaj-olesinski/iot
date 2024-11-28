#define POTENTIOMETER_PIN A0 

void setup()
{
  Serial.begin(9600);
    while (!Serial) {
    } 
}

void loop() 
{
  int adcValue = analogRead(POTENTIOMETER_PIN);

  Serial.println("ADC:\t" + String(adcValue));

  delay(100); 
}
