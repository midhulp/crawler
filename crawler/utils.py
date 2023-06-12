import logging
import os


def save_track(artist, track, lyrics):
    artist = artist.replace("/","_").replace(" ","_").lower()
    track = track.replace("/","_").replace(" ","_").lower()
    artist_dir = os.path.join("hit_songs", artist)
    os.makedirs(artist_dir,exist_ok=True)
    track_path = os.path.join(artist_dir, track) + ".txt"
    # new=get_song_lyrics(lyrics)
    with open(track_path, "w") as f:
        f.write(lyrics)

def setup_logger(debug):
    l = logging.getLogger("lyrics")
    l.setLevel(logging.DEBUG)
    h = logging.StreamHandler()
    if debug:
        h.setLevel(logging.DEBUG)
    else:
        h.setLevel(logging.INFO)
    h.setFormatter(logging.Formatter("[%(levelname)s] %(filename)s:%(lineno)d : %(message)s"))
    l.addHandler(h)
    
def get_logger():
    return logging.getLogger("lyrics")