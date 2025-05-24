from datetime import datetime
from Model.database import insert_alerte

class TemperatureSimulator:
    def __init__(self):
        self.temperature = 37.0
        self.last_alert = None

    def get_temperature(self):
        return round(self.temperature, 2)

    def set_temperature(self, new_temp):
        self.temperature = float(new_temp)
        return f"Température réglée à {self.temperature} °C"

    def check_alert(self):
        if self.temperature < 35.5:
            if self.last_alert != "low":
                self.last_alert = "low"
                self.log_alert("Trop basse")
            return "⚠️ Température trop basse !"
        elif self.temperature > 37.5:
            if self.last_alert != "high":
                self.last_alert = "high"
                self.log_alert("Trop élevée")
            return "⚠️ Température trop élevée !"
        else:
            self.last_alert = None
            return None

   