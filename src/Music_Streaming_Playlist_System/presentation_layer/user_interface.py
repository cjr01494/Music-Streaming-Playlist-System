"""Implements the applicatin user interface."""

from Music_Streaming_Playlist_System.application_base import ApplicationBase
from Music_Streaming_Playlist_System.service_layer.app_services import AppServices
import inspect
import json

"""User interface for Music Streaming Playlist System."""

from Music_Streaming_Playlist_System.application_base import ApplicationBase

class UserInterface(ApplicationBase):
    def __init__(self, services, config):
        self._services = services
        self.META = config["meta"]

        super().__init__(
            subclass_name=self.__class__.__name__,
            logfile_prefix_name=self.META["log_prefix"]
        )
        self._logger.log_debug("__init__:It works!")




    def start(self):
        """Start simple CLI interface."""
        self._logger.log_debug("start: User interface started!")
        print("\n🎵 Welcome to the Music Streaming Playlist System 🎵")

        while True:
            print("""
            ==============================
            1. View all songs
            2. View all playlists
            3. View songs in a playlist
            4. Add a song
            5. Create playlist
            6. Add song to playlist
            7. Delete a song
            8. Delete a playlist
            0. Exit
            ==============================
            """)
            choice = input("Select an option: ")

            if choice == "1":
                self.view_all_songs()
            elif choice == "2":
                self.view_all_playlists()
            elif choice == "3":
                self.view_songs_in_playlist()
            elif choice == "4":
                self.add_song()
            elif choice == "5":
                self.create_playlist()
            elif choice == "6":
                self.add_song_to_playlist()
            elif choice == "7":
                self.delete_song()
            elif choice == "8":
                self.delete_playlist()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Try again!")

    # ---- Menu Actions ----
    def view_all_songs(self):
        songs = self._services.get_all_songs()
        print("\n--- Songs ---")
        for s in songs:
            print(f"{s[0]} | {s[1]} | {s[2]} | {s[3]} | {s[4]}")

    def view_all_playlists(self):
        playlists = self._services.get_all_playlists()
        print("\n--- Playlists ---")
        for p in playlists:
            print(f"{p[0]} | {p[1]} | {p[2]}")

    def view_songs_in_playlist(self):
        playlist_id = input("Enter playlist ID: ")
        songs = self._services.get_songs_by_playlist(int(playlist_id))
        print(f"\n--- Songs in Playlist {playlist_id} ---")
        for s in songs:
            print(f"{s[0]} | {s[1]} | {s[2]}")

    def add_song(self):
        title = input("Title: ")
        artist = input("Artist: ")
        album = input("Album: ")
        duration = input("Duration (e.g., 3:30): ")

        song_id = self._services.add_song(title, artist, album, duration)
        print(f"Added song ID: {song_id}")

    def create_playlist(self):
        name = input("Playlist name: ")
        desc = input("Description: ")
        pid = self._services.create_playlist(name, desc)
        print(f"Created playlist ID: {pid}")

    def add_song_to_playlist(self):
        pid = input("Playlist ID: ")
        sid = input("Song ID: ")
        self._services.add_song_to_playlist(int(pid), int(sid))
        print("Song added to playlist")

    def delete_song(self):
        print("\n--- Delete Song ---")
        songs = self._services.get_all_songs()
        if not songs:
            print("No songs available.")
            return
        for song in songs:
            print(f"{song[0]} | {song[1]} by {song[2]}")

        try:
            song_id = int(input("Enter the song ID to delete: "))
            self._services.delete_song_by_id(song_id)
            print("Song deleted successfully!")
        except Exception as e:
            print(f"Error deleting song: {e}")


    def delete_playlist(self):
        print("\n--- Delete Playlist ---")
        playlists = self._services.get_all_playlists()
        if not playlists:
            print("No playlists available.")
            return
        for playlist in playlists:
            print(f"{playlist[0]} | {playlist[1]} - {playlist[2]}")

        try:
            playlist_id = int(input("Enter the playlist ID to delete: "))
            self._services.delete_playlist_by_id(playlist_id)
            print("Playlist deleted successfully!")
        except Exception as e:
            print(f"Error deleting playlist: {e}")



