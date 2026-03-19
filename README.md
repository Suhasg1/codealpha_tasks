# 🌿 Nature Group — E-Commerce Web Application

<div align="center">

![Nature Group Banner](https://images.unsplash.com/photo-1542838132-92c53300491e?w=900&q=80)

**A full-stack e-commerce web application for Nature Group — selling Premium Dry Fruits, Spices & Seeds**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![HTML5](https://img.shields.io/badge/HTML5-Frontend-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-Styling-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

</div>

---

## 📋 Table of Contents

- [About the Project](#-about-the-project)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [API Reference](#-api-reference)
- [Database Schema](#-database-schema)
- [Products Catalogue](#-products-catalogue)
- [Future Enhancements](#-future-enhancements)

---

## 🌱 About the Project

**Nature Group** is a full-stack e-commerce web application built as part of a Full Stack Web Development project. It allows users to browse, search, and purchase premium natural products including Dry Fruits, Spices, and Seeds.

The project demonstrates end-to-end web development — from a Python Flask REST API backend with SQLite database, to a fully responsive vanilla HTML/CSS/JavaScript frontend.

> 💡 All product prices are based on **Bangalore market rates (2025)**.

---

## ✨ Features

### 🛍️ Shopping Experience
- Browse **26 products** across 3 categories — Dry Fruits, Spices, Seeds
- Filter products by **category** and **price range**
- **Search** products by name or description
- **Sort** by name, price (low→high / high→low), or top rated
- Individual **product detail page** with description, rating, stock info
- **Related products** suggestions on each product page

### 🛒 Shopping Cart
- Add products with custom **quantity selector**
- **Update quantity** or remove items from cart
- **Live price calculation** — subtotal + shipping
- **Free shipping** on orders above ₹500
- Persistent cart tied to user account

### 🔐 User Authentication
- **Register** with name, email and password
- **Login / Logout** with session management
- Passwords securely hashed with **SHA-256**
- Protected routes — cart and orders require login

### 📦 Order Management
- **Checkout** with full delivery address form
- Choose payment method — **COD / UPI / Card** (UI ready)
- **Order confirmation** with unique Order ID
- Complete **order history** with status tracking

### 🎨 UI & Design
- Custom **forest green theme** with gold accents
- **Playfair Display + DM Sans** typography
- Fully **responsive** — works on mobile and desktop
- Real **product images** from Unsplash (free CDN)
- Toast notifications, loading spinners, empty states

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Python 3 + Flask | REST API server, routing, session management |
| **Database** | SQLite + sqlite3 | Storing users, products, cart, orders |
| **Frontend** | HTML5, CSS3, JavaScript ES6 | UI pages, interactivity |
| **Auth** | Flask Sessions + SHA-256 | User authentication and security |
| **Fonts** | Google Fonts | Playfair Display + DM Sans |
| **Images** | Unsplash CDN | Free high-quality product photos |

---

## 📁 Project Structure

```
nature_group/
│
├── backend/
│   ├── app.py                  ← Flask server — all routes + REST API
│   └── nature_group.db         ← SQLite database (auto-created on first run)
│
├── frontend/
│   ├── css/
│   │   └── style.css           ← Complete stylesheet (green theme, all components)
│   │
│   ├── js/
│   │   ├── main.js             ← Shared utilities (API helper, toast, auth, cart count)
│   │   ├── products.js         ← Products page (filter, search, sort logic)
│   │   ├── cart.js             ← Cart page (add, update, remove items)
│   │   ├── checkout.js         ← Checkout + order placement
│   │   └── auth.js             ← Login + Register form logic
│   │
│   └── pages/
│       ├── index.html          ← Homepage (hero, featured products, categories)
│       ├── products.html       ← Product listing with sidebar filters
│       ├── product_detail.html ← Single product page with related items
│       ├── cart.html           ← Shopping cart with order summary
│       ├── checkout.html       ← Checkout form + payment selection
│       ├── orders.html         ← Order history page
│       ├── login.html          ← User login page
│       └── register.html       ← User registration page
│
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.8+** installed → [Download Python](https://python.org/downloads)
- **pip** (comes with Python)
- A modern web browser (Chrome, Edge, Firefox)

### Installation & Setup

**Step 1 — Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/nature-group.git
cd nature-group
```

**Step 2 — Create a virtual environment**
```bash
python -m venv venv
```

**Step 3 — Activate the virtual environment**

Windows (Command Prompt):
```bash
venv\Scripts\activate.bat
```
Windows (PowerShell):
```bash
venv\Scripts\Activate.ps1
```
Mac / Linux:
```bash
source venv/bin/activate
```

**Step 4 — Install dependencies**
```bash
pip install flask
```

**Step 5 — Run the server**
```bash
cd backend
python app.py
```

**Step 6 — Open in browser**
```
http://localhost:5000
```

> ✅ The SQLite database is **automatically created** on first run with all 26 products seeded. No extra setup needed!

### Resetting the Database
```bash
# Windows
del backend\nature_group.db

# Mac / Linux
rm backend/nature_group.db

# Then restart
python app.py
```

---

## 📡 API Reference

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|---------|-------------|:---:|
| POST | /api/register | Create new user account | ❌ |
| POST | /api/login | Login with email + password | ❌ |
| POST | /api/logout | Logout current user | ❌ |
| GET | /api/me | Get current logged-in user | ❌ |

### Products

| Method | Endpoint | Description | Auth Required |
|--------|---------|-------------|:---:|
| GET | /api/products | Get all products (supports filters) | ❌ |
| GET | /api/products/:id | Get single product by ID | ❌ |

**Query Parameters for GET /api/products:**

| Param | Values | Example |
|-------|--------|---------|
| category | Dry Fruits, Spices, Seeds | ?category=Spices |
| search | Any keyword | ?search=almond |
| sort | name, price_asc, price_desc, rating | ?sort=price_asc |

### Cart

| Method | Endpoint | Description | Auth Required |
|--------|---------|-------------|:---:|
| GET | /api/cart | Get all cart items | ✅ |
| GET | /api/cart/count | Get total item count | ❌ |
| POST | /api/cart | Add item to cart | ✅ |
| PUT | /api/cart/:id | Update item quantity | ✅ |
| DELETE | /api/cart/:id | Remove item from cart | ✅ |

### Orders

| Method | Endpoint | Description | Auth Required |
|--------|---------|-------------|:---:|
| GET | /api/orders | Get all orders for current user | ✅ |
| POST | /api/orders | Place a new order | ✅ |

---

## 🗄️ Database Schema

```sql
CREATE TABLE users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    email       TEXT    UNIQUE NOT NULL,
    password    TEXT    NOT NULL,
    created_at  TEXT    DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
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

CREATE TABLE cart (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    product_id  INTEGER NOT NULL,
    quantity    INTEGER DEFAULT 1,
    FOREIGN KEY (user_id)    REFERENCES users(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE orders (
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
```

---

## 🛒 Products Catalogue

### 🌰 Dry Fruits — 10 Products
| Product | Pack | Price |
|---------|------|-------|
| Premium Almonds (Badam) | 250g | ₹399 |
| Cashew Nuts W240 (Kaju) | 250g | ₹412 |
| Walnuts (Akhrot) | 250g | ₹449 |
| Dry Dates (Kharik) | 250g | ₹50 |
| Wet Dates / Medjool (Khajur) | 500g | ₹299 |
| Pistachios (Pista) | 250g | ₹400 |
| Dried Black Grapes (Kali Kishmish) | 250g | ₹150 |
| Dried Figs (Anjeer) | 250g | ₹450 |
| Kishmish (Green Raisins) | 500g | ₹175 |
| Dried Apricots (Khumani) | 250g | ₹225 |

### 🌸 Spices — 6 Products
| Product | Pack | Price |
|---------|------|-------|
| Kashmiri Saffron (Kesar) | 1g | ₹899 |
| Black Pepper Whole | 200g | ₹249 |
| Cinnamon Sticks (Ceylon) | 100g | ₹189 |
| Star Anise (Chakra Phool) | 100g | ₹149 |
| Turmeric Powder (Haldi) | 200g | ₹129 |
| Green Cardamom (Elaichi) | 100g | ₹449 |

### 🌱 Seeds — 10 Products
| Product | Pack | Price |
|---------|------|-------|
| Chia Seeds | 500g | ₹249 |
| Flax Seeds (Alsi) | 500g | ₹129 |
| Pumpkin Seeds (Pepitas) | 250g | ₹299 |
| Sunflower Seeds | 500g | ₹99 |
| Hemp Seeds | 250g | ₹449 |
| Sesame Seeds White (Til) | 500g | ₹79 |
| Basil Seeds (Sabja) | 250g | ₹149 |
| Poppy Seeds (Khus Khus) | 250g | ₹199 |
| Muskmelon Seeds (Charmagaz) | 250g | ₹249 |
| Lotus Seeds (Makhana / Fox Nut) | 250g | ₹299 |

> 📍 Prices based on Bangalore market rates, 2025

---

## 🔮 Future Enhancements

- [ ] Razorpay Integration — Real UPI / Card payments for Indian market
- [ ] Email Confirmation — Order confirmation emails via Gmail SMTP
- [ ] Admin Dashboard — Manage products, view all orders, update stock
- [ ] Product Reviews — Users can rate and review purchased products
- [ ] Wishlist — Save products for later
- [ ] Coupon Codes — Discount code support at checkout
- [ ] Deploy to Cloud — Host on Render / Railway for permanent public URL

---

## 👨‍💻 Author

Built as a **Full Stack Web Development Project**

---

## 📄 License

This project is built for educational purposes as part of a Full Stack Development course.

---

<div align="center">
  Made with ❤️ and 🌿 — Nature Group
</div>
