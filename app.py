from flask import Flask, request, jsonify, send_from_directory
import sqlite3

app = Flask(__name__)
DB_PATH = 'music_player.db'

# ─────────────────────────────
# DATABASE
# ─────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    import os
    conn = get_db()
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS artists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        bio TEXT,
        genre TEXT
    );
    
    CREATE TABLE IF NOT EXISTS playlists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS playlist_songs (
    playlist_id INTEGER,
    song_id INTEGER,
    PRIMARY KEY (playlist_id, song_id),
    FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
);

    CREATE TABLE IF NOT EXISTS albums (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist_id INTEGER,
        release_year INTEGER,
        genre TEXT,
        FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist_id INTEGER,
    album_id INTEGER,
    duration INTEGER,
    genre TEXT,
    year INTEGER,
    file_path TEXT,
    play_count INTEGER DEFAULT 0,
    FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE,
    FOREIGN KEY (album_id) REFERENCES albums(id) ON DELETE CASCADE
);
    """)
    c.execute("""
CREATE TABLE IF NOT EXISTS favorites (
    song_id INTEGER PRIMARY KEY,
    FOREIGN KEY (song_id) REFERENCES songs(id)
)
""")

    c.execute("DELETE FROM playlist_songs")
    c.execute("DELETE FROM favorites")
    c.execute("DELETE FROM songs")
    c.execute("DELETE FROM albums")
    c.execute("DELETE FROM artists")
    c.execute("DELETE FROM playlists")

    # ───────── ARTISTS ─────────
    c.execute("INSERT INTO artists (name,bio,genre) VALUES (?,?,?)",
              ('Atif Aslam','Singer','Pop'))
    atif_id = c.lastrowid

    c.execute("INSERT INTO artists (name,bio,genre) VALUES (?,?,?)",
              ('Shubh','Punjabi singer','Punjabi'))
    shubh_id = c.lastrowid

    c.execute("INSERT INTO artists (name,bio,genre) VALUES (?,?,?)",
              ('Bayaan','Band','Rock'))
    bayaan_id = c.lastrowid

    c.execute("INSERT INTO artists (name,bio,genre) VALUES (?,?,?)",
              ('Abdul Hannan','Singer','Pop'))
    hannan_id = c.lastrowid

    c.execute("INSERT INTO artists (name,bio,genre) VALUES (?,?,?)",
              ('Hasan Raheem','Singer','Pop/R&B'))
    hasan_id = c.lastrowid

    # ───────── ALBUMS ─────────
    c.execute("INSERT INTO albums (title,artist_id,release_year,genre) VALUES (?,?,?,?)",
              ('Woh Lamhe', atif_id, 2007, 'Pop'))
    atif_album = c.lastrowid

    c.execute("INSERT INTO albums (title,artist_id,release_year,genre) VALUES (?,?,?,?)",
              ('Shubh Album', shubh_id, 2023, 'Punjabi'))
    shubh_album = c.lastrowid

    c.execute("INSERT INTO albums (title,artist_id,release_year,genre) VALUES (?,?,?,?)",
              ('Suno', bayaan_id, 2018, 'Rock'))
    bayaan_album = c.lastrowid

    c.execute("INSERT INTO albums (title,artist_id,release_year,genre) VALUES (?,?,?,?)",
              ('Hannan Hits', hannan_id, 2022, 'Pop'))
    hannan_album = c.lastrowid

    c.execute("INSERT INTO albums (title,artist_id,release_year,genre) VALUES (?,?,?,?)",
              ('Hasan Collection', hasan_id, 2022, 'Pop/R&B'))
    hasan_album = c.lastrowid

    # ───────── SONGS ─────────
    songs = [
    ('Aadat', atif_id, atif_album, 245, 'Pop', 2006, '/static/music/Adaat.mpeg'),
    ('Dekhte Dekhte', atif_id, atif_album, 267, 'Pop', 2007, '/static/music/Dekhte Dekhte.mpeg'),

    ('Be Mine', shubh_id, shubh_album, 312, 'Punjabi', 2023, '/static/music/Be Mine.mpeg'),
    ('Together', shubh_id, shubh_album, 300, 'Punjabi', 2023, '/static/music/Together.mpeg'),

    ('din dhalay', bayaan_id, bayaan_album, 285, 'Rock', 2018, '/static/music/Din dhalay.mpeg'),
    ('Teri Tasveer', bayaan_id, bayaan_album, 301, 'Rock', 2018, '/static/music/Teri tasveer.mpeg'),

    ('Iraaday', hannan_id, hannan_album, 245, 'Pop', 2022, '/static/music/Iraday.mpeg'),
    ('Khasara', hannan_id, hannan_album, 248, 'Pop', 2023, '/static/music/khasara.mpeg'),

    ('Obvious', hasan_id, hasan_album, 235, 'Pop/R&B', 2022, '/static/music/Obvious.mpeg'),
    ('Bewajah', hasan_id, hasan_album, 215, 'Pop/R&B', 2021, '/static/music/Bewajah.mpeg'),
    ('Wishes', hasan_id, hasan_album, 220, 'Pop/R&B', 2022, '/static/music/Wishes.mpeg'),
]

    c.executemany("""
    INSERT INTO songs
    (title,artist_id,album_id,duration,genre,year,file_path)
    VALUES (?,?,?,?,?,?,?)
