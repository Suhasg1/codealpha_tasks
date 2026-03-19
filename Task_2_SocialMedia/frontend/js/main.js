/**
 * ConnectSphere — Main JS
 * Shared utilities: API helper, toast, auth state, navbar
 * CodeAlpha Internship | Task 2
 */

/* ── API Helper ─────────────────────────────────────────────── */
async function apiFetch(url, options = {}) {
  const config = { headers: { 'Content-Type': 'application/json' }, ...options };
  if (options.body && typeof options.body === 'object') {
    config.body = JSON.stringify(options.body);
  }
  const res = await fetch(url, config);
  return res.json();
}

/* ── Toast ──────────────────────────────────────────────────── */
function showToast(message, type = 'success') {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = (type === 'success' ? '✓  ' : '✕  ') + message;
  toast.className = `show ${type}`;
  clearTimeout(toast._t);
  toast._t = setTimeout(() => { toast.className = ''; }, 3000);
}

/* ── Time Ago ───────────────────────────────────────────────── */
function timeAgo(dateStr) {
  const now  = new Date();
  const date = new Date(dateStr);
  const diff = Math.floor((now - date) / 1000);
  if (diff < 60)     return 'just now';
  if (diff < 3600)   return Math.floor(diff / 60) + 'm ago';
  if (diff < 86400)  return Math.floor(diff / 3600) + 'h ago';
  if (diff < 604800) return Math.floor(diff / 86400) + 'd ago';
  return date.toLocaleDateString('en-IN', { day: 'numeric', month: 'short' });
}

/* ── Avatar Helper ──────────────────────────────────────────── */
function avatarHTML(avatar, name, size = 42) {
  if (avatar) {
    return `<img src="${avatar}" alt="${name}" style="width:${size}px;height:${size}px;border-radius:50%;object-fit:cover;background:var(--bg3)"
                 onerror="this.src='https://i.pravatar.cc/${size}?u=${encodeURIComponent(name)}'">`;
  }
  const initials = (name || '?').split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
  const colors   = ['#4f8ef7','#ff6b6b','#3fb950','#e3b341','#a371f7'];
  const color    = colors[name.charCodeAt(0) % colors.length];
  return `<div style="width:${size}px;height:${size}px;border-radius:50%;background:${color};
          display:flex;align-items:center;justify-content:center;font-weight:700;font-size:${size*0.35}px;
          color:white;flex-shrink:0;font-family:'Sora',sans-serif">${initials}</div>`;
}

/* ── Build Post Card ────────────────────────────────────────── */
function buildPostCard(post, currentUserId = null) {
  const isOwner = currentUserId && post.user_id === currentUserId;
  return `
  <div class="post-card" id="post-${post.id}">
    <div class="post-header">
      ${avatarHTML(post.avatar, post.name, 42)}
      <div class="post-meta">
        <div>
          <span class="post-author" onclick="location.href='/profile/${post.username}'">${post.name}</span>
          <span class="post-username"> @${post.username}</span>
        </div>
        <div class="post-time">${timeAgo(post.created_at)}</div>
      </div>
      ${isOwner ? `<button class="btn btn-ghost btn-sm post-delete-btn" onclick="deletePost(${post.id})" title="Delete post">🗑</button>` : ''}
    </div>
    <div class="post-content">${escapeHTML(post.content)}</div>
    ${post.image_url ? `<img src="${post.image_url}" class="post-img" alt="post image" onerror="this.style.display='none'">` : ''}
    <div class="post-actions">
      <button class="action-btn ${post.liked_by_me ? 'liked' : ''}" onclick="toggleLike(${post.id}, this)">
        <span class="icon">${post.liked_by_me ? '❤️' : '🤍'}</span>
        <span class="like-count">${post.like_count}</span>
      </button>
      <button class="action-btn" onclick="toggleComments(${post.id})">
        <span class="icon">💬</span>
        <span class="comment-count">${post.comment_count}</span>
      </button>
      <button class="action-btn" onclick="sharePost(${post.id})">
        <span class="icon">↗️</span>
        Share
      </button>
    </div>
    <div class="comments-section" id="comments-${post.id}">
      <div class="comments-list" id="comments-list-${post.id}">
        <div class="loading" style="padding:1rem"><div class="spinner" style="width:20px;height:20px;border-width:2px"></div></div>
      </div>
      <div class="add-comment-row">
        <input class="comment-input" id="comment-input-${post.id}"
               placeholder="Write a comment…"
               onkeydown="if(event.key==='Enter')submitComment(${post.id})">
        <button class="btn btn-primary btn-sm" onclick="submitComment(${post.id})">Post</button>
      </div>
    </div>
  </div>`;
}

