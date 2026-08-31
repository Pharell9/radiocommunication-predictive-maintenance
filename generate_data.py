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

    print(f"Génération des données bruitées et réalistes pour {NUM_DEVICES} radios...")

    for device_id in range(1, NUM_DEVICES + 1):
        # 20% de chances de tomber en panne
        will_fail = np.random.choice([True, False], p=[0.05, 0.95])
        failure_start_hour = np.random.randint(TOTAL_RECORDS_PER_DEVICE - 48, TOTAL_RECORDS_PER_DEVICE) if will_fail else TOTAL_RECORDS_PER_DEVICE + 1

        for hour in range(TOTAL_RECORDS_PER_DEVICE):
            timestamp = start_date + timedelta(hours=hour)
            
            # Base : Comportement normal avec beaucoup de bruit statistique
            temp = np.random.normal(35, 4.0)  # Forte variance de température
            battery = max(0.0, 12.0 - (hour * np.random.normal(0.002, 0.0002))) # Décharge irrégulière
            signal = np.random.normal(-65, 8.0) 
            packet_loss = abs(np.random.normal(1, 1.5))
            latency = abs(np.random.normal(20, 5.0))
            risk_label = 0 # 0 = Sain

            # Comportement dégradé (Alerte - 48h avant panne)
            # Les données chevauchent fortement la classe normale (difficile à détecter)
            if will_fail and (failure_start_hour - 48 <= hour < failure_start_hour):
                risk_label = 1 # 1 = Alerte
                temp += np.random.normal(2, 4.0) 
                packet_loss += abs(np.random.normal(1.5, 3.0))
                latency += abs(np.random.normal(10, 6.0))
                signal -= np.random.normal(2, 5.0)
                
            # Panne critique imminente
            elif will_fail and hour >= failure_start_hour:
                risk_label = 2 # 2 = Panne
                temp += np.random.normal(15, 6.0)
                packet_loss += abs(np.random.normal(15, 6.0))
                latency += abs(np.random.normal(30, 10.0))
                signal -= np.random.normal(20, 8.0)

            # --- LE PIÈGE : Les anomalies passagères (Faux positifs) ---
            # 2% de chances qu'un capteur "bug" ou subisse un obstacle temporaire
            if np.random.random() < 0.02: 
                temp += np.random.normal(12, 3.0)       # Surchauffe soudaine
                packet_loss += np.random.normal(10, 4.0) # Grosse perte réseau
                # Note: Le label ne change pas ! C'est une anomalie, pas une vraie panne.

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
    print(f"Génération terminée ! Fichier 'telemetry_data.csv' recréé avec du chaos contrôlé.")

if __name__ == "__main__":
    generate_telemetry()
    