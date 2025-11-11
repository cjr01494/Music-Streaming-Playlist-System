/* *************************************************************
   Drop and Create the tables for the music_db database.
   ************************************************************* */

-- Switch to the music_db database
USE `music_db`;


/* =============================================================
   Drop existing tables in reverse dependency order
   ============================================================= */

-- Drop cross-reference table first (depends on playlists & songs)
DROP TABLE IF EXISTS `playlist_song_xref`;

-- Drop base tables
DROP TABLE IF EXISTS `songs`;
DROP TABLE IF EXISTS `playlists`;


/* =============================================================
   Create the songs table
   ============================================================= */

CREATE TABLE IF NOT EXISTS `songs` (
  `id` INT(11) NOT NULL,
  `title` VARCHAR(100) NOT NULL,
  `artist` VARCHAR(100) NOT NULL,
  `album` VARCHAR(100),
  `duration` VARCHAR(10)
);

-- Designate the `id` column as the primary key
ALTER TABLE `songs`
  ADD PRIMARY KEY (`id`);

-- Make `id` column auto-increment on inserts
ALTER TABLE `songs`
  MODIFY `id` INT(11) NOT NULL AUTO_INCREMENT;


/* =============================================================
   Create the playlists table
   ============================================================= */

CREATE TABLE IF NOT EXISTS `playlists` (
  `id` INT(11) NOT NULL,
  `name` VARCHAR(100) NOT NULL UNIQUE,
  `description` VARCHAR(255)
);

-- Designate the `id` column as the primary key
ALTER TABLE `playlists`
  ADD PRIMARY KEY (`id`);

-- Make `id` column auto-increment on inserts
ALTER TABLE `playlists`
  MODIFY `id` INT(11) NOT NULL AUTO_INCREMENT;


/* =============================================================
   Create the playlist_song_xref table (junction table)
   ============================================================= */

CREATE TABLE IF NOT EXISTS `playlist_song_xref` (
  `playlist_id` INT(11) NOT NULL,
  `song_id` INT(11) NOT NULL,
  PRIMARY KEY (`playlist_id`, `song_id`),
  FOREIGN KEY (`playlist_id`) REFERENCES `playlists`(`id`)
      ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (`song_id`) REFERENCES `songs`(`id`)
      ON DELETE CASCADE ON UPDATE CASCADE
);
