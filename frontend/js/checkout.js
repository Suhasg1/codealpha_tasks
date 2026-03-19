/**
 * Nature Group – Checkout Page JS
 */

let checkoutItems = [];

document.addEventListener('DOMContentLoaded', initCheckout);

async function initCheckout() {
  const me = await apiFetch('/api/me');
  if (!me.logged_in) { window.location.href = '/login'; return; }

  checkoutItems = await apiFetch('/api/cart');
  if (!checkoutItems.length) { window.location.href = '/cart'; return; }

  renderCheckout(me);
}

function renderCheckout(me) {
  const subtotal = checkoutItems.reduce((s, i) => s + i.price * i.quantity, 0);
  const shipping = subtotal >= 500 ? 0 : 49;
  const total    = subtotal + shipping;

  // Fill user name
  const nameInput = document.getElementById('d-name');
  if (nameInput) nameInput.value = me.name;

  // Render order summary sidebar
  const summaryEl = document.getElementById('order-summary-items');
  if (summaryEl) {
    summaryEl.innerHTML = checkoutItems.map(i => `
      <div class="checkout-item">
        <span class="checkout-item-emoji">${i.emoji}</span>
        <div class="checkout-item-info">
          <span class="checkout-item-name">${i.name}</span>
          <span class="checkout-item-qty">× ${i.quantity}  ·  ${i.weight}</span>
        </div>
        <span class="checkout-item-price">₹${(i.price * i.quantity).toFixed(0)}</span>
      </div>`).join('');
  }

  const subtotalEl = document.getElementById('summary-subtotal');
  const shippingEl = document.getElementById('summary-shipping');
  const totalEl    = document.getElementById('summary-total');
  const placeBtn   = document.getElementById('place-order-btn');

  if (subtotalEl) subtotalEl.textContent = `₹${subtotal.toFixed(0)}`;
  if (shippingEl) shippingEl.innerHTML   = shipping === 0 ? '<span style="color:var(--sage)">FREE</span>' : `₹${shipping}`;
  if (totalEl)    totalEl.textContent    = `₹${total.toFixed(0)}`;
  if (placeBtn)   placeBtn.textContent   = `🛒 Place Order — ₹${total.toFixed(0)}`;
}

async function placeOrder() {
  const fields = {
    name:  document.getElementById('d-name')?.value.trim(),
    phone: document.getElementById('d-phone')?.value.trim(),
    addr1: document.getElementById('d-addr1')?.value.trim(),
    city:  document.getElementById('d-city')?.value.trim(),
    state: document.getElementById('d-state')?.value.trim(),
    pin:   document.getElementById('d-pin')?.value.trim(),
  };

  if (Object.values(fields).some(v => !v)) {
    showToast('Please fill in all required fields', 'error');
    return;
  }

  const addr2   = document.getElementById('d-addr2')?.value.trim() || '';
  const payment = document.querySelector('input[name="payment"]:checked')?.value || 'cod';
  const address = `${fields.name}, ${fields.addr1}${addr2 ? ', ' + addr2 : ''}, ${fields.city}, ${fields.state} – ${fields.pin} | Phone: ${fields.phone}`;

  const btn = document.getElementById('place-order-btn');
  if (btn) { btn.textContent = 'Placing order…'; btn.disabled = true; }

  const data = await apiFetch('/api/orders', {
    method: 'POST',
    body:   { address, payment },
  });

  if (data.success) {
    updateCartCount();
    document.getElementById('checkout-wrapper').innerHTML = `
      <div style="max-width:600px;margin:3rem auto;padding:0 2rem">
        <div class="empty-state" style="padding:3rem">
          <div class="big-emoji">🎉</div>
          <h2>Order Placed!</h2>
          <p>Thank you for shopping with Nature Group.</p>
          <div class="order-id-tag">Order #${data.order_id}</div>
          <p style="margin:.75rem 0 1.5rem;color:var(--muted)">Total paid: <strong>₹${data.total.toFixed(0)}</strong></p>
          <a href="/orders" class="btn btn-primary btn-lg" style="margin-right:.75rem">View My Orders</a>
          <a href="/products" class="btn btn-outline btn-lg">Continue Shopping</a>
        </div>
      </div>`;
  } else {
    showToast(data.error || 'Order failed. Please try again.', 'error');
    if (btn) { btn.textContent = '🛒 Place Order'; btn.disabled = false; }
  }
}