""", songs)
    conn.commit()
    conn.close()

# ─────────────────────────────
# HELPERS
# ─────────────────────────────

def row_to_dict(row):
    return dict(row)

def rows_to_list(rows):
    return [dict(r) for r in rows]

# ─────────────────────────────
# ROUTES
# ─────────────────────────────

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/api/songs', methods=['GET'])
def songs():
    try:
        conn = get_db()
        data = conn.execute("""
            SELECT songs.*, artists.name as artist_name
            FROM songs
            JOIN artists ON songs.artist_id = artists.id
        """).fetchall()
        conn.close()

        return jsonify(rows_to_list(data))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/artists')
def artists():
    conn = get_db()
    data = conn.execute("SELECT * FROM artists").fetchall()
    conn.close()
    return jsonify(rows_to_list(data))

@app.route('/api/artists', methods=['POST'])
def add_artist():

    data = request.json

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO artists(name,bio,genre)
        VALUES(?,?,?)
    """, (
        data['name'],
        data.get('bio'),
        data.get('genre')
    ))

    conn.commit()

    artist_id = cur.lastrowid

    artist = conn.execute(
        "SELECT * FROM artists WHERE id=?",
        (artist_id,)
    ).fetchone()

    conn.close()

    return jsonify(dict(artist))

@app.route('/api/playlists')
def get_playlists():
    try:
        conn = get_db()
        data = conn.execute("SELECT * FROM playlists").fetchall()
        conn.close()
        return jsonify(rows_to_list(data))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/playlists/<int:pl_id>/songs')
def get_playlist_songs(pl_id):
    conn = get_db()
    data = conn.execute("""
        SELECT songs.*, artists.name as artist_name
        FROM songs
        JOIN playlist_songs ON songs.id = playlist_songs.song_id
        JOIN artists ON songs.artist_id = artists.id
        WHERE playlist_songs.playlist_id = ?
    """, (pl_id,)).fetchall()

    conn.close()
    return jsonify(rows_to_list(data))

@app.route('/api/albums')
def albums():
    conn = get_db()
    data = conn.execute("SELECT * FROM albums").fetchall()
    conn.close()
    return jsonify(rows_to_list(data))

