
const byte ROWS = 4; //four rows
const byte COLS = 3; //three columns
char keys[ROWS][COLS] = {
    {'1','2','3'},
    {'4','5','6'},
    {'7','8','9'},
    {'*','0','#'}
};

byte rowPins[ROWS] = {A5, A4, A3, A2}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {A1, A0, 9}; //connect to the column pinouts of the keypad

Keypad getKeypad() {
  Keypad  keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );
  return keypad;
}
