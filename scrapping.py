from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class MagentoAssistant:
    def __init__(self):
        # 1. Configurația inițială
        self.url = 'https://domeniu.ro/'  # Sau URL-ul de login Loken
        self.driver = None # Robotul nu este pornit încă
        
        # 2. Setări Browser
        self.chrome_options = Options()
        # self.chrome_options.add_argument('--headless') # Dezactivat pentru a putea vedea site-ul
        self.chrome_options.add_argument('--start-maximized')

    def pornire_robot(self):
        """Metodă dedicată lansării browserului."""
        print(" Se lansează Chrome...")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 15)

    def deschide_si_vezi(self):
        """Navigare protejată de blocul try-except."""
        if not self.driver:
            self.pornire_robot()

        try:
            print(f" Navigăm către: {self.url}")
            # CORECȚIE: Folosim self.driver.get, nu webdriver.get
            self.driver.get(self.url)
            
            # Așteptăm să apară un element cheie (ex: logo-ul) pentru a confirma încărcarea
            print(" Pagina a fost încărcată. Verifică structura!")
            time.sleep(10) # Timp de observație vizuală

        except Exception as e:
            print(f" Eroare la navigare: {e}")

    def intra_in_frame(self, selector_frame):
        """Logica de 'sărit gardul' într-un Iframe (esențial pentru Magento/Loken)."""
        try:
            print(f" Încercăm să intrăm în frame: {selector_frame}")
            # Așteptăm ca frame-ul să fie disponibil și comutăm automat
            self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, selector_frame)))
            print(" Focusul este acum în interiorul frame-ului.")
        except Exception as e:
            print(f" Nu am putut găsi frame-ul: {e}")

    def iesi_la_suprafata(self):
        """Revenirea la conținutul principal al paginii."""
        if self.driver:
            self.driver.switch_to.default_content()
            print("🔙 Focus revenit la pagina principală.")

    def inchide_tot(self):
        if self.driver:
            self.driver.quit()
            print(" Browser închis.")

# --- EXECUTARE ---
if __name__ == "__main__":
    bot = MagentoAssistant()
    bot.deschide_si_vezi()
    
    
