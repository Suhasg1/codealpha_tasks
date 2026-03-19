/**
 * Nature Group – Auth JS (Login + Register)
 */

/* ── LOGIN ─────────────────────────────────────────────────── */
async function doLogin() {
  const email    = document.getElementById('email')?.value.trim();
  const password = document.getElementById('password')?.value;
  const errEl    = document.getElementById('error-msg');
  const btn      = document.getElementById('auth-submit');

  if (errEl) errEl.style.display = 'none';

  if (!email || !password) {
    if (errEl) { errEl.textContent = 'Please enter your email and password.'; errEl.style.display = 'block'; }
    return;
  }

  if (btn) { btn.textContent = 'Signing in…'; btn.disabled = true; }

  const data = await apiFetch('/api/login', {
    method: 'POST',
    body:   { email, password },
  });

  if (data.success) {
    showToast(`Welcome back, ${data.name}! 🌿`);
    setTimeout(() => { window.location.href = '/'; }, 1000);
  } else {
    if (errEl) { errEl.textContent = data.error || 'Login failed.'; errEl.style.display = 'block'; }
    if (btn)   { btn.textContent = 'Sign In →'; btn.disabled = false; }
  }
}

/* ── REGISTER ──────────────────────────────────────────────── */
async function doRegister() {
  const name     = document.getElementById('name')?.value.trim();
  const email    = document.getElementById('email')?.value.trim();
  const password = document.getElementById('password')?.value;
  const errEl    = document.getElementById('error-msg');
  const btn      = document.getElementById('auth-submit');

  if (errEl) errEl.style.display = 'none';

  if (!name || !email || !password) {
    if (errEl) { errEl.textContent = 'All fields are required.'; errEl.style.display = 'block'; }
    return;
  }
  if (password.length < 6) {
    if (errEl) { errEl.textContent = 'Password must be at least 6 characters.'; errEl.style.display = 'block'; }
    return;
  }

  if (btn) { btn.textContent = 'Creating account…'; btn.disabled = true; }

  const data = await apiFetch('/api/register', {
    method: 'POST',
    body:   { name, email, password },
  });

  if (data.success) {
    showToast(`Welcome to Nature Group, ${data.name}! 🌿`);
    setTimeout(() => { window.location.href = '/'; }, 1200);
  } else {
    if (errEl) { errEl.textContent = data.error || 'Registration failed.'; errEl.style.display = 'block'; }
    if (btn)   { btn.textContent = 'Create Account →'; btn.disabled = false; }
  }
}

/* ── Enter key support ─────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('input').forEach(input => {
    input.addEventListener('keydown', e => {
      if (e.key === 'Enter') {
        const fn = document.getElementById('auth-submit')?.dataset.fn;
        if (fn === 'login')    doLogin();
        if (fn === 'register') doRegister();
      }
    });
  });
});
