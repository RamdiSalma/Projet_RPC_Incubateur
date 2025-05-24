let alertActive = false;
let audio = new Audio('/static/bip.mp3');
audio.loop = true;

const warningDiv = document.getElementById("temperature-warning");


let temperatureHistory = [];

const temperatureData = {
    labels: [],
    datasets: [{
        label: 'Température (°C)',
        data: [],
        borderColor: 'rgba(255, 99, 132, 1)',
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        fill: true,
        tension: 0.3,
    }]
};

const ctx = document.getElementById('tempChart').getContext('2d');

const config = {
    type: 'line',
    data: temperatureData,
    options: {
        responsive: true,
        scales: {
            y: {
                suggestedMin: 20,
                suggestedMax: 50,
                title: { display: true, text: 'Température (°C)' }
            },
            x: {
                title: { display: true, text: 'Heure' }
            }
        }
    }
};

const salesChart = new Chart(ctx, config);

function updateStats() {
    if (temperatureHistory.length === 0) return;

    const min = Math.min(...temperatureHistory).toFixed(1);
    const max = Math.max(...temperatureHistory).toFixed(1);
    const sum = temperatureHistory.reduce((a, b) => a + b, 0);
    const avg = (sum / temperatureHistory.length).toFixed(1);

    document.getElementById('tempMin').textContent = min;
    document.getElementById('tempMax').textContent = max;
    document.getElementById('tempAvg').textContent = avg;
}

function fetchTemperature() {
    fetch('/get_temperature')
        .then(response => response.json())
        .then(data => {
            const temperatureDisplay = document.getElementById("temperature");
            temperatureDisplay.textContent = data.temperature + " °C";

          
            temperatureHistory.push(data.temperature);

            
            if (temperatureHistory.length > 100) {
                temperatureHistory.shift();
            }

            
            updateStats();

            const now = new Date();
            const timeLabel = now.getHours() + ":" + now.getMinutes() + ":" + now.getSeconds();

            temperatureData.labels.push(timeLabel);
            temperatureData.datasets[0].data.push(data.temperature);

            if (temperatureData.labels.length > 10) {
                temperatureData.labels.shift();
                temperatureData.datasets[0].data.shift();
            }

            salesChart.update();

            
            if (data.temperature >= 37.5 || data.temperature <= 35.5) {
                if (!alertActive) {
                    alertActive = true;
                    audio.play().catch(error => console.error("Erreur audio :", error));

                    warningDiv.textContent = data.temperature >= 37.5
                        ? "⚠️ Température trop élevée !"
                        : "⚠️ Température trop basse !";
                    warningDiv.classList.remove("hidden");
                    warningDiv.classList.add("blinking");
                }
            } else {
                if (alertActive) {
                    alertActive = false;
                    audio.pause();
                    audio.currentTime = 0;
                    warningDiv.classList.add("hidden");
                    warningDiv.classList.remove("blinking");
                    warningDiv.textContent = "";
                }
            }
        })
        .catch(error => console.error("Erreur en récupérant la température :", error));
}

setInterval(fetchTemperature, 3000);

function setTemperature() {
    const val = document.getElementById('new-temp').value;
    fetch('/set_temperature', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ temperature: val })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
    });
}
