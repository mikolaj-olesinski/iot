#include <LiquidCrystal_I2C.h>

#define POTENTIOMETER_PIN A0 
#define VREF 5.0
#define ADC_RESOLUTION 10

#define 

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() 
{
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);

  lcd.print("Odczyt ADC:");
  delay(1000);

  pinMode(POTENTIOMETER_PIN, INPUT);
}

void loop() {
  int adcValue = analogRead(POTENTIOMETER_PIN);
  adcValue = min(max(0, value - 10), 1023);

  float voltage = (adcValue * VREF) / pow(2, ADC_RESOLUTION);

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("ADC: ");
  lcd.print(adcValue);
  lcd.setCursor(0, 1);
  lcd.print("U: ");
  lcd.print(voltage, 2); 
  lcd.print("V");

  if (adcValue == 0) 
  {
    lcd.setCursor(10, 0);
    lcd.print("Min");
  }
  else if (adcValue == 1023) 
  {
    lcd.setCursor(10, 0);
    lcd.print("Max");
  }

  delay(500);
}