@app.route('/api/albums', methods=['POST'])
def add_album():

    data = request.json

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO albums
        (title,artist_id,release_year,genre)
        VALUES(?,?,?,?)
    """, (
        data['title'],
        data['artist_id'],
        data['release_year'],
        data['genre']
    ))

    conn.commit()

    album_id = cur.lastrowid

    album = conn.execute(
        "SELECT * FROM albums WHERE id=?",
        (album_id,)
    ).fetchone()

    conn.close()

    return jsonify(dict(album))

@app.route('/api/favorites')
def get_favorites():
    conn = get_db()
    data = conn.execute("""
        SELECT songs.*, artists.name as artist_name
        FROM songs
        JOIN artists ON songs.artist_id = artists.id
        JOIN favorites ON songs.id = favorites.song_id
    """).fetchall()
    conn.close()
    return jsonify(rows_to_list(data))

#@app.route('/favorites/<int:song_id>', methods=['POST'])
@app.route('/api/favorites/<int:song_id>', methods=['POST'])
def toggle_favorite(song_id):
#def toggle_favorite(song_id):
    conn = get_db()

    existing = conn.execute(
        "SELECT * FROM favorites WHERE song_id=?",
        (song_id,)
    ).fetchone()

    if existing:
        conn.execute("DELETE FROM favorites WHERE song_id=?", (song_id,))
        conn.commit()
        conn.close()
        return jsonify({"is_favorite": False})

    else:
        conn.execute("INSERT INTO favorites (song_id) VALUES (?)", (song_id,))
        conn.commit()
        conn.close()
        return jsonify({"is_favorite": True})
    
@app.route('/api/playlists', methods=['POST'])
def create_playlist():
    data = request.json

    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({"error": "name required"}), 400

    # 👉 Example DB insert (adjust to your DB)
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO playlists (name, description)
        VALUES (?, ?)
    """, (name, description))

    conn.commit()

    new_id = cur.lastrowid

    return jsonify({
        "id": new_id,
        "name": name,
        "description": description
    })
    
