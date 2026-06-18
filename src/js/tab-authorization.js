// tab-authorization.js

// Initialize the authorization page when DOM loads
document.addEventListener('DOMContentLoaded', () => {
  const labTab = document.querySelector('[data-tab="lab-workspace"]');
  const authPage = document.getElementById('auth-page');
  const authForm = document.getElementById('auth-form');
  const statusAmber = document.querySelector('.status-pill.status-amber');
  const statusPrimary = document.querySelector('.status-pill.status-primary');

  // Initialize form validation
  authForm.addEventListener('submit', (e) => {
    e.preventDefault();

    // CSRF protection
    const csrfToken = document.querySelector('meta[name="csrf-token"]')?.content;
    if (!csrfToken) {
      alert('CSRF protection required. Please configure your server to include CSRF tokens');
      return;
    }

    // Password complexity check
    const password = document.getElementById('password').value;
    if (password.length < 12 || !/[A-Z]/.test(password)) {
      alert('Password must be 12+ characters with uppercase letters');
      return;
    }

    // Automated access detection
    if (window.navigator.webdriver) {
      alert('Automated access detected. Please sign in manually');
      return;
    }

    // Update UI for authentication process
    statusAmber.style.display = 'flex';
    statusPrimary.style.display = 'none';
    authForm.style.opacity = 0.5;

    // Simulate API call (in production, replace with actual auth endpoint)
    setTimeout(() => {
      const success = Math.random() > 0.3;

      if (success) {
        statusAmber.style.display = 'none';
        statusPrimary.style.display = 'flex';
        authForm.style.opacity = 1;

        // Redirect to workspace after brief delay
        setTimeout(() => {
          window.location.href = '/lab-workspace';
        }, 1000);
      } else {
        alert('Authentication failed. Please check your credentials');
        statusAmber.style.display = 'none';
        statusPrimary.style.display = 'flex';
      }
    }, 1500);
  });

  // Handle tab click
  if (labTab) {
    labTab.addEventListener('click', (e) => {
      e.preventDefault();
      authPage.style.display = 'block';

      // Clear any previous form state
      authForm.reset();
      statusAmber.style.display = 'flex';
      statusPrimary.style.display = 'none';
      authForm.style.opacity = 1;

      // Set focus on email field
      document.getElementById('email').focus();
    });
  }
});