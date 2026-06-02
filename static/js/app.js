// ================= STATE MANAGEMENT =================
let currentUser = null;
let currentChatId = null;
let chatsList = [];
let moodHistory = [];
let taskList = [];

const API_BASE = ""; // Relative to host

// ================= DOM ELEMENT REFERENCES =================
const DOM = {
    // Views
    viewSignin: document.getElementById("view-signin"),
    viewSignup: document.getElementById("view-signup"),
    viewDashboard: document.getElementById("view-dashboard"),
    
    // Forms
    signinForm: document.getElementById("signin-form"),
    signupForm: document.getElementById("signup-form"),
    chatMessageForm: document.getElementById("chat-message-form"),
    manualMoodForm: document.getElementById("manual-mood-form"),
    plannerTaskForm: document.getElementById("planner-task-form"),
    
    // Auth inputs
    signinEmail: document.getElementById("signin-email"),
    signinPassword: document.getElementById("signin-password"),
    signupFirstname: document.getElementById("signup-firstname"),
    signupLastname: document.getElementById("signup-lastname"),
    signupEmail: document.getElementById("signup-email"),
    signupPassword: document.getElementById("signup-password"),
    signupConfirmPassword: document.getElementById("signup-confirm-password"),
    signupPasswordLabel: document.getElementById("signup-password-label"),
    signupPasswordMeter: document.querySelector(".password-strength-meter"),
    
    // View navigation buttons/links
    linkGotoSignup: document.getElementById("link-goto-signup"),
    linkGotoSignin: document.getElementById("link-goto-signin"),
    btnNewChat: document.getElementById("btn-new-chat"),
    navItems: document.querySelectorAll(".nav-item"),
    tabPanes: document.querySelectorAll(".tab-pane"),
    btnLogout: document.getElementById("btn-logout"),
    btnLogMoodHeader: document.getElementById("btn-log-mood-header"),
    btnClearData: document.getElementById("btn-clear-data"),
    userProfileMenuTrigger: document.getElementById("user-profile-menu-trigger"),
    profileDropdown: document.getElementById("profile-dropdown"),
    
    // Profile displays
    profileName: document.getElementById("profile-name"),
    profileEmail: document.getElementById("profile-email"),
    profileAvatar: document.getElementById("user-avatar-initial"),
    settingsUserFullname: document.getElementById("settings-user-fullname"),
    settingsUserEmail: document.getElementById("settings-user-email"),
    
    // Chat UI elements
    chatInput: document.getElementById("chat-input-field"),
    chatMessagesList: document.getElementById("chat-messages-list"),
    chatWelcomeOverlay: document.getElementById("chat-welcome-overlay"),
    recentChatsList: document.getElementById("recent-chats-list"),
    currentMoodText: document.getElementById("current-mood-text"),
    currentMoodBadge: document.getElementById("current-mood-badge"),
    suggestionChips: document.querySelectorAll(".chip-btn"),
    
    // Mood tracker elements
    moodSelect: document.getElementById("mood-select"),
    moodNotes: document.getElementById("mood-notes"),
    moodHistoryList: document.getElementById("mood-history-list"),
    statsTotalLogs: document.getElementById("stats-total-logs"),
    statsDominantMood: document.getElementById("stats-dominant-mood"),
    
    // Study planner elements
    taskTitleInput: document.getElementById("task-title-input"),
    tasksList: document.getElementById("tasks-list")
};

// ================= APP INITIALIZATION =================
document.addEventListener("DOMContentLoaded", () => {
    initApp();
    setupEventListeners();
});

function initApp() {
    // Check if user is cached in local storage
    const cachedUser = localStorage.getItem("mindmate_user");
    if (cachedUser) {
        currentUser = JSON.parse(cachedUser);
        loadUserSession();
    } else {
        // Show Sign-in view without prefilled email
        showView("signin");
    }
}

