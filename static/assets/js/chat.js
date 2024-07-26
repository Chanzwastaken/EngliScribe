document.getElementById('chat-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const messageInput = document.getElementById('message');
    const message = messageInput.value;

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `message=${encodeURIComponent(message)}`
    })
    .then(response => response.json())
    .then(data => {
        const chatBox = document.getElementById('chat-box');
        chatBox.innerHTML = '';  // Clear the chat box

        // Append chat history
        data.history.forEach(chat => {
            const chatMessage = document.createElement('div');
            chatMessage.classList.add('message');
            chatMessage.innerHTML = `<strong>${chat.sender}:</strong> ${chat.message} <div class="timestamp">${chat.timestamp}</div>`;
            chatBox.appendChild(chatMessage);
        });

        chatBox.scrollTop = chatBox.scrollHeight;
        messageInput.value = '';
    })
    .catch(error => console.error('Error:', error));
});
