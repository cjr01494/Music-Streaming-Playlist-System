"""Entry point for the Music Streaming Playlist System."""

import json
import inspect
from argparse import ArgumentParser

from Music_Streaming_Playlist_System.presentation_layer.user_interface import UserInterface
from Music_Streaming_Playlist_System.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
from Music_Streaming_Playlist_System.service_layer.app_services import AppServices

print(">>> MAIN IMPORTED WRAPPER FROM:", inspect.getfile(MySQLPersistenceWrapper))

def main():
    """Entry point."""
    args = configure_and_parse_commandline_arguments()

    with open(args.configfile, 'r') as f:
        config = json.loads(f.read())
        print(config)

    # Create DB Connection Wrapper
    db = MySQLPersistenceWrapper(config)

    # Service layer
    services = AppServices(config, db)


    # UI
    ui = UserInterface(services, config)

    print(f"{inspect.currentframe().f_code.co_name}: Starting User Interface")

    # personal pref on where the tables are printed 
    #ui.start()

    print("\n--- Database Songs Test ---")
    songs_list = db.select_all_songs()
    for song in songs_list:
        print(song)

    print("\n--- Database Playlists Test ---")
    playlists_list = db.select_all_playlists()   
    for pl in playlists_list:
        print(pl)

    ui.start()






def configure_and_parse_commandline_arguments():
    """Configure and parse command-line arguments."""
    parser = ArgumentParser(
        prog='main.py',
        description='Start the application with a configuration file.',
        epilog='POC: Cara Rocha-Ortanez | cjr01494@marymount.edu'
    )

    parser.add_argument('-c', '--configfile',
                        help="Configuration file to load.",
                        required=True)
    return parser.parse_args()


if __name__ == "__main__":
    main()
