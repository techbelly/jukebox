#!/usr/bin/env python
import sys, glob, os
import vlc
import curses
from display import PiLcdDisplay, FakeDisplay
from collections import defaultdict
from contextlib import contextmanager

if 'USE_LCD' in os.environ:
    Display = PiLcdDisplay
else: 
    Display = FakeDisplay

def songs_in(folder):
    file_paths = glob.glob(folder+"/**/*.m4a") + glob.glob(folder+"/**/*.mp3")

    def file_prefix_number(path):
        return int(os.path.basename(path).split(" ")[0], base=10)

    for path in file_paths:
        song = file_prefix_number(path)
        album = file_prefix_number(os.path.dirname(path))
        yield (album, song, path)

def build_songbook(folder):
    songbook = defaultdict(dict) 
    for (album, song, path) in songs_in(sys.argv[1]):
        songbook[album][song] = path 
    return songbook

def make_player():
    player = vlc.MediaPlayer()
    mlplayer = vlc.MediaListPlayer()
    mlplayer.set_media_player(player)
    return mlplayer

def play_list(songs, player, current_song):
    player.stop()
    medialist = vlc.MediaList(songs)
    player.set_media_list(medialist)
    player.current_song = current_song
    player.play()

def play_song(songbook, album_id, song_id, display, player):
    song_number = "%02d%02d" % (album_id,song_id) 
    if album_id in songbook and song_id == 0:
        album = songbook[album_id]
        if album:
            songs = [album[key] for key in sorted(album.keys())] 
            play_list(songs, player, song_number)
    elif album_id in songbook and song_id in songbook[album_id]:
        play_list([songbook[album_id][song_id]], player, song_numer)


def convert_keypresses(keypresses):
    album = int("".join(keypresses[0:2]), base=10)
    song = int("".join(keypresses[2:4]), base=10)
    return (album, song)

def getch(key, songbook, display, keypresses, player):
    if ord("0") <= key <= ord("9"):
        keypresses.append(chr(key))
        if len(keypresses) == 4:
            album, song = convert_keypresses(keypresses)
            play_song(songbook, album, song, display, player)
            keypresses[:] = []
    if key == ord("."):
        if len(keypresses):
            keypresses.pop()
        else:
            player.stop()


def update_display(keypresses, player):
    if len(keypresses):
        display.set("".join(keypresses)+"_")
    elif player.is_playing() and player.current_song:
        display.set("Playing "+player.current_song)
    else:
        display.set("READY")


def main_loop(display, songbook, player, stdscr):
    keypresses = [] 
    key = ''

    while key != ord('q'):
        update_display(keypresses, player)
        key = stdscr.getch()
        if key != -1:
            getch(key, songbook, display, keypresses, player) 

@contextmanager
def curses_context():
    try:
        stdscr = curses.initscr()
        stdscr.timeout(1000)
        curses.cbreak()
        stdscr.keypad(1)
        yield stdscr
    finally:
        curses.nocbreak(); stdscr.keypad(0); curses.echo()
        curses.endwin()


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: $0 folder")
        sys.exit(1)

    with curses_context() as screen:
        music_folder = sys.argv[1]
        display = Display(screen)
        display.set("Starting up","")
        songbook = build_songbook(music_folder)
        player = make_player()
        main_loop(display, songbook, player, screen)
