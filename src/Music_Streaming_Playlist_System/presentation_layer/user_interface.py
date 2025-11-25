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
        #error tester
        #self._logger.log_debug("__init__:It works!")


    def get_non_empty(self,prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Input cannot be empty.")


    def start(self):
        """Start simple CLI interface."""
        #error tester
        #self._logger.log_debug("start: User interface started!")
        print("\nWelcome to the Music Streaming Playlist System")

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
        print(f"{'ID':<5} {'Title':<30} {'Artist':<35} {'Album':<40} {'Duration':<10}")
        print("-" * 125)

        for s in songs:
            print(f"{s[0]:<5} {s[1]:<30} {s[2]:<35} {s[3]:<40} {s[4]:<10}")


    def view_all_playlists(self):
        playlists = self._services.get_all_playlists()
        print("\n--- Playlists ---")
        print(f"{'ID':<5} {'Name':<35} {'Description':<60}")
        print("-" * 100)
        for p in playlists:
            print(f"{p[0]:<5} {p[1]:<35} {p[2]:<60}")



    def view_songs_in_playlist(self):
        playlists = self._services.get_all_playlists()
        print("\n--- Playlists ---")
        print(f"{'ID':<5} {'Name':<35} {'Description':<60}")
        print("-" * 100)
        for p in playlists:
            print(f"{p[0]:<5} {p[1]:<35} {p[2]:<60}")
        #playlist_id = input("\nEnter playlist ID: ")
        # Loop until valid playlist ID is chosen
        valid_ids = [p[0] for p in playlists]   # first element is ID

        while True:
            try:
                playlist_id = int(input("\nEnter playlist ID: "))
                if playlist_id in valid_ids:
                    break
                else:
                    print("Invalid playlist ID. Please choose one from the list.")
            except ValueError:
                print("Please enter a valid number.")

        songs = self._services.get_songs_by_playlist(int(playlist_id))
        # Find playlist name from playlists list
        playlist_name = next((p[1] for p in playlists if p[0] == playlist_id), "Unknown")

        print(f"\n--- Songs in Playlist, {playlist_name}  ---")

        # Header row with larger Artist and Album widths
        print(f"{'ID':<5} {'Title':<30} {'Artist':<35} {'Album':<40} {'Duration':<10}")
        print("-" * 125)

        if not songs:
            print("No songs found in this playlist.")
            return

        for s in songs:
            # Some SELECT queries may not include album/duration depending on your join
            # So we handle missing indexes gracefully
            title = s[1] if len(s) > 1 else ""
            artist = s[2] if len(s) > 2 else ""
            album = s[3] if len(s) > 3 else ""
            duration = s[4] if len(s) > 4 else ""

            print(f"{s[0]:<5} {title:<30} {artist:<35} {album:<40} {duration:<10}")


    def add_song(self):
        title = self.get_non_empty("Title: ")
        artist = self.get_non_empty("Artist: ")
        album = self.get_non_empty("Album: ")
        duration = self.get_non_empty("Duration (e.g., 3:30): ")

        song_id = self._services.add_song(title, artist, album, duration)
        print(f"Added song ID: {song_id}")

    def create_playlist(self):
        name = self.get_non_empty("Playlist name: ")
        desc = self.get_non_empty("Description: ")
        pid = self._services.create_playlist(name, desc)
        print(f"Created playlist ID: {pid}")

    def add_song_to_playlist(self):
        songs = self._services.get_all_songs()
        print("\n--- Songs ---")
        print(f"{'ID':<5} {'Title':<30} {'Artist':<35} {'Album':<40} {'Duration':<10}")
        print("-" * 125)

        for s in songs:
            print(f"{s[0]:<5} {s[1]:<30} {s[2]:<35} {s[3]:<40} {s[4]:<10}")

        sid = self.get_non_empty("\nSong ID: ")

        playlists = self._services.get_all_playlists()
        print("\n--- Playlists ---")
        print(f"{'ID':<5} {'Name':<35} {'Description':<60}")
        print("-" * 100)
        for p in playlists:
            print(f"{p[0]:<5} {p[1]:<35} {p[2]:<60}")

        pid = self.get_non_empty("\nPlaylist ID: ")
        #sid = self.get_non_empty("Song ID: ")
        self._services.add_song_to_playlist(int(pid), int(sid))
        print("Song added to playlist")

    def delete_song(self):
        print("\n––– Delete Song –––")
        songs = self._services.get_all_songs()

        if not songs:
            print("No songs available.")
            return

        for song in songs:
            print(f"{song[0]} | {song[1]} by {song[2]}")

        valid_ids = [s[0] for s in songs]   # extract all song IDs

         # validation loop
        while True:
            try:
                song_id = int(input("\nEnter the song ID to delete: "))
                if song_id in valid_ids:
                    break
                else:
                    print("\nInvalid song ID. Please choose one from the list.")
            except ValueError:
                print("\nPlease enter a valid number.")

        try:
            self._services.delete_song_by_id(song_id)
            print("Song deleted successfully!\n")
        except Exception as e:
            print(f"Error deleting song: {e}")



    def delete_playlist(self):
        print("\n––– Delete Playlist –––")
        playlists = self._services.get_all_playlists()

        if not playlists:
            print("No playlists available.")
            return

        for playlist in playlists:
            print(f"{playlist[0]} | {playlist[1]} - {playlist[2]}")

        valid_ids = [p[0] for p in playlists]

       # validation loop
        while True:
            user_input = input("\nEnter the playlist ID to delete: ").strip()
            try:
                playlist_id = int(user_input)

                if playlist_id in valid_ids:
                    break
                else:
                    print("Invalid playlist ID. Choose one from the list.")
            except ValueError:
                print("Please enter a valid number.")

        try:
            self._services.delete_playlist_by_id(playlist_id)
            print("Playlist deleted successfully!")
        except Exception as e:
            print(f"Error deleting playlist: {e}")




