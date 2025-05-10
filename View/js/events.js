const ctx = document.getElementById('salesChart').getContext('2d');

const salesChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    datasets: [{
      label: 'Monthly Sales',
      data: [150, 370, 190, 310, 180, 160, 290, 170, 200, 340, 250, 100],
      backgroundColor: '#6366f1'
    }]
  },
  options: {
    responsive: true,
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});

/* temperateur */
const thermometerFill = document.getElementById('thermometerFill');
const thermometerBulb = document.getElementById('thermometerBulb');
const temperatureSlider = document.getElementById('temperatureSlider');
const temperatureValueDisplay = document.getElementById('temperatureValue');
const temperatureIndicator = document.getElementById('temperatureIndicator');

temperatureSlider.addEventListener('input', function() {
    const temperature = parseInt(this.value);
    updateThermometer(temperature);
});

function updateThermometer(temperature) {
    // Assurer que la température reste dans la nouvelle plage 20-50
    const clampedTemperature = Math.max(20, Math.min(temperature, 50));

    // Calculer le pourcentage de remplissage (échelle de 20 à 50, soit 30 unités)
    const percentage = ((clampedTemperature - 20) / 30) * 100;

    thermometerFill.style.height = `${percentage}%`;
    thermometerFill.textContent = `${clampedTemperature}°C`;
    temperatureValueDisplay.textContent = `Température: ${clampedTemperature}°C`;

    // Vérifier si la température est dans la plage "correcte" (35-37)
    if (clampedTemperature >= 35 && clampedTemperature <= 37) {
        thermometerFill.classList.add('correct-temperature');
        thermometerBulb.classList.add('correct-temperature');
        temperatureIndicator.textContent = "Température correcte";
        temperatureIndicator.classList.add('correct');
    } else {
        thermometerFill.classList.remove('correct-temperature');
        thermometerBulb.classList.remove('correct-temperature');
        temperatureIndicator.textContent = "";
        temperatureIndicator.classList.remove('correct');
    }
}

// Initialiser le thermomètre avec la valeur par défaut du curseur
updateThermometer(parseInt(temperatureSlider.value));
