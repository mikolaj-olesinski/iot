#define GREEN_LED 5

#define RED_BUTTON 2
#define GREEN_BUTTON 4

int currentPower = 0;
int step = 10;

void setup() {
  pinMode(GREEN_LED, OUTPUT);
  pinMode(RED_BUTTON, INPUT_PULLUP);
  pinMode(GREEN_BUTTON, INPUT_PULLUP);

  digitalWrite(GREEN_LED, LOW);
}

void loop() {
  if (digitalRead(GREEN_BUTTON) == LOW) {
    if ((currentPower + step) > 255) {
      currentPower = 255;
    }
    else currentPower += step;

    analogWrite(GREEN_LED, currentPower);
    delay(300);
  }

  if (digitalRead(RED_BUTTON) == LOW) {
    if ((currentPower - step) < 0) {
      currentPower = 0;
    }
    else currentPower -= step;

    analogWrite(GREEN_LED, currentPower);
    delay(300);
  }
}