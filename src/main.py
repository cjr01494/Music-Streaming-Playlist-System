"""Entry point for the Employee Training Application."""

import json
from argparse import ArgumentParser
from Music_Streaming_Playlist_System.presentation_layer.user_interface import UserInterface
from Music_Streaming_Playlist_System.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper



def main():
	"""Entry point."""
	args = configure_and_parse_commandline_arguments()

	if args.configfile:
		config = None
		with open(args.configfile, 'r') as f:
			config = json.loads(f.read())
			print(config)

		db = MySQLPersistenceWrapper(config)
		songs_list = db.select_all_songs()
		for song in songs_list:
			print(f'{song}')
	ui = UserInterface(config)
	ui.start()
			
		


def configure_and_parse_commandline_arguments():
	"""Configure and parse command-line arguments."""
	parser = ArgumentParser(
	prog='main.py',
	description='Start the application with a configuration file.',
	epilog='POC: Cara Rocha-Ortanez | cjr01494@marymount.edu')

	parser.add_argument('-c','--configfile',
					help="Configuration file to load.",
					required=True)
	args = parser.parse_args()
	return args



if __name__ == "__main__":
	main()