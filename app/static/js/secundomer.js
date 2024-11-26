let stopwatchInterval = null;
let stopwatchTime = 0;
let clicked = false;

function startStopwatch() {
    if (clicked) {
        location.href = '/profile/end-test';
    }
    else if (!clicked) {
        stopwatchInterval = setInterval(updateStopwatch, 1000);
        document.getElementById("start").innerHTML = 'Закончить тест';
        location.href = '/profile/start-test';
        clicked = true;
    }
}


function updateStopwatch() {
    stopwatchTime++;
    const minutes = Math.floor(stopwatchTime / 60);
    const seconds = stopwatchTime % 60;
    document.getElementById("stopwatch").innerText = `Время: ${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}