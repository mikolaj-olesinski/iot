#ifndef RGBCONTROLLER_H_
#define RGBCONTROLLER_H_

#include "Arduino.h"

class RGBController {
public:
    void init(byte pinR, byte pinG, byte pinB);
    void setColor(byte r, byte g, byte b);
    void setColor(String colorName);

private:
    byte pinR_, pinG_, pinB_;
    void writeColor(byte r, byte g, byte b);
};

#endif
