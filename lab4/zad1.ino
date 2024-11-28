#define RED_BUTTON 2
#define GREEN_BUTTON 4

void setup() 
{
    Serial.begin(9600);
    pinMode(RED_BUTTON, INPUT_PULLUP);
    pinMode(GREEN_BUTTON, INPUT_PULLUP); 

    while (!Serial) {
    }
}

void loop() 
{

    Serial.println("Red:" + String(!digitalRead(RED_BUTTON)) + "\t" + "Green:" + String(!digitalRead(GREEN_BUTTON)));

    delay(100); 
}