#include <util/atomic.h>
#include <LiquidCrystal_I2C.h>

#define LED_RED 6
#define LED_GREEN 5
#define LED_BLUE 3

#define RED_BUTTON 2
#define GREEN_BUTTON 4

#define ENCODER1 A2
#define ENCODER2 A3

#define DEBOUNCE_PERIOD 10UL

LiquidCrystal_I2C lcd(0x27, 16, 2);

struct Button 
{
    int pin;
    int state;
    int previousState;
    unsigned long lastChangeTime;
};

Button greenButton = {RED_BUTTON, HIGH, HIGH, 0UL};

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

void displayResult(int value, int selectedOption)
{
    lcd.setCursor(0, 0);
    lcd.print("Selected: ");
    lcd.print(selectedOption == 0 ? "Red" : (selectedOption == 1 ? "Green" : "Blue"));

    char buffer[40];
    sprintf(buffer, "Intensity: %3d", value);
    lcd.setCursor(0, 1);
    lcd.print(buffer);
}

void showMenu(int selectedOption) 
{
    lcd.clear();
    switch (selectedOption) 
    {
        case 0:
            lcd.setCursor(0, 0);
            lcd.print(">Red LED");
            lcd.setCursor(1, 1);
            lcd.print("Green LED");
            break;
        case 1:
            lcd.setCursor(0, 0);
            lcd.print("Red LED");
            lcd.setCursor(1, 1);
            lcd.print(">Green LED");
            break;
        case 2:
            lcd.setCursor(0, 0);
            lcd.print("Green LED");
            lcd.setCursor(1, 1);
            lcd.print(">Blue LED");
            break;
        default:
            lcd.setCursor(0, 0);
            lcd.print(">Blue LED");
            break;
    }
}

void setup() 
{
    pinMode(LED_RED, OUTPUT);
    digitalWrite(LED_RED, LOW);

    pinMode(LED_GREEN, OUTPUT);
    digitalWrite(LED_GREEN, LOW);

    pinMode(LED_BLUE, OUTPUT);
    digitalWrite(LED_BLUE, LOW);

    pinMode(ENCODER1, INPUT_PULLUP);
    pinMode(ENCODER2, INPUT_PULLUP);

    pinMode(RED_BUTTON, INPUT_PULLUP);

    lcd.init();
    lcd.backlight();
    showMenu(0);

    PCICR |= (1 << PCIE1);
    PCMSK1 |= (1 << PCINT10);
}

int getLedPin(int option)
{
    if (option == 0) return LED_RED;
    else if (option == 1) return LED_GREEN;
    else return LED_BLUE;
}

struct EncoderState 
{
    volatile int encoder1 = HIGH;
    volatile int encoder2 = HIGH;
    volatile unsigned long encoderTimestamp = 0UL;
    int selectedOption = 0;
    int values[3] = {0, 0, 0}; 
    unsigned long lastEncoderTime = 0UL;
};

EncoderState es;
volatile bool isInMenuMode = true;

ISR(PCINT1_vect)
{
    es.encoder1 = digitalRead(ENCODER1);
    es.encoder2 = digitalRead(ENCODER2);
    es.encoderTimestamp = millis();
}

void loop() 
{
    int en1;
    int en2;
    unsigned long timestamp;

    ATOMIC_BLOCK(ATOMIC_RESTORESTATE) 
    {
        en1 = es.encoder1;
        en2 = es.encoder2;
        timestamp = es.encoderTimestamp;
    }

    if (isInMenuMode) handleMenuMode(en1, en2, timestamp);
    else handleIntensityMode(en1, en2, timestamp);

    if (isButtonPressed(greenButton)) toggleMenuMode();
}

void handleMenuMode(int en1, int en2, unsigned long timestamp) 
{
    if (en1 == LOW && timestamp > es.lastEncoderTime + DEBOUNCE_PERIOD)
    {
        if (en2 == HIGH && es.selectedOption < 2) es.selectedOption++;
        else if (en2 == LOW && es.selectedOption > 0) es.selectedOption--;

        es.lastEncoderTime = timestamp;
        showMenu(es.selectedOption);
    }
}

void handleIntensityMode(int en1, int en2, unsigned long timestamp) 
{
    if (en1 == LOW && timestamp > es.lastEncoderTime + DEBOUNCE_PERIOD) 
    {
        if (en2 == HIGH && es.values[es.selectedOption] < 255) es.values[es.selectedOption] += 15;
        else if (en2 == LOW && es.values[es.selectedOption] > 0) es.values[es.selectedOption] -= 15;
        
        es.lastEncoderTime = timestamp;
        analogWrite(getLedPin(es.selectedOption), es.values[es.selectedOption]);
        displayResult(es.values[es.selectedOption], es.selectedOption);
    }
}

void toggleMenuMode() 
{
    isInMenuMode = !isInMenuMode;
    lcd.clear();
    
    if (isInMenuMode) 
    {
        showMenu(es.selectedOption);
    } 
    else {
        displayResult(es.values[es.selectedOption], es.selectedOption);
    }
}