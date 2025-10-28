USE `music_db`;

/*Drop playlist_song_xref table if exists
NEED to Drop first since it refernces other tables*/
DROP TABLE IF EXISTS `playlist_song_xref`;


/*Drop songs table if exists*/
DROP TABLE IF EXISTS `songs`;
/*Drop playlists table if exists*/
DROP TABLE IF EXISTS `playlists`;

/*Drop songs table if exists*/
/*DROP TABLE IF EXISTS `songs`;*/

/* Create songs table*/
CREATE TABLE songs (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(100) NOT NULL,
  artist VARCHAR(100) NOT NULL,
  album VARCHAR(100),
  duration VARCHAR(10)
);

/*Drop playlists table if exists*/
/*DROP TABLE IF EXISTS `playlists`;*/


/* Create playlists table*/
CREATE TABLE playlists (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(255)
);


/*Drop playlist_song_xref table if exists*/
/*DROP TABLE IF EXISTS `playlist_song_xref`;*/


/* Create playlist_song_xref table*/
CREATE TABLE playlist_song_xref (
  playlist_id INT NOT NULL,
  song_id INT NOT NULL,
  PRIMARY KEY (playlist_id, song_id),
  FOREIGN KEY (playlist_id) REFERENCES playlists(id)
      ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (song_id) REFERENCES songs(id)
      ON DELETE CASCADE ON UPDATE CASCADE
);
