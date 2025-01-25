// Chatbot initialization
(function() {
    function initChatbot() {
        const toggle = document.getElementById('chat-toggle');
        const container = document.getElementById('chat-container');
        const closeBtn = document.getElementById('chat-close');
        
        if (!toggle || !container || !closeBtn) {
            console.warn('Chatbot elements not found');
            return;
        }

        function showChat() {
            container.style.display = 'flex';
        }

        function hideChat() {
            container.style.display = 'none';
        }

        toggle.addEventListener('click', function(e) {
            e.preventDefault();
            if (container.style.display === 'none') {
                showChat();
            } else {
                hideChat();
            }
            e.stopPropagation();
        });

        closeBtn.addEventListener('click', function(e) {
            hideChat();
            e.stopPropagation();
        });

        document.addEventListener('click', function(e) {
            if (!container.contains(e.target) && e.target !== toggle) {
                hideChat();
            }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initChatbot);
    } else {
        initChatbot();
    }
})(); 