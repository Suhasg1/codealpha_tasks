"""
Nature Group - E-Commerce Backend
Flask + SQLite

Run:
    pip install flask
    python app.py

Server starts at: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify, session
import sqlite3, hashlib, os, json
from functools import wraps

app = Flask(__name__, template_folder='../frontend/pages',
            static_folder='../frontend', static_url_path='/static')
app.secret_key = 'nature_group_secret_key_2024'
DB_PATH = os.path.join(os.path.dirname(__file__), 'nature_group.db')


# ──────────────────────────────────────────────
#  DATABASE
# ──────────────────────────────────────────────

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
            name        TEXT    NOT NULL,
            email       TEXT    UNIQUE NOT NULL,
            password    TEXT    NOT NULL,
            created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS products (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            name           TEXT    NOT NULL,
            category       TEXT    NOT NULL,
            price          REAL    NOT NULL,
            original_price REAL,
            description    TEXT,
            weight         TEXT,
            stock          INTEGER DEFAULT 100,
            badge          TEXT,
            emoji          TEXT,
            image_url      TEXT,
            rating         REAL    DEFAULT 4.5,
            reviews        INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS cart (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            product_id  INTEGER NOT NULL,
            quantity    INTEGER DEFAULT 1,
            FOREIGN KEY (user_id)    REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        );

        CREATE TABLE IF NOT EXISTS orders (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER,
            user_name   TEXT,
            user_email  TEXT,
            items       TEXT    NOT NULL,
            subtotal    REAL,
            shipping    REAL,
            total       REAL,
            status      TEXT    DEFAULT 'Processing',
            address     TEXT,
            payment     TEXT,
            created_at  TEXT    DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')

    # Seed products only once
    if c.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
        # Format: (name, category, price/250g, original_price, description, weight, stock, badge, emoji, image_url, rating, reviews)
        # Prices are per 250g pack unless stated. Based on Bangalore market rates 2025.
        products = [

            # ── DRY FRUITS ──────────────────────────────────────────────────────────
            ('Premium Almonds (Badam)',
             'Dry Fruits', 399, 499,
             'California almonds, rich in Vitamin E and healthy fats. Promotes heart health, boosts energy and perfect for daily snacking.',
             '250g', 150, 'Best Seller', '🌰',
             'https://images.unsplash.com/photo-1772986798556-94527d2caab9?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fGFsbW9uZCUyMHdpdGglMjB3aGl0ZSUyMGJhY2tncm91bmR8ZW58MHx8MHx8fDA%3D',
             4.8, 234),

            ('Cashew Nuts W240 (Kaju)',
             'Dry Fruits', 412, 499,
             'Premium whole cashews, grade W240. Creamy and buttery — ideal for curries, desserts and snacking. Rich in zinc and magnesium.',
             '250g', 120, 'Premium', '🥜',
             'https://images.unsplash.com/photo-1641718111847-7e509a4dd208?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTV8fGNhc2hldyUyMG51dHMlMjBmdWxsJTIwZnJhbWV8ZW58MHx8MHx8fDA%3D',
             4.7, 189),

            ('Walnuts (Akhrot)',
             'Dry Fruits', 449, 549,
             'Handpicked walnuts loaded with Omega-3 fatty acids. Excellent for brain health, heart function and reducing inflammation.',
             '250g', 100, None, '🪨',
             'https://images.unsplash.com/photo-1605525483148-8fb743b620da?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fHdhbG51dHN8ZW58MHx8MHx8fDA%3D',
             4.6, 178),

            ('Dry Dates (Kharik)',
             'Dry Fruits', 50, 75,
             'Natural sundried dates. Low in fat, high in fibre. Traditional energy booster — great for fasting and cooking.',
             '250g', 200, None, '🟤',
             'https://pngimg.com/uploads/dates/dates_PNG11044.png',
             4.3, 89),

            ('Wet Dates / Medjool (Khajur)',
             'Dry Fruits', 299, 374,
             'Premium soft Medjool dates, king of dates. Naturally sweet, rich in potassium and instant natural energy.',
             '500g', 90, 'Organic', '🌴',
             'https://media.istockphoto.com/id/181077887/photo/dates.jpg?s=612x612&w=0&k=20&c=SDwqs0oumCH9P0ZPC__x27r12zGcfDn-Tcakq3FyZVs=',
             4.9, 312),

            ('Pistachios (Pista)',
             'Dry Fruits', 400, 499,
             'Premium California pistachios, lightly roasted. Rich in antioxidants, fibre and heart-healthy fats.',
             '250g', 80, 'Premium', '💚',
             'https://img.freepik.com/premium-photo/pistachio-nuts-with-green-leaves-isolated-white-background_252965-390.jpg',
             4.7, 203),

            ('Dried Black Grapes (Kali Kishmish)',
             'Dry Fruits', 150, 199,
             'Sundried black raisins from Nashik. Rich in iron, antioxidants and natural sweetness. Great for digestion.',
             '250g', 200, None, '🍇',
             'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSTncOaztNyRpWlRG98UV0sc3KS7f9tRs2AWg&s',
             4.5, 134),

            ('Dried Figs (Anjeer)',
             'Dry Fruits', 450, 549,
             'Afghani dried figs — soft, naturally sweet and loaded with fibre, calcium and iron. A true superfood.',
             '250g', 80, 'Imported', '🟣',
             'https://thumbs.dreamstime.com/b/indian-anjeer-dried-figs-healthy-dry-fruit-india-nutritional-food-188711299.jpg',
             4.6, 98),

            ('Kishmish (Green Raisins)',
             'Dry Fruits', 175, 225,
             'Premium green seedless raisins. Naturally sweet, no added sugar. Perfect for baking, cooking and snacking.',
             '500g', 250, None, '🟢',
             'https://www.alzameendar.com/cdn/shop/products/greenkishmish1.webp?v=1681953453&width=1445',
             4.4, 112),

            ('Dried Apricots (Khumani)',
             'Dry Fruits', 225, 279,
             'Sundried Turkish apricots, sulphur-free. Rich in iron, Vitamin A and beta carotene. Great for skin and eye health.',
             '250g', 110, None, '🟠',
             'https://www.kashmironlinestore.com/cdn/shop/products/apricot-seedless.jpg?v=1738998891',
             4.4, 87),

            # ── SPICES ──────────────────────────────────────────────────────────────
            ('Kashmiri Saffron (Kesar)',
             'Spices', 899, 1199,
             'Pure hand-picked Kashmiri saffron. Intense golden colour and rich aroma — elevates biryani, kheer and desserts.',
             '1g', 50, 'Pure', '🌸',
             'https://www.gitagged.com/wp-content/uploads/2021/06/Kashmir-Saffron-Online-2.jpg',
             4.9, 445),

            ('Black Pepper Whole',
             'Spices', 249, 299,
             'Malabar black pepper, hand-sorted. Bold and pungent, perfect for all cuisines.',
             '200g', 180, None, '⚫',
             'https://images.unsplash.com/photo-1649952052743-5e8f37c348c5?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8QmxhY2slMjBQZXBwZXIlMjBXaG9sZXxlbnwwfHwwfHx8MA%3D%3D',
             4.7, 178),

            ('Cinnamon Sticks (Ceylon)',
             'Spices', 189, 229,
             'True Ceylon cinnamon sticks. Mild, sweet and fragrant. Superior quality for chai, desserts and cooking.',
             '100g', 160, 'Ceylon', '🟫',
             'https://media.istockphoto.com/id/959028954/photo/three-cinnamon-sticks-isolated-on-a-white-background.webp?a=1&b=1&s=612x612&w=0&k=20&c=vDgVI4SlOQy0O4157KC99oZxh2FrkjwsThv4F8xTB2c=',
             4.6, 134),

            ('Star Anise (Chakra Phool)',
             'Spices', 149, 199,
             'Whole star anise, intensely aromatic. Essential for biryani, masala chai and flavouring curries.',
             '100g', 200, None, '⭐',
             'https://images.unsplash.com/photo-1642255487710-93529c00660e?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fFN0YXIlMjBBbmlzZXxlbnwwfHwwfHx8MA%3D%3D',
             4.5, 92),

            ('Turmeric Powder (Haldi)',
             'Spices', 129, 159,
             'High-curcumin Lakadong turmeric. 5% curcumin content, deep golden colour. Anti-inflammatory superfood.',
             '200g', 300, 'High Curcumin', '🟡',
             'https://media.gettyimages.com/id/672151311/photo/pile-of-yellow-powder.jpg?s=612x612&w=0&k=20&c=FXB-xQ5ijWa52s2-L4J8avjdy28mUT6uRXEx-N-QxxY=',
             4.8, 267),

            ('Green Cardamom (Elaichi)',
             'Spices', 449, 549,
             'Bold green cardamom from Kerala. Strong aroma, perfect for chai, sweets and biryanis.',
             '100g', 90, 'Kerala', '💚',
             'https://images.unsplash.com/photo-1642255486695-a52c59347cfa?w=600&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTZ8fEdyZWVuJTIwQ2FyZGFtb218ZW58MHx8MHx8fDA%3D',
             4.7, 203),

            # ── SEEDS ───────────────────────────────────────────────────────────────
            ('Chia Seeds',
             'Seeds', 249, 349,
             'Raw chia seeds, rich in Omega-3 and fibre. Great for puddings, smoothies, weight loss and baking. Bangalore market rate ₹250–275/kg.',
             '500g', 250, 'Superfood', '⚪',
             'https://img.freepik.com/free-photo/chia-seed_1368-9200.jpg',
             4.7, 389),

            ('Flax Seeds (Alsi)',
             'Seeds', 129, 169,
             'Golden flaxseeds. High in lignans and Omega-3 fatty acids. Excellent for heart health and digestion.',
             '500g', 300, None, '🟤',
             'https://png.pngtree.com/png-vector/20240926/ourmid/pngtree-flax-seeds-on-transparent-background-png-image_13919779.png',
             4.5, 167),

            ('Pumpkin Seeds (Pepitas)',
             'Seeds', 299, 399,
             'Raw hulled pumpkin seeds. Excellent source of zinc, magnesium and protein. Great for snacking and topping salads.',
             '250g', 140, 'Raw', '🎃',
             'https://t3.ftcdn.net/jpg/02/85/25/36/360_F_285253607_Vz4kNaAgT1j7x8cDQoL2c572jnz6cxlx.jpg',
             4.6, 145),

            ('Sunflower Seeds',
             'Seeds', 99, 139,
             'Raw hulled sunflower seeds. Packed with Vitamin E, selenium and healthy fats. Perfect for snacking and baking.',
             '500g', 220, None, '🌻',
             'https://media.istockphoto.com/id/918670510/photo/unpeeled-sunflower-seeds.jpg?s=612x612&w=0&k=20&c=CuH5juUisdY9-RKETGjttSCTtAfB3E6ZY46zVHBfz5k=',
             4.4, 123),

            ('Hemp Seeds',
             'Seeds', 449, 599,
             'Organic hulled hemp seeds. Complete protein source with all 9 essential amino acids. Rich in Omega-3 and Omega-6.',
             '250g', 80, 'Organic', '🌿',
             'https://www.forestwholefoods.co.uk/wp-content/uploads/2017/04/Organic-Whole-Hemp-Seed-1500px.jpg',
             4.8, 234),

            ('Sesame Seeds White (Til)',
             'Seeds', 79, 109,
             'Pure white sesame seeds. Essential for tahini, til ladoo, chikki and garnishing dishes.',
             '500g', 400, None, '⬜',
             'https://i.pinimg.com/736x/a5/72/cb/a572cb04c192b66c3a849bb9fac9b289.jpg',
             4.5, 98),

            ('Basil Seeds (Sabja / Tukmaria)',
             'Seeds', 149, 199,
             'Natural sabja seeds used in sharbat, falooda and cooling drinks. High in fibre and known for cooling properties.',
             '250g', 180, 'Cooling', '🖤',
             'https://i.pinimg.com/1200x/66/8d/76/668d769a584ce6f8234b5f17a3337513.jpg',
             4.6, 156),

            ('Poppy Seeds (Khus Khus)',
             'Seeds', 199, 249,
             'White poppy seeds, finely ground. Essential culinary ingredient for gravies, pastries and korma recipes.',
             '250g', 120, None, '🌾',
             'https://i.pinimg.com/1200x/83/96/00/839600722c94288fc354a697f988f0a6.jpg',
             4.4, 78),

            ('Muskmelon Seeds (Charmagaz)',
             'Seeds', 249, 319,
             'Dried muskmelon seeds, high in protein and healthy fats. Used in milkshakes, thandai and traditional cooling drinks.',
             '250g', 90, None, '🍈',
             'https://i.pinimg.com/736x/5c/37/8c/5c378c315ba7830a127c4cbbeca3fd11.jpg',
             4.3, 67),

            ('Lotus Seeds (Makhana / Fox Nut)',
             'Seeds', 299, 399,
             'Premium roasted lotus seeds (makhana). Low in calories, high in protein. Perfect for fasting, snacking and kheer.',
             '250g', 150, 'Fasting Food', '⭕',
             'https://i.pinimg.com/1200x/a2/3a/c2/a23ac2acb43bf63d51520f23dfb54842.jpg',
             4.7, 198),
        ]
        c.executemany(
            '''INSERT INTO products
               (name, category, price, original_price, description, weight, stock, badge, emoji, image_url, rating, reviews)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
            products
        )

    conn.commit()
    conn.close()
    print("✅ Database ready with products seeded.")


def hash_pw(password):
    return hashlib.sha256(password.encode()).hexdigest()


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Login required', 'redirect': '/login'}), 401
        return f(*args, **kwargs)
    return decorated


# ──────────────────────────────────────────────
#  PAGE ROUTES  (serve HTML files)
# ──────────────────────────────────────────────

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/products')
def products_page():
    return render_template('products.html')

@app.route('/product/<int:pid>')
def product_detail(pid):
    return render_template('product_detail.html', product_id=pid)

@app.route('/cart')
def cart_page():
    return render_template('cart.html')

@app.route('/checkout')
def checkout_page():
    return render_template('checkout.html')

@app.route('/orders')
def orders_page():
    return render_template('orders.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')


# ──────────────────────────────────────────────
#  AUTH API
# ──────────────────────────────────────────────

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    name     = data.get('name', '').strip()
    email    = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not name or not email or not password:
        return jsonify({'error': 'All fields are required'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    conn = get_db()
    try:
        conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                     (name, email, hash_pw(password)))
        conn.commit()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        session['user_id']    = user['id']
        session['user_name']  = user['name']
        session['user_email'] = user['email']
        return jsonify({'success': True, 'name': user['name']})
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Email already registered'}), 409
    finally:
        conn.close()


@app.route('/api/login', methods=['POST'])
def login():
    data  = request.get_json()
    email = data.get('email', '').strip().lower()
    pw    = data.get('password', '')

    conn = get_db()
    user = conn.execute(
        'SELECT * FROM users WHERE email = ? AND password = ?',
        (email, hash_pw(pw))
    ).fetchone()
    conn.close()

    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401

    session['user_id']    = user['id']
    session['user_name']  = user['name']
    session['user_email'] = user['email']
    return jsonify({'success': True, 'name': user['name']})


@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})


@app.route('/api/me')
def me():
    if 'user_id' in session:
        return jsonify({
            'logged_in': True,
            'name':  session['user_name'],
            'email': session['user_email'],
        })
    return jsonify({'logged_in': False})


# ──────────────────────────────────────────────
#  PRODUCTS API
# ──────────────────────────────────────────────

@app.route('/api/products')
def get_products():
    category = request.args.get('category', '')
    search   = request.args.get('search', '')
    sort     = request.args.get('sort', 'name')

    query  = 'SELECT * FROM products WHERE 1=1'
    params = []

    if category and category != 'All':
        query += ' AND category = ?'
        params.append(category)

    if search:
        query += ' AND (name LIKE ? OR description LIKE ?)'
        params += [f'%{search}%', f'%{search}%']

    sort_map = {
        'name':       'name ASC',
        'price_asc':  'price ASC',
        'price_desc': 'price DESC',
        'rating':     'rating DESC',
    }
    query += f' ORDER BY {sort_map.get(sort, "name ASC")}'

    conn = get_db()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/products/<int:pid>')
def get_product(pid):
    conn = get_db()
    row  = conn.execute('SELECT * FROM products WHERE id = ?', (pid,)).fetchone()
    conn.close()
    if not row:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify(dict(row))


# ──────────────────────────────────────────────
#  CART API
# ──────────────────────────────────────────────

@app.route('/api/cart', methods=['GET'])
@login_required
def get_cart():
    conn = get_db()
    rows = conn.execute(
        '''SELECT c.id, c.quantity,
                  p.id AS product_id, p.name, p.price, p.emoji, p.weight, p.category, p.image_url
           FROM cart c
           JOIN products p ON c.product_id = p.id
           WHERE c.user_id = ?''',
        (session['user_id'],)
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route('/api/cart', methods=['POST'])
@login_required
def add_to_cart():
    data       = request.get_json()
    product_id = data.get('product_id')
    quantity   = data.get('quantity', 1)

    conn     = get_db()
    existing = conn.execute(
        'SELECT id FROM cart WHERE user_id = ? AND product_id = ?',
        (session['user_id'], product_id)
    ).fetchone()

    if existing:
        conn.execute(
            'UPDATE cart SET quantity = quantity + ? WHERE id = ?',
            (quantity, existing['id'])
        )
    else:
        conn.execute(
            'INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)',
            (session['user_id'], product_id, quantity)
        )

    conn.commit()
    total = conn.execute(
        'SELECT SUM(quantity) FROM cart WHERE user_id = ?',
        (session['user_id'],)
    ).fetchone()[0] or 0
    conn.close()
    return jsonify({'success': True, 'cart_count': total})


@app.route('/api/cart/<int:cart_id>', methods=['PUT'])
@login_required
def update_cart(cart_id):
    quantity = request.get_json().get('quantity', 1)
    conn = get_db()
    if quantity <= 0:
        conn.execute('DELETE FROM cart WHERE id = ? AND user_id = ?',
                     (cart_id, session['user_id']))
    else:
        conn.execute('UPDATE cart SET quantity = ? WHERE id = ? AND user_id = ?',
                     (quantity, cart_id, session['user_id']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


@app.route('/api/cart/<int:cart_id>', methods=['DELETE'])
@login_required
def remove_from_cart(cart_id):
    conn = get_db()
    conn.execute('DELETE FROM cart WHERE id = ? AND user_id = ?',
                 (cart_id, session['user_id']))
    conn.commit()
    conn.close()
    return jsonify({'success': True})


@app.route('/api/cart/count')
def cart_count():
    if 'user_id' not in session:
        return jsonify({'count': 0})
    conn  = get_db()
    count = conn.execute(
        'SELECT SUM(quantity) FROM cart WHERE user_id = ?',
        (session['user_id'],)
    ).fetchone()[0] or 0
    conn.close()
    return jsonify({'count': count})


# ──────────────────────────────────────────────
#  ORDERS API
# ──────────────────────────────────────────────

@app.route('/api/orders', methods=['POST'])
@login_required
def place_order():
    data = request.get_json()
    conn = get_db()

    cart_items = conn.execute(
        '''SELECT c.quantity, p.name, p.price, p.emoji
           FROM cart c
           JOIN products p ON c.product_id = p.id
           WHERE c.user_id = ?''',
        (session['user_id'],)
    ).fetchall()

    if not cart_items:
        conn.close()
        return jsonify({'error': 'Cart is empty'}), 400

    items    = [{'name': r['name'], 'qty': r['quantity'],
                 'price': r['price'], 'emoji': r['emoji']} for r in cart_items]
    subtotal = sum(i['price'] * i['qty'] for i in items)
    shipping = 0 if subtotal >= 500 else 49
    total    = subtotal + shipping

    conn.execute(
        '''INSERT INTO orders
           (user_id, user_name, user_email, items, subtotal, shipping, total, address, payment)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (session['user_id'], session['user_name'], session['user_email'],
         json.dumps(items), subtotal, shipping, total,
         data.get('address', ''), data.get('payment', 'COD'))
    )
    conn.execute('DELETE FROM cart WHERE user_id = ?', (session['user_id'],))
    conn.commit()

    order_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]
    conn.close()
    return jsonify({'success': True, 'order_id': order_id, 'total': total})


@app.route('/api/orders', methods=['GET'])
@login_required
def get_orders():
    conn = get_db()
    rows = conn.execute(
        'SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC',
        (session['user_id'],)
    ).fetchall()
    conn.close()

    orders = []
    for r in rows:
        o = dict(r)
        o['items'] = json.loads(o['items'])
        orders.append(o)
    return jsonify(orders)


# ──────────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    print("\n🌿 Nature Group server running at http://localhost:5000\n")
    app.run(debug=True, port=5000)
