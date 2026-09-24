import streamlit as st
import pandas as pd
from google.cloud import firestore
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="Monitoring Dashboard", layout="wide")
st.title("📊 Monitoring des jobs")

# 🔹 Connexion Firestore
db = firestore.Client.from_service_account_json("serviceAccountKey.json")

# 🔹 Récupération des jobs
jobs_ref = db.collection("jobs")
docs = jobs_ref.stream()

date_counts = {}
for doc in docs:
    d = doc.to_dict()
    date = d.get("DateSentStr", "inconnu")
    date_counts[date] = date_counts.get(date, 0) + 1

# 🔹 DataFrame trié
data = pd.DataFrame(list(date_counts.items()), columns=["Date", "Count"])
data["Date"] = pd.to_datetime(data["Date"], format="%d/%m/%Y", errors="coerce")
data = data.sort_values("Date").dropna()

# 🔹 Résumés
total_jobs = data["Count"].sum()
today = datetime.now().strftime("%d/%m/%Y")
jobs_today = date_counts.get(today, 0)

# 🔹 Indicateurs
col1, col2 = st.columns(2)
col1.metric("Total jobs", total_jobs)
col2.metric("Jobs today", jobs_today)

# 🔹 Graphique Matplotlib – style clair
plt.style.use("ggplot")

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(data["Date"], data["Count"], color="royalblue", linewidth=2.5, marker="o", markersize=6)
ax.fill_between(data["Date"], data["Count"], color="lightblue", alpha=0.3)

# 🔹 Mise en forme
ax.set_title("Évolution du nombre de jobs / jour", fontsize=16, fontweight="bold")
ax.set_xlabel("Date", fontsize=12)
ax.set_ylabel("Nombre de jobs", fontsize=12)
ax.tick_params(axis="x", rotation=45)
ax.grid(True, linestyle="--", alpha=0.7)

st.pyplot(fig)
