# Noddy jukebox for raspberry pi (also works on a mac)

The kids made me build this. 

"Here's how a jukebox works, Daddy: you press some numbers and it plays songs. Then you write all the songs down in a book, ok?" 

So, this is a simple thing where you press some numbers and it plays some songs. I haven't written them down yet.

## running it

It requires libvlc.

Usage:

$ python juke.py _music_folder_

To play a song type the two digit album_id and then the two digit song_id. You can play the whole album by using 00 as the song_id. Type a full-stop '.' to stop playing or to erase a number. Type 'q' to quit.

## the music folder

The music folder needs to be structured as follows:
   + [album_id] album name/
       + [song_id] song name.[mp3|mp4]


So, given 

   + 50 Some Album/
      + 01 First Song.mp3
      + 02 Secong Song.mp3

5001 would play First Song and 5002 Second Song and 5000 The whole album. See, easy?

Clearly it only supports 100 albums using numbers, and a bunch more if you start using letters. 

## optional LCD display

If the environment variable USE_LCD is set, the status output is written to the serial port /dev/ttyAMA0 - which is where I've attached a serial two character LCD display to the Raspberry PI.
