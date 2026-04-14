document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatMessages');
    const messageInput = document.getElementById('messageInput');
    const sendBtn = document.getElementById('sendBtn');
    const quickBtns = document.querySelectorAll('.quick-btn');
    const exampleItems = document.querySelectorAll('.example-item');

    let isSending = false;

    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = isUser ? '👤' : '🤖';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const paragraphs = content.split('\n').filter(p => p.trim());
        paragraphs.forEach(p => {
            const pElement = document.createElement('p');
            pElement.textContent = p;
            messageContent.appendChild(pElement);
        });
        
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTyping() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'message bot-message typing-message';
        typingDiv.id = 'typingIndicator';
        
        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = '🤖';
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.innerHTML = '<p>AI正在思考...</p>';
        
        typingDiv.appendChild(avatar);
        typingDiv.appendChild(messageContent);
        
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function removeTyping() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    async function sendMessage(message) {
        if (!message.trim() || isSending) {
            return;
        }

        isSending = true;
        sendBtn.disabled = true;
        sendBtn.querySelector('.btn-text').style.display = 'none';
        sendBtn.querySelector('.btn-loading').style.display = 'inline';

        addMessage(message, true);
        messageInput.value = '';
        
        showTyping();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message
                })
            });

            const result = await response.json();

            removeTyping();

            if (result.success) {
                addMessage(result.reply);
            } else {
                addMessage('抱歉，我遇到了一些问题。请稍后重试。');
            }
        } catch (error) {
            console.error('发送消息失败:', error);
            removeTyping();
            addMessage('抱歉，网络连接出现问题。请检查您的网络连接后重试。');
        } finally {
            isSending = false;
            sendBtn.disabled = false;
            sendBtn.querySelector('.btn-text').style.display = 'inline';
            sendBtn.querySelector('.btn-loading').style.display = 'none';
        }
    }

    sendBtn.addEventListener('click', function() {
        const message = messageInput.value.trim();
        if (message) {
            sendMessage(message);
        }
    });

    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            const message = messageInput.value.trim();
            if (message) {
                sendMessage(message);
            }
        }
    });

    quickBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const question = this.dataset.question;
            if (question) {
                sendMessage(question);
            }
        });
    });

    exampleItems.forEach(item => {
        item.addEventListener('click', function() {
            const question = this.textContent.trim();
            if (question) {
                sendMessage(question);
            }
        });
    });

    messageInput.focus();
});