// ================= VIEW NAVIGATION =================
function showView(viewName) {
    DOM.viewSignin.classList.remove("active");
    DOM.viewSignup.classList.remove("active");
    DOM.viewDashboard.classList.remove("active");
    
    if (viewName === "signin") {
        DOM.viewSignin.classList.add("active");
    } else if (viewName === "signup") {
        DOM.viewSignup.classList.add("active");
    } else if (viewName === "dashboard") {
        DOM.viewDashboard.classList.add("active");
    }
}

function showTab(tabId) {
    // Deactivate all navigation items & tabs
    DOM.navItems.forEach(item => item.classList.remove("active"));
    DOM.tabPanes.forEach(pane => pane.classList.remove("active"));
    
    // Activate clicked tab
    const navItem = document.querySelector(`.nav-item[data-tab="${tabId}"]`);
    if (navItem) navItem.classList.add("active");
    
    const tabPane = document.getElementById(tabId);
    if (tabPane) tabPane.classList.add("active");
    
    // Trigger tab-specific loads
    if (tabId === "tab-mood") {
        loadMoodHistory();
    } else if (tabId === "tab-planner") {
        loadPlannerTasks();
    } else if (tabId === "tab-settings") {
        loadSettingsInfo();
    }
}

// ================= EVENT LISTENERS SETUP =================
function setupEventListeners() {
    // View Switch links
    DOM.linkGotoSignup.addEventListener("click", (e) => {
        e.preventDefault();
        showView("signup");
    });
    
    DOM.linkGotoSignin.addEventListener("click", (e) => {
        e.preventDefault();
        showView("signin");
    });
    
    // Tab navigations
    DOM.navItems.forEach(item => {
        item.addEventListener("click", (e) => {
            e.preventDefault();
            const tabId = item.getAttribute("data-tab");
            showTab(tabId);
        });
    });
    
    // Sign In Submission
    DOM.signinForm.addEventListener("submit", handleSignIn);
    
    // Sign Up Submission
    DOM.signupForm.addEventListener("submit", handleSignUp);
    
    // Password Strength Meter Listener
    DOM.signupPassword.addEventListener("input", updatePasswordStrength);
    
    // Sidebar User Profile click (toggle dropdown)
    DOM.userProfileMenuTrigger.addEventListener("click", (e) => {
        e.stopPropagation();
        DOM.profileDropdown.classList.toggle("show");
    });
    
    // Document click to close profile dropdown
    document.addEventListener("click", () => {
        DOM.profileDropdown.classList.remove("show");
    });
    
    // Log Out
    DOM.btnLogout.addEventListener("click", handleLogout);
    
    // Create new conversation
    DOM.btnNewChat.addEventListener("click", createNewChat);
    
    // Chat Message Submission
    DOM.chatMessageForm.addEventListener("submit", handleSendMessage);
    
    // Chip suggestions clicks
    DOM.suggestionChips.forEach(chip => {
        chip.addEventListener("click", () => {
            const promptText = chip.getAttribute("data-text");
            if (promptText) {
                sendPromptMessage(promptText);
            }
        });
    });
    
    // Log Mood manually
    DOM.manualMoodForm.addEventListener("submit", handleManualMoodLog);
    
    // Header Log mood button shortcut (redirects to Mood Tracker tab)
    DOM.btnLogMoodHeader.addEventListener("click", () => {
        showTab("tab-mood");
        DOM.moodSelect.focus();
    });
    
    // Planner Task Submission
    DOM.plannerTaskForm.addEventListener("submit", handleCreateTask);
    
    // Settings Clear Data
    DOM.btnClearData.addEventListener("click", handleClearData);
}

// ================= PASSWORD VISIBILITY TOGGLE =================
window.togglePasswordVisibility = function(inputId, iconEl) {
    const input = document.getElementById(inputId);
    if (input.type === "password") {
        input.type = "text";
        iconEl.className = "fa-regular fa-eye";
    } else {
        input.type = "password";
        iconEl.className = "fa-regular fa-eye-slash";
    }
};

