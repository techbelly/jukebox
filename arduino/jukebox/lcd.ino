#include "serLCD.h"

serLCD lcd = serLCD(10);
String current_display;

serLCD getDisplay(int pin) {
  return lcd;
}

void setDisplay(String string) {
  if (string != current_display) {
    lcd.clear();
    current_display = string;
    lcd.print(string);
  }
}
