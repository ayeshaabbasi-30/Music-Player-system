-- ============================================
-- MUSIC PLAYER DATABASE SCHEMA
-- ============================================

CREATE DATABASE IF NOT EXISTS music_player;
USE music_player;

-- Artists Table
CREATE TABLE IF NOT EXISTS artists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    bio TEXT,
    image_url VARCHAR(500),
    genre VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Albums Table
CREATE TABLE IF NOT EXISTS albums (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INT NOT NULL,
    cover_url VARCHAR(500),
    release_year INT,
    genre VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE
);

-- Songs Table
CREATE TABLE IF NOT EXISTS songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INT NOT NULL,
    album_id INT,
    file_path VARCHAR(500),
    duration INT DEFAULT 0,
    genre VARCHAR(100),
    year INT,
    play_count INT DEFAULT 0,
    cover_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE,
    FOREIGN KEY (album_id) REFERENCES albums(id) ON DELETE SET NULL
);

-- Playlists Table
CREATE TABLE IF NOT EXISTS playlists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    cover_url VARCHAR(500),
    is_favorite BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Playlist Songs (Junction Table)
CREATE TABLE IF NOT EXISTS playlist_songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    playlist_id INT NOT NULL,
    song_id INT NOT NULL,
    position INT DEFAULT 0,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE,
    UNIQUE KEY unique_playlist_song (playlist_id, song_id)
);

-- Favorites Table
CREATE TABLE IF NOT EXISTS favorites (
    id INT AUTO_INCREMENT PRIMARY KEY,
    song_id INT NOT NULL UNIQUE,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
);

-- Sample Data
INSERT INTO artists (name,bio,genre) VALUES
('Atif Aslam','Singer','Pop'),
('Shubh','Punjabi singer','Punjabi'),
('Bayaan','Band','Rock'),
('Abdul Hannan','Singer','Pop'),
('Hasan Raheem','Singer','Pop/R&B');

INSERT INTO albums (title,artist_id,release_year,genre) VALUES
('Woh Lamhe',1,2007,'Pop'),
('Shubh Album',2,2023,'Punjabi'),
('Suno',3,2018,'Rock'),
('Hannan Hits',4,2022,'Pop'),
('Hasan Collection',5,2022,'Pop/R&B');

INSERT INTO songs
(title,artist_id,album_id,duration,genre,year,file_path)
VALUES
('Aadat',1,1,245,'Pop',2006,'/static/music/Adaat.mpeg'),
('Dekhte Dekhte',1,1,267,'Pop',2007,'/static/music/Dekhte Dekhte.mpeg'),

('Be Mine',2,2,312,'Punjabi',2023,'/static/music/Be Mine.mpeg'),
('Together',2,2,300,'Punjabi',2023,'/static/music/Together.mpeg'),

('din dhalay',3,3,285,'Rock',2018,'/static/music/Din dhalay.mpeg'),
('Teri Tasveer',3,3,301,'Rock',2018,'/static/music/Teri tasveer.mpeg'),

('Iraaday',4,4,245,'Pop',2022,'/static/music/Iraday.mpeg'),
('Khasara',4,4,248,'Pop',2023,'/static/music/khasara.mpeg'),

('Obvious',5,5,235,'Pop/R&B',2022,'/static/music/Obvious.mpeg'),
('Bewajah',5,5,215,'Pop/R&B',2021,'/static/music/Bewajah.mpeg'),
('Wishes',5,5,220,'Pop/R&B',2022,'/static/music/Wishes.mpeg');

INSERT INTO playlists (name, description) VALUES
('My Favorites', 'My favorite songs'),
('Workout Mix', 'Energetic songs for exercise'),
('Night Solitude', 'Songs for listening at night');

INSERT INTO playlist_songs (playlist_id, song_id, position) VALUES
(1, 1, 1), (1, 2, 2), (1, 5, 3),
(2, 9, 1), (2, 10, 2),
(3, 7, 1), (3, 8, 2), (3, 4, 3);

INSERT INTO favorites (song_id) VALUES (1), (5), (7);
