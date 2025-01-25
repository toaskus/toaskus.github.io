// Chatbot initialization
(function() {
    function initChatbot() {
        const toggle = document.getElementById('chat-toggle');
        const container = document.getElementById('chat-container');
        const closeBtn = document.getElementById('chat-close');
        const iframe = document.getElementById('chatbot-iframe');
        let isIframeLoaded = false;
        
        if (!toggle || !container || !closeBtn || !iframe) {
            console.warn('Chatbot elements not found');
            return;
        }

        function loadIframe() {
            if (!isIframeLoaded) {
                iframe.src = iframe.dataset.src;
                isIframeLoaded = true;
            }
        }

        function showChat() {
            container.style.display = 'flex';
            loadIframe();
            // 애니메이션을 위한 setTimeout
            setTimeout(() => {
                container.style.opacity = '1';
                container.style.transform = 'translateY(0)';
            }, 10);
        }

        function hideChat() {
            container.style.opacity = '0';
            container.style.transform = 'translateY(10px)';
            setTimeout(() => {
                container.style.display = 'none';
            }, 300);
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
            e.preventDefault();
            hideChat();
            e.stopPropagation();
        });

        // 채팅창 외부 클릭시 닫기
        document.addEventListener('click', function(e) {
            if (container.style.display !== 'none' && 
                !container.contains(e.target) && 
                e.target !== toggle) {
                hideChat();
            }
        });

        // 모바일에서 키보드가 올라올 때 위치 조정
        if ('visualViewport' in window) {
            window.visualViewport.addEventListener('resize', function() {
                if (window.visualViewport.height < window.innerHeight) {
                    container.style.bottom = '0';
                } else {
                    container.style.bottom = '90px';
                }
            });
        }
    }

    // DOM 로드 상태 확인 후 초기화
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initChatbot);
    } else {
        initChatbot();
    }
})(); 