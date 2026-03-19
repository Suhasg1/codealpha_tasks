"""
ConnectSphere — Social Media Platform
CodeAlpha Internship | Full Stack Web Development | Task 2

Backend: Python Flask + SQLite

Run:
    pip install flask
    python app.py

Server: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify, session
import sqlite3, hashlib, os, json
from datetime import datetime
from functools import wraps

# Absolute paths -- works on all systems (Windows, Mac, Linux)
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR  = os.path.join(BASE_DIR, '..', 'frontend')
TEMPLATES_DIR = os.path.join(FRONTEND_DIR, 'pages')

app = Flask(
    __name__,
    template_folder=os.path.abspath(TEMPLATES_DIR),
    static_folder=os.path.abspath(FRONTEND_DIR),
    static_url_path='/static'
)
app.secret_key = 'connectsphere_secret_2024'
DB_PATH = os.path.join(BASE_DIR, 'connectsphere.db')


# ──────────────────────────────────────────────────────────────
#  DATABASE
# ──────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    c = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT    UNIQUE NOT NULL,
            name        TEXT    NOT NULL,
            email       TEXT    UNIQUE NOT NULL,
            password    TEXT    NOT NULL,
            bio         TEXT    DEFAULT '',
            avatar      TEXT    DEFAULT '',
            website     TEXT    DEFAULT '',
            location    TEXT    DEFAULT '',
            created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS posts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            content     TEXT    NOT NULL,
            image_url   TEXT    DEFAULT '',
            created_at  TEXT    DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS comments (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id     INTEGER NOT NULL,
            user_id     INTEGER NOT NULL,
            content     TEXT    NOT NULL,
            created_at  TEXT    DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS likes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id     INTEGER NOT NULL,
            user_id     INTEGER NOT NULL,
            created_at  TEXT    DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (post_id, user_id),
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS follows (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            follower_id     INTEGER NOT NULL,
            following_id    INTEGER NOT NULL,
            created_at      TEXT    DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (follower_id, following_id),
            FOREIGN KEY (follower_id)  REFERENCES users(id),
            FOREIGN KEY (following_id) REFERENCES users(id)
        );
    ''')

    # Seed demo users and posts
    if c.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        demo_users = [
            ('nature_lover',  'Priya Sharma',   'priya@demo.com',   hashlib.sha256(b'demo123').hexdigest(),
             'Nature enthusiast 🌿 | Bangalore | Dry fruits & healthy living advocate',
             'https://i.pravatar.cc/150?img=47', 'priya.blog', 'Bangalore'),
            ('foodie_rajan',  'Rajan Mehta',    'rajan@demo.com',   hashlib.sha256(b'demo123').hexdigest(),
             'Food blogger 🍜 | Exploring flavours across India | Coffee addict ☕',
             'https://i.pravatar.cc/150?img=12', 'foodblog.in', 'Mumbai'),
            ('tech_arjun',    'Arjun Nair',     'arjun@demo.com',   hashlib.sha256(b'demo123').hexdigest(),
             'Full Stack Dev 💻 | Open source contributor | Python & JS enthusiast',
             'https://i.pravatar.cc/150?img=33', 'arjun.dev', 'Hyderabad'),
            ('wellness_sara', 'Sara Krishnan',  'sara@demo.com',    hashlib.sha256(b'demo123').hexdigest(),
             'Wellness coach 🧘 | Nutritionist | Helping people live healthier lives',
             'https://i.pravatar.cc/150?img=5',  'wellness.in', 'Chennai'),
            ('travel_vikram', 'Vikram Patel',   'vikram@demo.com',  hashlib.sha256(b'demo123').hexdigest(),
             'Travel photographer 📸 | 30+ countries | Currently exploring South India',
             'https://i.pravatar.cc/150?img=68', 'vikramphotos.com', 'Pune'),
        ]
        c.executemany('''INSERT INTO users (username, name, email, password, bio, avatar, website, location)
                         VALUES (?,?,?,?,?,?,?,?)''', demo_users)

        demo_posts = [
            (1, "Just received my first shipment of premium Kashmiri saffron! The colour and aroma is absolutely divine 🌸 Nothing beats pure, natural spices. #NaturalLiving #Spices #Saffron",
             'https://images.unsplash.com/photo-1625944525533-473f1a3d54e7?w=600&q=80'),
            (2, "Tried making a dry fruit kheer today with almonds, cashews and medjool dates. Turned out absolutely incredible! Recipe in comments 👇 #Foodie #DryFruits #HealthyRecipes",
             'https://images.unsplash.com/photo-1574856344991-aaa31b6f4ce3?w=600&q=80'),
            (3, "Just deployed my first full stack web app! Flask backend + SQLite + Vanilla JS frontend. Simple, clean and fast. No frameworks needed sometimes 🚀 #WebDev #Python #Flask",
             ''),
            (4, "Morning smoothie with chia seeds, flax seeds and fresh fruits 🥤 Starting the day right! These superfoods are seriously life-changing. #Wellness #SuperFoods #ChiaSeeds",
             'https://images.unsplash.com/photo-1611171711791-7c73bd5dcd87?w=600&q=80'),
            (5, "Golden hour at Hampi 🌅 The ancient ruins are absolutely breathtaking. Karnataka is truly incredible. #Travel #Hampi #Karnataka #Photography",
             'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&q=80'),
            (1, "Did you know? Soaking almonds overnight removes tannins and increases nutrient absorption by up to 50%! 🌰 Small habit, big difference. #HealthTips #Almonds #Nutrition",
             ''),
            (2, "Street food trail in Old Delhi — chaat, jalebi and everything in between. Food is the best way to understand a culture 🍛 #StreetFood #Delhi #FoodTrail",
             'https://images.unsplash.com/photo-1568702846914-96b305d2aaeb?w=600&q=80'),
            (4, "Pumpkin seeds are one of the most underrated superfoods! Zinc, magnesium, healthy fats — all in one tiny seed 🎃 Add them to your salads! #Nutrition #PumpkinSeeds #Wellness",
             'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&q=80'),
        ]
        c.executemany('INSERT INTO posts (user_id, content, image_url) VALUES (?,?,?)', demo_posts)

        demo_comments = [
            (1, 2, "Where did you get this from? Would love to buy some!"),
            (1, 3, "I completely agree! Natural spices are just on another level 🌸"),
            (2, 1, "That kheer sounds amazing! Please share the recipe 😍"),
            (3, 1, "Great post! I need to start eating more dry fruits"),
            (4, 2, "Love your food content! Always so inspiring 🙌"),
            (5, 4, "Hampi is on my bucket list! Stunning photo 📸"),
            (2, 3, "Nice work! What framework did you use for the frontend?"),
            (1, 4, "Chia seeds are amazing! I add them to my morning oats too"),
        ]
        c.executemany('INSERT INTO comments (post_id, user_id, content) VALUES (?,?,?)', demo_comments)

        demo_likes = [
            (1,2),(1,3),(1,4),(1,5),
            (2,1),(2,3),(2,4),
            (3,1),(3,2),(3,5),
            (4,1),(4,2),(4,3),(4,5),
            (5,1),(5,2),(5,4),
            (6,2),(6,3),(6,4),
            (7,1),(7,3),(7,5),
            (8,1),(8,2),(8,3),
        ]
        c.executemany('INSERT INTO likes (post_id, user_id) VALUES (?,?)', demo_likes)

        demo_follows = [
            (1,2),(1,3),(1,4),(1,5),
            (2,1),(2,3),(2,4),
            (3,1),(3,2),(3,5),
            (4,1),(4,2),(4,3),
            (5,1),(5,2),(5,3),(5,4),
        ]
        c.executemany('INSERT INTO follows (follower_id, following_id) VALUES (?,?)', demo_follows)

    conn.commit()
    conn.close()
    print("✅ ConnectSphere database ready!")


def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Login required', 'redirect': '/login'}), 401
        return f(*args, **kwargs)
    return decorated


def get_post_data(post_id, current_user_id=None):
    """Helper — returns full post dict with author, likes, comments count."""
    conn = get_db()
    post = conn.execute('''
        SELECT p.*, u.username, u.name, u.avatar
        FROM posts p JOIN users u ON p.user_id = u.id
        WHERE p.id = ?
    ''', (post_id,)).fetchone()
    if not post:
        conn.close()
        return None
    d = dict(post)
    d['like_count']    = conn.execute('SELECT COUNT(*) FROM likes WHERE post_id=?', (post_id,)).fetchone()[0]
    d['comment_count'] = conn.execute('SELECT COUNT(*) FROM comments WHERE post_id=?', (post_id,)).fetchone()[0]
    d['liked_by_me']   = False
    if current_user_id:
        d['liked_by_me'] = bool(conn.execute(
            'SELECT 1 FROM likes WHERE post_id=? AND user_id=?', (post_id, current_user_id)
        ).fetchone())
    conn.close()
    return d


# ──────────────────────────────────────────────────────────────
#  PAGE ROUTES
# ──────────────────────────────────────────────────────────────

@app.route('/')
def home():           return render_template('index.html')

@app.route('/login')
def login_page():     return render_template('login.html')

@app.route('/register')
def register_page():  return render_template('register.html')

@app.route('/profile')
def profile_page():   return render_template('profile.html')

@app.route('/profile/<username>')
def user_profile(username): return render_template('profile.html', profile_username=username)

@app.route('/explore')
def explore_page():   return render_template('explore.html')

@app.route('/post/<int:pid>')
def post_page(pid):   return render_template('post.html', post_id=pid)


# ──────────────────────────────────────────────────────────────
#  AUTH API
# ──────────────────────────────────────────────────────────────

@app.route('/api/register', methods=['POST'])
def register():
    d = request.get_json()
    name     = d.get('name', '').strip()
    username = d.get('username', '').strip().lower()
    email    = d.get('email', '').strip().lower()
    password = d.get('password', '')

    if not all([name, username, email, password]):
        return jsonify({'error': 'All fields are required'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400

    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO users (username, name, email, password) VALUES (?,?,?,?)',
            (username, name, email, hash_pw(password))
        )
        conn.commit()
        user = conn.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
        session['user_id']       = user['id']
        session['username']      = user['username']
        session['name']          = user['name']
        return jsonify({'success': True, 'username': user['username'], 'name': user['name']})
    except sqlite3.IntegrityError as e:
        if 'username' in str(e):
            return jsonify({'error': 'Username already taken'}), 409
        return jsonify({'error': 'Email already registered'}), 409
    finally:
        conn.close()


@app.route('/api/login', methods=['POST'])
def login():
    d = request.get_json()
    email    = d.get('email', '').strip().lower()
    password = d.get('password', '')
    conn = get_db()
    user = conn.execute(
        'SELECT * FROM users WHERE email=? AND password=?',
        (email, hash_pw(password))
    ).fetchone()
    conn.close()
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401
    session['user_id']  = user['id']
    session['username'] = user['username']
    session['name']     = user['name']
    return jsonify({'success': True, 'username': user['username'], 'name': user['name']})


@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})


@app.route('/api/me')
def me():
    if 'user_id' not in session:
        return jsonify({'logged_in': False})
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id=?', (session['user_id'],)).fetchone()
    conn.close()
    if not user:
        return jsonify({'logged_in': False})
    return jsonify({'logged_in': True, **dict(user)})


# ──────────────────────────────────────────────────────────────
#  USERS API
# ──────────────────────────────────────────────────────────────

@app.route('/api/users/<username>')
def get_user(username):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username=?', (username,)).fetchone()
    if not user:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    d = dict(user)
    d.pop('password', None)
    uid = d['id']
    d['followers_count'] = conn.execute('SELECT COUNT(*) FROM follows WHERE following_id=?', (uid,)).fetchone()[0]
    d['following_count'] = conn.execute('SELECT COUNT(*) FROM follows WHERE follower_id=?',  (uid,)).fetchone()[0]
    d['posts_count']     = conn.execute('SELECT COUNT(*) FROM posts WHERE user_id=?', (uid,)).fetchone()[0]
    d['is_following']    = False
    if 'user_id' in session and session['user_id'] != uid:
        d['is_following'] = bool(conn.execute(
            'SELECT 1 FROM follows WHERE follower_id=? AND following_id=?',
            (session['user_id'], uid)
        ).fetchone())
    conn.close()
    return jsonify(d)


@app.route('/api/users/<username>/posts')
def get_user_posts(username):
    conn = get_db()
    user = conn.execute('SELECT id FROM users WHERE username=?', (username,)).fetchone()
    if not user:
        conn.close()
        return jsonify([])
    posts = conn.execute('''
        SELECT p.*, u.username, u.name, u.avatar
        FROM posts p JOIN users u ON p.user_id = u.id
        WHERE p.user_id = ?
        ORDER BY p.created_at DESC
    ''', (user['id'],)).fetchall()
    result = []
    uid = session.get('user_id')
    for p in posts:
        d = dict(p)
        d['like_count']    = conn.execute('SELECT COUNT(*) FROM likes    WHERE post_id=?', (p['id'],)).fetchone()[0]
        d['comment_count'] = conn.execute('SELECT COUNT(*) FROM comments WHERE post_id=?', (p['id'],)).fetchone()[0]
        d['liked_by_me']   = bool(conn.execute('SELECT 1 FROM likes WHERE post_id=? AND user_id=?', (p['id'], uid)).fetchone()) if uid else False
        result.append(d)
    conn.close()
    return jsonify(result)


@app.route('/api/users/search')
def search_users():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify([])
    conn = get_db()
    users = conn.execute('''
        SELECT id, username, name, avatar, bio FROM users
        WHERE username LIKE ? OR name LIKE ?
        LIMIT 10
    ''', (f'%{q}%', f'%{q}%')).fetchall()
    conn.close()
    return jsonify([dict(u) for u in users])


@app.route('/api/users/<username>/update', methods=['PUT'])
@login_required
def update_profile(username):
    if session['username'] != username:
        return jsonify({'error': 'Unauthorized'}), 403
    d = request.get_json()
    conn = get_db()
    conn.execute('''UPDATE users SET name=?, bio=?, website=?, location=?, avatar=?
                    WHERE id=?''',
                 (d.get('name',''), d.get('bio',''), d.get('website',''),
                  d.get('location',''), d.get('avatar',''), session['user_id']))
    conn.commit()
    session['name'] = d.get('name', session['name'])
    conn.close()
    return jsonify({'success': True})


# ──────────────────────────────────────────────────────────────
#  FOLLOW API
# ──────────────────────────────────────────────────────────────

@app.route('/api/follow/<username>', methods=['POST'])
@login_required
def follow_user(username):
    conn = get_db()
    target = conn.execute('SELECT id FROM users WHERE username=?', (username,)).fetchone()
    if not target:
        conn.close()
        return jsonify({'error': 'User not found'}), 404
    if target['id'] == session['user_id']:
        conn.close()
        return jsonify({'error': 'Cannot follow yourself'}), 400
    try:
        conn.execute('INSERT INTO follows (follower_id, following_id) VALUES (?,?)',
                     (session['user_id'], target['id']))
        conn.commit()
        action = 'followed'
    except sqlite3.IntegrityError:
        conn.execute('DELETE FROM follows WHERE follower_id=? AND following_id=?',
                     (session['user_id'], target['id']))
        conn.commit()
        action = 'unfollowed'
    count = conn.execute('SELECT COUNT(*) FROM follows WHERE following_id=?', (target['id'],)).fetchone()[0]
    conn.close()
    return jsonify({'success': True, 'action': action, 'followers_count': count})


# ──────────────────────────────────────────────────────────────
#  POSTS API
# ──────────────────────────────────────────────────────────────

@app.route('/api/posts', methods=['GET'])
def get_posts():
    """Feed — if logged in: posts from followed users + own. Else: all posts."""
    uid  = session.get('user_id')
    conn = get_db()
    if uid:
        posts = conn.execute('''
            SELECT p.*, u.username, u.name, u.avatar
            FROM posts p JOIN users u ON p.user_id = u.id
            WHERE p.user_id = ?
               OR p.user_id IN (SELECT following_id FROM follows WHERE follower_id=?)
            ORDER BY p.created_at DESC LIMIT 30
        ''', (uid, uid)).fetchall()
    else:
        posts = conn.execute('''
            SELECT p.*, u.username, u.name, u.avatar
            FROM posts p JOIN users u ON p.user_id = u.id
            ORDER BY p.created_at DESC LIMIT 30
        ''').fetchall()
    result = []
    for p in posts:
        d = dict(p)
        d['like_count']    = conn.execute('SELECT COUNT(*) FROM likes    WHERE post_id=?', (p['id'],)).fetchone()[0]
        d['comment_count'] = conn.execute('SELECT COUNT(*) FROM comments WHERE post_id=?', (p['id'],)).fetchone()[0]
        d['liked_by_me']   = bool(conn.execute('SELECT 1 FROM likes WHERE post_id=? AND user_id=?', (p['id'], uid)).fetchone()) if uid else False
        result.append(d)
    conn.close()
    return jsonify(result)


@app.route('/api/posts', methods=['POST'])
@login_required
def create_post():
    d = request.get_json()
    content   = d.get('content', '').strip()
    image_url = d.get('image_url', '').strip()
    if not content:
        return jsonify({'error': 'Post content cannot be empty'}), 400
    if len(content) > 500:
        return jsonify({'error': 'Post too long (max 500 characters)'}), 400
    conn = get_db()
    conn.execute('INSERT INTO posts (user_id, content, image_url) VALUES (?,?,?)',
                 (session['user_id'], content, image_url))
    conn.commit()
    post_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    return jsonify({'success': True, 'post_id': post_id})


@app.route('/api/posts/<int:pid>', methods=['GET'])
def get_post(pid):
    post = get_post_data(pid, session.get('user_id'))
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    return jsonify(post)


@app.route('/api/posts/<int:pid>', methods=['DELETE'])
@login_required
def delete_post(pid):
    conn = get_db()
    post = conn.execute('SELECT user_id FROM posts WHERE id=?', (pid,)).fetchone()
    if not post or post['user_id'] != session['user_id']:
        conn.close()
        return jsonify({'error': 'Unauthorized'}), 403
    conn.execute('DELETE FROM comments WHERE post_id=?', (pid,))
    conn.execute('DELETE FROM likes    WHERE post_id=?', (pid,))
    conn.execute('DELETE FROM posts    WHERE id=?',      (pid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


# ──────────────────────────────────────────────────────────────
#  LIKES API
# ──────────────────────────────────────────────────────────────

@app.route('/api/posts/<int:pid>/like', methods=['POST'])
@login_required
def toggle_like(pid):
    conn = get_db()
    try:
        conn.execute('INSERT INTO likes (post_id, user_id) VALUES (?,?)',
                     (pid, session['user_id']))
        conn.commit()
        action = 'liked'
    except sqlite3.IntegrityError:
        conn.execute('DELETE FROM likes WHERE post_id=? AND user_id=?',
                     (pid, session['user_id']))
        conn.commit()
        action = 'unliked'
    count = conn.execute('SELECT COUNT(*) FROM likes WHERE post_id=?', (pid,)).fetchone()[0]
    conn.close()
    return jsonify({'success': True, 'action': action, 'like_count': count})


# ──────────────────────────────────────────────────────────────
#  COMMENTS API
# ──────────────────────────────────────────────────────────────

@app.route('/api/posts/<int:pid>/comments', methods=['GET'])
def get_comments(pid):
    conn = get_db()
    rows = conn.execute('''
        SELECT c.*, u.username, u.name, u.avatar
        FROM comments c JOIN users u ON c.user_id = u.id
        WHERE c.post_id = ?
        ORDER BY c.created_at ASC
    ''', (pid,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/posts/<int:pid>/comments', methods=['POST'])
@login_required
def add_comment(pid):
    content = request.get_json().get('content', '').strip()
    if not content:
        return jsonify({'error': 'Comment cannot be empty'}), 400
    conn = get_db()
    conn.execute('INSERT INTO comments (post_id, user_id, content) VALUES (?,?,?)',
                 (pid, session['user_id'], content))
    conn.commit()
    cid = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    row = conn.execute('''
        SELECT c.*, u.username, u.name, u.avatar
        FROM comments c JOIN users u ON c.user_id=u.id WHERE c.id=?
    ''', (cid,)).fetchone()
    conn.close()
    return jsonify({'success': True, **dict(row)})


@app.route('/api/comments/<int:cid>', methods=['DELETE'])
@login_required
def delete_comment(cid):
    conn = get_db()
    c = conn.execute('SELECT user_id FROM comments WHERE id=?', (cid,)).fetchone()
    if not c or c['user_id'] != session['user_id']:
        conn.close()
        return jsonify({'error': 'Unauthorized'}), 403
    conn.execute('DELETE FROM comments WHERE id=?', (cid,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


# ──────────────────────────────────────────────────────────────
#  EXPLORE API
# ──────────────────────────────────────────────────────────────

@app.route('/api/explore/users')
def explore_users():
    uid  = session.get('user_id')
    conn = get_db()
    users = conn.execute('''
        SELECT u.id, u.username, u.name, u.avatar, u.bio,
               (SELECT COUNT(*) FROM follows WHERE following_id=u.id) AS followers_count,
               (SELECT COUNT(*) FROM posts   WHERE user_id=u.id)      AS posts_count
        FROM users u
        ORDER BY followers_count DESC
        LIMIT 10
    ''').fetchall()
    result = []
    for u in users:
        d = dict(u)
        d['is_following'] = False
        if uid and uid != u['id']:
            d['is_following'] = bool(conn.execute(
                'SELECT 1 FROM follows WHERE follower_id=? AND following_id=?',
                (uid, u['id'])
            ).fetchone())
        result.append(d)
    conn.close()
    return jsonify(result)


# ──────────────────────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    print("\n🌐 ConnectSphere running at http://localhost:5000\n")
    app.run(debug=True, port=5000)