/* ── Escape HTML ────────────────────────────────────────────── */
function escapeHTML(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/\n/g, '<br>');
}

/* ── Toggle Like ────────────────────────────────────────────── */
async function toggleLike(postId, btn) {
  const me = await apiFetch('/api/me');
  if (!me.logged_in) { location.href = '/login'; return; }
  const data = await apiFetch(`/api/posts/${postId}/like`, { method: 'POST' });
  if (data.success) {
    const liked = data.action === 'liked';
    btn.className = `action-btn ${liked ? 'liked' : ''}`;
    btn.innerHTML = `<span class="icon">${liked ? '❤️' : '🤍'}</span><span class="like-count">${data.like_count}</span>`;
  }
}

/* ── Toggle Comments ────────────────────────────────────────── */
async function toggleComments(postId) {
  const section = document.getElementById(`comments-${postId}`);
  if (!section) return;
  if (section.classList.contains('open')) {
    section.classList.remove('open');
    return;
  }
  section.classList.add('open');
  loadComments(postId);
}

/* ── Load Comments ──────────────────────────────────────────── */
async function loadComments(postId) {
  const list = document.getElementById(`comments-list-${postId}`);
  if (!list) return;
  const comments = await apiFetch(`/api/posts/${postId}/comments`);
  const me = await apiFetch('/api/me');
  if (!comments.length) {
    list.innerHTML = '<p style="color:var(--text3);font-size:.82rem;padding:.5rem 0">No comments yet. Be the first!</p>';
    return;
  }
  list.innerHTML = comments.map(c => `
    <div class="comment-item" id="comment-${c.id}">
      ${avatarHTML(c.avatar, c.name, 30)}
      <div class="comment-body">
        <span class="comment-author" onclick="location.href='/profile/${c.username}'">${c.name}</span>
        <div class="comment-text">${escapeHTML(c.content)}</div>
        <div class="comment-time">${timeAgo(c.created_at)}
          ${me.logged_in && me.id === c.user_id
            ? `<button onclick="deleteComment(${c.id})" style="background:none;border:none;color:var(--text3);cursor:pointer;font-size:.72rem;margin-left:.5rem">delete</button>`
            : ''}
        </div>
      </div>
    </div>`).join('');
}

/* ── Submit Comment ─────────────────────────────────────────── */
async function submitComment(postId) {
  const me = await apiFetch('/api/me');
  if (!me.logged_in) { location.href = '/login'; return; }
  const input = document.getElementById(`comment-input-${postId}`);
  const content = input.value.trim();
  if (!content) return;
  const data = await apiFetch(`/api/posts/${postId}/comments`, { method: 'POST', body: { content } });
  if (data.success) {
    input.value = '';
    const list = document.getElementById(`comments-list-${postId}`);
    const newComment = `
      <div class="comment-item" id="comment-${data.id}">
        ${avatarHTML(data.avatar, data.name, 30)}
        <div class="comment-body">
          <span class="comment-author">${data.name}</span>
          <div class="comment-text">${escapeHTML(data.content)}</div>
          <div class="comment-time">just now
            <button onclick="deleteComment(${data.id})" style="background:none;border:none;color:var(--text3);cursor:pointer;font-size:.72rem;margin-left:.5rem">delete</button>
          </div>
        </div>
      </div>`;
    if (list.querySelector('p')) list.innerHTML = '';
    list.insertAdjacentHTML('beforeend', newComment);
    // Update comment count
    const countEl = document.querySelector(`#post-${postId} .comment-count`);
    if (countEl) countEl.textContent = parseInt(countEl.textContent || 0) + 1;
  }
}

/* ── Delete Comment ─────────────────────────────────────────── */
async function deleteComment(cid) {
  const data = await apiFetch(`/api/comments/${cid}`, { method: 'DELETE' });
  if (data.success) {
    document.getElementById(`comment-${cid}`)?.remove();
    showToast('Comment deleted');
  }
}

