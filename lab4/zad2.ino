#define LED_RED 6
#define LED_GREEN 5
#define LED_BLUE 3

#define RED_BUTTON 2
#define GREEN_BUTTON 4

String color;
int pwmValue;

void setup() 
{
    pinMode(LED_RED, OUTPUT);
    pinMode(LED_GREEN, OUTPUT);
    pinMode(LED_BLUE, OUTPUT);
    
    Serial.begin(9600);
    while (!Serial) {
    }
    Serial.println("Enter command: <color> <pwm_value>");
}

bool isNumber(String str) 
{
    for (int i = 0; i < str.length(); i++) if (!isdigit(str[i])) return false;
    
    return true;
}

bool checkCommand(String command, String &color, int &pwmValue) 
{
    if (command.length() == 0) return false;
    
    command.trim();
    command.toLowerCase();
    
    int spaceIndex = command.indexOf(' ');
    
    if (spaceIndex > 0) 
    {
        color = command.substring(0, spaceIndex);
        String pwmStr = command.substring(spaceIndex + 1);
        
        if (!isNumber(pwmStr)) 
        {
            Serial.println("Invalid PWM value. Must be a number.");
            return false;
        }

        pwmValue = pwmStr.toInt();
        if (pwmValue < 0 || pwmValue > 255)
        {
            Serial.println("Invalid PWM value. Must be between 0 and 255.");
            return false;
        }
        return true;

    } else 
    {
        Serial.println("Enter command: <color> <pwm_value> Invalid command: " + command);
        return false;
    }
}

void setColor(const String &color, int &pwmValue) 
{
    if (color == "red") analogWrite(LED_RED, pwmValue);
    else if (color == "green") analogWrite(LED_GREEN, pwmValue);
    else if (color == "blue") analogWrite(LED_BLUE, pwmValue);
    else 
    {
        Serial.println("Unknown color.");
        return;
    }
    Serial.println("Setting " + color + " to " + String(pwmValue) + "...");
}

void loop() 
{
    String command = Serial.readStringUntil('\n');

    if (checkCommand(command, color, pwmValue)) 
    {    
        setColor(color, pwmValue);
    }
}