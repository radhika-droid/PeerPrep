// Create this file: core/static/js/study_partners.js

// Study Partners functionality
var selectedPartnership = null;

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeStudyPartners();
});

function initializeStudyPartners() {
    // Initialize schedule form if it exists
    var scheduleForm = document.getElementById('scheduleForm');
    if (scheduleForm) {
        scheduleForm.addEventListener('submit', handleScheduleFormSubmit);
    }
    
    // Set up modal close handlers
    window.onclick = function(event) {
        var scheduleModal = document.getElementById('scheduleModal');
        if (event.target === scheduleModal) {
            closeScheduleModal();
        }
        
        var sessionsModal = document.getElementById('sessionsModal');
        if (event.target === sessionsModal) {
            closeSessionsModal();
        }
    };
}

// Open schedule modal
function openScheduleModal(partnershipId, partnerName) {
    selectedPartnership = partnershipId;
    
    // Set minimum date to current date/time
    var now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    var minDateTime = now.toISOString().slice(0, 16);
    var timeInput = document.querySelector('input[name="scheduled_time"]');
    if (timeInput) {
        timeInput.min = minDateTime;
    }
    
    // Update partner info
    var partnerInfo = document.getElementById('partnerInfo');
    if (partnerInfo) {
        partnerInfo.innerHTML = createPartnerInfoHTML(partnerName);
    }
    
    // Clear form
    var form = document.getElementById('scheduleForm');
    if (form) {
        form.reset();
    }
    
    // Show modal
    var modal = document.getElementById('scheduleModal');
    if (modal) {
        modal.style.display = 'block';
    }
}

// Create partner info HTML
function createPartnerInfoHTML(partnerName) {
    var div = document.createElement('div');
    div.style.cssText = 'display: flex; align-items: center; padding: 1rem; background: rgba(0,0,0,0.2); border-radius: 8px;';
    
    var innerDiv = document.createElement('div');
    innerDiv.style.cssText = 'color: white; font-weight: 600;';
    
    var icon = document.createElement('i');
    icon.className = 'fas fa-calendar-plus';
    icon.style.cssText = 'color: #3b82f6; margin-right: 0.5rem;';
    
    innerDiv.appendChild(icon);
    innerDiv.appendChild(document.createTextNode('Scheduling session with ' + partnerName));
    div.appendChild(innerDiv);
    
    return div.outerHTML;
}

// Close schedule modal
function closeScheduleModal() {
    var modal = document.getElementById('scheduleModal');
    if (modal) {
        modal.style.display = 'none';
    }
    selectedPartnership = null;
}

// Handle schedule form submission
function handleScheduleFormSubmit(e) {
    e.preventDefault();
    
    if (!selectedPartnership) return;
    
    var form = e.target;
    var formData = new FormData(form);
    var submitBtn = form.querySelector('button[type="submit"]');
    var originalText = submitBtn.innerHTML;
    
    // Validate scheduled time
    var scheduledTime = new Date(formData.get('scheduled_time'));
    var now = new Date();
    
    if (scheduledTime <= now) {
        showNotification('Please select a future date and time', 'error');
        return;
    }
    
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin" style="margin-right: 0.5rem;"></i>Scheduling...';
    submitBtn.disabled = true;
    
    var sessionData = {
        partnership_id: selectedPartnership,
        title: formData.get('title'),
        subject: formData.get('subject'),
        scheduled_time: formData.get('scheduled_time'),
        duration_hours: formData.get('duration_hours'),
        description: formData.get('description')
    };
    
    fetch('/api/schedule-session/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(sessionData)
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        if (data.success) {
            showNotification('Study session scheduled successfully!', 'success');
            closeScheduleModal();
            setTimeout(function() {
                window.location.reload();
            }, 1000);
        } else {
            var errorMsg = 'Error scheduling session';
            if (data.errors) {
                errorMsg += ': ' + JSON.stringify(data.errors);
            }
            showNotification(errorMsg, 'error');
        }
    })
    .catch(function(error) {
        console.error('Error:', error);
        showNotification('Failed to schedule session', 'error');
    })
    .finally(function() {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    });
}

// View partnership sessions
function viewPartnershipSessions(partnershipId) {
    fetch('/api/partnership-sessions/' + partnershipId + '/')
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        if (data.success) {
            showSessionsModal(data.sessions);
        } else {
            showNotification('Error loading sessions: ' + data.error, 'error');
        }
    })
    .catch(function(error) {
        console.error('Error:', error);
        showNotification('Failed to load sessions', 'error');
    });
}

