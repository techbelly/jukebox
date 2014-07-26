

#define SHIELD_RESET  -1     
#define SHIELD_CS     7      
#define SHIELD_DCS    6      

#define CARDCS 4     // Card chip select pin
#define DREQ 3       // VS1053 Data request, ideally an Interrupt pin

Adafruit_VS1053_FilePlayer getMusicPlayer() {
  return Adafruit_VS1053_FilePlayer(SHIELD_RESET, SHIELD_CS, SHIELD_DCS, DREQ, CARDCS);
}

boolean beginMusicPlayer() {
  return musicPlayer.begin() && SD.begin(CARDCS);
}
