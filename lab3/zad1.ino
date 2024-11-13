#define LED_RED 6
#define LED_GREEN 5
#define LED_BLUE 3
#define RED_BUTTON 2
#define GREEN_BUTTON 4
#define DEBOUNCE_PERIOD 10UL

int led[] = {LED_RED, LED_GREEN, LED_BLUE};
int led_index = 0;

struct Button 
{
    int pin;
    int state;
    int previousState;
    unsigned long lastChangeTime;
};

Button redButton = {RED_BUTTON, HIGH, HIGH, 0UL};
Button greenButton = {GREEN_BUTTON, HIGH, HIGH, 0UL};

void initRGB() 
{
    pinMode(LED_RED, OUTPUT);
    pinMode(LED_GREEN, OUTPUT);
    pinMode(LED_BLUE, OUTPUT);
}

void initButtons() 
{
    pinMode(RED_BUTTON, INPUT_PULLUP);
    pinMode(GREEN_BUTTON, INPUT_PULLUP);
}

bool isButtonPressed(Button &button)
{
    if (millis() - button.lastChangeTime >= DEBOUNCE_PERIOD) {
        button.state = digitalRead(button.pin);
        if (button.state != button.previousState) {
            button.lastChangeTime = millis();
            button.previousState = button.state;
            if (button.state == LOW) return true;
            
        }
    }
    return false;
}

void setup() 
{
    initRGB();
    initButtons();
}

void loop() 
{
    if (isButtonPressed(redButton) || isButtonPressed(greenButton)) 
    {
        digitalWrite(led[led_index], LOW);
        led_index = ++led_index % 3;
        digitalWrite(led[led_index], HIGH);
    }
}
