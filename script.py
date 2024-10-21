from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

# Initialiser le driver (assurez-vous d'avoir téléchargé ChromeDriver)
driver = webdriver.Chrome(service=webdriver.chrome.service.Service(r'C:\Program Files (x86)\chromedriver\chromedriver.exe'))

# Accéder à la page de la grille de trottinettes
driver.get('https://fr-fr.segway.com/kickscooter-comparison')

# Attendre que la page charge complètement
time.sleep(3)

# Trouver tous les boutons "learn more" sur la page
boutons_details = driver.find_elements(By.XPATH, "//button[contains(text(), 'learn more')]")

# Initialiser une liste pour stocker les données
data = []

# Boucler sur chaque bouton et collecter les données
for bouton in boutons_details:
    try:
        bouton.click()
        time.sleep(2)  # Attendre que les détails se chargent

        # Scraper les données de la page actuelle
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Récupérer les spécifications
        specifications_section = soup.find('section', {'id': 'specifications'})
        if specifications_section:
            specifications = specifications_section.find_all('div', class_='specification')
            spec_data = {}
            
            for spec in specifications:
                try:
                    key = spec.find('span', class_='key').text.strip()
                    value = spec.find('span', class_='value').text.strip()
                    spec_data[key] = value
                except AttributeError:
                    continue

            # Ajouter les données dans la liste
            data.append(spec_data)

        # Revenir en arrière pour retourner à la grille
        driver.back()
        time.sleep(2)
    except Exception as e:
        print(f"Erreur lors de la collecte des données : {e}")
        continue

# Convertir les données en DataFrame pandas
df = pd.DataFrame(data)

# Afficher ou enregistrer les données
print(df)
df.to_csv('trottinettes.csv', index=False)

# Fermer le navigateur
driver.quit()
