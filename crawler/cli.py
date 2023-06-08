import argparse

import liblyrics1

def parse():
    parser = argparse.ArgumentParser(
        prog = "lyrics",
        description = "Offline song lyrics browser")
    
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("listartists", help = "List of artists in the system")
    subparsers.add_parser("initdb", help = "Initialise the database")
    crawl_parser = subparsers.add_parser("crawl", help = "Crawl lyrics")

    crawl_parser.add_argument("--nartists", help="Number of artists to crawl (Default : %(default)s)", 
                              type=int, 
                              default=8)

    crawl_parser.add_argument("--ntracks", help="Number of tracks to crawl per artist (Default : %(default)s)",
                              type=int,
                              default=5)
    gettracks_parser = subparsers.add_parser("gettracks", help="Get all tracks of a specific artist")
    gettracks_parser.add_argument("artist", help="Name of the artist")


    args = parser.parse_args()
    return args

def handle_listartists(args):
    artists=liblyrics1.get
    for idx, name in enumerate(artists, start=1):
        print (f"{idx}. {name}")

def handle_initdb(args):
    liblyrics1.initdb()

def handle_crawl(args):
    print (args)
    liblyrics1.crawl("https://www.songlyrics.com/top-artists-lyrics.html", 
                    args.nartists, 
                    args.ntracks)

def handle_gettracks(args):
    artist_name = args.artist
    tracks = liblyrics1.get_tracks_by_artist(artist_name)
    if tracks:
        for idx, track in enumerate(tracks, start=1):
            print(f"{idx}. {track}")
    else:
        print("No tracks found for the artist.")

def main():
    commands = {"listartists" : handle_listartists,
                "initdb"  : handle_initdb ,
                "crawl" : handle_crawl,
                "gettracks": handle_gettracks}

    args = parse()
    commands[args.command](args)

if __name__ == "__main__":
    main()
    