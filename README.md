# Dashboard Monitoring

Petit tableau de bord Streamlit affichant le nombre de jobs exécutés par jour à partir d'une base Firestore : indicateurs (total de jobs, jobs du jour) et graphique d'évolution.

## Stack

- Python
- Streamlit
- Google Cloud Firestore
- pandas / matplotlib

## Usage

Nécessite un fichier de clé de compte de service Google Cloud (non versionné) pour se connecter à Firestore, puis :

```
streamlit run app.py
```
