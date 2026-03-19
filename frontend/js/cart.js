/**
 * Nature Group – Cart Page JS
 */

let cartItems = [];

document.addEventListener('DOMContentLoaded', loadCart);

async function loadCart() {
  const wrapper = document.getElementById('cart-wrapper');
  const me = await apiFetch('/api/me');

  if (!me.logged_in) {
    wrapper.innerHTML = `
      <div style="max-width:500px;margin:3rem auto;padding:0 2rem">
        <div class="empty-state">
          <div class="big-emoji">🔒</div>
          <h2>Login to View Cart</h2>
          <p>Please sign in to access your shopping cart.</p>
          <a href="/login" class="btn btn-primary btn-lg" style="margin-right:.75rem">Login</a>
          <a href="/register" class="btn btn-outline btn-lg">Register</a>
        </div>
      </div>`;
    return;
  }

  cartItems = await apiFetch('/api/cart');
  renderCart();
}

function renderCart() {
  const wrapper = document.getElementById('cart-wrapper');

  if (!cartItems.length) {
    wrapper.innerHTML = `
      <div style="max-width:500px;margin:3rem auto;padding:0 2rem">
        <div class="empty-state">
          <div class="big-emoji">🛒</div>
          <h2>Your Cart is Empty</h2>
          <p>You haven't added any products yet.</p>
          <a href="/products" class="btn btn-primary btn-lg">Start Shopping</a>
        </div>
      </div>`;
    return;
  }

  const subtotal = cartItems.reduce((sum, i) => sum + i.price * i.quantity, 0);
  const shipping = subtotal >= 500 ? 0 : 49;
  const total    = subtotal + shipping;

  wrapper.innerHTML = `
    <div class="cart-layout">
      <div>
        <div class="cart-items" id="cart-items">
          ${cartItems.map(cartItemHTML).join('')}
        </div>
      </div>
      <aside class="cart-summary card">
        <h3>Order Summary</h3>
        <div class="summary-row">
          <span>Subtotal (${cartItems.length} item${cartItems.length > 1 ? 's' : ''})</span>
          <span>₹${subtotal.toFixed(0)}</span>
        </div>
        <div class="summary-row">
          <span>Shipping</span>
          <span>${shipping === 0 ? '<span style="color:var(--sage)">FREE</span>' : '₹' + shipping}</span>
        </div>
        ${subtotal < 500
          ? `<p class="free-ship-note">🚚 Add ₹${(500 - subtotal).toFixed(0)} more for free shipping!</p>`
          : `<p class="free-ship-note success">🎉 You qualify for FREE shipping!</p>`}
        <div class="summary-row total">
          <span>Total</span>
          <span>₹${total.toFixed(0)}</span>
        </div>
        <a href="/checkout" class="btn btn-gold btn-lg btn-full" style="margin-top:1.25rem">
          Proceed to Checkout →
        </a>
        <a href="/products" class="btn btn-secondary btn-full" style="margin-top:.75rem">
          Continue Shopping
        </a>
      </aside>
    </div>`;
}

function cartItemHTML(item) {
  return `
    <div class="cart-item" id="cart-item-${item.id}">
      <div class="cart-item-img" style="padding:0;overflow:hidden;background:var(--cream);">
        ${item.image_url
          ? `<img src="${item.image_url}" alt="${item.name}" style="width:100%;height:100%;object-fit:cover;"
                  onerror="this.style.display='none';this.nextElementSibling.style.display='flex'">`
          : ''}
        <span style="font-size:2.5rem;display:${item.image_url ? 'none' : 'flex'};align-items:center;justify-content:center;width:100%;height:100%">${item.emoji}</span>
      </div>
      <div class="cart-item-info">
        <div class="cart-item-cat">${item.category}</div>
        <div class="cart-item-name">${item.name}</div>
        <div class="cart-item-weight">${item.weight}</div>
      </div>
      <div class="cart-item-controls">
        <div class="qty-control">
          <button class="qty-btn" onclick="changeQty(${item.id}, ${item.quantity - 1})">−</button>
          <span class="qty-val">${item.quantity}</span>
          <button class="qty-btn" onclick="changeQty(${item.id}, ${item.quantity + 1})">+</button>
        </div>
        <span class="cart-item-price">₹${(item.price * item.quantity).toFixed(0)}</span>
        <button class="remove-btn" onclick="removeItem(${item.id})" title="Remove">🗑</button>
      </div>
    </div>`;
}

async function changeQty(cartId, newQty) {
  await apiFetch(`/api/cart/${cartId}`, { method: 'PUT', body: { quantity: newQty } });
  cartItems = await apiFetch('/api/cart');
  renderCart();
  updateCartCount();
}

async function removeItem(cartId) {
  await apiFetch(`/api/cart/${cartId}`, { method: 'DELETE' });
  cartItems = cartItems.filter(i => i.id !== cartId);
  renderCart();
  updateCartCount();
  showToast('Item removed from cart');
}
