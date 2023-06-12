import psycopg2

db = psycopg2.connect("dbname=lyrics")

def initdb():
    cur = db.cursor()
    with open("init.sql") as f:
        cur.execute(f.read())
    db.commit()
    cur.close()
    
def get_artists():
    cur = db.cursor()
    cur.execute("SELECT name from artists ORDER BY name")
    artists = cur.fetchall()
    ret = []
    for i in artists:
        ret.append(i[0])
    cur.close()
    return ret

def get_tracks_by_artist(artist_name):
    cur = db.cursor()
    cur.execute("SELECT name FROM tracks WHERE artist_id IN (SELECT id FROM artists WHERE name = %s)", (artist_name,))
    tracks = cur.fetchall()
    cur.close()
    return [track[0] for track in tracks]

def save_track_to_db(artist, track, lyrics, db=db):
    #track=track.replace("/","_").replace(" ","_").lower()
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
        artist_id = cur.fetchone()[0]
    print("Id is",artist_id,"Song is",track)

    
    db.commit()
    cur.close()











