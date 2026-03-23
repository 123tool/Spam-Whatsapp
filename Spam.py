import os
import random
import logging
import time
from typing import List, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION CLASS ---
class Config:
    SESSION_DIR = "wa_pro_session"
    TARGET_PHONE = "628383872084"
    MESSAGE = "Halo Bro, ini transmisi Pro Sentinel."
    COUNT = 10
    BASE_DELAY = 1.5
    # List Fallback XPaths untuk Input Pesan
    XPATH_INPUTS = [
        '//div[@contenteditable="true"][@data-tab="10"]',
        '//footer//div[@contenteditable="true"]',
        '//div[@aria-label="Ketik pesan"]',
        '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
    ]

# --- LOGGING ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger("WA-PRO")

class WhatsAppSentinel:
    def __init__(self):
        self.driver = self._setup_driver()
        self.wait = WebDriverWait(self.driver, 35)

    def _setup_driver(self):
        options = Options()
        options.add_argument(f"--user-data-dir={os.path.join(os.getcwd(), Config.SESSION_DIR)}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--start-maximized")
        # Anti-detection fingerprinting
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        # Menghapus jejak bot di navigator
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    def get_input_box(self):
        """Mencoba berbagai XPath untuk menemukan kotak pesan."""
        for xpath in Config.XPATH_INPUTS:
            try:
                element = self.wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
                if element:
                    return element
            except:
                continue
        return None

    def login(self):
        self.driver.get("https://web.whatsapp.com")
        logger.info("Silahkan Scan QR jika belum login...")
        # Tunggu sampai elemen 'side' (daftar chat) muncul
        self.wait.until(EC.presence_of_element_located((By.ID, "side")))
        logger.info("Login Terdeteksi!")

    def send_broadcast(self, phone: str, text: str, total: int):
        url = f"https://web.whatsapp.com/send?phone={phone}"
        logger.info(f"Membuka jalur komunikasi ke: {phone}")
        self.driver.get(url)

        # Tunggu box muncul
        input_box = self.get_input_box()
        if not input_box:
            logger.error("Gagal menemukan kotak pesan. Cek koneksi atau nomor.")
            return

        for i in range(1, total + 1):
            try:
                # Tambahkan variasi pesan agar tidak dianggap duplikat oleh filter WA
                final_msg = f"{text} [{random.getrandbits(16)}]"
                
                # Fokus dan ketik
                input_box.click()
                input_box.send_keys(final_msg + Keys.ENTER)
                
                # Human Jitter (Sangat Penting untuk Keamanan)
                jitter = Config.BASE_DELAY + random.uniform(0.5, 2.0)
                logger.info(f"✅ [{i}/{total}] Pesan terkirim. Jeda: {jitter:.2f}s")
                time.sleep(jitter)
            except Exception as e:
                logger.warning(f"⚠️ Gangguan pada pesan ke-{i}: {e}")
                # Re-fetch input box jika error (misal page refresh)
                input_box = self.get_input_box()

if __name__ == "__main__":
    bot = WhatsAppSentinel()
    try:
        bot.login()
        bot.send_broadcast(Config.TARGET_PHONE, Config.MESSAGE, Config.COUNT)
    except KeyboardInterrupt:
        logger.info("Proses dihentikan paksa.")
    finally:
        print("\n[INFO] Driver tetap aktif untuk pengecekan manual.")
