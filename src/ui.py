import sys
import os
import customtkinter as ctk
from tkinter import filedialog

# Beyni (Core Engine) içeri aktarıyoruz
from main import TomirisCore

# DeltaVerse Tema Ayarları
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TomirisUI(ctk.CTk):
    def __init__(self, core_instance):
        super().__init__()
        self.core = core_instance # Tomiris'in beyni artık arayüze bağlı
        
        self.title("Tomiris AI - DeltaVerse Ecosystem")
        self.geometry("750x500")
        
        # Grid düzenini ayarla
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Ana Sekme Yapısı
        self.tabview = ctk.CTkTabview(self, width=720, height=460)
        self.tabview.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        
        self.tabview.add("🖥️ Konsol")
        self.tabview.add("🧩 Modül Yönetimi")
        
        self.init_console_tab()
        self.init_modules_tab()
        
        # Çekirdeğin ilk açılış loglarını ekrana yazdır
        self.boot_core()

    def boot_core(self):
        """Çekirdek motoru tetikler ve başlangıç mesajlarını ekrana yazar."""
        self.core.bootstrap()
        self.log_write(f"🐺 TOMIRIS CORE v{self.core.version} initialized.")
        self.log_write("Architecture: DeltaVerse Ecosystem")
        self.log_write("-" * 45)
        self.log_write("[CORE] Sistem kontrol ediliyor... Modül yükleyici aktif.\n")

    def log_write(self, text):
        """Arayüzdeki log alanına yazı ekler."""
        self.log_area.insert("end", text + "\n")
        self.log_area.see("end") # Otomatik aşağı kaydır

    def init_console_tab(self):
        tab = self.tabview.tab("🖥️ Konsol")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        
        self.log_area = ctk.CTkTextbox(tab, activate_scrollbars=True)
        self.log_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        
        self.cmd_input = ctk.CTkEntry(tab, placeholder_text="Delta > Komut girin veya sohbet edin...")
        self.cmd_input.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="ew")
        # Enter tuşuna basınca da göndersin
        self.cmd_input.bind("<Return>", lambda event: self.process_command())
        
        self.send_btn = ctk.CTkButton(tab, text="Gönder", width=100, command=self.process_command)
        self.send_btn.grid(row=1, column=1, padx=10, pady=10)
        
    def process_command(self):
        """Arayüzden gelen komutu çekirdek motora gönderir."""
        user_input = self.cmd_input.get().strip()
        if not user_input:
            return
            
        self.log_write(f"\nDelta > {user_input}")
        self.cmd_input.delete(0, "end")
        
        if user_input.lower() == 'exit':
            self.log_write("[CORE] Tomiris kapatılıyor...")
            self.after(1000, self.destroy)
            return
            
        # Komutu arka plandaki main.py çekirdeğine pasla
        # İleride burası dinamik modülleri tetikleyecek
        response = f"[TOMIRIS] Alındı: '{user_input}' (Bu komut için henüz bir modül yüklenmedi.)"
        self.log_write(response)
        
    def init_modules_tab(self):
        tab = self.tabview.tab("🧩 Modül Yönetimi")
        tab.grid_columnconfigure(0, weight=1)
        
        lbl_installed = ctk.CTkLabel(tab, text="Yüklü Modüller", font=ctk.CTkFont(size=14, weight="bold"))
        lbl_installed.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        self.module_list = ctk.CTkTextbox(tab, height=150)
        self.module_list.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        self.module_list.insert("0.0", "• SystemControl v1.0 [Aktif]\n• SpeechSynthesis v0.5 [İnaktif]\n")
        self.module_list.configure(state="disabled")
        
        lbl_add = ctk.CTkLabel(tab, text="Yeni Modül Ekle", font=ctk.CTkFont(size=14, weight="bold"))
        lbl_add.grid(row=2, column=0, padx=10, pady=(20, 5), sticky="w")
        
        self.module_path_input = ctk.CTkEntry(tab, placeholder_text="GitHub Repo Linki veya Yerel .py Dosya Yolu")
        self.module_path_input.grid(row=3, column=0, padx=(10, 5), pady=5, sticky="ew")
        
        self.browse_btn = ctk.CTkButton(tab, text="Dosya Seç", width=90, command=self.browse_local_module)
        self.browse_btn.grid(row=3, column=1, padx=5, pady=5)
        
        self.install_btn = ctk.CTkButton(tab, text="Modülü Kur", width=90, fg_color="green", hover_color="darkgreen", command=self.install_module)
        self.install_btn.grid(row=3, column=2, padx=(5, 10), pady=5)

    def browse_local_module(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            self.module_path_input.delete(0, "end")
            self.module_path_input.insert(0, file_path)
            
    def install_module(self):
        """Arayüzden girilen modülü çekirdeğe kaydeder (İskelet fonksiyon)."""
        path = self.module_path_input.get().strip()
        if path:
            self.log_write(f"\n[CORE] Yeni modül yükleme isteği alındı: {path}")
            self.log_write("[CORE] Modül entegrasyonu tamamlanıyor...")
            self.module_path_input.delete(0, "end")

if __name__ == "__main__":
    # Önce beyni oluşturuyoruz
    core = TomirisCore()
    # Sonra beyni arayüze verip düğünü bitiriyoruz
    app = TomirisUI(core)
    app.mainloop()
