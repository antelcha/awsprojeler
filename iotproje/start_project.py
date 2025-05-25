#!/usr/bin/env python3
"""
IoT Ağırlık Projesi Başlatma Scripti
Bu script hem simülatörü hem de dashboard'u başlatır.
"""

import subprocess
import time
import sys
import os
from threading import Thread

def run_simulator():
    """Ağırlık simülatörünü çalıştır"""
    print("🚀 Ağırlık simülatörü başlatılıyor...")
    try:
        subprocess.run([sys.executable, "src/weight_simulator_v2.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Simülatör durduruldu")
    except Exception as e:
        print(f"❌ Simülatör hatası: {e}")

def run_dashboard():
    """Dashboard'u çalıştır"""
    print("📊 Dashboard başlatılıyor...")
    try:
        os.chdir("dashboard")
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Dashboard durduruldu")
    except Exception as e:
        print(f"❌ Dashboard hatası: {e}")

def main():
    print("🎯 IoT Ağırlık İzleme Projesi")
    print("=" * 40)
    print("Bu script aşağıdaki bileşenleri başlatacak:")
    print("1. 📡 Ağırlık Simülatörü (AWS IoT Core'a veri gönderir)")
    print("2. 📊 Web Dashboard (http://localhost:5001)")
    print()
    
    choice = input("Hangi bileşeni başlatmak istiyorsunuz?\n"
                  "1. Sadece Simülatör\n"
                  "2. Sadece Dashboard\n"
                  "3. Her ikisi birden\n"
                  "Seçiminiz (1-3): ").strip()
    
    if choice == "1":
        print("\n📡 Sadece simülatör başlatılıyor...")
        run_simulator()
        
    elif choice == "2":
        print("\n📊 Sadece dashboard başlatılıyor...")
        print("🌐 Dashboard: http://localhost:5001")
        run_dashboard()
        
    elif choice == "3":
        print("\n🚀 Her iki bileşen de başlatılıyor...")
        print("📡 Simülatör: Arka planda çalışacak")
        print("🌐 Dashboard: http://localhost:5001")
        
        # Simülatörü ayrı thread'de başlat
        simulator_thread = Thread(target=run_simulator, daemon=True)
        simulator_thread.start()
        
        # Simülatörün başlaması için bekle
        time.sleep(3)
        
        # Dashboard'u ana thread'de başlat
        run_dashboard()
        
    else:
        print("❌ Geçersiz seçim!")
        return

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Program sonlandırıldı. Güle güle!")
    except Exception as e:
        print(f"\n❌ Beklenmeyen hata: {e}") 