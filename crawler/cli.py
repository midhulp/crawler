import argparse
import models
import db
import utils
import web
import liblyrics1
import sqlalchemy as sa
from sqlalchemy.orm import Session
logger=utils.get_logger()

def parse():
    parser = argparse.ArgumentParser(
        prog = "lyrics",
        description = "Offline song lyrics browser")
    parser.add_argument("-d", "--debug", help = "Display detailed debug", action="store_true", default=False)
    
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("web", help = "Run web server")
    subparsers.add_parser("test", help = "Temporary testing")
    subparsers.add_parser("listartists", help = "List of artists in the system")
    subparsers.add_parser("initdb", help = "Initialise the database")
    crawl_parser = subparsers.add_parser("crawl", help = "Crawl lyrics")

    crawl_parser.add_argument("--nartists", help="Number of artists to crawl (Default : %(default)s)", 
                              type=int, 
                              default=3)

    crawl_parser.add_argument("--ntracks", help="Number of tracks to crawl per artist (Default : %(default)s)",
                              type=int,
                              default=3)
    gettracks_parser = subparsers.add_parser("gettracks", help="Get all tracks of a specific artist",)
    gettracks_parser.add_argument("artist", help="Name of the artist")


    args = parser.parse_args()
    return args

def handle_listartists(args):
    # artists=db.get_artists()
    # for idx, name in enumerate(artists, start=1):
    #     print (f"{idx}. {name}")
    db = models.init_db(web.app, "postgresql:///lyrics")
    with web.app.app_context():
        artists = db.session.execute(db.select(models.Artist)).scalars()
        for idx,artist in enumerate(artists, start=1):
            print (f"{idx}. {artist.name}")

def handle_initdb(args):
    db = models.init_db(web.app, "postgresql:///lyrics")
    with web.app.app_context():
        db.drop_all()
        db.create_all()

def handle_crawl(args):
    db = models.init_db(web.app, "postgresql:///lyrics")
    liblyrics1.crawl("https://www.songlyrics.com/top-artists-lyrics.html", 
                    args.nartists, 
                    args.ntracks)

def handle_gettracks(args):
    artist_name = args.artist
    tracks = db.get_tracks_by_artist(artist_name)
    if tracks:
        for idx, track in enumerate(tracks, start=1):
            print(f"{idx}. {track}")
    else:
        print("No tracks found for the artist or \nEnter in 'Firstname Lastname' format for artist with firstname and lastname\nRun crawl if no artist found")

def handle_test(args):
    engine = sa.create_engine("postgresql:///lyrics")
    query= sa.select(models.Artist)
    with Session(engine) as sess:
        results = sess.scalars(query)
        for artist in results:
            print (artist.name)
            for song in artist.tracks:
                print("   ", song.name)

def handle_web(args):
    db = models.init_db(web.app, "postgresql:///lyrics")
    web.app.run()


def main():
    commands = {"listartists" : handle_listartists,
                "initdb"  : handle_initdb ,
                "crawl" : handle_crawl,
                "gettracks": handle_gettracks,
                 "test" : handle_test,
                 "web" :handle_web}

    args = parse()
    utils.setup_logger(args.debug)
    commands[args.command](args)

if __name__ == "__main__":
    main()
    