// ================= PASSWORD STRENGTH METER =================
function updatePasswordStrength() {
    const val = DOM.signupPassword.value;
    const label = DOM.signupPasswordLabel;
    const meter = DOM.signupPasswordMeter;
    
    // Reset strength styles
    meter.className = "password-strength-meter";
    label.className = "password-strength-label";
    
    if (val.length === 0) {
        label.innerText = "Enter a password";
        return;
    }
    
    if (val.length < 8) {
        label.innerText = "Password too short (min 8 characters)";
        label.classList.add("strength-weak-label");
        meter.classList.add("strength-weak");
        return;
    }
    
    let score = 0;
    if (/[A-Z]/.test(val)) score++;
    if (/[a-z]/.test(val)) score++;
    if (/[0-9]/.test(val)) score++;
    if (/[^A-Za-z0-9]/.test(val)) score++;
    
    if (score <= 1) {
        label.innerText = "Weak password";
        label.classList.add("strength-weak-label");
        meter.classList.add("strength-weak");
    } else if (score === 2) {
        label.innerText = "Fair password";
        label.classList.add("strength-fair-label");
        meter.classList.add("strength-fair");
    } else if (score === 3) {
        label.innerText = "Good password";
        label.classList.add("strength-good-label");
        meter.classList.add("strength-good");
    } else if (score >= 4) {
        label.innerText = "Strong password";
        label.classList.add("strength-strong-label");
        meter.classList.add("strength-strong");
    }
}