@app.route('/api/playlists/<int:pl_id>/songs', methods=['POST'])
def add_song_to_playlist(pl_id):
    data = request.json
    song_id = data.get('song_id')
    print("playlist:", pl_id, "song:", song_id)
    if not song_id:
        return jsonify({"success": False, "msg": "song_id missing"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO playlist_songs (playlist_id, song_id)
        VALUES (?, ?)
    """, (pl_id, song_id))

    conn.commit()

    return jsonify({"success": True})

@app.route('/api/songs/<int:id>', methods=['DELETE'])
def delete_song(id):
    conn = get_db()

    conn.execute("DELETE FROM playlist_songs WHERE song_id=?", (id,))
    conn.execute("DELETE FROM favorites WHERE song_id=?", (id,))
    conn.execute("DELETE FROM songs WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route('/api/artists/<int:id>', methods=['DELETE'])
def delete_artist(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM artists WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route('/api/albums/<int:id>', methods=['DELETE'])
def delete_album(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM albums WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route('/api/artists/<int:id>/songs')
def artist_songs(id):
    conn = get_db()
    data = conn.execute("""
        SELECT songs.*, artists.name as artist_name
        FROM songs
        JOIN artists ON songs.artist_id = artists.id
        WHERE artists.id = ?
    """, (id,)).fetchall()
    conn.close()
    return jsonify(rows_to_list(data))

@app.route('/api/albums/<int:id>/songs')
def album_songs(id):
    conn = get_db()
    data = conn.execute("""
        SELECT songs.*, artists.name as artist_name
        FROM songs
        JOIN artists ON songs.artist_id = artists.id
        WHERE songs.album_id = ?
    """, (id,)).fetchall()
    conn.close()
    return jsonify(rows_to_list(data))

@app.route('/api/songs', methods=['POST'])
def add_song():
    data = request.json

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO songs
        (title, artist_id, album_id, duration, genre, year, file_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data['title'],
        data['artist_id'],
        data['album_id'],
        data.get('duration'),
        data.get('genre'),
        data.get('year'),
        data.get('file_path')
    ))

    conn.commit()

    song_id = cur.lastrowid
    song = conn.execute("SELECT * FROM songs WHERE id=?", (song_id,)).fetchone()

    conn.close()
    return jsonify(dict(song))

@app.route('/api/songs/<int:id>/play', methods=['POST'])
def play_song(id):
    try:
        conn = get_db()

        song = conn.execute("SELECT * FROM songs WHERE id=?", (id,)).fetchone()
        if not song:
            return jsonify({"error": "Song not found"}), 404

        conn.execute("""
            UPDATE songs 
            SET play_count = COALESCE(play_count,0) + 1 
            WHERE id=?
        """, (id,))

        conn.commit()
        conn.close()

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats')
def stats():
    conn = get_db()

    total_songs = conn.execute("SELECT COUNT(*) FROM songs").fetchone()[0]
    total_artists = conn.execute("SELECT COUNT(*) FROM artists").fetchone()[0]
    total_albums = conn.execute("SELECT COUNT(*) FROM albums").fetchone()[0]

    total_playlists = conn.execute("SELECT COUNT(*) FROM playlists").fetchone()[0]

    total_favorites = conn.execute("SELECT COUNT(*) FROM favorites").fetchone()[0]

    top_songs = conn.execute("""
        SELECT songs.*, artists.name as artist_name
        FROM songs
        JOIN artists ON songs.artist_id = artists.id
        ORDER BY songs.id DESC
        LIMIT 5
    """).fetchall()

    conn.close()

    return jsonify({
        "total_songs": total_songs,
        "total_artists": total_artists,
        "total_albums": total_albums,
        "total_playlists": total_playlists,
        "total_favorites": total_favorites,
        "top_songs": rows_to_list(top_songs)
    })

# ─────────────────────────────
# MAIN
# ─────────────────────────────

if __name__ == '__main__':
    with app.app_context():
        init_db() 
        from flask import Flask, request, jsonify, send_from_directory
import sqlite3

app = Flask(__name__)
DB_PATH = 'music_player.db'

# ─────────────────────────────
# DATABASE
# ─────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    import os
    conn = get_db()
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE IF NOT EXISTS artists (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        bio TEXT,
        genre TEXT
    );
    
    CREATE TABLE IF NOT EXISTS playlists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE IF NOT EXISTS playlist_songs (
    playlist_id INTEGER,
    song_id INTEGER,
    PRIMARY KEY (playlist_id, song_id),
    FOREIGN KEY (playlist_id) REFERENCES playlists(id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
);

    CREATE TABLE IF NOT EXISTS albums (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        artist_id INTEGER,
        release_year INTEGER,
        genre TEXT,
        FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS songs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    artist_id INTEGER,
    album_id INTEGER,
    duration INTEGER,
    genre TEXT,
    year INTEGER,
    file_path TEXT,
    play_count INTEGER DEFAULT 0,
    FOREIGN KEY (artist_id) REFERENCES artists(id) ON DELETE CASCADE,
    FOREIGN KEY (album_id) REFERENCES albums(id) ON DELETE CASCADE
);
    """)
    c.execute("""
CREATE TABLE IF NOT EXISTS favorites (
    song_id INTEGER PRIMARY KEY,
    FOREIGN KEY (song_id) REFERENCES songs(id)
)
""")

    c.execute("DELETE FROM playlist_songs")
    c.execute("DELETE FROM favorites")
    c.execute("DELETE FROM songs")
    c.execute("DELETE FROM albums")
    c.execute("DELETE FROM artists")
    c.execute("DELETE FROM playlists")

    # ───────── ARTISTS ─────────
    c.execute("INSERT INTO artists (name,bio,genre) VALUES (?,?,?)",
              ('Atif Aslam','Singer','Pop'))
    atif_id = c.lastrowid

    c.execute("INSERT INTO artists (name,bio,genre) VALUES (?,?,?)",
              ('Shubh','Punjabi singer','Punjabi'))
    shubh_id = c.lastrowid

    c.execute("INSERT INTO artists (name,bio,genre) VALUES (?,?,?)",
              ('Bayaan','Band','Rock'))
    bayaan_id = c.lastrowid

    c.execute("INSERT INTO artists (name,bio,genre) VALUES (?,?,?)",
              ('Abdul Hannan','Singer','Pop'))
    hannan_id = c.lastrowid

    c.execute("INSERT INTO artists (name,bio,genre) VALUES (?,?,?)",
              ('Hasan Raheem','Singer','Pop/R&B'))
    hasan_id = c.lastrowid

    # ───────── ALBUMS ─────────
    c.execute("INSERT INTO albums (title,artist_id,release_year,genre) VALUES (?,?,?,?)",
              ('Woh Lamhe', atif_id, 2007, 'Pop'))
    atif_album = c.lastrowid

    c.execute("INSERT INTO albums (title,artist_id,release_year,genre) VALUES (?,?,?,?)",
              ('Shubh Album', shubh_id, 2023, 'Punjabi'))
    shubh_album = c.lastrowid

    c.execute("INSERT INTO albums (title,artist_id,release_year,genre) VALUES (?,?,?,?)",
              ('Suno', bayaan_id, 2018, 'Rock'))
    bayaan_album = c.lastrowid

    c.execute("INSERT INTO albums (title,artist_id,release_year,genre) VALUES (?,?,?,?)",
              ('Hannan Hits', hannan_id, 2022, 'Pop'))
    hannan_album = c.lastrowid

    c.execute("INSERT INTO albums (title,artist_id,release_year,genre) VALUES (?,?,?,?)",
              ('Hasan Collection', hasan_id, 2022, 'Pop/R&B'))
    hasan_album = c.lastrowid

    # ───────── SONGS ─────────
    songs = [
    ('Aadat', atif_id, atif_album, 245, 'Pop', 2006, '/static/music/Adaat.mpeg'),
    ('Dekhte Dekhte', atif_id, atif_album, 267, 'Pop', 2007, '/static/music/Dekhte Dekhte.mpeg'),

    ('Be Mine', shubh_id, shubh_album, 312, 'Punjabi', 2023, '/static/music/Be Mine.mpeg'),
    ('Together', shubh_id, shubh_album, 300, 'Punjabi', 2023, '/static/music/Together.mpeg'),

    ('din dhalay', bayaan_id, bayaan_album, 285, 'Rock', 2018, '/static/music/Din dhalay.mpeg'),
    ('Teri Tasveer', bayaan_id, bayaan_album, 301, 'Rock', 2018, '/static/music/Teri tasveer.mpeg'),

    ('Iraaday', hannan_id, hannan_album, 245, 'Pop', 2022, '/static/music/Iraday.mpeg'),
    ('Khasara', hannan_id, hannan_album, 248, 'Pop', 2023, '/static/music/khasara.mpeg'),

    ('Obvious', hasan_id, hasan_album, 235, 'Pop/R&B', 2022, '/static/music/Obvious.mpeg'),
    ('Bewajah', hasan_id, hasan_album, 215, 'Pop/R&B', 2021, '/static/music/Bewajah.mpeg'),
    ('Wishes', hasan_id, hasan_album, 220, 'Pop/R&B', 2022, '/static/music/Wishes.mpeg'),
]

    c.executemany("""
    INSERT INTO songs
    (title,artist_id,album_id,duration,genre,year,file_path)
    VALUES (?,?,?,?,?,?,?)
""", songs)
    conn.commit()
    conn.close()

# ─────────────────────────────
# HELPERS
# ─────────────────────────────

def row_to_dict(row):
    return dict(row)

def rows_to_list(rows):
    return [dict(r) for r in rows]

# ─────────────────────────────
# ROUTES
# ─────────────────────────────

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/api/songs', methods=['GET'])
def songs():
    try:
        conn = get_db()
        data = conn.execute("""
            SELECT songs.*, artists.name as artist_name
            FROM songs
            JOIN artists ON songs.artist_id = artists.id
        """).fetchall()
        conn.close()

        return jsonify(rows_to_list(data))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/artists')
def artists():
    conn = get_db()
    data = conn.execute("SELECT * FROM artists").fetchall()
    conn.close()
    return jsonify(rows_to_list(data))

@app.route('/api/artists', methods=['POST'])
def add_artist():

    data = request.json

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO artists(name,bio,genre)
        VALUES(?,?,?)
    """, (
        data['name'],
        data.get('bio'),
        data.get('genre')
    ))

    conn.commit()

    artist_id = cur.lastrowid

    artist = conn.execute(
        "SELECT * FROM artists WHERE id=?",
        (artist_id,)
    ).fetchone()

    conn.close()

    return jsonify(dict(artist))

@app.route('/api/playlists')
def get_playlists():
    try:
        conn = get_db()
        data = conn.execute("SELECT * FROM playlists").fetchall()
        conn.close()
        return jsonify(rows_to_list(data))

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/playlists/<int:pl_id>/songs')
def get_playlist_songs(pl_id):
    conn = get_db()
    data = conn.execute("""
        SELECT songs.*, artists.name as artist_name
        FROM songs
        JOIN playlist_songs ON songs.id = playlist_songs.song_id
        JOIN artists ON songs.artist_id = artists.id
        WHERE playlist_songs.playlist_id = ?
    """, (pl_id,)).fetchall()

    conn.close()
    return jsonify(rows_to_list(data))

@app.route('/api/albums')
def albums():
    conn = get_db()
    data = conn.execute("SELECT * FROM albums").fetchall()
    conn.close()
    return jsonify(rows_to_list(data))

@app.route('/api/albums', methods=['POST'])
def add_album():

    data = request.json

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO albums
        (title,artist_id,release_year,genre)
        VALUES(?,?,?,?)
    """, (
        data['title'],
        data['artist_id'],
        data['release_year'],
        data['genre']
    ))

    conn.commit()

    album_id = cur.lastrowid

    album = conn.execute(
        "SELECT * FROM albums WHERE id=?",
        (album_id,)
    ).fetchone()

    conn.close()

    return jsonify(dict(album))

