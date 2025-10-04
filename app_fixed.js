// Fixed Chat Application JavaScript

class ChatApp {
    constructor() {
        this.ws = null;
        this.nickname = '';
        this.isConnected = false;
        this.typingTimeout = null;
        this.isTyping = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        
        // DOM Elements
        this.loginScreen = document.getElementById('login-screen');
        this.chatContainer = document.getElementById('chat-container');
        this.nicknameInput = document.getElementById('nickname-input');
        this.joinBtn = document.getElementById('join-btn');
        this.loginError = document.getElementById('login-error');
        this.messagesContainer = document.getElementById('messages-container');
        this.messageInput = document.getElementById('message-input');
        this.sendBtn = document.getElementById('send-btn');
        this.userList = document.getElementById('user-list');
        this.userCount = document.getElementById('user-count');
        this.currentUserNickname = document.getElementById('current-user-nickname');
        this.connectionStatus = document.getElementById('connection-status');
        this.sidebarStatus = document.getElementById('sidebar-status');
        this.typingIndicator = document.getElementById('typing-indicator');
        this.logoutBtn = document.getElementById('logout-btn');
        
        this.initEventListeners();
    }
    
    initEventListeners() {
        // Join button click
        this.joinBtn.addEventListener('click', () => this.joinChat());
        
        // Enter key on nickname input
        this.nicknameInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.joinChat();
            }
        });
        
        // Send button click
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        // Enter key on message input
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        
        // Typing indicator
        this.messageInput.addEventListener('input', () => {
            this.handleTyping();
        });
        
        // Logout button
        this.logoutBtn.addEventListener('click', () => this.logout());
    }
    
    joinChat() {
        const nickname = this.nicknameInput.value.trim();
        
        if (!nickname) {
            this.showLoginError('Please enter a nickname');
            return;
        }
        
        if (nickname.length < 2) {
            this.showLoginError('Nickname must be at least 2 characters');
            return;
        }
        
        this.nickname = nickname;
        this.connectWebSocket();
    }
    
    connectWebSocket() {
        try {
            // Try to connect to the WebSocket server
            const wsUrl = 'wss://8765-566bbffc-be5f-4b4b-9f91-e404e1f921df.proxy.daytona.works';
            console.log('Attempting to connect to WebSocket:', wsUrl);
            
            this.ws = new WebSocket(wsUrl);
            
            this.ws.onopen = () => {
                console.log('✅ WebSocket connected successfully!');
                this.handleWebSocketOpen();
            };
            
            this.ws.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    console.log('📨 Received message:', data);
                    this.handleMessage(data);
                } catch (e) {
                    console.error('Error parsing message:', e);
                }
            };
            
            this.ws.onerror = (error) => {
                console.error('❌ WebSocket error:', error);
                this.showLoginError('Cannot connect to chat server. The server might be experiencing issues.');
            };
            
            this.ws.onclose = () => {
                console.log('🔌 WebSocket connection closed');
                this.isConnected = false;
                this.updateConnectionStatus(false);
                if (this.chatContainer.classList.contains('active')) {
                    this.addSystemMessage('Connection lost. Please refresh the page to reconnect.');
                }
            };
            
        } catch (error) {
            console.error('💥 Connection failed:', error);
            this.showLoginError('Failed to connect to server: ' + error.message);
        }
    }
    
    handleWebSocketOpen() {
        console.log('🎉 WebSocket connection established!');
        this.isConnected = true;
        this.updateConnectionStatus(true);
        
        // Send join message
        this.sendToServer({
            type: 'join',
            nickname: this.nickname
        });
        
        // Switch to chat interface
        this.showChatInterface();
    }
    
    sendToServer(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            const message = JSON.stringify(data);
            console.log('📤 Sending message:', message);
            this.ws.send(message);
        } else {
            console.warn('⚠️ WebSocket not connected, cannot send:', data);
        }
    }
    
    handleMessage(data) {
        switch (data.type) {
            case 'message':
                this.addChatMessage(data.nickname, data.text, data.timestamp);
                break;
            case 'system':
                this.addSystemMessage(data.text, data.timestamp);
                break;
            case 'user_list':
                this.updateUserList(data.users);
                break;
            case 'typing':
                this.showTypingIndicator(data.nickname, data.is_typing);
                break;
            default:
                console.log('🤔 Unknown message type:', data.type);
        }
    }
    
    sendMessage() {
        const text = this.messageInput.value.trim();
        
        if (!text || !this.isConnected) {
            return;
        }
        
        this.sendToServer({
            type: 'message',
            text: text
        });
        
        this.messageInput.value = '';
        this.stopTyping();
    }
    
    addChatMessage(nickname, text, timestamp) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message';
        
        if (nickname === this.nickname) {
            messageDiv.classList.add('own');
        }
        
        messageDiv.innerHTML = `
            <div class="message-header">
                <span class="message-nickname">${this.escapeHtml(nickname)}</span>
                <span class="message-time">${timestamp}</span>
            </div>
            <div class="message-text">${this.escapeHtml(text)}</div>
        `;
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    addSystemMessage(text, timestamp = '') {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message system';
        
        messageDiv.innerHTML = `
            <div class="message-text">
                ${this.escapeHtml(text)}
                ${timestamp ? `<span style="margin-left: 10px; opacity: 0.7;">${timestamp}</span>` : ''}
            </div>
        `;
        
        this.messagesContainer.appendChild(messageDiv);
        this.scrollToBottom();
    }
    
    updateUserList(users) {
        this.userList.innerHTML = '';
        this.userCount.textContent = users.length;
        
        users.forEach(user => {
            const li = document.createElement('li');
            li.className = 'user-item';
            li.textContent = user;
            this.userList.appendChild(li);
        });
    }
    
    handleTyping() {
        if (!this.isConnected) return;
        
        if (!this.isTyping) {
            this.isTyping = true;
            this.sendToServer({
                type: 'typing',
                is_typing: true
            });
        }
        
        clearTimeout(this.typingTimeout);
        this.typingTimeout = setTimeout(() => {
            this.stopTyping();
        }, 1000);
    }
    
    stopTyping() {
        if (this.isTyping && this.isConnected) {
            this.isTyping = false;
            this.sendToServer({
                type: 'typing',
                is_typing: false
            });
        }
    }
    
    showTypingIndicator(nickname, isTyping) {
        if (isTyping && nickname !== this.nickname) {
            this.typingIndicator.textContent = `${nickname} is typing...`;
        } else {
            this.typingIndicator.textContent = '';
        }
    }
    
    showChatInterface() {
        console.log('🎨 Switching to chat interface');
        this.loginScreen.style.display = 'none';
        this.chatContainer.classList.add('active');
        this.currentUserNickname.textContent = this.nickname;
        this.messageInput.disabled = false;
        this.sendBtn.disabled = false;
        this.messageInput.focus();
        
        // Add welcome message
        this.addSystemMessage(`Welcome to the chat, ${this.nickname}!`);
    }
    
    updateConnectionStatus(connected) {
        const statusElements = [this.connectionStatus, this.sidebarStatus];
        
        statusElements.forEach(element => {
            if (connected) {
                element.textContent = 'Connected';
                element.className = 'connection-status connected';
            } else {
                element.textContent = 'Disconnected';
                element.className = 'connection-status disconnected';
            }
        });
        
        this.messageInput.disabled = !connected;
        this.sendBtn.disabled = !connected;
    }
    
    showLoginError(message) {
        console.error('❌ Login error:', message);
        this.loginError.textContent = message;
        this.loginError.style.display = 'block';
        
        setTimeout(() => {
            this.loginError.style.display = 'none';
        }, 5000);
    }
    
    logout() {
        if (confirm('Are you sure you want to leave the chat?')) {
            if (this.ws) {
                this.ws.close();
            }
            location.reload();
        }
    }
    
    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Initialize the app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 Chat application initializing...');
    new ChatApp();
});