/* ── Delete Post ────────────────────────────────────────────── */
async function deletePost(pid) {
  if (!confirm('Delete this post?')) return;
  const data = await apiFetch(`/api/posts/${pid}`, { method: 'DELETE' });
  if (data.success) {
    document.getElementById(`post-${pid}`)?.remove();
    showToast('Post deleted');
  } else {
    showToast(data.error || 'Error', 'error');
  }
}

/* ── Share Post ─────────────────────────────────────────────── */
function sharePost(pid) {
  const url = `${window.location.origin}/post/${pid}`;
  if (navigator.clipboard) {
    navigator.clipboard.writeText(url);
    showToast('Link copied to clipboard!');
  }
}

/* ── Follow Toggle ──────────────────────────────────────────── */
async function toggleFollow(username, btn) {
  const me = await apiFetch('/api/me');
  if (!me.logged_in) { location.href = '/login'; return; }
  const data = await apiFetch(`/api/follow/${username}`, { method: 'POST' });
  if (data.success) {
    if (data.action === 'followed') {
      btn.textContent = 'Following';
      btn.classList.add('following');
    } else {
      btn.textContent = 'Follow';
      btn.classList.remove('following');
    }
    // Update follower counts on page if visible
    const fcEl = document.getElementById('followers-count');
    if (fcEl) fcEl.textContent = data.followers_count;
  }
}

/* ── Navbar Search ──────────────────────────────────────────── */
let searchTimer;
function initNavSearch() {
  const input   = document.getElementById('nav-search');
  const results = document.getElementById('search-results');
  if (!input || !results) return;
  input.addEventListener('input', () => {
    clearTimeout(searchTimer);
    const q = input.value.trim();
    if (!q) { results.classList.remove('show'); return; }
    searchTimer = setTimeout(async () => {
      const users = await apiFetch(`/api/users/search?q=${encodeURIComponent(q)}`);
      if (!users.length) { results.classList.remove('show'); return; }
      results.innerHTML = users.map(u => `
        <div class="search-result-item" onclick="location.href='/profile/${u.username}'">
          ${avatarHTML(u.avatar, u.name, 32)}
          <div>
            <div style="font-weight:700;font-size:.85rem;color:var(--text)">${u.name}</div>
            <div style="font-size:.75rem;color:var(--text3)">@${u.username}</div>
          </div>
        </div>`).join('');
      results.classList.add('show');
    }, 300);
  });
  document.addEventListener('click', e => {
    if (!input.contains(e.target)) results.classList.remove('show');
  });
}

/* ── Auth State ─────────────────────────────────────────────── */
async function checkAuth() {
  try {
    const data = await apiFetch('/api/me');
    const loginBtn   = document.getElementById('nav-login-btn');
    const logoutBtn  = document.getElementById('nav-logout-btn');
    const profileBtn = document.getElementById('nav-profile-btn');
    const navAvatar  = document.getElementById('nav-avatar');
    if (data.logged_in) {
      if (loginBtn)   loginBtn.style.display   = 'none';
      if (logoutBtn)  logoutBtn.style.display  = '';
      if (profileBtn) {
        profileBtn.style.display = '';
        profileBtn.href = `/profile/${data.username}`;
      }
      if (navAvatar) {
        navAvatar.style.display = '';
        navAvatar.src = data.avatar || `https://i.pravatar.cc/34?u=${data.username}`;
        navAvatar.onclick = () => location.href = `/profile/${data.username}`;
      }
    } else {
      if (loginBtn)   loginBtn.style.display   = '';
      if (logoutBtn)  logoutBtn.style.display  = 'none';
      if (profileBtn) profileBtn.style.display = 'none';
      if (navAvatar)  navAvatar.style.display  = 'none';
    }
    return data;
  } catch (_) { return { logged_in: false }; }
}

async function logout() {
  await apiFetch('/api/logout', { method: 'POST' });
  window.location.href = '/login';
}

/* ── Highlight Active Nav ───────────────────────────────────── */
function highlightNav() {
  document.querySelectorAll('.sidebar-nav a, .navbar-links a').forEach(a => {
    if (a.pathname && a.pathname === window.location.pathname) a.classList.add('active');
  });
}

/* ── On DOM Ready ───────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  checkAuth();
  highlightNav();
  initNavSearch();
});
