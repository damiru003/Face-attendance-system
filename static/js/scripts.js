document.addEventListener('DOMContentLoaded', () => {
    const video = document.querySelector('.video-container img');
    if (video) {
        setInterval(() => {
            const message = document.getElementById('detection-message');
            if (message) {
                message.style.opacity = message.style.opacity === '0' ? '1' : '0';
                message.style.transition = 'opacity 0.5s';
            }
        }, 2000); // Blink every 2 seconds
    }
});