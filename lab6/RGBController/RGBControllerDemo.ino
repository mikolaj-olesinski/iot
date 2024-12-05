#include "RGBController.h"

#define PIN_RED 9
#define PIN_GREEN 10
#define PIN_BLUE 11

RGBController rgb;

void setup() 
{
    rgb.init(PIN_RED, PIN_GREEN, PIN_BLUE);
}

void loop() 
{
    rgb.setColor("RED");
    delay(1000);
    rgb.setColor("GREEN");
    delay(1000);
    rgb.setColor("BLUE");
    delay(1000);
    rgb.setColor("YELLOW");
    delay(1000);
    rgb.setColor("CYAN");
    delay(1000);
    rgb.setColor("MAGENTA");
    delay(1000);
    rgb.setColor("WHITE");
    delay(1000);
    rgb.setColor("BLACK");
}
