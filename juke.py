#!/usr/bin/env python
import sys
import glob
import os
import vlc
import curses
from display import PiLcdDisplay, CursesDisplay
from collections import defaultdict
from contextlib import contextmanager

if 'USE_LCD' in os.environ:
    Display = PiLcdDisplay
else:
    Display = CursesDisplay


def songs_in(folder):
    file_paths = glob.glob(
        folder + "/**/*.m4a") + glob.glob(folder + "/**/*.mp3")

    def file_prefix_number(path):
        return int(os.path.basename(path).split(" ")[0], base=10)

    for path in file_paths:
        song = file_prefix_number(path)
        album = file_prefix_number(os.path.dirname(path))
        yield (album, song, path)


def build_songbook(folder):
    songbook = defaultdict(dict)
    for (album, song, path) in songs_in(folder):
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


def path_component(path, num):
    return path.split("/")[num]


def name_without_number(path, num):
    return " ".join(path_component(path, num).split(" ")[1:])


def song_from_path(path):
    return ".".join(name_without_number(path, -1).split(".")[:-1])


def album_from_path(path):
    return name_without_number(path, -2)


def format_title(album_id, song_id, title):
    return "%02d%02d: %s" % (album_id, song_id, title)


def play_whole_album(songbook, album_id, song_id, display, player):
    album = songbook[album_id]
    songs = [album[key] for key in sorted(album.keys())]
    if songs:
        title = format_title(album_id, song_id, album_from_path(songs[0]))
        play_list(songs, player, title)


def play_single_song(songbook, album_id, song_id, display, player):
    song = songbook[album_id][song_id]
    title = format_title(album_id, song_id, song_from_path(song))
    play_list([song], player, title)


def play_song(songbook, album_id, song_id, display, player):
    if album_id in songbook:
        if song_id == 0:
            play_whole_album(songbook, album_id, song_id, display, player)
        elif song_id in songbook[album_id]:
            play_single_song(songbook, album_id, song_id, display, player)


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
        display.set("".join(keypresses) + "_")
    elif player.is_playing() and player.current_song:
        display.set(player.current_song)
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
        curses.nocbreak()
        stdscr.keypad(0)
        curses.echo()
        curses.endwin()


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("Usage: $0 folder")
        sys.exit(1)

    with curses_context() as screen:
        music_folder = sys.argv[1]
        display = Display(screen)
        display.set("Starting up", "")
        songbook = build_songbook(music_folder)
        player = make_player()
        main_loop(display, songbook, player, screen)
