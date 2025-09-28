// Theme management
const THEME_KEY = "peerprep_theme";

function applyThemeFromStorage() {
    let theme = localStorage.getItem(THEME_KEY);
    
    // Set default theme to dark if not set
    if (!theme) {
        theme = "dark";
        localStorage.setItem(THEME_KEY, theme);
    }

    if (theme === "light") {
        document.body.classList.add("light-mode");
        setLightModeIcon(true);
    } else {
        document.body.classList.remove("light-mode");
        setLightModeIcon(false);
    }
}

function setLightModeIcon(isLight) {
    const icon = document.getElementById("modeToggle")?.querySelector("i");
    if (!icon) return;
    
    if (isLight) {
        icon.classList.remove("fa-moon");
        icon.classList.add("fa-sun");
        icon.title = "Switch to Dark Mode";
    } else {
        icon.classList.remove("fa-sun");
        icon.classList.add("fa-moon");
        icon.title = "Switch to Light Mode";
    }
}

function toggleMode() {
    const isNowLight = !document.body.classList.contains("light-mode");
    
    if (isNowLight) {
        document.body.classList.add("light-mode");
    } else {
        document.body.classList.remove("light-mode");
    }
    
    setLightModeIcon(isNowLight);
    localStorage.setItem(THEME_KEY, isNowLight ? "light" : "dark");
}

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Form submission with Django backend
document.querySelector('.contact-form')?.addEventListener('submit', function(e) {
    e.preventDefault();

    const submitBtn = document.querySelector('.submit-btn');
    const originalText = submitBtn.textContent;
    const formData = new FormData(this);

    submitBtn.textContent = 'Sending...';
    submitBtn.disabled = true;

    fetch('/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            submitBtn.textContent = 'Message Sent! ✓';
            submitBtn.style.background = 'linear-gradient(135deg, #10b981, #059669)';

            // Show success message
            showNotification('Thank you! Your message has been sent successfully!', 'success');

            setTimeout(() => {
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                submitBtn.style.background = 'linear-gradient(135deg, #3b82f6, #1d4ed8)';
                this.reset();
            }, 2000);
        } else {
            submitBtn.textContent = 'Try Again';
            submitBtn.disabled = false;
            showNotification('Please check your form and try again.', 'error');

            setTimeout(() => {
                submitBtn.textContent = originalText;
            }, 2000);
        }
    })
    .catch(error => {
        submitBtn.textContent = 'Try Again';
        submitBtn.disabled = false;
        showNotification('Something went wrong. Please try again.', 'error');

        setTimeout(() => {
            submitBtn.textContent = originalText;
        }, 2000);
    });
});

// Notification system
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('show');
    }, 100);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 4000);
}

// Add scroll effect to navbar
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.background = 'rgba(15, 23, 42, 0.95)';
    } else {
        navbar.style.background = 'rgba(15, 23, 42, 0.85)';
    }
});

// Add floating animation to input focus
document.querySelectorAll('.form-input').forEach(input => {
    input.addEventListener('focus', function() {
        this.parentElement.style.transform = 'translateY(-2px)';
    });
    
    input.addEventListener('blur', function() {
        this.parentElement.style.transform = 'translateY(0)';
    });
});

// Login form handling
document.querySelector('.login-form')?.addEventListener('submit', function(e) {
    e.preventDefault();

    const submitBtn = this.querySelector('.submit-btn');
    const originalText = submitBtn.textContent;
    const formData = new FormData(this);

    submitBtn.textContent = 'Signing In...';
    submitBtn.disabled = true;

    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            submitBtn.textContent = 'Success! ✓';
            submitBtn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
            showNotification('Login successful!', 'success');

            window.location.href = data.redirect_url || '/dashboard/';
        } else {
            submitBtn.textContent = 'Try Again';
            submitBtn.disabled = false;
            showNotification(data.message || 'Please check your credentials and try again.', 'error');

            setTimeout(() => {
                submitBtn.textContent = originalText;
            }, 2000);
        }
    })
    .catch(error => {
        submitBtn.textContent = 'Try Again';
        submitBtn.disabled = false;
        showNotification('Something went wrong. Please try again.', 'error');

        setTimeout(() => {
            submitBtn.textContent = originalText;
        }, 2000);
    });
});

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', function() {
    applyThemeFromStorage();
});
// Enhanced theme management with session storage fallback
function getStoredTheme() {
    // Try localStorage first, then sessionStorage, then default to dark
    return localStorage.getItem(THEME_KEY) || 
           sessionStorage.getItem(THEME_KEY) || 
           'dark';
}

function setStoredTheme(theme) {
    // Store in both localStorage and sessionStorage for redundancy
    localStorage.setItem(THEME_KEY, theme);
    sessionStorage.setItem(THEME_KEY, theme);
}

function applyThemeFromStorage() {
    const theme = getStoredTheme();
    
    if (theme === "light") {
        document.body.classList.add("light-mode");
        setLightModeIcon(true);
    } else {
        document.body.classList.remove("light-mode");
        setLightModeIcon(false);
    }
}

function toggleMode() {
    const isNowLight = !document.body.classList.contains("light-mode");
    const newTheme = isNowLight ? "light" : "dark";
    
    if (isNowLight) {
        document.body.classList.add("light-mode");
    } else {
        document.body.classList.remove("light-mode");
    }
    
    setLightModeIcon(isNowLight);
    setStoredTheme(newTheme);
    
    // Sync with server session
    syncThemeWithServer(newTheme);
}

function syncThemeWithServer(theme) {
    // Optional: Sync theme preference with server
    fetch('/api/toggle-theme/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({theme: theme})
    }).catch(error => {
        console.log('Theme sync failed, but local storage will persist');
    });
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}