# 🌐 ConnectSphere — Social Media Platform

<div align="center">

### 🏢 CodeAlpha Internship — Full Stack Web Development
### 📌 Task 2 — Social Media Platform

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![HTML5](https://img.shields.io/badge/HTML5-Frontend-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-Styling-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

</div>

---

## 🏢 Internship Details

| Field | Details |
|-------|---------|
| **Organization** | CodeAlpha |
| **Internship Domain** | Full Stack Web Development |
| **Task Number** | Task 2 |
| **Project Name** | ConnectSphere — Social Media Platform |
| **Tech Stack** | Python Flask + SQLite + HTML + CSS + JavaScript |

---

## 🌱 About the Project

**ConnectSphere** is a full-stack mini social media platform built as **Task 2** of the **CodeAlpha Full Stack Web Development Internship**. Users can create profiles, write posts, like and comment on content, and follow other users — similar to Twitter/X.

---

## ✨ Features

### 👤 User Profiles
- Register and login with email + password
- Customizable profile — name, bio, avatar, location, website
- View post count, followers and following count
- Edit profile from the profile page

### 📝 Posts & Feed
- Create text posts with optional image URL
- Home feed shows posts from followed users
- 500 character limit with live counter
- Delete your own posts

### 💬 Comments
- Comment on any post
- Comments load dynamically without page refresh
- Delete your own comments
- Real-time comment count update

### ❤️ Like System
- Like / unlike posts with one click
- Live like count updates instantly
- Heart animation on toggle

### 👥 Follow System
- Follow / unfollow any user
- Follower and following counts update instantly
- Personalised feed based on who you follow
- "Who to Follow" suggestions on home page

### 🔍 Search & Explore
- Search users by name or username (live search)
- Explore page with user cards and follow buttons
- Trending hashtags sidebar

### 🎨 UI & Design
- Dark navy theme with electric blue + coral accents
- Sora + Nunito typography
- Fully responsive — mobile and desktop
- Toast notifications, loading spinners

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Python 3 + Flask | REST API, routing, session management |
| **Database** | SQLite + sqlite3 | Users, posts, comments, likes, follows |
| **Frontend** | HTML5, CSS3, JavaScript ES6 | UI, interactivity |
| **Auth** | Flask Sessions + SHA-256 | Secure authentication |
| **Avatars** | pravatar.cc | Demo user avatars |

---

## 📁 Project Structure

```
Task_2_SocialMedia/
│
├── backend/
│   ├── app.py                ← Flask server — all routes + REST API
│   └── connectsphere.db      ← SQLite database (auto-created on first run)
│
├── frontend/
│   ├── css/
│   │   └── style.css         ← Complete dark theme stylesheet
│   │
│   ├── js/
│   │   └── main.js           ← All shared JS — posts, comments, likes, follows
│   │
│   └── pages/
│       ├── index.html        ← Home feed
│       ├── profile.html      ← User profile page
│       ├── explore.html      ← Explore / discover users
│       ├── post.html         ← Single post detail
│       ├── login.html        ← Login page
│       └── register.html     ← Register page
│
└── README.md
```

---

## 🚀 Getting Started

**Step 1 — Clone and navigate**
```bash
git clone https://github.com/YOUR_USERNAME/codealpha_tasks.git
cd codealpha_tasks/Task_2_SocialMedia
```

**Step 2 — Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate.bat     # Windows
source venv/bin/activate      # Mac/Linux
```

**Step 3 — Install Flask**
```bash
pip install flask
```

**Step 4 — Run the server**
```bash
cd backend
python app.py
```

**Step 5 — Open browser**
```
http://localhost:5000
```

> ✅ Database auto-created with 5 demo users, 8 posts, comments, likes and follows!

### 🎭 Demo Login Credentials
| Email | Password |
|-------|----------|
| priya@demo.com | demo123 |
| rajan@demo.com | demo123 |
| arjun@demo.com | demo123 |
| sara@demo.com  | demo123 |
| vikram@demo.com| demo123 |

---

## 📡 API Reference

### Auth
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | /api/register | Register new user |
| POST | /api/login | Login |
| POST | /api/logout | Logout |
| GET | /api/me | Current user info |

### Users
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | /api/users/:username | Get user profile |
| GET | /api/users/:username/posts | Get user's posts |
| PUT | /api/users/:username/update | Update profile |
| GET | /api/users/search?q= | Search users |

### Posts
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | /api/posts | Get feed posts |
| POST | /api/posts | Create post |
| GET | /api/posts/:id | Get single post |
| DELETE | /api/posts/:id | Delete post |

### Likes
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | /api/posts/:id/like | Toggle like |

### Comments
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | /api/posts/:id/comments | Get comments |
| POST | /api/posts/:id/comments | Add comment |
| DELETE | /api/comments/:id | Delete comment |

### Follow
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | /api/follow/:username | Toggle follow/unfollow |

---

## 🗄️ Database Schema

```sql
users    (id, username, name, email, password, bio, avatar, website, location, created_at)
posts    (id, user_id, content, image_url, created_at)
comments (id, post_id, user_id, content, created_at)
likes    (id, post_id, user_id, created_at)  -- UNIQUE(post_id, user_id)
follows  (id, follower_id, following_id, created_at)  -- UNIQUE(follower_id, following_id)
```

---

## 🔮 Future Enhancements

- [ ] Real-time notifications using WebSockets
- [ ] Direct messaging between users
- [ ] Image upload (Cloudinary integration)
- [ ] Stories feature (24-hour posts)
- [ ] Post bookmarks / saved posts
- [ ] Hashtag search and trending topics
- [ ] Email verification on register

---

## 👨‍💻 Intern Details

| Field | Details |
|-------|---------|
| **Internship** | CodeAlpha |
| **Domain** | Full Stack Web Development |
| **Task** | Task 2 — Social Media Platform |
| **Project** | ConnectSphere |

---

<div align="center">

### 🌐 ConnectSphere
**CodeAlpha Internship — Full Stack Web Development — Task 2**

Made with ❤️ for CodeAlpha Internship

</div>
