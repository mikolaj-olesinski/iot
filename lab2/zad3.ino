#define GREEN_LED 5
#define RED_LED 6
#define BLUE_LED 3

void setup() {
  pinMode(RED_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
  pinMode(BLUE_LED, OUTPUT);
}

void loop() {
  for (int i = 0; i <= 255; i++) {
    analogWrite(RED_LED, 255 - i);   
    analogWrite(BLUE_LED, i);        
    delay(10);  
  }

  for (int i = 0; i <= 255; i++) 
  {
    analogWrite(BLUE_LED, 255 - i);  
    analogWrite(GREEN_LED, i);       
    delay(10);
  }

  for (int i = 0; i <= 255; i++) {
    analogWrite(GREEN_LED, 255 - i); 
    analogWrite(RED_LED, i);         
    delay(10);
  }
}