import os

import crawler

def test_get_popular_artists():
    data_file = os.path.join(os.path.dirname(__file__), "data", "top-artists-lyrics.html")
    with open(data_file) as f:
        data = f.read()
    artists = crawler.get_artists(data)
    name0, link0 = artists[0]
    name1, link1 = artists[1]
    name99, link99 = artists[98]
    name100, link100 = artists[99]

    assert len(artists) == 100

    assert name0 == "Hillsong"
    assert link0 == "https://www.songlyrics.com/hillsong-lyrics/"
    assert name1 == "Eminem"
    assert link1 == "https://www.songlyrics.com/eminem-lyrics/"

    assert name99 == "Skrillex"
    assert link99 == "https://www.songlyrics.com/skrillex-lyrics/"

    assert name100 == "Shakira"
    assert link100 == "https://www.songlyrics.com/shakira-lyrics/"

def test_get_popular_artists_song():
    song_file = os.path.join(os.path.dirname(__file__), "data", "hillsong.html")
    with open(song_file) as f:
        data=f.read()
    lyrics=crawler.get_lyrics(data)
    lyr1, link1 = lyrics[0]

    assert lyr1=="Oceans (Where Feet May Fail)"
    assert link1=="https://www.songlyrics.com/hillsong/oceans-where-feet-may-fail-lyrics/"

def test_get_song_lyrics():
    lyric_file=os.path.join(os.path.dirname(__file__),"data","lyrics.html")
    with open(lyric_file) as f:
        data=f.read()
    song_line=crawler.get_song_lyrics(data) 
    assert song_line.startswith("You call me out upon the waters")
    assert song_line.endswith("I am Yours and You are mine")

