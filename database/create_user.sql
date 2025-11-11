/* ******************************************
   Drop and create the music_db_user account
   ********************************************/

/* Drop user if exists */
DROP USER IF EXISTS 'music_db_user'@'%';

/* Create user if not exists */
CREATE USER IF NOT EXISTS 'music_db_user'@'%' IDENTIFIED BY '';

/* Grant full privileges on all databases and objects */
GRANT ALL PRIVILEGES ON *.* TO 'music_db_user'@'%';

/* Configure user resource limits */
ALTER USER 'music_db_user'@'%'
  REQUIRE NONE
  WITH
  MAX_QUERIES_PER_HOUR 0
  MAX_CONNECTIONS_PER_HOUR 0
  MAX_UPDATES_PER_HOUR 0
  MAX_USER_CONNECTIONS 0;

/* Grant privileges specifically on music_db */
GRANT ALL PRIVILEGES ON `music_db`.* TO 'music_db_user'@'%' WITH GRANT OPTION;

/* Apply changes */
FLUSH PRIVILEGES;

/* Verify the new user */
SELECT user, host FROM mysql.user WHERE user = 'music_db_user';
