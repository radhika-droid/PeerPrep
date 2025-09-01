let charts = {};
let currentGoals = [];

document.addEventListener('DOMContentLoaded', function() {
    loadProgressData();
    setupEventListeners();
});

function setupEventListeners() {
    document.getElementById('goalForm').addEventListener('submit', handleGoalSubmission);
    
    document.getElementById('sessionForm').addEventListener('submit', handleSessionSubmission);
    
    document.getElementById('weeklyForm').addEventListener('submit', handleWeeklyGoalSubmission);
    
    window.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            closeModal(e.target.id);
        }
    });
}

async function loadProgressData() {
    try {
        showLoading();
        
        const response = await fetch('/api/progress-dashboard/', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            updateStatistics(data.stats);
            updateWeeklyProgress(data.weekly_progress);
            renderDailyChart(data.daily_data);
            renderSubjectChart(data.subject_data);
            displayRecentActivity(data.recent_sessions);
            displayAchievements(data.recent_achievements);
        }
        
        await loadGoals();
        
        hideLoading();
        
    } catch (error) {
        console.error('Error loading progress data:', error);
        showNotification('Failed to load progress data', 'error');
        hideLoading();
    }
}

async function loadGoals() {
    try {
        const response = await fetch('/api/goals/', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentGoals = data.goals;
            displayGoals(data.goals);
        }
        
    } catch (error) {
        console.error('Error loading goals:', error);
    }
}

function updateStatistics(stats) {
    document.getElementById('totalHours').textContent = stats.total_study_hours;
    document.getElementById('completedGoals').textContent = stats.total_goals_completed;
    document.getElementById('currentStreak').textContent = stats.current_streak_days;
    document.getElementById('achievementPoints').textContent = stats.achievement_points;
}

function updateWeeklyProgress(weekly) {
    const hoursProgress = Math.min((weekly.actual_hours / weekly.target_hours) * 100, 100);
    const sessionsProgress = Math.min((weekly.actual_sessions / weekly.target_sessions) * 100, 100);
    
    document.getElementById('weeklyHoursProgress').style.width = hoursProgress + '%';
    document.getElementById('weeklySessionsProgress').style.width = sessionsProgress + '%';
    document.getElementById('weeklyHoursText').textContent = `${weekly.actual_hours} / ${weekly.target_hours} hrs`;
    document.getElementById('weeklySessionsText').textContent = `${weekly.actual_sessions} / ${weekly.target_sessions} sessions`;
}

function renderDailyChart(dailyData) {
    const ctx = document.getElementById('dailyChart').getContext('2d');
    
    if (charts.daily) {
        charts.daily.destroy();
    }
    
    charts.daily = new Chart(ctx, {
        type: 'line',
        data: {
            labels: dailyData.map(d => d.day),
            datasets: [{
                label: 'Study Hours',
                data: dailyData.map(d => d.hours),
                borderColor: '#3b82f6',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: '#3b82f6',
                pointBorderColor: '#ffffff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    }
                },
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.7)'
                    }
                }
            }
        }
    });
}

