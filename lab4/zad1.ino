const int redButtonPin = 2; 
const int greenButtonPin = 4;

void setup() 
{
    Serial.begin(115200);
    pinMode(redButtonPin, INPUT_PULLUP);
    pinMode(greenButtonPin, INPUT_PULLUP); 

    while (!Serial) {
    }
}

void loop() 
{
    int redButtonState = digitalRead(redButtonPin);
    int greenButtonState = digitalRead(greenButtonPin); 

    int redValue = (redButtonState == LOW) ? 1 : 0;
    int greenValue = (greenButtonState == LOW) ? 1 : 0;

    Serial.print("Green button state: " + String(greenValue));
    Serial.println("\t Red button state: " + String(redValue));

    delay(100); 
}