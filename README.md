Noddy jukebox for raspberry pi (also works on a mac)

The kids made me build this. 

"Here's how a jukebox words, Daddy: you press some numbers and it plays songs. Then you write all the songs down in a book, ok?" 

So, this is a simple thing where you press some numbers and it plays some songs.

It requires libvlc.

Usage: python juke.py _music_folder_

The music folder needs to be structured as follows:
   + [album_id] album name/
       + [song_id] song name.[mp3|mp4]

To play the album enter the two digit album_id and then the two_digit song_id. You can play the whole album by using 00 as the song_is. Press a period '.' to stop playing or to erase a number.

So, given 

   + 50 Some Album/
      + 01 First Song.mp3
      + 02 Secong Song.mp3

5001 would play First Song and 5002 Second Song and 5000 The whole album. See, easy?

If the environment variable USE_LCD is set, the display is written to the serial port /dev/ttyAMA0, assuming there's a serial two character LCD display attached.
