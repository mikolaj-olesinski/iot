#include "RGBController.h"

void RGBController::init(byte pinR, byte pinG, byte pinB) {
    pinR_ = pinR;
    pinG_ = pinG;
    pinB_ = pinB;

    pinMode(pinR_, OUTPUT);
    pinMode(pinG_, OUTPUT);
    pinMode(pinB_, OUTPUT);

    setColor(0, 0, 0);
}

void RGBController::setColor(byte r, byte g, byte b) {
    writeColor(r, g, b);
}

void RGBController::setColor(String colorName) {
    if (colorName == "RED") writeColor(255, 0, 0);
    else if (colorName == "GREEN") writeColor(0, 255, 0);
    else if (colorName == "BLUE") writeColor(0, 0, 255);
    else if (colorName == "YELLOW") writeColor(255, 255, 0);
    else if (colorName == "CYAN") writeColor(0, 255, 255);
    else if (colorName == "MAGENTA") writeColor(255, 0, 255);
    else if (colorName == "WHITE") writeColor(255, 255, 255);
    else if (colorName == "BLACK") writeColor(0, 0, 0);
    else writeColor(0, 0, 0);
}

void RGBController::writeColor(byte r, byte g, byte b) {
    analogWrite(pinR_, r);
    analogWrite(pinG_, g);
    analogWrite(pinB_, b);
}
