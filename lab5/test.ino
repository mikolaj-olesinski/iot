#include <util/atomic.h>
2 #include <LiquidCrystal_I2C.h>
3
4 #define LED_RED 6
5 #define LED_BLUE 3
6
7 #define ENCODER1 A2
8 #define ENCODER2 A3
9
10 #define DEBOUNCING_PERIOD 100
11
12 LiquidCrystal_I2C lcd(0x27, 16, 2);
13
14 void printResults(int val)
15 {
16 char buffer[40];
17 sprintf(buffer, "Encoder: %3d", val);
18 lcd.setCursor(2, 0);
19 lcd.print(buffer);
20 }
21
22 void myAction(int val)
23 {
24 printResults(val);
25 analogWrite(LED_RED, val);
26 analogWrite(LED_BLUE, 255 - val);
27 }
28
29 void setup()
30 {
31 pinMode(LED_RED, OUTPUT);
32 pinMode(LED_BLUE, OUTPUT);
33 pinMode(ENCODER1, INPUT_PULLUP);
34 pinMode(ENCODER2, INPUT_PULLUP);
35 lcd.init();
36 lcd.backlight();
37 myAction(0);
38
39 PCICR |= (1 << PCIE1);
40 PCMSK1 |= (1 << PCINT10);
41 }
42
43 volatile int encoder1 = HIGH;
44 volatile int encoder2 = HIGH;
45 volatile unsigned long encoderTimestamp = 0UL;
46
47 ISR(PCINT1_vect)
48 {
49 encoder1 = digitalRead(ENCODER1);
9
50 encoder2 = digitalRead(ENCODER2);
51 encoderTimestamp = millis();
52 }
53
54 int encoderValue = 0;
55 int lastEn1 = LOW;
56 unsigned long lastChangeTimestamp = 0UL;
57 void loop()
58 {
59
60 int en1;
61 int en2;
62 unsigned long timestamp;
63
64 ATOMIC_BLOCK(ATOMIC_RESTORESTATE)
65 {
66 en1 = encoder1;
67 en2 = encoder2;
68 timestamp = encoderTimestamp;
69 }
70
71 if (en1 == LOW && timestamp > lastChangeTimestamp + DEBOUNCING_PERIOD)
72 {
73 if (en2 == HIGH)
74 {
75 if (encoderValue < 255)
76 encoderValue += 15;
77 }
78 else
79 {
80 if (encoderValue > 0)
81 encoderValue -= 15;
82 }
83 lastChangeTimestamp = timestamp;
84
85 myAction(encoderValue);
86 }
87 lastEn1 = en1;
88 }