"""Implements AppServices Class."""

from Music_Streaming_Playlist_System.application_base import ApplicationBase
from Music_Streaming_Playlist_System.persistence_layer.mysql_persistence_wrapper import MySQLPersistenceWrapper
import inspect

"""Service layer for Music Streaming Playlist System."""


class AppServices(ApplicationBase):
    def __init__(self, config: dict, db):
        self._config = config
        self._db = db

        self.META = config["meta"]
        super().__init__(
            subclass_name=self.__class__.__name__,
            logfile_prefix_name=self.META["log_prefix"]
        )
        self._logger.log_debug("__init__: It works!")

    # ---- Song Services ----
    def get_all_songs(self):
        return self._db.select_all_songs()

    def add_song(self, title, artist, album=None, duration=None):
        return self._db.add_song(title, artist, album, duration)

    # ---- Playlist Services ----
    def get_all_playlists(self):
        return self._db.select_all_playlists()

    def create_playlist(self, name, description=None):
        return self._db.create_playlist(name, description)

    def add_song_to_playlist(self, playlist_id, song_id):
        return self._db.add_song_to_playlist(playlist_id, song_id)

    def get_songs_by_playlist(self, playlist_id: int):
        return self._db.select_songs_by_playlist_id(playlist_id)
