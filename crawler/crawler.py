from bs4 import BeautifulSoup
import os
import requests
import psycopg2

db = psycopg2.connect("dbname=lyrics")

def get_artists(data):
    soup = BeautifulSoup(data, features="html.parser") # Create soup
    artists = soup.find_all("td", {"class": "td-last"}) # Search for all artist td nodes
    ret = []
    for i in artists: # For each td node
        a = i.find("a") # Get the anchor inside the td
        ret.append((a.text.strip(), a["href"]))
    return ret    
     # Extract the name and target from anchor
    # for i in ret:
    #     with open("artists.txt","w") as f:


    # return ret

def get_tracks(data):
    count=5
    soup = BeautifulSoup(data, features="html.parser")
    tracks = soup.find("table", {"class" : "tracklist"})
    ret=[]
    for track in list(tracks.find_all("a")):
        lyrics_page = requests.get(track['href']).text
        lyrics = get_song_lyrics(lyrics_page)
        ret.append([track.text.strip(), lyrics])
        if count == 0:
            break
        count -=1
    return ret
    #  for i in lyrics:
    #     a=i.find_all("a")[:5]
    #     for b in a:
    #      ret1.append((b.text.strip(), b["href"]))
    #  return ret1

def get_song_lyrics(data):
    soup=BeautifulSoup(data,features="html.parser")
    lyrics=soup.find("p",{"id" : "songLyricsDiv"})
    if lyrics:
        lyrics=lyrics.text
    else :
        lyrics=" "
    return lyrics

def save_track_to_db(artist, track, lyrics, db=db):
    track=track.replace("/","_").replace(" ","_").lower()
    cur = db.cursor()
    cur.execute("SELECT id from artists where name = %s", (artist,))
    artist_id = cur.fetchone()
    if artist_id:
        artist_id = artist_id[0]
        cur.execute("INSERT INTO tracks (artist_id, name ,lyrics) VALUES (%s, %s, %s)", (artist_id, track, lyrics))
        cur.execute("SELECT artist_id, name FROM tracks WHERE artist_id=%s AND name=%s", (artist_id, track))
        artist_id, track = cur.fetchone()
    else:
        cur.execute("INSERT INTO artists (name) VALUES(%s)", (artist,))
        cur.execute("SELECT id from artists where name = %s", (artist,))
        artist_id = cur.fetchone()
    print("Id is",artist_id,"Song is",track)

    
    db.commit()
    cur.close()

def save_track(artist, track, lyrics):
    artist = artist.replace("/","_").replace(" ","_").lower()
    track = track.replace("/","_").replace(" ","_").lower()
    artist_dir = os.path.join("hit_songs", artist)
    os.makedirs(artist_dir,exist_ok=True)
    track_path = os.path.join(artist_dir, track) + ".txt"
    # new=get_song_lyrics(lyrics)
    with open(track_path, "w") as f:
        f.write(lyrics)

def crawl(start_url):
    data = requests.get(start_url).text
    artists = get_artists(data)[:5]
    for artist_name, artist_link in artists:
        tracks_page = requests.get(artist_link).text
        tracks = get_tracks(tracks_page)[:5]
        for track_name, lyrics in tracks:
            save_track(artist_name, track_name, lyrics)
            save_track_to_db(artist_name, track_name, lyrics, db=db)

        
def main():
   crawl("https://www.songlyrics.com/top-artists-lyrics.html")
    
if __name__ =="__main__":
    main()
            





    




           












