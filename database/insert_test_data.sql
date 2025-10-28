USE `music_db`;


/* Songs data */
INSERT INTO `songs` (title, artist, album, duration)
VALUES 
  ('Peru', 'Ed Sheeran', 'Peru (Single)', '3:07'),
  ('Free Mind', 'Tems', 'If Orange Was A Place', '3:25'),
  ('25', 'Rod Wave', 'SoulFly', '3:30');

/* Playlist Data */
INSERT INTO `playlists` (name, description)
VALUES
  ('Calm', 'Studying and relaxing'),
  ('Cleaning Music', 'Pump up to get moving');

/* CROSS-REFERENCE TABLE (link songs ↔ playlists) */
-- Calm playlist includes Peru and Free Mind
INSERT INTO `playlist_song_xref` (playlist_id, song_id)
VALUES
  (1, 1),
  (1, 2);

-- Cleaning Music playlist includes all three songs
INSERT INTO `playlist_song_xref` (playlist_id, song_id)
VALUES
  (2, 1),
  (2, 2),
  (2, 3);
