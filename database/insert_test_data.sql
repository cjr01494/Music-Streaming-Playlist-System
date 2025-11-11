USE `music_db`;


/* Songs data */
INSERT INTO `songs` (title, artist, album, duration)
VALUES 
  ('Peru', 'Ed Sheeran', 'Peru (Single)', '3:07'),
  ('Free Mind', 'Tems', 'If Orange Was A Place', '3:25'),
  ('25', 'Rod Wave', 'SoulFly', '3:30'),
  ('Snooze', 'SZA', 'SOS', '3:21'),
  ('Good Days', 'SZA', 'Good Days (Single)', '4:39'),
  ('On My Mind', 'Jorja Smith', 'Be Right Back', '3:02'),
  ('Damage', 'H.E.R.', 'Back of My Mind', '3:47'),
  ('Hours & Hours', 'Muni Long', 'Public Displays of Affection', '3:24'),
  ('U 2 Luv', 'Ne-Yo ft. Jeremih', 'U 2 Luv (Single)', '3:28'),
  ('Find Someone Like You', 'Snoh Aalegra', 'Ugh, Those Feels Again', '3:02'),
  ('Let Me Go', 'Daniel Caesar', 'NEVER ENOUGH', '3:47'),
  ('Come Through', 'H.E.R. ft. Chris Brown', 'Back of My Mind', '3:35'),
  ('Location', 'Khalid', 'American Teen', '3:40'),
  ('Talk', 'Khalid', 'Free Spirit', '3:18'),
  ('Best Part', 'Daniel Caesar ft. H.E.R.', 'Freudian', '3:29'),
  ('Heartbreak Anniversary', 'Giveon', 'When It’s All Said and Done', '3:18'),
  ('Over', 'Lucky Daye', 'Candydrip', '3:29'),
  ('Pick Up Your Feelings', 'Jazmine Sullivan', 'Heaux Tales', '3:52');

/* Playlist Data */
INSERT INTO `playlists` (name, description)
VALUES
  ('Calm', 'Studying and relaxing'),
  ('Cleaning Music', 'Pump up to get moving');

/* CROSS-REFERENCE TABLE (link songs ↔ playlists) */
-- Calm Music Playlist
INSERT INTO `playlist_song_xref` (playlist_id, song_id)
VALUES
  (1, 1),  -- Peru
  (1, 2),  -- Free Mind
  (1, 15); -- Best Part
  

-- Cleaning Music playlist 
INSERT INTO `playlist_song_xref` (playlist_id, song_id)
VALUES
  (2, 3),   -- 25
  (2, 6),   -- On My Mind
  (2, 9),   -- U 2 Luv
  (2, 13),  -- Talk
  (2, 17);  -- Over
