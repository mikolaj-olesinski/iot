#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <OneWire.h>
#include <DallasTemperature.h>


LiquidCrystal_I2C lcd(0x27, 16, 2);

#define ONE_WIRE_BUS A1
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature tempSensors(&oneWire);

#define RGB_RED 6
#define RGB_GREEN 5
#define RGB_BLUE 3

#define TEMP_MIN 25.0
#define TEMP_MAX 26.0

#define DEBOUNCE_PERIOD 10UL

float tempOutMin = 500.0;
float tempOutMax = -500.0; 

bool isWeatherInfo = true;

void setup() 
{
  lcd.init();
  lcd.backlight();
  lcd.clear();

  tempSensors.begin();

  pinMode(RGB_RED, OUTPUT);
  pinMode(RGB_GREEN, OUTPUT);
  pinMode(RGB_BLUE, OUTPUT);

  lcd.clear();
}

void loop() 
{

  tempSensors.requestTemperatures();
  float tempIn = tempSensors.getTempCByIndex(1);
  float tempOut = tempSensors.getTempCByIndex(0); 

  if (tempOut < tempOutMin) tempOutMin = tempOut;
  if (tempOut > tempOutMax) tempOutMax = tempOut;

  if (tempOut < TEMP_MIN) setRGB(0, 0, 255);
  else if (tempOut > TEMP_MAX) setRGB(255, 0, 0);
  else setRGB(0, 255, 0);


  displayWeatherInfo(tempIn, tempOut, tempOutMin, tempOutMax);

}

void displayWeatherInfo(float tempIn, float tempOut, float tempOutMin, float tempOutMax)
{
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("I:");
    lcd.print(tempIn, 1);
    lcd.print(" O:");
    lcd.print(tempOut, 1);
    lcd.setCursor(0, 1);
    lcd.print("Mn:");
    lcd.print(tempOutMin, 1);
    lcd.print(" Mx:");
    lcd.print(tempOutMax, 1);
}



void setRGB(int red, int green, int blue) 
{
  analogWrite(RGB_RED, red);
  analogWrite(RGB_GREEN, green);
  analogWrite(RGB_BLUE, blue);
}