// Show sessions modal
function showSessionsModal(sessions) {
    var modalContainer = document.createElement('div');
    modalContainer.id = 'sessionsModal';
    modalContainer.className = 'modal';
    modalContainer.style.display = 'block';
    
    var modalContent = document.createElement('div');
    modalContent.className = 'modal-content';
    
    // Header
    var header = document.createElement('div');
    header.className = 'modal-header';
    
    var title = document.createElement('h2');
    title.className = 'modal-title';
    title.textContent = 'Partnership Sessions';
    
    var closeBtn = document.createElement('span');
    closeBtn.className = 'close';
    closeBtn.innerHTML = '&times;';
    closeBtn.onclick = closeSessionsModal;
    
    header.appendChild(title);
    header.appendChild(closeBtn);
    
    // Body
    var body = document.createElement('div');
    body.className = 'modal-body';
    body.style.cssText = 'max-height: 400px; overflow-y: auto;';
    
    if (sessions.length > 0) {
        sessions.forEach(function(session) {
            var sessionItem = createSessionItem(session);
            body.appendChild(sessionItem);
        });
    } else {
        var emptyState = document.createElement('div');
        emptyState.className = 'empty-state';
        emptyState.innerHTML = '<i class="fas fa-calendar-times"></i><h3>No sessions yet</h3><p>Schedule your first study session together!</p>';
        body.appendChild(emptyState);
    }
    
    modalContent.appendChild(header);
    modalContent.appendChild(body);
    modalContainer.appendChild(modalContent);
    
    document.body.appendChild(modalContainer);
}

// Create session item element
function createSessionItem(session) {
    var item = document.createElement('div');
    item.className = 'session-item';
    item.style.marginBottom = '1rem';
    
    var scheduledDate = new Date(session.scheduled_time).toLocaleString();
    var statusClass = session.is_completed ? 'status-completed' : 'status-upcoming';
    var statusText = session.is_completed ? 'Completed' : 'Scheduled';
    
    var headerDiv = document.createElement('div');
    headerDiv.className = 'session-header';
    
    var titleEl = document.createElement('h5');
    titleEl.className = 'session-title';
    titleEl.textContent = session.title;
    
    var statusEl = document.createElement('span');
    statusEl.className = 'session-status ' + statusClass;
    statusEl.textContent = statusText;
    
    headerDiv.appendChild(titleEl);
    headerDiv.appendChild(statusEl);
    
    var detailsDiv = document.createElement('div');
    detailsDiv.className = 'session-details';
    detailsDiv.innerHTML = 
        '<div><i class="fas fa-book" style="margin-right: 0.5rem; color: #3b82f6;"></i>' + session.subject + '</div>' +
        '<div><i class="fas fa-calendar" style="margin-right: 0.5rem; color: #3b82f6;"></i>' + scheduledDate + '</div>' +
        '<div><i class="fas fa-clock" style="margin-right: 0.5rem; color: #3b82f6;"></i>' + session.duration_hours + ' hours</div>' +
        '<div><i class="fas fa-user" style="margin-right: 0.5rem; color: #3b82f6;"></i>Created by ' + session.created_by + '</div>';
    
    if (session.description) {
        var descDiv = document.createElement('div');
        descDiv.style.cssText = 'margin-top: 0.5rem; font-style: italic;';
        descDiv.textContent = session.description;
        detailsDiv.appendChild(descDiv);
    }
    
    if (session.notes) {
        var notesDiv = document.createElement('div');
        notesDiv.style.cssText = 'margin-top: 0.5rem; padding: 0.5rem; background: rgba(16,185,129,0.1); border-radius: 4px; color: #10b981;';
        notesDiv.innerHTML = '<i class="fas fa-sticky-note" style="margin-right: 0.5rem;"></i>' + session.notes;
        detailsDiv.appendChild(notesDiv);
    }
    
    if (!session.is_completed && new Date(session.scheduled_time) < new Date()) {
        var completeBtn = document.createElement('button');
        completeBtn.className = 'btn-schedule';
        completeBtn.style.cssText = 'margin-top: 0.5rem; font-size: 0.8rem; padding: 0.25rem 0.75rem;';
        completeBtn.innerHTML = '<i class="fas fa-check" style="margin-right: 0.25rem;"></i>Mark as Completed';
        completeBtn.onclick = function() { markSessionCompleted(session.id); };
        detailsDiv.appendChild(completeBtn);
    }
    
    item.appendChild(headerDiv);
    item.appendChild(detailsDiv);
    
    return item;
}

