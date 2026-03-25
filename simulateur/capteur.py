import paho.mqtt.client as mqtt
import json, time, random

# Configuration
BROKER = "localhost"
PORT   = 1883

CAPTEURS = [
    { "id": "air_01",    "topic": "angers/air/capteur_01/data",
      "min": 80,  "max": 260, "unite": "ug/m3", "seuil": 200 },
    { "id": "trafic_01", "topic": "angers/trafic/capteur_01/data",
      "min": 0,   "max": 120, "unite": "vh/min","seuil": 100 },
    { "id": "dechet_01", "topic": "angers/dechet/capteur_01/data",
      "min": 0,   "max": 100, "unite": "%",     "seuil": 80  },
]

client = mqtt.Client()
client.connect(BROKER, PORT)

print("Simulateur demarre - publication toutes les 5 secondes")
print("Ctrl+C pour arreter")

while True:
    for capteur in CAPTEURS:
        valeur = round(random.uniform(capteur["min"], capteur["max"]), 2)
        message = {
            "capteur_id": capteur["id"],
            "valeur":     valeur,
            "unite":      capteur["unite"],
            "seuil":      capteur["seuil"],
            "alerte":     valeur > capteur["seuil"],
            "timestamp":  time.time()
        }
        client.publish(capteur["topic"], json.dumps(message))
        statut = "ALERTE" if message["alerte"] else "OK"
        print(f"[{capteur['id']}] {valeur} {capteur['unite']} {statut}")
    print("---")
    time.sleep(5)
