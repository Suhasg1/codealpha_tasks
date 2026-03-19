/**
 * Nature Group – Products Page JS
 * Handles filtering, searching, sorting and rendering product grid
 */

let currentCategory = new URLSearchParams(window.location.search).get('category') || 'All';
let priceMin = 0;
let priceMax = 9999;
let searchTimer = null;

/* ── Init ──────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  // Pre-select category from URL param
  if (currentCategory !== 'All') {
    document.querySelectorAll('.filter-btn').forEach(btn => {
      btn.classList.toggle('active', btn.dataset.cat === currentCategory);
    });
    const titleEl = document.getElementById('cat-title');
    if (titleEl) titleEl.textContent = currentCategory;
  }
  loadProducts();
});

/* ── Category Filter ───────────────────────────────────────── */
function setCategory(cat, btn) {
  currentCategory = cat;
  document.querySelectorAll('.filter-btn[data-cat]').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  const titleEl = document.getElementById('cat-title');
  if (titleEl) titleEl.textContent = cat === 'All' ? 'All Products' : cat;
  loadProducts();
}

/* ── Price Filter ──────────────────────────────────────────── */
function setPriceFilter(min, max, btn) {
  priceMin = min;
  priceMax = max;
  document.querySelectorAll('.filter-btn[data-price]').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  loadProducts();
}

/* ── Debounced Search ───────────────────────────────────────── */
function onSearchInput() {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(loadProducts, 320);
}

/* ── Load + Render Products ─────────────────────────────────── */
async function loadProducts() {
  const grid    = document.getElementById('products-grid');
  const countEl = document.getElementById('result-count');
  const search  = (document.getElementById('search-input')?.value || '').trim();
  const sort    = document.getElementById('sort-select')?.value || 'name';

  if (grid) grid.innerHTML = '<div class="loading" style="grid-column:1/-1"><div class="spinner"></div></div>';

  let url = `/api/products?sort=${sort}`;
  if (currentCategory !== 'All') url += `&category=${encodeURIComponent(currentCategory)}`;
  if (search)                     url += `&search=${encodeURIComponent(search)}`;

  const products = await apiFetch(url);
  const filtered = products.filter(p => p.price >= priceMin && p.price <= priceMax);

  if (countEl) countEl.textContent = `${filtered.length} product${filtered.length !== 1 ? 's' : ''} found`;

  if (!grid) return;
  if (!filtered.length) {
    grid.innerHTML = `
      <div style="grid-column:1/-1; text-align:center; padding:3rem; color:var(--muted)">
        <div style="font-size:3rem;margin-bottom:1rem">🔍</div>
        <p>No products found. Try a different search or filter.</p>
      </div>`;
    return;
  }

  grid.innerHTML = filtered.map(p => buildProductCard(p)).join('');
}
