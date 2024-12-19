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

#define GREEN_BUTTON 4

#define TEMP_MIN 25.0
#define TEMP_MAX 26.0

#define DEBOUNCE_PERIOD 10UL

float tempOutMin = 500.0;
float tempOutMax = -500.0; 

bool isWeatherInfo = true;

struct Button 
{
    int pin;
    int state;
    int previousState;
    unsigned long lastChangeTime;
};

Button greenButton = {GREEN_BUTTON, HIGH, HIGH, 0UL};

bool isButtonPressed(Button &button)
{
    if (millis() - button.lastChangeTime >= DEBOUNCE_PERIOD) 
    {
        button.state = digitalRead(button.pin);
        if (button.state != button.previousState) 
        {
            button.lastChangeTime = millis();
            button.previousState = button.state;
            if (button.state == LOW) return true;
        }
    }
    return false;
}


void setup() 
{
  lcd.init();
  lcd.backlight();
  lcd.clear();

  tempSensors.begin();

  pinMode(RGB_RED, OUTPUT);
  pinMode(RGB_GREEN, OUTPUT);
  pinMode(RGB_BLUE, OUTPUT);

  pinMode(GREEN_BUTTON, INPUT_PULLUP);

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


  if (isButtonPressed(greenButton)) isWeatherInfo = !isWeatherInfo;

  if (isWeatherInfo) displayWeatherInfo(tempIn, tempOut);
  else maxAndMinTempDisplay(tempOutMin, tempOutMax);

}

void displayWeatherInfo(float tempIn, float tempOut)
{
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("In: ");
  lcd.print(tempIn, 2); 
  lcd.print(" C");
  lcd.setCursor(0, 1);
  lcd.print("Out: ");
  lcd.print(tempOut, 2);
  lcd.print(" C");
}

void maxAndMinTempDisplay(float tempOutMin, float tempOutMax)
{
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Min: ");
  lcd.print(tempOutMin, 2);
  lcd.print(" C");
  lcd.setCursor(0, 1);
  lcd.print("Max: ");
  lcd.print(tempOutMax, 2);
  lcd.print(" C");
}

void setRGB(int red, int green, int blue) 
{
  analogWrite(RGB_RED, red);
  analogWrite(RGB_GREEN, green);
  analogWrite(RGB_BLUE, blue);
}
