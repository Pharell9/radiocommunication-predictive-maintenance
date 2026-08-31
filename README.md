# 📡 POC : MCO & Maintenance Prédictive pour Systèmes Critiques
![Démo Dashboard](illustration.png)

Copilote de supervision IA conçu pour anticiper les pannes des équipements de radiocommunication militaire. Il analyse les séries temporelles de télémétrie pour passer d'une maintenance réactive à une approche préventive et prédictive.

🚀 **[Démo live : Accéder au Centre de Contrôle MCO](https://radiocommunication-predictive-maintenance-bypharell9.streamlit.app/)**

---

## 🎯 Contexte & Motivation
Le Maintien en Condition Opérationnelle (MCO) des équipements de radiocommunication est un enjeu vital. Une panne sur le terrain entraîne une rupture de la continuité des missions. Ces équipements (radios, réseaux LAN, chiffreurs) génèrent des milliers de points de données sous-exploités.

Ce projet propose un tableau de bord intelligent qui surveille l'état de santé de la flotte et utilise le Machine Learning pour repérer les signaux faibles (surchauffe, perte de paquets, chute de tension) avant la panne.

* **Cas d'usage cible :** Industrie de la Défense et Télécommunications (équipes de soutien opérationnel cherchant à fiabiliser des systèmes critiques).
* **Statut du projet :** POC fonctionnel. L'architecture démontre la chaîne de valeur complète : Ingestion de données temporelles ➔ Inférence ML ➔ Visualisation d'aide à la décision.

---

## 🏗️ Architecture

```text
┌─────────────────────┐
│  Sondes Équipements │  Génération de télémétrie synthétique
│  (Radios tactiques) │  (Température, Batterie, Signal, Latence)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    generate_data.py │  Création du dataset 'telemetry_data.csv'
│                     │  (72 000 relevés horaires / 100 radios)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    Scikit-Learn     │  Entraînement : Random Forest Classifier
│   (train_model.py)  │  (Séparation 80% Train / 20% Test)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Joblib (Export)   │  Modèle sérialisé : predictive_model.joblib
└──────────┬──────────┘
           │
           ▼   ┌─── Interface Utilisateur ───┐
           │   │                             │
           ▼   ▼                             │
┌─────────────────────┐                      │
│    Streamlit App    │ ◄────────────────────┘
│  (Dashboard MCO)    │  Filtres par radio, KPI temps réel
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Alertes & Graphes  │  Statut (Sain / Alerte / Panne) + Courbes
└─────────────────────┘

🚀 Stack technique
Composant,Choix technique,Justification
Génération Données,"Pandas, NumPy",Manipulation optimisée des DataFrames et calcul vectoriel
Machine Learning,Scikit-Learn (Random Forest),"Robuste, performant sur les données tabulaires, et interprétable (vital pour la Défense)"
Sérialisation,Joblib,Export léger du modèle pré-entraîné pour des inférences à faible latence
Interface (C2),"Streamlit, Plotly",Prototypage rapide d'un centre de contrôle avec visualisation dynamique des Time Series
💡 Pourquoi cette stack pour un passage en production ?

Interprétabilité : Contrairement au Deep Learning ("boîte noire"), les algorithmes ensemblistes comme Random Forest permettent d'extraire l'importance des variables (Feature Importance), aidant les techniciens à comprendre pourquoi l'IA alerte.

Séparation des préoccupations : Le modèle est entraîné hors ligne (train_model.py) et l'inférence est servie de manière indépendante (app.py), une architecture compatible avec un déploiement MLOps (via API FastAPI).

📂 Structure du projet
thales-predictive-maintenance/
├── generate_data.py          # Script de génération de la télémétrie (injection d'anomalies)
├── train_model.py            # Script d'entraînement et d'évaluation du Random Forest
├── app.py                    # Tableau de bord interactif (Streamlit)
├── telemetry_data.csv        # Dataset généré (72 000 relevés horaires)
├── predictive_model.joblib   # Modèle Machine Learning sérialisé
├── requirements.txt          # Dépendances Python
└── README.md                 # Documentation

🛠️ Installation & Exécution locale
Prérequis : Python 3.11+

1. Cloner le repository
git clone https://github.com/Pharell9/radiocommunication-predictive-maintenance.git
cd radiocommunication-predictive-maintenance
2. Environnement virtuel et dépendances
python -m venv venv
# Windows : venv\Scripts\activate | Mac/Linux : source venv/bin/activate
pip install -r requirements.txt
3. (Optionnel) Régénérer les données et réentraîner le modèle
python generate_data.py
python train_model.py
4. Lancer le tableau de bord
python -m streamlit run app.py

📊 Résultats & Évaluation
Précision du modèle (Accuracy) : 100 %
Note de transparence : Ce score parfait est assumé. Il s'explique par la nature synthétique et déterministe du jeu de données (les anomalies suivent des règles mathématiques programmées dans generate_data.py). L'objectif de ce POC est de valider l'architecture logicielle de bout en bout. Sur le terrain, face à des données bruitées, le score s'ajusterait naturellement, mais l'architecture de supervision resterait identique.

⚠️ Limites actuelles
Limites de la modélisation (Data Science)

Absence de séquentialité temporelle : Le modèle actuel évalue le risque sur la base d'une observation à un instant T. Une approche par fenêtre glissante (Rolling Window) ou un modèle récurrent (LSTM) serait nécessaire pour capter la dynamique d'une dégradation.

Données synthétiques : Dans un environnement industriel, les données des sondes nécessiteraient une étape complexe de Feature Engineering et de lissage (Filtre de Kalman).

Limites d'architecture (Data Engineering)

Inférence statique : L'application lit un fichier CSV statique. Dans un vrai centre de contrôle, les données arriveraient en flux continu (Data Streaming).

Pas de gestion MLOps : Le cycle de vie du modèle n'est pas versionné (absence d'outils comme MLflow).

🗺️ Roadmap & Améliorations futures
🎯 Priorité haute (v1.1 — Modélisation)

Implémentation d'une approche par séries temporelles avec création de variables retardées (lag features).

Ajout d'une analyse SHAP Values dans l'interface pour expliquer visuellement la décision de l'IA.

🎯 Priorité moyenne (v2.0 — Data Temps Réel)

Simulation d'un flux de données en continu via Apache Kafka ou un broker MQTT (protocole IoT industriel).

Bascule vers une base de données orientée séries temporelles (InfluxDB).

🎯 Priorité basse (v3.0 — MLOps)

Mise en place d'un pipeline d'entraînement automatisé avec MLflow.

Système de Webhook pour envoyer des alertes email/SMS aux techniciens d'astreinte.

👤 Auteur
Guy Pharell KAMGANG SIMO — Étudiant Ingénieur en Big Data & Intelligence Artificielle (ECE Paris)

📧 Email : pharellkamgang@gmail.com

🔗 LinkedIn : Guy Pharell KAMGANG SIMO

🐙 GitHub : @Pharell9

📜 Licence MIT. Fait pour explorer les applications de la Data Science dans le maintien en condition opérationnelle (MCO).
