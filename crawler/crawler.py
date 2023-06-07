from bs4 import BeautifulSoup
import os
import requests

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
     soup = BeautifulSoup(data, features="html.parser")
     lyrics = soup.find_all("table", {"class" : "tracklist"})
     ret1=[]
     for i in lyrics:
        a=i.find_all("a")[:5]
        for b in a:
         ret1.append((b.text.strip(), b["href"]))
     return ret1

def get_song_lyrics(data):
    soup=BeautifulSoup(data,features="html.parser")
    song_line=[]
    song_line=soup.find("p",{"id" : "songLyricsDiv"})
    if song_line:
        song_line=song_line.text
    else :
        song_line=" "
    return song_line

def save_track(artist, track, lyrics):
    artist = artist.replace("/","_").replace(" ","_").lower()
    track = track.replace("/","_").replace(" ","_").lower()
    artist_dir = os.path.join("hit_songs", artist)
    os.makedirs(artist_dir,exist_ok=True)
    track_path = os.path.join(artist_dir, track) + ".txt"
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
        
def main():
   crawl("https://www.songlyrics.com/top-artists-lyrics.html")
    
if __name__ =="__main__":
    main()
            





    




           












