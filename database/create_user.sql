/* Drop the user first if it already exists */
DROP USER IF EXISTS 'cjortanez'@'localhost';

/* Create a new user for the Music Streaming Playlist System */
CREATE USER 'cjortanez'@'localhost' IDENTIFIED BY '';

/* Grant privileges to manage the music_db schema */
GRANT ALL PRIVILEGES ON music_db.* TO 'cjortanez'@'localhost' WITH GRANT OPTION;

/* Apply changes immediately */
FLUSH PRIVILEGES;

/* Optional: verify */
SELECT user, host FROM mysql.user WHERE user = 'cjortanez';
