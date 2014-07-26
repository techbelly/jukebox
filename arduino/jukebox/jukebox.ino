#include <SoftwareSerial.h>
#include <serLCD.h>
#include <Keypad.h>
#include <SPI.h>
#include <Adafruit_VS1053.h>
#include <SD.h>

Keypad keypad = getKeypad();
Adafruit_VS1053_FilePlayer musicPlayer = getMusicPlayer();


String keypresses = "";
String lastsong = "";

void setup() {

  Serial.begin(9600);
  setDisplay("Starting Up");
  
  
  if (! beginMusicPlayer()) {
    setDisplay("Initializing failed.");
    while (1);
  }
  musicPlayer.setVolume(20,20);
  musicPlayer.useInterrupt(VS1053_FILEPLAYER_PIN_INT);
  delay(100);
}

void updateDisplay() {
  if (keypresses.length() > 0) {
    setDisplay("Take me to      "+keypresses + "_");
  } else if (musicPlayer.playingMusic) {
    setDisplay("Travelling to   "+lastsong);
  } else {
    setDisplay("Ready to take   you back");
  }
}


void loop() {  

  char key = keypad.getKey();
  char charBuf[10];

  if (key) {
    if (key == '#') {
      if (keypresses.length() > 0) {
        keypresses = keypresses.substring(0, keypresses.length() - 1);
      } else {
         musicPlayer.stopPlaying();
      }
    } else {
      keypresses = keypresses + key;
      updateDisplay();  
      if (keypresses.length() == 4) {
        (keypresses + ".mp3").toCharArray(charBuf, 10);
        musicPlayer.startPlayingFile(charBuf);
        lastsong = keypresses;
        keypresses = "";
      }
    }
  }
  updateDisplay();  
}
