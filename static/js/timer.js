let timeLeft = 1800; // 30 min in seconds
const timerDisplay = document.getElementById("timer");

function updateTimer() {
    let minutes = Math.floor(timeLeft / 60);
    let seconds = timeLeft % 60;
    timerDisplay.innerText = `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
    timeLeft--;

    if (timeLeft < 0) {
        document.getElementById("examForm").submit(); // auto-submit
    }
}

setInterval(updateTimer, 1000);
