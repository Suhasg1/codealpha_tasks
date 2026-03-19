/**
 * Nature Group – Main JavaScript
 * Shared utilities: API helper, toast, cart count, auth state
 */

/* ── API Helper ─────────────────────────────────────────────── */
async function apiFetch(url, options = {}) {
  const config = {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  };
  if (options.body && typeof options.body === 'object') {
    config.body = JSON.stringify(options.body);
  }
  const res = await fetch(url, config);
  return res.json();
}

/* ── Toast Notification ─────────────────────────────────────── */
function showToast(message, type = 'success') {
  const toast = document.getElementById('toast');
  if (!toast) return;
  toast.textContent = (type === 'success' ? '✓  ' : '⚠  ') + message;
  toast.className = `show ${type}`;
  clearTimeout(toast._timeout);
  toast._timeout = setTimeout(() => { toast.className = ''; }, 3200);
}

/* ── Cart Count Refresh ─────────────────────────────────────── */
async function updateCartCount() {
  try {
    const data = await apiFetch('/api/cart/count');
    const badge = document.getElementById('cart-count');
    if (badge) badge.textContent = data.count || 0;
  } catch (_) {}
}

/* ── Auth State ─────────────────────────────────────────────── */
async function checkAuth() {
  try {
    const data = await apiFetch('/api/me');
    const userName   = document.getElementById('nav-user-name');
    const loginBtn   = document.getElementById('nav-login-btn');
    const logoutBtn  = document.getElementById('nav-logout-btn');
    const ordersLink = document.getElementById('nav-orders-link');

    if (data.logged_in) {
      if (userName)   userName.textContent = '👤 ' + data.name.split(' ')[0];
      if (loginBtn)   loginBtn.style.display = 'none';
      if (logoutBtn)  logoutBtn.style.display = '';
      if (ordersLink) ordersLink.style.display = '';
    } else {
      if (loginBtn)   loginBtn.style.display = '';
      if (logoutBtn)  logoutBtn.style.display = 'none';
      if (ordersLink) ordersLink.style.display = 'none';
    }
  } catch (_) {}
}

/* ── Logout ─────────────────────────────────────────────────── */
async function logout() {
  await apiFetch('/api/logout', { method: 'POST' });
  window.location.href = '/';
}

/* ── Product Card HTML ──────────────────────────────────────── */
function buildProductCard(product) {
  const save  = product.original_price
    ? Math.round((1 - product.price / product.original_price) * 100)
    : 0;
  const stars = '★'.repeat(Math.round(product.rating)) +
                '☆'.repeat(5 - Math.round(product.rating));

  const imgContent = product.image_url
    ? `<img src="${product.image_url}" alt="${product.name}"
            style="width:100%;height:100%;object-fit:cover;border-radius:0;"
            onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">`
    : '';
  const emojiFallback = `<span style="font-size:4rem;display:${product.image_url ? 'none' : 'flex'};align-items:center;justify-content:center;width:100%;height:100%">${product.emoji}</span>`;

  return `
    <div class="product-card" onclick="location.href='/product/${product.id}'">
      <div class="product-card-img" style="padding:0;overflow:hidden;">
        ${product.badge
          ? `<span class="product-card-badge ${product.badge === 'Best Seller' ? 'gold' : ''}">${product.badge}</span>`
          : ''}
        ${imgContent}${emojiFallback}
      </div>
      <div class="product-card-body">
        <div class="product-card-cat">${product.category}</div>
        <div class="product-card-name">${product.name}</div>
        <div>
          <span class="product-card-stars">${stars}</span>
          <span class="product-card-reviews">(${product.reviews})</span>
        </div>
        <div class="product-card-price-row">
          <span class="price-now">₹${product.price}</span>
          ${product.original_price ? `<span class="price-old">₹${product.original_price}</span>` : ''}
          ${save > 0 ? `<span class="price-save">${save}% off</span>` : ''}
        </div>
        <div class="product-card-footer">
          <span class="product-card-weight">${product.weight}</span>
          <button class="btn btn-primary btn-sm"
            onclick="event.stopPropagation(); addToCart(${product.id})">
            Add +
          </button>
        </div>
      </div>
    </div>`;
}

/* ── Add to Cart (shared) ───────────────────────────────────── */
async function addToCart(productId, quantity = 1) {
  const data = await apiFetch('/api/cart', {
    method: 'POST',
    body: { product_id: productId, quantity },
  });

  if (data.error && data.redirect) {
    window.location.href = data.redirect;
    return false;
  }

  if (data.success) {
    showToast('Added to cart!');
    updateCartCount();
    return true;
  }

  showToast(data.error || 'Something went wrong', 'error');
  return false;
}

/* ── Highlight Active Nav Link ──────────────────────────────── */
function highlightNav() {
  document.querySelectorAll('.navbar-links a').forEach(link => {
    if (link.pathname === window.location.pathname) {
      link.classList.add('active');
    }
  });
}

/* ── On DOM Ready ───────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  checkAuth();
  updateCartCount();
  highlightNav();
});