// ================= AUTHENTICATION ACTIONS =================
async function handleSignIn(e) {
    e.preventDefault();
    const email = DOM.signinEmail.value.trim();
    const password = DOM.signinPassword.value;
    
    try {
        const response = await fetch(`${API_BASE}/api/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            alert(result.error || "Login failed");
            return;
        }
        
        currentUser = result;
        localStorage.setItem("mindmate_user", JSON.stringify(currentUser));
        loadUserSession();
        
    } catch (err) {
        console.error(err);
        alert("An error occurred. Check backend server.");
    }
}

async function handleSignUp(e) {
    e.preventDefault();
    const first_name = DOM.signupFirstname.value.trim();
    const last_name = DOM.signupLastname.value.trim();
    const email = DOM.signupEmail.value.trim();
    const password = DOM.signupPassword.value;
    const confirmPassword = DOM.signupConfirmPassword.value;
    
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ first_name, last_name, email, password })
        });
        
        const result = await response.json();
        
        if (!response.ok) {
            alert(result.error || "Account creation failed");
            return;
        }
        
        // Auto sign in on register success
        currentUser = result;
        localStorage.setItem("mindmate_user", JSON.stringify(currentUser));
        loadUserSession();
        
        // Reset form
        DOM.signupForm.reset();
        updatePasswordStrength();
        
    } catch (err) {
        console.error(err);
        alert("An error occurred. Check backend server.");
    }
}

function handleLogout(e) {
    e.preventDefault();
    currentUser = null;
    currentChatId = null;
    localStorage.removeItem("mindmate_user");
    
    // Clear dynamic states
    DOM.recentChatsList.innerHTML = "";
    DOM.chatMessagesList.innerHTML = "";
    DOM.chatWelcomeOverlay.style.display = "block";
    updateMoodBadge("neutral");
    
    showView("signin");
}

// ================= USER SESSION LOADING =================
function loadUserSession() {
    // Set profile names in UI
    const fullName = `${currentUser.first_name} ${currentUser.last_name}`;
    DOM.profileName.innerText = currentUser.first_name; // Sidebar shows first name: "manu"
    DOM.profileEmail.innerText = currentUser.email;
    DOM.profileAvatar.innerText = currentUser.first_name.charAt(0).toUpperCase();
    
    // Populate settings view
    DOM.settingsUserFullname.innerText = fullName;
    DOM.settingsUserEmail.innerText = currentUser.email;
    
    // Go to dashboard
    showView("dashboard");
    showTab("tab-chat");
    
    // Load lists
    loadChatsList();
}

// ================= CHAT LIST LOADING =================
async function loadChatsList() {
    try {
        const response = await fetch(`${API_BASE}/api/chats?user_id=${currentUser.id}`);
        const list = await response.json();
        
        chatsList = list;
        renderRecentChats();
        
        // Load active chat or start new one
        if (chatsList.length > 0) {
            loadChatConversation(chatsList[0].id);
        } else {
            // First time use, create a default chat
            createNewChat();
        }
    } catch (err) {
        console.error(err);
    }
}

function renderRecentChats() {
    DOM.recentChatsList.innerHTML = "";
    
    if (chatsList.length === 0) {
        DOM.recentChatsList.innerHTML = '<span class="empty-state-text">No chats yet</span>';
        return;
    }
    
    chatsList.forEach(chat => {
        const chatItem = document.createElement("a");
        chatItem.href = "#";
        chatItem.className = `recent-item ${chat.id === currentChatId ? 'active' : ''}`;
        chatItem.setAttribute("data-id", chat.id);
        
        const titleContainer = document.createElement("div");
        titleContainer.className = "recent-item-title-container";
        titleContainer.innerHTML = `<i class="fa-regular fa-comment"></i> <span class="recent-item-title">${chat.title}</span>`;
        chatItem.appendChild(titleContainer);
        
        // Delete button
        const delBtn = document.createElement("button");
        delBtn.className = "btn-delete-chat";
        delBtn.innerHTML = '<i class="fa-solid fa-trash-can"></i>';
        delBtn.addEventListener("click", (e) => {
            e.stopPropagation();
            e.preventDefault();
            deleteChatSession(chat.id);
        });
        chatItem.appendChild(delBtn);
        
        // Select chat on click
        chatItem.addEventListener("click", (e) => {
            e.preventDefault();
            loadChatConversation(chat.id);
        });
        
        DOM.recentChatsList.appendChild(chatItem);
    });
}

// ================= CHAT MANAGEMENT =================
async function createNewChat() {
    try {
        const response = await fetch(`${API_BASE}/api/chats`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-User-Id": currentUser.id
            },
            body: JSON.stringify({ title: "New conversation" })
        });
        
        const newChat = await response.json();
        
        currentChatId = newChat.id;
        chatsList.unshift(newChat); // Put at top of list
        renderRecentChats();
        showTab("tab-chat");
        
        // Reset chat view for the new conversation
        DOM.chatMessagesList.innerHTML = "";
        DOM.chatInput.value = "";
        DOM.chatWelcomeOverlay.style.display = "block";
        updateMoodBadge("neutral");
        DOM.chatInput.focus();
        
    } catch (err) {
        console.error(err);
    }
}

async function loadChatConversation(chatId) {
    currentChatId = chatId;
    
    // Highlight correct recent item
    document.querySelectorAll(".recent-item").forEach(item => {
        if (item.getAttribute("data-id") === chatId) {
            item.classList.add("active");
        } else {
            item.classList.remove("active");
        }
    });
    
    try {
        const response = await fetch(`${API_BASE}/api/chats/${chatId}?user_id=${currentUser.id}`);
        const data = await response.json();
        const messages = Array.isArray(data) ? data : data.messages || [];
        const tips = Array.isArray(data) ? [] : data.tips || [];
        
        DOM.chatMessagesList.innerHTML = "";
        
        if (messages.length === 0) {
            // Show welcome overlay
            DOM.chatMessagesList.innerHTML = "";
            DOM.chatInput.value = "";
            DOM.chatWelcomeOverlay.style.display = "block";
            updateMoodBadge("neutral");
        } else {
            // Hide welcome overlay
            DOM.chatWelcomeOverlay.style.display = "none";
            
            // Render bubbles
            messages.forEach(msg => {
                appendMessageBubble(msg.sender, msg.text, msg.mood);
            });

            if (Array.isArray(tips) && tips.length > 0) {
                appendTipCards(tips);
            }
            
            // Find last user message mood to set header badge
            const userMsgs = messages.filter(m => m.sender === "user" && m.mood);
            if (userMsgs.length > 0) {
                const latestMood = userMsgs[userMsgs.length - 1].mood;
                updateMoodBadge(latestMood);
            } else {
                updateMoodBadge("neutral");
            }
            
            scrollToBottom();
        }
    } catch (err) {
        console.error(err);
    }
}

async function deleteChatSession(chatId) {
    if (!confirm("Are you sure you want to delete this conversation?")) return;
    
    try {
        const response = await fetch(`${API_BASE}/api/chats/${chatId}`, {
            method: "DELETE",
            headers: {
                "X-User-Id": currentUser.id
            }
        });
        
        if (response.ok) {
            chatsList = chatsList.filter(c => c.id !== chatId);
            renderRecentChats();
            
            if (currentChatId === chatId) {
                if (chatsList.length > 0) {
                    loadChatConversation(chatsList[0].id);
                } else {
                    createNewChat();
                }
            }
        }
    } catch (err) {
        console.error(err);
    }
}

// ================= CHAT MESSAGE SENDING =================
async function handleSendMessage(e) {
    e.preventDefault();
    const text = DOM.chatInput.value.trim();
    if (!text) return;
    
    DOM.chatInput.value = "";
    await sendPromptMessage(text);
}

async function sendPromptMessage(text) {
    if (!currentChatId) return;
    
    // Hide welcome overlay
    DOM.chatWelcomeOverlay.style.display = "none";
    
    // Add user bubble
    appendMessageBubble("user", text);
    scrollToBottom();
    
    // Add fake typing state for bot
    const botTypingId = appendTypingIndicator();
    scrollToBottom();
    
    try {
        const response = await fetch(`${API_BASE}/api/chats/${currentChatId}/message`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-User-Id": currentUser.id
            },
            body: JSON.stringify({ text })
        });
        
        const result = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator(botTypingId);
        
        if (!response.ok) {
            appendMessageBubble("bot", "I encountered an error. Please try again.");
            return;
        }
        
        // Update user message bubble's mood if it exists
        const userBubbles = DOM.chatMessagesList.querySelectorAll(".message-bubble-wrapper.user");
        if (userBubbles.length > 0) {
            const lastUserBubble = userBubbles[userBubbles.length - 1];
            let meta = lastUserBubble.querySelector(".message-meta");
            if (meta && result.detected_mood && result.detected_mood !== "neutral") {
                const moodTag = document.createElement("span");
                moodTag.className = "message-mood-tag";
                moodTag.innerText = result.detected_mood;
                meta.appendChild(moodTag);
            }
        }
        
        // Add bot bubble
        appendMessageBubble("bot", result.bot_message.text);
        
        // Add tip cards if provided
        if (Array.isArray(result.tips) && result.tips.length > 0) {
            appendTipCards(result.tips);
        }
        
        // Update top mood badge
        updateMoodBadge(result.detected_mood);
        
        // Persist chat title when conversation begins
        const activeChatIndex = chatsList.findIndex(c => c.id === currentChatId);
        if (activeChatIndex !== -1 && (chatsList[activeChatIndex].title === "New conversation" || chatsList[activeChatIndex].title === "")) {
            const cleanTitle = text.length > 30 ? text.substring(0, 30) + "..." : text;
            chatsList[activeChatIndex].title = cleanTitle;
            renderRecentChats();
            await persistChatTitle(currentChatId, cleanTitle);
        }
        
        scrollToBottom();
        
    } catch (err) {
        console.error(err);
        removeTypingIndicator(botTypingId);
        appendMessageBubble("bot", "Network connection error.");
        scrollToBottom();
    }
}

async function persistChatTitle(chatId, title) {
    try {
        const response = await fetch(`${API_BASE}/api/chats/${chatId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                "X-User-Id": currentUser.id
            },
            body: JSON.stringify({ title })
        });
        if (!response.ok) {
            console.warn("Unable to persist chat title", await response.text());
        }
    } catch (err) {
        console.error("Error updating chat title", err);
    }
}

