# 🛡️ WHATSAPP SPAM
**Advanced WhatsApp Automation**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

WA-Sentinel adalah alat automasi tingkat lanjut yang dirancang untuk pengujian penetrasi sosial atau notifikasi sistem otomatis via WhatsApp Web. Menggunakan teknik *evasion* untuk meminimalisir deteksi bot.

## ✨ Fitur Utama
- **Persistent Session:** Tidak perlu scan QR berulang kali.
- **Anti-Bot Evasion:** Bypass deteksi Selenium via `AutomationControlled` flags.
- **Randomized Jitter:** Jeda pengiriman pesan yang dinamis (meniru perilaku manusia).
- **Cross-Platform:** Support Windows (CMD), Linux, dan Android (Termux dengan GUI/VNC).

## 🚀 Instalasi

### 1. Windows (CMD/PowerShell)
```bash
git clone [https://github.com/123tool/Spam-Whatsapp.git]
cd Spam-Whatsapp
pip install -r requirements.txt
python Spam.py
