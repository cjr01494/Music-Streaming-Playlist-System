"""Defines the MySQLPersistenceWrapper class."""

from Music_Streaming_Playlist_System.application_base import ApplicationBase
from mysql import connector
from mysql.connector.pooling import MySQLConnectionPool
import inspect
import json


class MySQLPersistenceWrapper(ApplicationBase):
    """Implements the MySQLPersistenceWrapper class."""

    def __init__(self, config: dict) -> None:
        """Initializes object."""
        self._config_dict = config
        self.META = config["meta"]
        self.DATABASE = config["database"]

        super().__init__(
            subclass_name=self.__class__.__name__,
            logfile_prefix_name=self.META["log_prefix"]
        )
        self._logger.log_debug(f'{inspect.currentframe().f_code.co_name}:It works!')

        # Database Configuration Constants
        self.DB_CONFIG = {
            "database": self.DATABASE["connection"]["config"]["database"],
            "user": self.DATABASE["connection"]["config"]["user"],
            "host": self.DATABASE["connection"]["config"]["host"],
            "port": int(self.DATABASE["connection"]["config"]["port"]),
            "password": self.DATABASE["connection"]["config"].get("password", "")
        }

        self._logger.log_debug(
            f'{inspect.currentframe().f_code.co_name}: DB Connection Config Dict: {self.DB_CONFIG}'
        )

        # Database Connection Pool
        self._connection_pool = self._initialize_database_connection_pool(self.DB_CONFIG)

        # SQL String Constants
        self.SELECT_ALL_SONGS = (
            "SELECT id, title, artist, album, duration FROM songs ORDER BY title"
        )

        self.SELECT_ALL_PLAYLISTS = (
            "SELECT id, name, description FROM playlists ORDER BY name"
        )

        self.SELECT_SONGS_BY_PLAYLIST_ID = """
        SELECT s.id, s.title, s.artist, s.album, s.duration
        FROM songs s
        JOIN playlist_song_xref x ON s.id = x.song_id
        WHERE x.playlist_id = %s
        ORDER BY s.id
        """

        self.INSERT_SONG = (
            "INSERT INTO songs (title, artist, album, duration) VALUES (%s,%s,%s,%s)"
        )

        self.INSERT_PLAYLIST = (
            "INSERT INTO playlists (name, description) VALUES (%s,%s)"
        )

        self.LINK_SONG = (
            "INSERT INTO playlist_song_xref (playlist_id, song_id) VALUES (%s,%s)"
        )

    # -------------------------------------------------------
    # Helper to get connection (pooled)
    # -------------------------------------------------------
    def get_connection(self):
        return self._connection_pool.get_connection()

    # -------------------------------------------------------
    # Select Methods
    # -------------------------------------------------------
    def select_all_songs(self) -> list:
        """Returns a list of all songs in the database."""
        cursor = None
        results = None
        connection = None
        try:
            connection = self.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(self.SELECT_ALL_SONGS)
                    results = cursor.fetchall()
            return results
        except Exception as e:
            self._logger.log_error(f'select_all_songs: {e}')
            return []

    def select_all_playlists(self) -> list:
        """Returns a list of all playlists."""
        cursor = None
        results = None
        connection = None
        try:
            connection = self.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(self.SELECT_ALL_PLAYLISTS)
                    results = cursor.fetchall()
            return results
        except Exception as e:
            self._logger.log_error(f'select_all_playlists: {e}')
            return []

    def select_songs_by_playlist_id(self, playlist_id: int) -> list:
        """Returns all songs for a given playlist id."""
        cursor = None
        results = None
        connection = None
        try:
            connection = self.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(self.SELECT_SONGS_BY_PLAYLIST_ID, (playlist_id,))
                    results = cursor.fetchall()
            return results
        except Exception as e:
            self._logger.log_error(f'select_songs_by_playlist_id: {e}')
            return []

    # -------------------------------------------------------
    # Insert Methods
    # -------------------------------------------------------
    def add_song(self, title, artist, album=None, duration=None) -> int:
        """Inserts a new song and returns its id."""
        cursor = None
        connection = None
        try:
            connection = self.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(self.INSERT_SONG, (title, artist, album, duration))
                    connection.commit()
                    return cursor.lastrowid
        except Exception as e:
            self._logger.log_error(f'add_song: {e}')
            return -1

    def create_playlist(self, name, description=None) -> int:
        """Creates a new playlist and returns its id."""
        cursor = None
        connection = None
        try:
            connection = self.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(self.INSERT_PLAYLIST, (name, description))
                    connection.commit()
                    return cursor.lastrowid
        except Exception as e:
            self._logger.log_error(f'create_playlist: {e}')
            return -1

    def add_song_to_playlist(self, playlist_id: int, song_id: int) -> None:
        """Links a song to a playlist."""
        cursor = None
        connection = None
        try:
            connection = self.get_connection()
            with connection:
                cursor = connection.cursor()
                with cursor:
                    cursor.execute(self.LINK_SONG, (playlist_id, song_id))
                    connection.commit()
        except Exception as e:
            self._logger.log_error(f'add_song_to_playlist: {e}')

    # -------------------------------------------------------
    # Delete Methods
    # -------------------------------------------------------
    def delete_song_by_id(self, song_id):
        """Deletes a song by its ID."""
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM songs WHERE id = %s", (song_id,))
            connection.commit()
            self._logger.log_debug(f"Deleted song ID {song_id} successfully.")
        except Exception as e:
            self._logger.log_error(f"delete_song_by_id: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def delete_playlist_by_id(self, playlist_id):
        """Deletes a playlist by its ID."""
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()

            # Optional: Delete associated playlist-song links before deleting the playlist
            cursor.execute("DELETE FROM playlist_song_xref WHERE playlist_id = %s", (playlist_id,))
            cursor.execute("DELETE FROM playlists WHERE id = %s", (playlist_id,))
            connection.commit()
            self._logger.log_debug(f"Deleted playlist ID {playlist_id} successfully.")
        except Exception as e:
            self._logger.log_error(f"delete_playlist_by_id: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    # -------------------------------------------------------
    # General Query Executor (for INSERT/UPDATE/DELETE)
    # -------------------------------------------------------
    def execute_non_query(self, query, params=None):
        """Executes INSERT, UPDATE, or DELETE statements."""
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            self._logger.log_debug(f"Query executed successfully: {query}")
        except Exception as e:
            self._logger.log_error(f"execute_non_query: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()



    # -------------------------------------------------------
    # Connection Pool Initialization
    # -------------------------------------------------------
    def _initialize_database_connection_pool(self, config: dict) -> MySQLConnectionPool:
        """Initializes database connection pool."""
        try:
            self._logger.log_debug(f'Creating connection pool...')
            cnx_pool = MySQLConnectionPool(
                pool_name=self.DATABASE["pool"]["name"],
                pool_size=self.DATABASE["pool"]["size"],
                pool_reset_session=self.DATABASE["pool"]["reset_session"],
                **config
            )
            self._logger.log_debug(
                f'{inspect.currentframe().f_code.co_name}: Connection pool successfully created!'
            )
            return cnx_pool
        except connector.Error as err:
            self._logger.log_error(f'Error creating connection pool: {err}')
            raise
        except Exception as e:
            self._logger.log_error(f'Unexpected error creating pool: {e}')
            raise
