// -------------------------------
// Smooth Scrolling for Anchor Links
// -------------------------------
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: "smooth", block: "start" });
        }
    });
});


// -------------------------------
// Contact Form AJAX Submit (Only if form exists)
// -------------------------------
const contactForm = document.querySelector(".contact-form");

if (contactForm) {
    contactForm.addEventListener("submit", function (e) {
        e.preventDefault();

        const submitBtn = contactForm.querySelector(".submit-btn");
        const originalText = submitBtn.textContent;
        const formData = new FormData(contactForm);

        submitBtn.textContent = "Sending...";
        submitBtn.disabled = true;

        fetch("/", {
            method: "POST",
            headers: { "X-Requested-With": "XMLHttpRequest" },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification("Message sent successfully!", "success");
                submitBtn.textContent = "Sent ✓";

                setTimeout(() => {
                    submitBtn.textContent = originalText;
                    submitBtn.disabled = false;
                    contactForm.reset();
                }, 1500);
            } else {
                showNotification("Please check your inputs and try again.", "error");
                submitBtn.textContent = "Try Again";

                setTimeout(() => {
                    submitBtn.textContent = originalText;
                }, 1500);
            }
        })
        .catch(() => {
            showNotification("Something went wrong. Please try again later.", "error");
            submitBtn.textContent = "Try Again";
            submitBtn.disabled = false;
        });
    });
}


// -------------------------------
// Notification System
// -------------------------------
function showNotification(message, type = "success") {
    const notification = document.createElement("div");
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    document.body.appendChild(notification);

    setTimeout(() => notification.classList.add("show"), 50);

    setTimeout(() => {
        notification.classList.remove("show");
        setTimeout(() => notification.remove(), 300);
    }, 3500);
}


// -------------------------------
// Navbar Scroll Darkening
// -------------------------------
const navbar = document.querySelector(".navbar");

if (navbar) {
    window.addEventListener("scroll", () => {
        if (window.scrollY > 50) {
            navbar.style.background = "rgba(15, 23, 42, 0.95)";
        } else {
            navbar.style.background = "rgba(15, 23, 42, 0.85)";
        }
    });
}


// -------------------------------
// Input Floating Animation
// -------------------------------
document.querySelectorAll(".form-input").forEach(input => {
    const parent = input.parentElement;
    
    input.addEventListener("focus", () => {
        parent.style.transform = "translateY(-2px)";
    });

    input.addEventListener("blur", () => {
        parent.style.transform = "translateY(0)";
    });
});


// -------------------------------
// Success Stories Modal Logic
// -------------------------------
document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("storyModal");
    const btn = document.getElementById("addStoryBtn");
    const closeBtn = document.querySelector(".modal .close");
    const form = document.getElementById("storyForm");
    const storiesContainer = document.getElementById("storiesContainer");

    if (btn) btn.addEventListener("click", () => modal.style.display = "block");
    if (closeBtn) closeBtn.addEventListener("click", () => modal.style.display = "none");

    window.addEventListener("click", e => {
        if (e.target === modal) modal.style.display = "none";
    });

    if (form) {
        form.addEventListener("submit", e => {
            e.preventDefault();

            fetch(form.action, {
                method: "POST",
                headers: { "X-Requested-With": "XMLHttpRequest" },
                body: new FormData(form)
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    modal.style.display = "none";
                    form.reset();

                    const story = document.createElement("div");
                    story.className = "feature-card";
                    story.innerHTML = `
                        <div class="feature-icon">🏆</div>
                        <h3>${data.title}</h3>
                        <p>${data.story}</p>
                        <small>By ${data.user}</small>
                    `;

                    if (storiesContainer) storiesContainer.prepend(story);
                } else {
                    alert("Error: " + JSON.stringify(data.errors));
                }
            })
            .catch(console.error);
        });
    }
});


// -------------------------------
// Theme Toggle (Light / Dark)
// -------------------------------
const THEME_KEY = "theme";

function applyThemeFromStorage() {
    const theme = localStorage.getItem(THEME_KEY) || "dark";
    document.body.classList.toggle("light-mode", theme === "light");
    document.body.classList.toggle("dark-mode", theme !== "light");
    updateThemeIcon(theme === "light");
}

function updateThemeIcon(isLight) {
    const toggle = document.getElementById("modeToggle");
    if (!toggle) return;

    const icon = toggle.querySelector("i");
    if (!icon) return;

    icon.classList.toggle("fa-sun", !isLight);
    icon.classList.toggle("fa-moon", isLight);
}

function toggleMode() {
    const isLight = document.body.classList.contains("dark-mode");
    localStorage.setItem(THEME_KEY, isLight ? "light" : "dark");
    applyThemeFromStorage();
}

document.addEventListener("DOMContentLoaded", applyThemeFromStorage);
