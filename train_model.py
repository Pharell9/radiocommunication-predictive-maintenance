import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# 1. Chargement des données
print("Chargement des données de télémétrie...")
df = pd.read_csv("telemetry_data.csv")

# 2. Sélection des variables explicatives (X) et de la cible (y)
features = ["temperature_c", "battery_level_v", "signal_strength_dbm", "packet_loss_pct", "encryption_latency_ms"]
X = df[features]
y = df["failure_risk"]

# 3. Séparation : 80% apprentissage / 20% test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. Entraînement du modèle Random Forest
print("Entraînement de l'IA en cours (Random Forest)...")
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# 5. Évaluation des performances
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\nPrécision du modèle (Accuracy) : {accuracy * 100:.2f}%")
print("\nRapport détaillé par classe (0=Sain, 1=Alerte, 2=Panne) :")
print(classification_report(y_test, y_pred))

# 6. Sauvegarde du modèle pour l'interface web
joblib.dump(model, "predictive_model.joblib")
print("Modèle sauvegardé sous 'predictive_model.joblib'. Prêt pour la production !")