function appendTipCards(tips) {
    const cardContainer = document.createElement("div");
    cardContainer.className = "tip-card-group";

    tips.forEach(tip => {
        const card = document.createElement("div");
        card.className = "tip-card";
        card.innerHTML = `
            <div class="tip-card-label">${tip.title}</div>
            <div class="tip-card-text">${tip.text}</div>
        `;
        cardContainer.appendChild(card);
    });

    const wrapper = document.createElement("div");
    wrapper.className = "message-bubble-wrapper bot tip-cards-wrapper";
    wrapper.appendChild(cardContainer);
    DOM.chatMessagesList.appendChild(wrapper);
}

// ================= MESSAGE BUBBLES INJECTION =================
function appendMessageBubble(sender, text, mood = null) {
    const bubbleWrapper = document.createElement("div");
    bubbleWrapper.className = `message-bubble-wrapper ${sender}`;
    
    // Add bot icon avatar
    if (sender === "bot") {
        bubbleWrapper.innerHTML = `
            <div class="message-avatar bot">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.58 1 9.2a7 7 0 0 1-9 8.8Z"></path><path d="M19 2c-2.26 4.33-5.27 7.14-8 10"></path></svg>
            </div>
        `;
    }
    
    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.innerText = text;
    
    // Create meta info block (timestamp, mood logs etc)
    const meta = document.createElement("div");
    meta.className = "message-meta";
    
    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    meta.innerHTML = `<span>${time}</span>`;
    
    if (mood && mood !== "neutral") {
        const moodTag = document.createElement("span");
        moodTag.className = "message-mood-tag";
        moodTag.innerText = mood;
        meta.appendChild(moodTag);
    }
    
    bubbleWrapper.appendChild(bubble);
    bubbleWrapper.appendChild(meta);
    DOM.chatMessagesList.appendChild(bubbleWrapper);
}

