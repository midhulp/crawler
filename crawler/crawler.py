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

def get_lyrics(data):
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

def get_save_lyrics(data):
    
    # artists = get_artists(data)
    # lyrics = get_lyrics(data)

    for i in data:
            name = i[0]
            link = i[1]
            song_data= requests.get(link)
            song_html_content = song_data.text
            artist_folder = os.path.join("artists", name)
            os.makedirs(artist_folder, exist_ok=True)
            songs = get_lyrics(song_html_content)
            
    
            for i in songs :
                name = i[0].replace('/','_')
                link = i[1]
                if link:
                        lyrics_get = requests.get(link)
                        lyrics_file = lyrics_get.text
                        lyrics = get_song_lyrics(lyrics_file)
                        # song_folder = os.path.join(artist_folder, name)
                        
                        # os.makedirs(artist_folder, exist_ok=True)
                        song_filename = os.path.join(artist_folder, f"{name}.txt")
                        
                        with open(song_filename, "w") as f:
                            f.write(lyrics)



def main():
      data_file = os.path.join(os.path.dirname(__file__),"tests", "data", "top-artists-lyrics.html")
      with open(data_file) as file:
          data = file.read()
          song_data = get_artists(data)[:5]
          get_save_lyrics(song_data)
    #   get_save_lyrics(data)
        #  print("Done")


if __name__ =="__main__":
    main()
    







# def main():
#         data=requests.get().text)
#          get_artists(data)

