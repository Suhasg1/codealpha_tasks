/**
 * ConnectSphere — Theme Manager
 * - Auto-detects device theme (light/dark)
 * - Toggle button to override manually
 * - Saves preference to localStorage
 */

(function () {
  const STORAGE_KEY = 'cs-theme';

  function getTheme() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) return saved;
    return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem(STORAGE_KEY, theme);
    document.querySelectorAll('.theme-toggle').forEach(btn => {
      btn.textContent = theme === 'dark' ? '☀️' : '🌙';
      btn.title = theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
    });
  }

  window.toggleTheme = function () {
    const current = document.documentElement.getAttribute('data-theme') || getTheme();
    applyTheme(current === 'dark' ? 'light' : 'dark');
  };

  // Apply immediately on load — prevents flash
  applyTheme(getTheme());

  // Auto-update if device theme changes (only if user hasn't manually toggled)
  window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', (e) => {
    if (!localStorage.getItem(STORAGE_KEY)) {
      applyTheme(e.matches ? 'light' : 'dark');
    }
  });
})();
