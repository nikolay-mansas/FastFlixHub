const videoPlayer = document.getElementById('videoPlayer');

videoPlayer.addEventListener('timeupdate', () => {
    localStorage.setItem('lastTime', videoPlayer.currentTime);
});

window.onload = () => {
    const lastTime = localStorage.getItem('lastTime');
    if (lastTime) {
        videoPlayer.currentTime = parseFloat(lastTime);
    }
};