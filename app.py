
import streamlit as st
from app_logic import envoyer_fichiers
import tempfile
import os

st.title("📤 Envoi de fichiers WhatsApp")

excel_file = st.file_uploader("📄 Charger le fichier Excel", type=["xlsx"])
dossier_fichiers = st.text_input("📁 Chemin vers le dossier des fichiers à envoyer")
capture_dir = st.text_input("📸 Chemin vers le dossier de captures (si besoin)")
message = st.text_area("📝 Message à envoyer", height=200)
fichier_stats = st.text_input("📊 Chemin vers le fichier Excel pour sauvegarder les statistiques", value="resultats_envoi.xlsx")

if st.button("🚀 Lancer l'envoi"):
    if excel_file and dossier_fichiers and message and fichier_stats:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(excel_file.read())
            tmp_path = tmp.name

        st.info("⏳ Lancement de l'envoi... Veuillez scanner le QR code WhatsApp si demandé.")
        envoyer_fichiers(tmp_path, dossier_fichiers, capture_dir, message, fichier_stats)
        st.success("✅ Envoi terminé. Les résultats sont enregistrés dans : " + fichier_stats)
    else:
        st.warning("⚠️ Merci de remplir tous les champs requis.")