// Close sessions modal
function closeSessionsModal() {
    var modal = document.getElementById('sessionsModal');
    if (modal) {
        modal.remove();
    }
}

// Mark session as completed
function markSessionCompleted(sessionId) {
    var notes = prompt('Add any notes about this session (optional):');
    
    fetch('/api/complete-session/' + sessionId + '/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ notes: notes || '' })
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        if (data.success) {
            showNotification('Session marked as completed!', 'success');
            closeSessionsModal();
            setTimeout(function() {
                window.location.reload();
            }, 1000);
        } else {
            showNotification('Error: ' + data.error, 'error');
        }
    })
    .catch(function(error) {
        console.error('Error:', error);
        showNotification('Failed to complete session', 'error');
    });
}

// Confirm end partnership
function confirmEndPartnership(partnershipId) {
    if (confirm('Are you sure you want to end this study partnership? This action cannot be undone.')) {
        endPartnership(partnershipId);
    }
}

// End partnership
function endPartnership(partnershipId) {
    fetch('/api/end-partnership/' + partnershipId + '/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        if (data.success) {
            showNotification('Partnership ended successfully', 'success');
            var card = document.querySelector('[data-partnership-id="' + partnershipId + '"]');
            if (card) {
                card.style.transition = 'all 0.3s ease';
                card.style.opacity = '0';
                card.style.transform = 'translateY(-20px)';
                setTimeout(function() {
                    card.remove();
                    if (document.querySelectorAll('[data-partnership-id]').length === 0) {
                        window.location.reload();
                    }
                }, 300);
            }
        } else {
            showNotification('Error: ' + data.error, 'error');
        }
    })
    .catch(function(error) {
        console.error('Error:', error);
        showNotification('Failed to end partnership', 'error');
    });
}

// Partner requests functionality
function respondToRequest(requestId, action) {
    var card = document.querySelector('[data-request-id="' + requestId + '"]');
    var buttons = card.querySelectorAll('.request-actions button');
    
    // Disable buttons during request
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].disabled = true;
        buttons[i].style.opacity = '0.6';
    }
    
    fetch('/api/respond-to-request/' + requestId + '/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ action: action })
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        if (data.success) {
            showNotification('Request ' + action + 'ed successfully!', 'success');
            
            // Update the card UI
            var statusElement = card.querySelector('.request-status');
            var actionsElement = card.querySelector('.request-actions');
            
            statusElement.className = 'request-status status-' + action + 'ed';
            statusElement.textContent = action === 'accept' ? 'ACCEPTED' : 'DECLINED';
            
            // Replace actions with status message
            var statusHTML;
            if (action === 'accept') {
                statusHTML = '<div style="margin-top: 1rem; padding: 0.75rem; background: rgba(16, 185, 129, 0.1); border-radius: 8px; text-align: center;">' +
                    '<i class="fas fa-handshake" style="color: #10b981; margin-right: 0.5rem;"></i>' +
                    '<span style="color: #10b981; font-weight: 600;">You accepted this request!</span>' +
                    '<div style="margin-top: 0.5rem;">' +
                        '<a href="/my-study-partners/" style="color: #10b981; text-decoration: none;">View your partnerships →</a>' +
                    '</div>' +
                '</div>';
            } else {
                statusHTML = '<div style="margin-top: 1rem; padding: 0.75rem; background: rgba(239, 68, 68, 0.1); border-radius: 8px; text-align: center;">' +
                    '<i class="fas fa-times-circle" style="color: #ef4444; margin-right: 0.5rem;"></i>' +
                    '<span style="color: #ef4444; font-weight: 600;">You declined this request</span>' +
                '</div>';
            }
            actionsElement.innerHTML = statusHTML;
            
        } else {
            showNotification('Error: ' + data.error, 'error');
            // Re-enable buttons on error
            for (var i = 0; i < buttons.length; i++) {
                buttons[i].disabled = false;
                buttons[i].style.opacity = '1';
            }
        }
    })
    .catch(function(error) {
        console.error('Error:', error);
        showNotification('Failed to respond to request', 'error');
        // Re-enable buttons on error
        for (var i = 0; i < buttons.length; i++) {
            buttons[i].disabled = false;
            buttons[i].style.opacity = '1';
        }
    });
}

// Utility function to get CSRF token
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}