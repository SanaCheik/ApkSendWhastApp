
import pandas as pd
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def envoyer_fichiers(excel_path, dossier_fichiers, capture_dir, message, fichier_stats):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://web.whatsapp.com")
    WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CSS_SELECTOR, "canvas")))

    df = pd.read_excel(excel_path)
    df = df[['A', 'B']].rename(columns={'A': 'cle', 'B': 'numero'})
    df['numero'] = df['numero'].astype(str).str.replace(r'\D', '', regex=True)
    df['numero_complet'] = '+226' + df['numero']
    resultats = []

    for index, row in df.iterrows():
        try:
            numero = str(row['numero']).replace(' ', '').strip()
            cle = str(row['cle']).strip()
            fichier_path = os.path.join(dossier_fichiers, cle + ".pdf")
            if not os.path.isfile(fichier_path):
                resultats.append((numero, cle, "Numéro non WhatsApp"))
                continue

            driver.get(f"https://web.whatsapp.com/send?phone={numero}&text={message}")

            bouton_plus = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//button[@title="Joindre"]'))
            )
            bouton_plus.click()

            bouton_document = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//input[@accept="*"]'))
            )
            bouton_document.send_keys(fichier_path)

            bouton_envoyer = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//div[@aria-label="Envoyer"]'))
            )
            bouton_envoyer.click()

            time.sleep(2)
            resultats.append((numero, cle, "Envoyé"))
        except Exception as e:
            resultats.append((row.get('numero', 'inconnu'), row.get('cle', 'inconnu'), f"Erreur: {str(e)}"))
            continue

    df_resultats = pd.DataFrame(resultats, columns=["Numero", "Cle", "Statut"])
    df_resultats.to_excel(fichier_stats, index=False)
    driver.quit()
