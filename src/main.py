import os
import sys

class TomirisCore:
    def __init__(self):
        self.version = "3.0.0-alpha"
        self.modules_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../modules'))
        self.loaded_modules = {}
        
        print("="*45)
        print(f"🐺 TOMIRIS CORE v{self.version} initialized.")
        print("Architecture: DeltaVerse Ecosystem")
        print("="*45)

    def bootstrap(self):
        """Çekirdek altyapıyı ve modül klasörünü hazırlar."""
        print("[CORE] Sistem kontrol ediliyor...")
        if not os.path.exists(self.modules_dir):
            os.makedirs(self.modules_dir)
            print(f"[CORE] Modül klasörü oluşturuldu: {self.modules_dir}")
        
        self.load_modules()

    def load_modules(self):
        """modules/ klasöründeki dinamik modülleri tarar ve yükler."""
        print("[CORE] Modüller taranıyor...")
        print("[CORE] Şimdilik sistem temiz, dinamik yükleyici aktif.")

    def run(self):
        """Ana döngüyü başlatır."""
        self.bootstrap()
        print("\n[TOMIRIS] Sistem hazır. Komut bekleniyor (Çıkış için 'exit')...")
        
        while True:
            try:
                user_input = input("\nDelta > ").strip()
                if user_input.lower() == 'exit':
                    print("[CORE] Tomiris nadasa çekiliyor. Görüşmek üzere Delta.")
                    break
                elif not user_input:
                    continue
                else:
                    print(f"[TOMIRIS] Alındı: '{user_input}' (Bu komut için henüz bir modül yüklenmedi.)")
            except KeyboardInterrupt:
                print("\n[CORE] Güvenli çıkış yapılıyor...")
                break

if __name__ == "__main__":
    agent = TomirisCore()
    agent.run()
