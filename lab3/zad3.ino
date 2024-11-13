#include <LiquidCrystal_I2C.h>

#define LED_RED 6

#define DEBOUNCE_PERIOD 10UL

#define RED_BUTTON 2
#define GREEN_BUTTON 4

LiquidCrystal_I2C lcd(0x27, 16, 2);


unsigned long start_time = 0;   
unsigned long stopped_time = 0;     
bool running = false;

void initButtons() 
{
    pinMode(RED_BUTTON, INPUT_PULLUP);
    pinMode(GREEN_BUTTON, INPUT_PULLUP);
}



void reset() 
{
    start_time = millis();
    stopped_time = 0;
    lcd.setCursor(0, 1);
    lcd.print("               ");
}


void update() {
    unsigned long current_time;

    if (running) current_time = millis() - (start_time + stopped_time);
    else current_time = stopped_time;
    
    display(current_time);
}

void display(unsigned long timeInMillis) {
    unsigned long milliseconds = timeInMillis % 1000; 
    unsigned long seconds = (timeInMillis / 1000) % 60;
    unsigned int minutes = (timeInMillis / 60000);

    lcd.setCursor(0, 1);
    lcd.print(minutes);
    lcd.print(":");
    lcd.print(seconds);
    lcd.print(":");
    lcd.print(milliseconds / 10);  
}

void setup() 
{
    initButtons();
    lcd.init();
    lcd.backlight();
    lcd.setCursor(0, 0);
    lcd.print("Stoper: ");
}

bool isGreenButtonPressed() 
{
    static int debounced_button_state = HIGH;
    static int previous_reading = HIGH;
    static unsigned long last_change_time = 0UL;
    bool isPressed = false;
    int current_reading = digitalRead(GREEN_BUTTON);

    if (previous_reading != current_reading)
    {
        last_change_time = millis();
    }

    if (millis() - last_change_time > DEBOUNCE_PERIOD) 
    {
        if (current_reading != debounced_button_state) 
        {
            if (debounced_button_state == HIGH && current_reading == LOW) 
            {
                isPressed = true;
            }
            debounced_button_state = current_reading;
        }
    }

    previous_reading = current_reading;
    return isPressed;
}

bool isRedButtonPressed() 
{
    static int debounced_button_state = HIGH;
    static int previous_reading = HIGH;
    static unsigned long last_change_time = 0UL;
    bool isPressed = false;
    int current_reading = digitalRead(RED_BUTTON);

    if (previous_reading != current_reading) 
    {
        last_change_time = millis();
    }

    if (millis() - last_change_time > DEBOUNCE_PERIOD) 
    {
        if (current_reading != debounced_button_state) 
        {
            if (debounced_button_state == HIGH && current_reading == LOW) 
            {
                isPressed = true;
            }
            debounced_button_state = current_reading;
        }
    }

    previous_reading = current_reading;
    return isPressed;
}


void loop() 
{
    if (isGreenButtonPressed()){
        if (running) stopped_time += millis() - start_time;
        else start_time = millis();
        
        running = !running;
    }

    if (isRedButtonPressed()) {
        reset();
    }

    update();
}