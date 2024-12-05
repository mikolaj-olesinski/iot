#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <OneWire.h>
#include <DallasTemperature.h>


LiquidCrystal_I2C lcd(0x27, 16, 2);

#define ONE_WIRE_BUS A1
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature tempSensors(&oneWire);

#define RGB_RED 9
#define RGB_GREEN 10
#define RGB_BLUE 11

#define TEMP_MIN 20.0
#define TEMP_MAX 25.0

//wartości ekstremalne
float tempOutMin = 100.0;
float tempOutMax = -100.0; 

void setup() {
  lcd.init();
  lcd.backlight();
  lcd.clear();

  tempSensors.begin();

  pinMode(RGB_RED, OUTPUT);
  pinMode(RGB_GREEN, OUTPUT);
  pinMode(RGB_BLUE, OUTPUT);

  lcd.setCursor(0, 0);
  lcd.print("Weather Station");
  delay(2000);
  lcd.clear();
}

void loop() {
  tempSensors.requestTemperatures();
  float tempIn = tempSensors.getTempCByIndex(0);
  float tempOut = tempSensors.getTempCByIndex(1); 

  if (tempOut < tempOutMin) tempOutMin = tempOut;
  if (tempOut > tempOutMax) tempOutMax = tempOut;

  lcd.setCursor(0, 0);
  lcd.print("In: ");
  lcd.print(tempIn, 1); 
  lcd.print(" C");
  lcd.setCursor(0, 1);
  lcd.print("Out: ");
  lcd.print(tempOut, 1);
  lcd.print(" C");

  if (tempOut < TEMP_MIN) setRGB(0, 0, 255);
  else if (tempOut > TEMP_MAX) setRGB(255, 0, 0);
  else setRGB(0, 255, 0);
  
  delay(1000);
}

void setRGB(int red, int green, int blue) {
  analogWrite(RGB_RED, red);
  analogWrite(RGB_GREEN, green);
  analogWrite(RGB_BLUE, blue);
}
