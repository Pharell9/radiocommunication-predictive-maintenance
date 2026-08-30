import streamlit as st
import pandas as pd
import joblib
import plotly.express as px

# Configuration de la page
st.set_page_config(page_title="MCO Thales | Supervision IA", layout="wide")

# Chargement du modèle et des données en cache pour la rapidité
@st.cache_data
def load_data():
    return pd.read_csv("telemetry_data.csv")

@st.cache_resource
def load_model():
    return joblib.load("predictive_model.joblib")

df = load_data()
model = load_model()

st.title("📡 Centre de Contrôle MCO (Maintenance Prédictive)")
st.markdown("Surveillance des équipements de radiocommunication et anticipation des pannes par IA.")

# Sidebar : Sélection de l'équipement
st.sidebar.header("🎯 Filtres")
device_list = df["device_id"].unique()
selected_device = st.sidebar.selectbox("Sélectionner une Radio :", device_list)

# Filtrer les données pour la radio sélectionnée
device_data = df[df["device_id"] == selected_device].copy()

# Extraire les dernières constantes (dernière ligne temporelle)
latest_data = device_data.iloc[-1]
features = ["temperature_c", "battery_level_v", "signal_strength_dbm", "packet_loss_pct", "encryption_latency_ms"]
X_latest = pd.DataFrame([latest_data[features]])

# L'IA fait sa prédiction sur l'état ACTUEL
prediction = model.predict(X_latest)[0]

# Affichage du statut avec code couleur
st.header(f"Statut actuel : {selected_device}")

if prediction == 0:
    st.success("✅ État : SAIN - Fonctionnement nominal")
elif prediction == 1:
    st.warning("⚠️ État : ALERTE - Dégradation des signaux (Maintenance préventive conseillée)")
else:
    st.error("🚨 État : PANNE CRITIQUE IMMINENTE - Intervention immédiate requise")

# Métriques (KPIs) en temps réel
col1, col2, col3, col4 = st.columns(4)
col1.metric("Température", f"{latest_data['temperature_c']} °C")
col2.metric("Batterie", f"{latest_data['battery_level_v']} V")
col3.metric("Signal", f"{latest_data['signal_strength_dbm']} dBm")
col4.metric("Perte Paquets", f"{latest_data['packet_loss_pct']} %")

st.divider()

# Graphiques d'évolution
st.subheader("📊 Historique de télémétrie (30 derniers jours)")

# Création de deux colonnes pour les graphiques
g_col1, g_col2 = st.columns(2)

with g_col1:
    fig_temp = px.line(device_data, x="timestamp", y="temperature_c", title="Évolution de la Température (°C)", color_discrete_sequence=["#ff7f0e"])
    st.plotly_chart(fig_temp, use_container_width=True)
    
    fig_loss = px.line(device_data, x="timestamp", y="packet_loss_pct", title="Perte de Paquets (%)", color_discrete_sequence=["#d62728"])
    st.plotly_chart(fig_loss, use_container_width=True)

with g_col2:
    fig_batt = px.line(device_data, x="timestamp", y="battery_level_v", title="Niveau de Batterie (V)", color_discrete_sequence=["#2ca02c"])
    st.plotly_chart(fig_batt, use_container_width=True)
    
    fig_sig = px.line(device_data, x="timestamp", y="signal_strength_dbm", title="Puissance du Signal (dBm)", color_discrete_sequence=["#1f77b4"])
    st.plotly_chart(fig_sig, use_container_width=True)