@app.route('/api/favorites')
def get_favorites():
    conn = get_db()
    data = conn.execute("""
        SELECT songs.*, artists.name as artist_name
        FROM songs
        JOIN artists ON songs.artist_id = artists.id
        JOIN favorites ON songs.id = favorites.song_id
    """).fetchall()
    conn.close()
    return jsonify(rows_to_list(data))

#@app.route('/favorites/<int:song_id>', methods=['POST'])
@app.route('/api/favorites/<int:song_id>', methods=['POST'])
def toggle_favorite(song_id):
#def toggle_favorite(song_id):
    conn = get_db()

    existing = conn.execute(
        "SELECT * FROM favorites WHERE song_id=?",
        (song_id,)
    ).fetchone()

    if existing:
        conn.execute("DELETE FROM favorites WHERE song_id=?", (song_id,))
        conn.commit()
        conn.close()
        return jsonify({"is_favorite": False})

    else:
        conn.execute("INSERT INTO favorites (song_id) VALUES (?)", (song_id,))
        conn.commit()
        conn.close()
        return jsonify({"is_favorite": True})
    
@app.route('/api/playlists', methods=['POST'])
def create_playlist():
    data = request.json

    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({"error": "name required"}), 400

    # 👉 Example DB insert (adjust to your DB)
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO playlists (name, description)
        VALUES (?, ?)
    """, (name, description))

    conn.commit()

    new_id = cur.lastrowid

    return jsonify({
        "id": new_id,
        "name": name,
        "description": description
    })
    
@app.route('/api/playlists/<int:pl_id>/songs', methods=['POST'])
def add_song_to_playlist(pl_id):
    data = request.json
    song_id = data.get('song_id')
    print("playlist:", pl_id, "song:", song_id)
    if not song_id:
        return jsonify({"success": False, "msg": "song_id missing"}), 400

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO playlist_songs (playlist_id, song_id)
        VALUES (?, ?)
    """, (pl_id, song_id))

    conn.commit()

    return jsonify({"success": True})

