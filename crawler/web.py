from flask import Flask

import models

app = Flask("lyrics")


@app.route("/")
def index():
    db = models.init_db(app)
    artists_count = db.session.scalar(db.select(db.func.count(models.Artist.id)))
    tracks_count = db.session.scalar(db.select(db.func.count(models.Tracks.id)))
    return f"<h1>Welcome to the lyrics server. We have {artists_count} artists and {tracks_count} tracks.</h1>"

@app.route("/user/<id>")
def users(id):
    return f"You asked for user {id}"

@app.route("/artist")
def artist():
     
     db=models.init_db(app)
     artists=db.session.execute(db.select(models.Artist.name))
     new="<h1>List of artists</h1>"
     for artist in artists:
        #  for i,j in artist:
        #      new+=i.name
         



         new += f"<p>->{artist.name}</p>"
        #  return artists
     return new
         
@app.route("/artist/tracks")
def artist_tracks():
    db = models.init_db(app)
    query = db.session.query(models.Artist.name, models.Tracks.name).join(models.Tracks)
    tracks = query.all()
    new = "<h1>List of tracks and their artists</h1>"
    for artist_name, track_name in tracks:
        new += f"<p>{artist_name}=>{track_name}</p>"
    return new