function appendTypingIndicator() {
    const typingId = "typing-" + Date.now();
    const bubbleWrapper = document.createElement("div");
    bubbleWrapper.className = `message-bubble-wrapper bot`;
    bubbleWrapper.id = typingId;
    bubbleWrapper.innerHTML = `
        <div class="message-avatar bot">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 3.58 1 9.2a7 7 0 0 1-9 8.8Z"></path><path d="M19 2c-2.26 4.33-5.27 7.14-8 10"></path></svg>
        </div>
        <div class="message-bubble" style="padding: 12px 18px; color: var(--text-muted);">
            MindMate is thinking...
        </div>
    `;
    DOM.chatMessagesList.appendChild(bubbleWrapper);
    return typingId;
}

function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function scrollToBottom() {
    DOM.chatMessagesList.scrollTop = DOM.chatMessagesList.scrollHeight;
    DOM.chatMessagesList.parentElement.scrollTop = DOM.chatMessagesList.parentElement.scrollHeight;
}

function updateMoodBadge(mood) {
    DOM.currentMoodText.innerText = mood;
    DOM.currentMoodBadge.className = `mood-badge ${mood}`;
    
    // Choose appropriate emoji inside SVG or text
    let emoji = "😌";
    if (mood === "happy") emoji = "😊";
    if (mood === "stressed" || mood === "distracted") emoji = "😓";
    if (mood === "overwhelmed") emoji = "😫";
    if (mood === "anxious") emoji = "😟";
    
    DOM.currentMoodBadge.querySelector(".badge-leaf-svg").style.display = mood === "neutral" ? "block" : "none";
    
    let emojiSpan = DOM.currentMoodBadge.querySelector(".badge-emoji");
    if (!emojiSpan) {
        emojiSpan = document.createElement("span");
        emojiSpan.className = "badge-emoji";
        DOM.currentMoodBadge.insertBefore(emojiSpan, DOM.currentMoodText);
    }
    
    if (mood === "neutral") {
        emojiSpan.innerText = "";
        DOM.currentMoodBadge.querySelector(".badge-leaf-svg").style.display = "block";
    } else {
        emojiSpan.innerText = emoji + " ";
        DOM.currentMoodBadge.querySelector(".badge-leaf-svg").style.display = "none";
    }
}