function renderSubjectChart(subjectData) {
    const ctx = document.getElementById('subjectChart').getContext('2d');
    
    if (charts.subject) {
        charts.subject.destroy();
    }
    
    const colors = [
        '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
        '#06b6d4', '#84cc16', '#f97316', '#ec4899', '#6366f1'
    ];
    
    charts.subject = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: subjectData.map(d => d.subject_display),
            datasets: [{
                data: subjectData.map(d => d.hours),
                backgroundColor: colors.slice(0, subjectData.length),
                borderColor: colors.slice(0, subjectData.length),
                borderWidth: 2,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: 'rgba(255, 255, 255, 0.8)',
                        usePointStyle: true,
                        padding: 15
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value}h (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

function displayGoals(goals) {
    const container = document.getElementById('goalsContainer');
    
    if (goals.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-target" style="font-size: 3rem; color: rgba(255, 255, 255, 0.3); margin-bottom: 1rem;"></i>
                <p style="color: rgba(255, 255, 255, 0.6);">No goals yet. Create your first goal to start tracking progress!</p>
            </div>
        `;
        return;
    }
    
    const sortedGoals = goals.sort((a, b) => {
        const priorityOrder = { urgent: 4, high: 3, medium: 2, low: 1 };
        return priorityOrder[b.priority] - priorityOrder[a.priority];
    });
    
    const displayGoals = sortedGoals.slice(0, 3);
    
    container.innerHTML = displayGoals.map(goal => `
        <div class="goal-item" onclick="openGoalDetail(${goal.id})">
            <div class="goal-header">
                <div class="goal-info">
                    <div class="goal-title">${goal.title}</div>
                    <div class="goal-meta">
                        <span class="goal-badge priority-${goal.priority}">${goal.priority_display}</span>
                        <span class="goal-badge status-${goal.status}">${goal.status_display}</span>
                        ${goal.is_overdue ? '<span class="goal-badge priority-urgent">Overdue</span>' : ''}
                        ${goal.days_remaining !== null ? `<span style="color: rgba(255, 255, 255, 0.6); font-size: 0.8rem;">${goal.days_remaining} days left</span>` : ''}
                    </div>
                </div>
            </div>
            
            <div class="goal-progress">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.3rem;">
                    <span style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem;">Progress</span>
                    <span style="color: white; font-weight: 600;">${goal.progress_percentage}%</span>
                </div>
                <div class="goal-progress-bar">
                    <div class="goal-progress-fill" style="width: ${goal.progress_percentage}%"></div>
                </div>
            </div>
            
            <div class="goal-actions" onclick="event.stopPropagation()">
                <button class="goal-btn" onclick="updateGoalProgress(${goal.id}, ${Math.min(goal.progress_percentage + 10, 100)})">
                    +10%
                </button>
                <button class="goal-btn" onclick="openGoalDetail(${goal.id})">
                    Details
                </button>
            </div>
        </div>
    `).join('');
}

function displayRecentActivity(sessions) {
    const activityFeed = document.getElementById('activityFeed');
    
    if (sessions.length === 0) {
        activityFeed.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-history" style="font-size: 2rem; color: rgba(255, 255, 255, 0.3); margin-bottom: 0.5rem;"></i>
                <p style="color: rgba(255, 255, 255, 0.6); font-size: 0.9rem;">No recent activity</p>
            </div>
        `;
        return;
    }
    
    activityFeed.innerHTML = sessions.map(session => `
        <div class="activity-item">
            <div class="activity-header">
                <span class="activity-icon">📚</span>
                <span class="activity-title">Studied ${session.subject}</span>
            </div>
            <div class="activity-description">${session.title} (${session.duration_minutes} min)</div>
            <div class="activity-time">${formatRelativeTime(session.date)}</div>
        </div>
    `).join('');
}

function displayAchievements(achievements) {
    const container = document.getElementById('achievementsContainer');
    
    if (achievements.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-trophy" style="font-size: 2rem; color: rgba(255, 255, 255, 0.3); margin-bottom: 0.5rem;"></i>
                <p style="color: rgba(255, 255, 255, 0.6); font-size: 0.9rem;">No achievements yet</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = achievements.map(achievement => `
        <div class="achievement-item">
            <div class="achievement-icon">${achievement.icon}</div>
            <div class="achievement-content">
                <div class="achievement-title">${achievement.title}</div>
                <div class="achievement-description">${achievement.description}</div>
            </div>
            <div class="achievement-points">+${achievement.points}</div>
        </div>
    `).join('');
}

async function handleGoalSubmission(e) {
    e.preventDefault();
    
    const submitBtn = e.target.querySelector('.submit-btn');
    const originalText = submitBtn.textContent;
    const formData = new FormData(e.target);
    
    submitBtn.textContent = 'Creating...';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch('/api/create-goal/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            submitBtn.textContent = 'Goal Created! ✓';
            submitBtn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
            showNotification('Goal created successfully!', 'success');
            
            setTimeout(() => {
                closeModal('goalModal');
                e.target.reset();
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                submitBtn.style.background = 'linear-gradient(135deg, #3b82f6, #1d4ed8)';
                loadGoals(); 
            }, 1500);
        } else {
            submitBtn.textContent = 'Try Again';
            submitBtn.disabled = false;
            showNotification('Please check your form and try again.', 'error');
            
            setTimeout(() => {
                submitBtn.textContent = originalText;
            }, 2000);
        }
    } catch (error) {
        submitBtn.textContent = 'Try Again';
        submitBtn.disabled = false;
        showNotification('Something went wrong. Please try again.', 'error');
        
        setTimeout(() => {
            submitBtn.textContent = originalText;
        }, 2000);
    }
}

async function handleSessionSubmission(e) {
    e.preventDefault();
    
    const submitBtn = e.target.querySelector('.submit-btn');
    const originalText = submitBtn.textContent;
    const formData = new FormData(e.target);
    
    submitBtn.textContent = 'Logging...';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch('/api/log-study-session/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            submitBtn.textContent = 'Session Logged! ✓';
            submitBtn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
            showNotification('Study session logged successfully!', 'success');
            
            setTimeout(() => {
                closeModal('sessionModal');
                e.target.reset();
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                submitBtn.style.background = 'linear-gradient(135deg, #3b82f6, #1d4ed8)';
                
                
                const today = new Date().toISOString().split('T')[0];
                e.target.querySelector('input[name="date"]').value = today;
                
                loadProgressData(); 
            }, 1500);
        } else {
            submitBtn.textContent = 'Try Again';
            submitBtn.disabled = false;
            showNotification('Please check your form and try again.', 'error');
            
            setTimeout(() => {
                submitBtn.textContent = originalText;
            }, 2000);
        }
    } catch (error) {
        submitBtn.textContent = 'Try Again';
        submitBtn.disabled = false;
        showNotification('Something went wrong. Please try again.', 'error');
        
        setTimeout(() => {
            submitBtn.textContent = originalText;
        }, 2000);
    }
}

async function handleWeeklyGoalSubmission(e) {
    e.preventDefault();
    
    const submitBtn = e.target.querySelector('.submit-btn');
    const originalText = submitBtn.textContent;
    const targetHours = e.target.querySelector('input[name="target_hours"]').value;
    const targetSessions = e.target.querySelector('input[name="target_sessions"]').value;
    
    submitBtn.textContent = 'Setting...';
    submitBtn.disabled = true;
    
    try {
        const response = await fetch('/api/set-weekly-goals/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                target_hours: parseFloat(targetHours),
                target_sessions: parseInt(targetSessions)
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            submitBtn.textContent = 'Goals Set! ✓';
            submitBtn.style.background = 'linear-gradient(135deg, #10b981, #059669)';
            showNotification('Weekly goals updated successfully!', 'success');
            
            setTimeout(() => {
                closeModal('weeklyModal');
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                submitBtn.style.background = 'linear-gradient(135deg, #3b82f6, #1d4ed8)';
                loadProgressData(); 
            }, 1500);
        } else {
            submitBtn.textContent = 'Try Again';
            submitBtn.disabled = false;
            showNotification('Failed to set weekly goals', 'error');
            
            setTimeout(() => {
                submitBtn.textContent = originalText;
            }, 2000);
        }
    } catch (error) {
        submitBtn.textContent = 'Try Again';
        submitBtn.disabled = false;
        showNotification('Something went wrong. Please try again.', 'error');
        
        setTimeout(() => {
            submitBtn.textContent = originalText;
        }, 2000);
    }
}

async function updateGoalProgress(goalId, newProgress) {
    try {
        const response = await fetch(`/api/update-goal-progress/${goalId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                progress_percentage: newProgress
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Progress updated!', 'success');
            loadGoals(); 
            if (data.is_completed) {
                showNotification('🎉 Goal completed! Achievement unlocked!', 'success');
                loadProgressData(); 
            }
        } else {
            showNotification('Failed to update progress', 'error');
        }
    } catch (error) {
        console.error('Error updating goal progress:', error);
        showNotification('Something went wrong', 'error');
    }
}

async function openGoalDetail(goalId) {
    try {
        const response = await fetch(`/api/goal/${goalId}/`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayGoalDetail(data.goal);
            openModal('goalDetailModal');
        } else {
            showNotification('Failed to load goal details', 'error');
        }
    } catch (error) {
        console.error('Error loading goal detail:', error);
        showNotification('Something went wrong', 'error');
    }
}

function displayGoalDetail(goal) {
    document.getElementById('goalDetailTitle').textContent = goal.title;
    
    const content = document.getElementById('goalDetailContent');
    content.innerHTML = `
        <div class="goal-detail-header">
            <div class="goal-detail-info">
                <div class="goal-detail-title">${goal.title}</div>
                <div class="goal-detail-meta">
                    <span class="goal-badge priority-${goal.priority}">${goal.priority_display}</span>
                    <span class="goal-badge status-${goal.status}">${goal.status_display}</span>
                    ${goal.category ? `<span class="goal-badge">${goal.category_display}</span>` : ''}
                    ${goal.is_overdue ? '<span class="goal-badge priority-urgent">Overdue</span>' : ''}
                </div>
                <div class="goal-detail-description">${goal.description || 'No description provided.'}</div>
                ${goal.target_date ? `<p style="color: rgba(255, 255, 255, 0.7);"><strong>Target Date:</strong> ${formatDate(goal.target_date)}</p>` : ''}
                ${goal.days_remaining !== null ? `<p style="color: rgba(255, 255, 255, 0.7);"><strong>Days Remaining:</strong> ${goal.days_remaining}</p>` : ''}
            </div>
            
            <div class="goal-detail-actions">
                <div class="progress-update">
                    <h4>Update Progress</h4>
                    <input type="range" min="0" max="100" value="${goal.progress_percentage}" 
                           class="progress-slider" id="progressSlider" 
                           oninput="updateProgressDisplay(this.value)">
                    <div style="display: flex; justify-content: space-between; margin: 0.5rem 0;">
                        <span style="color: rgba(255, 255, 255, 0.6);">0%</span>
                        <span id="progressDisplay" style="color: white; font-weight: 600;">${goal.progress_percentage}%</span>
                        <span style="color: rgba(255, 255, 255, 0.6);">100%</span>
                    </div>
                    <button class="submit-btn" onclick="saveGoalProgress(${goal.id})">
                        Save Progress
                    </button>
                </div>
                
                <button class="goal-btn" style="width: 100%; margin-top: 1rem;" onclick="deleteGoal(${goal.id})">
                    <i class="fas fa-trash"></i> Delete Goal
                </button>
            </div>
        </div>
        
        ${goal.milestones && goal.milestones.length > 0 ? `
            <div class="milestones-section">
                <div class="milestones-header">
                    <h4 style="color: white; margin: 0;">Milestones (${goal.completed_milestones}/${goal.milestones_count})</h4>
                    <button class="header-btn" onclick="addMilestone(${goal.id})">
                        <i class="fas fa-plus"></i>
                    </button>
                </div>
                <div class="milestones-list">
                    ${goal.milestones.map(milestone => `
                        <div class="milestone-item">
                            <div class="milestone-checkbox ${milestone.is_completed ? 'completed' : ''}" 
                                 onclick="toggleMilestone(${milestone.id})">
                                ${milestone.is_completed ? '<i class="fas fa-check"></i>' : ''}
                            </div>
                            <div class="milestone-content">
                                <div class="milestone-title">${milestone.title}</div>
                                ${milestone.due_date ? `<div class="milestone-due">Due: ${formatDate(milestone.due_date)}</div>` : ''}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        ` : ''}
    `;
}

function updateProgressDisplay(value) {
    document.getElementById('progressDisplay').textContent = value + '%';
}

async function saveGoalProgress(goalId) {
    const progressSlider = document.getElementById('progressSlider');
    const newProgress = parseInt(progressSlider.value);
    
    try {
        const response = await fetch(`/api/update-goal-progress/${goalId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                progress_percentage: newProgress
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Progress updated successfully!', 'success');
            loadGoals(); 
            
            if (data.is_completed) {
                showNotification('🎉 Congratulations! Goal completed!', 'success');
                setTimeout(() => {
                    closeModal('goalDetailModal');
                    loadProgressData(); 
                }, 2000);
            }
        } else {
            showNotification('Failed to update progress', 'error');
        }
    } catch (error) {
        console.error('Error updating progress:', error);
        showNotification('Something went wrong', 'error');
    }
}

async function deleteGoal(goalId) {
    if (!confirm('Are you sure you want to delete this goal? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/delete-goal/${goalId}/`, {
            method: 'DELETE',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Goal deleted successfully', 'success');
            closeModal('goalDetailModal');
            loadGoals();
        } else {
            showNotification('Failed to delete goal', 'error');
        }
    } catch (error) {
        console.error('Error deleting goal:', error);
        showNotification('Something went wrong', 'error');
    }
}

async function toggleMilestone(milestoneId) {
    try {
        const response = await fetch(`/api/toggle-milestone/${milestoneId}/`, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(data.message, 'success');
            const goalId = getCurrentGoalId();
            if (goalId) {
                openGoalDetail(goalId);
            }
        } else {
            showNotification('Failed to update milestone', 'error');
        }
    } catch (error) {
        console.error('Error toggling milestone:', error);
        showNotification('Something went wrong', 'error');
    }
}

function getCurrentGoalId() {
    const goalDetailModal = document.getElementById('goalDetailModal');
    if (goalDetailModal.style.display === 'block') {
        const firstMilestone = goalDetailModal.querySelector('.milestone-checkbox');
        if (firstMilestone) {
            const onclickAttr = firstMilestone.getAttribute('onclick');
            const match = onclickAttr.match(/toggleMilestone\((\d+)\)/);
            if (match) {
                const milestoneId = parseInt(match[1]);
                return currentGoals.find(goal => 
                    goal.milestones && goal.milestones.some(m => m.id === milestoneId)
                )?.id;
            }
        }
    }
    return null;
}

function showAllGoals() {
    if (currentGoals.length <= 3) {
        showNotification('All goals are already displayed', 'info');
        return;
    }
    
    const container = document.getElementById('goalsContainer');
    displayGoals(currentGoals); 
    
    const viewAllBtn = document.querySelector('.view-all button');
    viewAllBtn.textContent = 'Show Less';
    viewAllBtn.onclick = () => {
        displayGoals(currentGoals.slice(0, 3));
        viewAllBtn.textContent = 'View All Goals';
        viewAllBtn.onclick = showAllGoals;
    };
}

function openModal(modalId) {
    document.getElementById(modalId).style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
    document.body.style.overflow = 'auto';
}

function formatRelativeTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    if (diffInSeconds < 60) return 'Just now';
    if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
    if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
    if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)} days ago`;
    
    return date.toLocaleDateString();
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

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

function showLoading() {
    const container = document.querySelector('.progress-container');
    if (!container.querySelector('.loading-spinner')) {
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        spinner.innerHTML = '<i class="fas fa-spinner fa-spin" style="font-size: 2rem; color: #3b82f6;"></i>';
        spinner.style.cssText = 'position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 3000;';
        document.body.appendChild(spinner);
    }
}

function hideLoading() {
    const spinner = document.querySelector('.loading-spinner');
    if (spinner) {
        spinner.remove();
    }
}

function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;

    const icon = document.createElement('i');
    switch(type) {
        case 'success':
            icon.className = 'fas fa-check-circle';
            break;
        case 'error':
            icon.className = 'fas fa-exclamation-circle';
            break;
        case 'info':
            icon.className = 'fas fa-info-circle';
            break;
        default:
            icon.className = 'fas fa-bell';
    }
    
    notification.insertBefore(icon, notification.firstChild);
    notification.insertBefore(document.createTextNode(' '), notification.firstChild.nextSibling);

    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('show');
    }, 100);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentNode) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 4000);
}