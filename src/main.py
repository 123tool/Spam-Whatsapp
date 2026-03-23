import os
import random
import logging
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- LOGGING SETUP ---
if not os.path.exists('logs'): os.makedirs('logs')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.FileHandler("logs/sentinel.log"), logging.StreamHandler()]
)
logger = logging.getLogger("WA-Sentinel")

class WhatsAppSentinel:
    def __init__(self, phone, message, count, delay):
        self.phone = phone
        self.message = message
        self.count = count
        self.delay = delay
        self.session_path = os.path.join(os.getcwd(), "wa_pro_session")
        self.driver = self._setup_driver()

    def _setup_driver(self):
        options = Options()
        options.add_argument(f"--user-data-dir={self.session_path}")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        # Masking User-Agent agar terlihat seperti user biasa
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        # Script tambahan untuk menyembunyikan status otomatisasi
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return driver

    def run(self):
        try:
            wait = WebDriverWait(self.driver, 45)
            logger.info("📡 Menghubungkan ke WhatsApp Web...")
            
            # Membuka chat langsung via URL API
            self.driver.get(f"https://web.whatsapp.com/send?phone={self.phone}")
            
            # List selector input (Multi-fallback agar lebih tahan banting)
            xpaths = [
                '//div[@contenteditable="true"][@data-tab="10"]',
                '//footer//div[@contenteditable="true"]',
                '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]'
            ]
            
            msg_box = None
            for xpath in xpaths:
                try:
                    msg_box = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
                    if msg_box: break
                except: continue

            if not msg_box:
                logger.error("❌ Gagal menemukan kotak input. Pastikan sudah login dan nomor benar.")
                return

            logger.info(f"🚀 Memulai transmisi {self.count} pesan ke {self.phone}...")

            for i in range(1, self.count + 1):
                # Tambahkan noise/random ID agar tidak dideteksi sebagai pesan duplikat (Anti-Spam)
                noise = f" [ID:{random.randint(100, 999)}]"
                msg_box.send_keys(self.message + noise + Keys.ENTER)
                
                # Jeda dinamis (Human-like behavior)
                jitter = self.delay + random.uniform(0.5, 2.0)
                logger.info(f"✅ Berhasil [{i}/{self.count}] | Delay: {jitter:.2f}s")
                time.sleep(jitter)

        except Exception as e:
            logger.error(f"⚠️ Terjadi kesalahan: {e}")
        finally:
            logger.info("🏁 Selesai. Browser tetap terbuka untuk monitoring.")

if __name__ == "__main__":
    # --- MASUKKAN DATA DI SINI ---
    TARGET = "628383872084"
    TEXT = "Halo Bro, Saya Sneijderlino (Pro Version)"
    JUMLAH = 10
    JEDA = 1.2

    bot = WhatsAppSentinel(TARGET, TEXT, JUMLAH, JEDA)
    bot.run()
