#define RED_LED 6
#define GREEN_LED 5
#define BLUE_LED 3

#define RED_BUTTON 2
#define GREEN_BUTTON 4

int currentColor = 0; // red = 0, blue = 1, green = 2
boolean ledOn = false;

void setup() {
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(BLUE_LED, OUTPUT);

  pinMode(RED_BUTTON, INPUT_PULLUP);
  pinMode(GREEN_BUTTON, INPUT_PULLUP);

  digitalWrite(RED_LED, LOW);
  digitalWrite(BLUE_LED, LOW);
  digitalWrite(GREEN_LED, LOW);
}

void loop() {
  if (digitalRead(RED_BUTTON) == LOW) { 
    ledOn = !ledOn;  
    delay(300);  
  }

  if (digitalRead(GREEN_BUTTON) == LOW) { 
    currentColor = (currentColor + 1) % 3;  
    delay(300);  
  }
  
  if (ledOn) {
    if (currentColor == 0) {
      digitalWrite(RED_LED, HIGH);
      digitalWrite(BLUE_LED, LOW);
      digitalWrite(GREEN_LED, LOW);
    }
    else if (currentColor == 1) {
      digitalWrite(RED_LED, LOW);
      digitalWrite(BLUE_LED, HIGH);
      digitalWrite(GREEN_LED, LOW);
    }
    else if (currentColor == 2) {
      digitalWrite(RED_LED, LOW);
      digitalWrite(BLUE_LED, LOW);
      digitalWrite(GREEN_LED, HIGH);
    }

  } else {
    digitalWrite(RED_LED, LOW);
    digitalWrite(BLUE_LED, LOW);
    digitalWrite(GREEN_LED, LOW);
  }
}