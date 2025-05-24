from xmlrpc.server import SimpleXMLRPCServer
from datetime import datetime
from Model.temperature import TemperatureSimulator

# On instancie la classe TemperatureSimulator qui gère la température + alertes
incubator = TemperatureSimulator()

class IncubatorRPC:
    def get_temperature(self):
        return incubator.get_temperature()

    def set_temperature(self, new_temp):
        message = incubator.set_temperature(new_temp)
        alert_message = incubator.check_alert()
        # On retourne message + éventuellement l’alerte pour info côté client
        return {"message": message, "alert": alert_message}

server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
server.register_instance(IncubatorRPC())
print("Serveur RPC démarré sur le port 8000...")
server.serve_forever()
