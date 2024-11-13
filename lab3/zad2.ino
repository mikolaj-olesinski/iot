#define LED_RED 6
#define LED_GREEN 5
#define LED_BLUE 3

const unsigned long RED_BLINK_PERIOD = 900UL;
const unsigned long GREEN_BLINK_PERIOD = 1000UL;
const unsigned long BLUE_BLINK_PERIOD = 1100UL;

struct LedControl 
{
    int pin;                   
    unsigned long blinkPeriod;
    int state;
    unsigned long lastChange;
};

LedControl redLed = {LED_RED, RED_BLINK_PERIOD, LOW, 0UL};
LedControl greenLed = {LED_GREEN, GREEN_BLINK_PERIOD, LOW, 0UL};
LedControl blueLed = {LED_BLUE, BLUE_BLINK_PERIOD, LOW, 0UL};

void setup() 
{
    pinMode(redLed.pin, OUTPUT);
    pinMode(greenLed.pin, OUTPUT);
    pinMode(blueLed.pin, OUTPUT);

    digitalWrite(redLed.pin, redLed.state);
    digitalWrite(greenLed.pin, greenLed.state);
    digitalWrite(blueLed.pin, blueLed.state);
}


void blinkLed(LedControl &led) 
{
    if (millis() - led.lastChange >= led.blinkPeriod) 
    {

        if (led.state == LOW) led.state = HIGH;
        else led.state = LOW;

        digitalWrite(led.pin, led.state);          
        led.lastChange += led.blinkPeriod;          
    }
}

void loop() 
{
    blinkLed(redLed);
    blinkLed(greenLed);
    blinkLed(blueLed);
}
