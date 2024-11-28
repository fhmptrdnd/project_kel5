import lyricsgenius
import sys
import time

API_KEY = "7xujk1yQ1x-VRZy5HWmp2AJY33P06Ge1EGmlXgPWEHJ7_46t3mhVnCIfCzP-cqz3"
artist = "Phoebe Bridgers"
song = "Scott Street"

genius = lyricsgenius.Genius(access_token=API_KEY)
artist = genius.search_artist(artist_name=artist, max_songs=3, sort="title")
song = artist.song(song_name=song)
lyrics = song.lyrics

try:
    for letter in lyrics:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.1)
except KeyboardInterrupt:
    sys.exit()