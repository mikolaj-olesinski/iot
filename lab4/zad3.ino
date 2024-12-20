#include <LiquidCrystal_I2C.h>

#define POTENTIOMETER_PIN A0 
#define VREF 5.0
#define ADC_RESOLUTION 10

int adcPreviousValue = 0;


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

void print_adc_value(int adcValue, float voltage)
{
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
}

void loop() 
{
  int adcValue = analogRead(POTENTIOMETER_PIN);

  float voltage = (adcValue * VREF) / pow(2, ADC_RESOLUTION);


  if (adcValue < adcPreviousValue - 10 || adcValue > adcPreviousValue + 10)
  {
    print_adc_value(adcValue, voltage);
    adcPreviousValue = adcValue;
  }

  delay(300);
}