@app.route('/api/songs/<int:id>', methods=['DELETE'])
def delete_song(id):
    conn = get_db()

    conn.execute("DELETE FROM playlist_songs WHERE song_id=?", (id,))
    conn.execute("DELETE FROM favorites WHERE song_id=?", (id,))
    conn.execute("DELETE FROM songs WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route('/api/artists/<int:id>', methods=['DELETE'])
def delete_artist(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM artists WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route('/api/albums/<int:id>', methods=['DELETE'])
def delete_album(id):

    conn = get_db()

    conn.execute(
        "DELETE FROM albums WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({"success": True})

@app.route('/api/artists/<int:id>/songs')
def artist_songs(id):
    conn = get_db()
    data = conn.execute("""
        SELECT songs.*, artists.name as artist_name
        FROM songs
        JOIN artists ON songs.artist_id = artists.id
        WHERE artists.id = ?
    """, (id,)).fetchall()
    conn.close()
    return jsonify(rows_to_list(data))

@app.route('/api/albums/<int:id>/songs')
def album_songs(id):
    conn = get_db()
    data = conn.execute("""
        SELECT songs.*, artists.name as artist_name
        FROM songs
        JOIN artists ON songs.artist_id = artists.id
        WHERE songs.album_id = ?
    """, (id,)).fetchall()
    conn.close()
    return jsonify(rows_to_list(data))

@app.route('/api/songs', methods=['POST'])
def add_song():
    data = request.json

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO songs
        (title, artist_id, album_id, duration, genre, year, file_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data['title'],
        data['artist_id'],
        data['album_id'],
        data.get('duration'),
        data.get('genre'),
        data.get('year'),
        data.get('file_path')
    ))

    conn.commit()

    song_id = cur.lastrowid
    song = conn.execute("SELECT * FROM songs WHERE id=?", (song_id,)).fetchone()

    conn.close()
    return jsonify(dict(song))

@app.route('/api/songs/<int:id>/play', methods=['POST'])
def play_song(id):
    try:
        conn = get_db()

        song = conn.execute("SELECT * FROM songs WHERE id=?", (id,)).fetchone()
        if not song:
            return jsonify({"error": "Song not found"}), 404

        conn.execute("""
            UPDATE songs 
            SET play_count = COALESCE(play_count,0) + 1 
            WHERE id=?
        """, (id,))

        conn.commit()
        conn.close()

        return jsonify({"success": True})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stats')
def stats():
    conn = get_db()

    total_songs = conn.execute("SELECT COUNT(*) FROM songs").fetchone()[0]
    total_artists = conn.execute("SELECT COUNT(*) FROM artists").fetchone()[0]
    total_albums = conn.execute("SELECT COUNT(*) FROM albums").fetchone()[0]

    total_playlists = conn.execute("SELECT COUNT(*) FROM playlists").fetchone()[0]

    total_favorites = conn.execute("SELECT COUNT(*) FROM favorites").fetchone()[0]

    top_songs = conn.execute("""
        SELECT songs.*, artists.name as artist_name
        FROM songs
        JOIN artists ON songs.artist_id = artists.id
        ORDER BY songs.id DESC
        LIMIT 5
    """).fetchall()

    conn.close()

    return jsonify({
        "total_songs": total_songs,
        "total_artists": total_artists,
        "total_albums": total_albums,
        "total_playlists": total_playlists,
        "total_favorites": total_favorites,
        "top_songs": rows_to_list(top_songs)
    })

# ─────────────────────────────
# MAIN
# ─────────────────────────────

if __name__ == '__main__':
    with app.app_context():
        init_db()

    app.run(debug=True, port=5000)