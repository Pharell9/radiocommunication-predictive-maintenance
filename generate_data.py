import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuration de la simulation
NUM_DEVICES = 100
DAYS = 30
HOURS_PER_DAY = 24
TOTAL_RECORDS_PER_DEVICE = DAYS * HOURS_PER_DAY

def generate_telemetry():
    data = []
    start_date = datetime.now() - timedelta(days=DAYS)

    print(f"Génération des données pour {NUM_DEVICES} radios...")

    for device_id in range(1, NUM_DEVICES + 1):
        # On décide aléatoirement si cette radio va subir une panne (20% de chances)
        will_fail = np.random.choice([True, False], p=[0.2, 0.8])
        failure_start_hour = np.random.randint(TOTAL_RECORDS_PER_DEVICE - 48, TOTAL_RECORDS_PER_DEVICE) if will_fail else TOTAL_RECORDS_PER_DEVICE + 1

        for hour in range(TOTAL_RECORDS_PER_DEVICE):
            timestamp = start_date + timedelta(hours=hour)
            
            # Comportement normal
            temp = np.random.normal(35, 2) # Température moyenne 35°C
            battery = max(10.0, 12.0 - (hour * 0.002)) # La batterie se décharge lentement
            signal = np.random.normal(-65, 5) # Signal autour de -65 dBm
            packet_loss = abs(np.random.normal(1, 0.5)) # 1% de perte environ
            latency = np.random.normal(20, 2) # 20ms de latence de chiffrement
            risk_label = 0 # 0 = Sain

            # Comportement dégradé (la radio approche d'une panne)
            if will_fail and hour >= failure_start_hour - 24:
                risk_label = 1 # 1 = Alerte (signaux faibles)
                temp += np.random.normal(10, 3) # Surchauffe
                packet_loss += np.random.normal(5, 2) # Perte de paquets augmente
                latency += np.random.normal(15, 5) # Le processeur de chiffrement rame
                
            # Panne critique imminente
            if will_fail and hour >= failure_start_hour:
                risk_label = 2 # 2 = Panne critique
                temp += np.random.normal(25, 5)
                packet_loss += np.random.normal(20, 5)
                signal -= np.random.normal(20, 5) # Chute du signal

            data.append([
                f"RADIO_{device_id:03d}",
                timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                round(temp, 2),
                round(battery, 2),
                round(signal, 2),
                round(packet_loss, 2),
                round(latency, 2),
                risk_label
            ])

    # Création du DataFrame
    columns = ["device_id", "timestamp", "temperature_c", "battery_level_v", "signal_strength_dbm", "packet_loss_pct", "encryption_latency_ms", "failure_risk"]
    df = pd.DataFrame(data, columns=columns)
    
    # Sauvegarde en CSV
    df.to_csv("telemetry_data.csv", index=False)
    print(f"Génération terminée ! Fichier 'telemetry_data.csv' créé avec {len(df)} lignes.")

if __name__ == "__main__":
    generate_telemetry()