// ================= MOOD TRACKER LOGGING =================
async function loadMoodHistory() {
    try {
        const response = await fetch(`${API_BASE}/api/mood/history?user_id=${currentUser.id}`);
        const logs = await response.json();
        
        moodHistory = logs;
        renderMoodHistory();
        calculateMoodMetrics();
        
    } catch (err) {
        console.error(err);
    }
}

function renderMoodHistory() {
    DOM.moodHistoryList.innerHTML = "";
    
    if (moodHistory.length === 0) {
        DOM.moodHistoryList.innerHTML = '<p class="empty-state-text">No mood logs saved yet. Start chatting or log your mood above!</p>';
        return;
    }
    
    moodHistory.forEach(log => {
        const item = document.createElement("div");
        item.className = "mood-history-item";
        
        let emoji = "😌";
        if (log.mood === "happy") emoji = "😊";
        if (log.mood === "stressed" || log.mood === "distracted") emoji = "😓";
        if (log.mood === "overwhelmed") emoji = "😫";
        if (log.mood === "anxious") emoji = "😟";
        
        const dateStr = new Date(log.created_at).toLocaleDateString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
        
        item.innerHTML = `
            <div class="history-mood-info">
                <span style="font-size: 1.15rem;">${emoji}</span>
                <div>
                    <span class="history-mood-name">${log.mood}</span>
                    <span class="history-mood-notes">${log.notes || ""}</span>
                </div>
            </div>
            <span class="history-mood-date">${dateStr}</span>
        `;
        
        DOM.moodHistoryList.appendChild(item);
    });
}

function calculateMoodMetrics() {
    DOM.statsTotalLogs.innerText = moodHistory.length;
    
    if (moodHistory.length === 0) {
        DOM.statsDominantMood.innerText = "None";
        return;
    }
    
    // Count frequencies
    const counts = {};
    moodHistory.forEach(log => {
        counts[log.mood] = (counts[log.mood] || 0) + 1;
    });
    
    // Find dominant
    let dominant = "None";
    let max = 0;
    for (const [mood, val] of Object.entries(counts)) {
        if (val > max) {
            max = val;
            dominant = mood;
        }
    }
    
    // Map emoji
    let emoji = "😌";
    if (dominant === "happy") emoji = "😊";
    if (dominant === "stressed" || dominant === "distracted") emoji = "😓";
    if (dominant === "overwhelmed") emoji = "😫";
    if (dominant === "anxious") emoji = "😟";
    
    DOM.statsDominantMood.innerText = `${emoji} ${dominant}`;
}

async function handleManualMoodLog(e) {
    e.preventDefault();
    const mood = DOM.moodSelect.value;
    const notes = DOM.moodNotes.value.trim();
    
    try {
        const response = await fetch(`${API_BASE}/api/mood/log`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-User-Id": currentUser.id
            },
            body: JSON.stringify({ mood, notes })
        });
        
        if (response.ok) {
            DOM.moodNotes.value = "";
            loadMoodHistory();
            // Automatically update chat badge if users logs it
            updateMoodBadge(mood);
        } else {
            alert("Failed to save log.");
        }
    } catch (err) {
        console.error(err);
    }
}

