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
document.querySelector('.contact-form').addEventListener('submit', function(e) {
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
// Adding success stories

document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("storyModal");
    const btn = document.getElementById("addStoryBtn");
    const span = document.querySelector(".modal .close");
    const form = document.getElementById("storyForm");
    const storiesContainer = document.getElementById("storiesContainer");

    // Open modal
    btn?.addEventListener("click", () => modal.style.display = "block");

    // Close modal
    span?.addEventListener("click", () => modal.style.display = "none");
    window.addEventListener("click", e => {
        if (e.target == modal) modal.style.display = "none";
    });

    // AJAX form submission
    form?.addEventListener("submit", function (e) {
        e.preventDefault();
        const url = form.action;
        const formData = new FormData(form);

        fetch(url, {
            method: "POST",
            headers: { "X-Requested-With": "XMLHttpRequest" },
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Close modal
                modal.style.display = "none";
                form.reset();

                // Append new story
                const newStory = document.createElement("div");
                newStory.classList.add("feature-card");
                newStory.innerHTML = `
                    <div class="feature-icon">🏆</div>
                    <h3 class="feature-title">${data.title}</h3>
                    <p class="feature-description">${data.story}</p>
                    <small>By ${data.user}</small>
                `;
                storiesContainer.prepend(newStory);
            } else {
                alert("Error: " + JSON.stringify(data.errors));
            }
        })
        .catch(err => console.error(err));
    });
});
