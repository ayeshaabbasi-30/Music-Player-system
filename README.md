# 🎵 Spotify – Music Player Database Project

## Project Structure

```
music_player/
├── app.py              ← Flask Backend (Python)
├── index.html          ← Frontend (HTML/CSS/JS)
├── schema.sql          ← MySQL  schema
├── requirements.txt    ← Python packages
└── music_player.db     ← SQLite database 
```

---

## Database Tables

| Table            | Working                           |
|------------------|-----------------------------------|
| `artists`        | Singer/band info                    |
| `albums`         | Albums and covers                   |
| `songs`          | Songs, duration, genre              |
| `playlists`      | User playlists                      |
| `playlist_songs` | Song ↔ Playlist junction table      |
| `favorites`      | Favorite songs                      |

---

## Setup

### 1. Check Python
```
python --version   # Python 3.8+ required
```

### 2. Install Flask
```bash
pip install flask
```

### 3. Run the project
```bash
cd music_player
python app.py
```

### 4. Open in browser
```
http://localhost:5000
```

---

## Features

✅ Add, edit, delete songs
✅ Add artists and browse their songs
✅ Create albums and assign songs
✅ Create custom playlists
✅ Add/remove songs from playlists
✅ Favorite songs collection
✅ Search by title, artist, album, or genre
✅ Play/Pause, Next/Prev, Shuffle, Repeat
✅ Volume control
✅ Play count tracking
✅ Statistics dashboard

---

## API Endpoints

### Songs
- `GET  /api/songs`              – All songs
- `POST /api/songs`              – Add new song 
- `PUT  /api/songs/<id>`         – update song
- `DELETE /api/songs/<id>`       – Song delete
- `POST /api/songs/<id>/play`    – Play count +1
- `GET  /api/search?q=...`       – Search

### Artists
- `GET  /api/artists`            – All artists
- `POST /api/artists`            – New artist
- `DELETE /api/artists/<id>`     – Artist delete
- `GET  /api/artists/<id>/songs` – Artist songs

### Albums
- `GET  /api/albums`             – All albums
- `POST /api/albums`             – New album
- `DELETE /api/albums/<id>`      – Album delete
- `GET  /api/albums/<id>/songs`  – Album songs

### Playlists
- `GET  /api/playlists`          – All playlists
- `POST /api/playlists`          – New playlist
- `DELETE /api/playlists/<id>`   – Playlist delete
- `GET  /api/playlists/<id>/songs`    – Playlist songs
- `POST /api/playlists/<id>/songs`    – Song add 
- `DELETE /api/playlists/<id>/songs/<song_id>` – Song remove

### Favorites
- `GET  /api/favorites`          – All favorites
- `POST /api/favorites/<id>`     – Toggle favorite
- `GET  /api/favorites/check/<id>` – Check favorite

### Stats
- `GET  /api/stats`              – Dashboard statistics

---

## MySQL (Optional)

To use MySQL instead of SQLite, run `schema.sql`:
```bash
mysql -u root -p < schema.sql
```
Then update `app.py` to use `mysql-connector-python` instead of SQLite.

---

## Technologies Used

- **Backend**: Python 3 + Flask (SQLite database)
- **Frontend**: Vanilla HTML/CSS/JavaScript (no framework needed)
- **Database**: SQLite (built-in) / MySQL-compatible schema included
- **Design**: Dark theme, Bebas Neue + DM Sans fonts