// ================= STUDY PLANNER CRUD =================
async function loadPlannerTasks() {
    try {
        const response = await fetch(`${API_BASE}/api/tasks?user_id=${currentUser.id}`);
        const tasks = await response.json();
        
        taskList = tasks;
        renderTasks();
    } catch (err) {
        console.error(err);
    }
}

function renderTasks() {
    DOM.tasksList.innerHTML = "";
    
    if (taskList.length === 0) {
        DOM.tasksList.innerHTML = '<p class="empty-state-text">No tasks created yet. Create a task to organize your study session!</p>';
        return;
    }
    
    taskList.forEach(task => {
        const item = document.createElement("div");
        item.className = `task-item ${task.completed ? 'completed' : ''}`;
        
        // Task checkbox check icon
        const checkIcon = task.completed ? '<i class="fa-solid fa-check"></i>' : '';
        
        item.innerHTML = `
            <div class="task-item-left" onclick="toggleTaskCompletion(${task.id})">
                <div class="task-checkbox">${checkIcon}</div>
                <span class="task-title">${task.title}</span>
            </div>
            <button class="btn-delete-task" onclick="deletePlannerTask(event, ${task.id})">
                <i class="fa-solid fa-trash-can"></i>
            </button>
        `;
        
        DOM.tasksList.appendChild(item);
    });
}

async function handleCreateTask(e) {
    e.preventDefault();
    const title = DOM.taskTitleInput.value.trim();
    if (!title) return;
    
    try {
        const response = await fetch(`${API_BASE}/api/tasks`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-User-Id": currentUser.id
            },
            body: JSON.stringify({ title })
        });
        
        if (response.ok) {
            DOM.taskTitleInput.value = "";
            loadPlannerTasks();
        }
    } catch (err) {
        console.error(err);
    }
}

window.toggleTaskCompletion = async function(taskId) {
    try {
        const response = await fetch(`${API_BASE}/api/tasks/${taskId}`, {
            method: "PUT",
            headers: {
                "X-User-Id": currentUser.id
            }
        });
        
        if (response.ok) {
            // Find task in local state and toggle
            const idx = taskList.findIndex(t => t.id === taskId);
            if (idx !== -1) {
                taskList[idx].completed = taskList[idx].completed === 0 ? 1 : 0;
                renderTasks();
            }
        }
    } catch (err) {
        console.error(err);
    }
};

window.deletePlannerTask = async function(e, taskId) {
    e.stopPropagation();
    
    try {
        const response = await fetch(`${API_BASE}/api/tasks/${taskId}?user_id=${currentUser.id}`, {
            method: "DELETE"
        });
        
        if (response.ok) {
            taskList = taskList.filter(t => t.id !== taskId);
            renderTasks();
        }
    } catch (err) {
        console.error(err);
    }
};

// ================= SETTINGS ACTIONS =================
function loadSettingsInfo() {
    // Already populated on session load
}

async function handleClearData() {
    if (!confirm("This will permanently delete all your chats, logged moods, and planner tasks. Are you sure?")) return;
    
    try {
        // Simple client-side sweep and backend call to delete user chats
        for (const chat of chatsList) {
            await fetch(`${API_BASE}/api/chats/${chat.id}`, {
                method: "DELETE",
                headers: { "X-User-Id": currentUser.id }
            });
        }
        
        // Remove tasks
        for (const task of taskList) {
            await fetch(`${API_BASE}/api/tasks/${task.id}?user_id=${currentUser.id}`, {
                method: "DELETE"
            });
        }
        
        alert("All user data has been cleared.");
        
        // Reload session view
        chatsList = [];
        taskList = [];
        moodHistory = [];
        
        renderRecentChats();
        createNewChat();
        showTab("tab-chat");
        
    } catch (err) {
        console.error(err);
        alert("Error while clearing data.");
    }
}
