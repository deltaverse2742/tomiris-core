import sys
import os
import customtkinter as ctk
from tkinter import filedialog
import shutil

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
        self.geometry("750x550") # Kaydırılabilir alan için yüksekliği biraz esnettim aga
        
        # Grid düzenini ayarla
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # Ana Sekme Yapısı
        self.tabview = ctk.CTkTabview(self, width=720, height=510)
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
        
        # --- ZORUNLU API MODÜL KONTROLÜ ---
        try:
            from modules.auth_core import AuthModule
            self.auth = AuthModule(self.core)
            is_authed, key = self.auth.check_auth()
            
            if not is_authed:
                self.log_write("[ERROR] API Key bulunamadı! Sistem kilitlendi.")
                self.request_api_key()
            else:
                self.log_write("[AUTH] API Key doğrulandı. Sistem Aktif.\n")
        except ImportError:
            self.log_write("[CRITICAL] Zorunlu Auth modülü eksik! Tomiris kapatılıyor...")
            self.after(2000, self.destroy)

    def request_api_key(self):
        """Kullanıcıdan zorunlu API key isteyen pop-up pencere."""
        input_dialog = ctk.CTkInputDialog(
            text="Tomiris Core'u aktif etmek için geçerli bir API Key girin:",
            title="Zorunlu Aktivasyon"
        )
        entered_key = input_dialog.get_input()
        
        if entered_key and len(entered_key.strip()) > 10:
            self.auth.save_key(entered_key)
            self.log_write("[SUCCESS] API Key başarıyla kaydedildi! Sistemi yeniden başlatın.")
            self.after(2000, self.destroy) # Sistemi güvenli kapatıp yeniden açtırıyoruz
        else:
            self.log_write("[CRITICAL] Geçersiz anahtar! Tomiris kapatılıyor...")
            self.after(2000, self.destroy)

    def log_write(self, text):
        """Arayüzdeki log alanına yazı ekler."""
        self.log_area.configure(state="normal")
        self.log_area.insert("end", text + "\n")
        self.log_area.configure(state="disabled")
        self.log_area.see("end") # Otomatik aşağı kaydır

    def init_console_tab(self):
        tab = self.tabview.tab("🖥️ Konsol")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(0, weight=1)
        
        self.log_area = ctk.CTkTextbox(tab, activate_scrollbars=True)
        self.log_area.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
        self.log_area.configure(state="disabled") # Kullanıcı elle silmesin
        
        self.cmd_input = ctk.CTkEntry(tab, placeholder_text="Delta > Komut girin veya sohbet edin...")
        self.cmd_input.grid(row=1, column=0, padx=(10, 5), pady=10, sticky="ew")
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
            
        response = f"[TOMIRIS] Alındı: '{user_input}' (Bu komut için henüz bir modül yüklenmedi.)"
        self.log_write(response)

    # --- DİNAMİK MODÜL YÖNETİMİ ALANLARI ---

    def init_modules_tab(self):
        """Modül yönetimi sekmesini dinamik listeleme altyapısıyla kurar."""
        tab = self.tabview.tab("🧩 Modül Yönetimi")
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1) # Listenin uzayabilmesi için
        
        lbl_installed = ctk.CTkLabel(tab, text="Yüklü Modüller", font=ctk.CTkFont(size=14, weight="bold"))
        lbl_installed.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        # Statik kutu yerine canlı, kaydırılabilir modül çerçevesi
        self.module_list_frame = ctk.CTkScrollableFrame(tab, height=200)
        self.module_list_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")
        
        lbl_add = ctk.CTkLabel(tab, text="Yeni Modül Ekle", font=ctk.CTkFont(size=14, weight="bold"))
        lbl_add.grid(row=2, column=0, padx=10, pady=(15, 5), sticky="w")
        
        self.module_path_input = ctk.CTkEntry(tab, placeholder_text="GitHub Repo Linki veya Yerel .py Dosya Yolu")
        self.module_path_input.grid(row=3, column=0, padx=(10, 5), pady=5, sticky="ew")
        
        self.browse_btn = ctk.CTkButton(tab, text="Dosya Seç", width=90, command=self.browse_local_module)
        self.browse_btn.grid(row=3, column=1, padx=5, pady=5)
        
        self.install_btn = ctk.CTkButton(tab, text="Modülü Kur", width=90, fg_color="green", hover_color="darkgreen", command=self.install_module)
        self.install_btn.grid(row=3, column=2, padx=(5, 10), pady=5)

        # İlk açılışta klasördeki gerçek modülleri listele
        self.refresh_module_list()

    def get_installed_modules(self):
        """modules/ klasöründeki aktif Python modüllerini tarar."""
        modules_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "modules"))
        if not os.path.exists(modules_dir):
            os.makedirs(modules_dir)
        
        ignored = ["__init__.py", "auth_core.py", "__pycache__"]
        all_items = os.listdir(modules_dir)
        
        installed = []
        for item in all_items:
            if item in ignored:
                continue
            if item.endswith(".py"):
                installed.append(item.replace(".py", " (Dosya)"))
            elif os.path.isdir(os.path.join(modules_dir, item)):
                installed.append(item + " (Klasör)")
        return installed

    def refresh_module_list(self):
        """Ekranda listelenen modülleri diskteki duruma göre günceller."""
        for widget in self.module_list_frame.winfo_children():
            widget.destroy()
            
        modules = self.get_installed_modules()
        
        # Varsayılan sistem kontrolünü görsel olarak en başa ekleyelim
        sys_frame = ctk.CTkFrame(self.module_list_frame)
        sys_frame.pack(pady=2, fill="x", padx=5)
        ctk.CTkLabel(sys_frame, text="• SystemControl v1.0 [Sistem]", font=("Arial", 12)).pack(side="left", padx=10, pady=5)

        if not modules:
            return
            
        for mod in modules:
            row_frame = ctk.CTkFrame(self.module_list_frame)
            row_frame.pack(pady=2, fill="x", padx=5)
            
            mod_label = ctk.CTkLabel(row_frame, text=f"• {mod} [Aktif]", font=("Arial", 12))
            mod_label.pack(side="left", padx=10, pady=5)
            
            del_btn = ctk.CTkButton(
                row_frame, 
                text="Kaldır", 
                width=60, 
                fg_color="#e74c3c", 
                hover_color="#c0392b",
                command=lambda m=mod: self.remove_custom_module(m)
            )
            del_btn.pack(side="right", padx=10, pady=5)

    def browse_local_module(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
        if file_path:
            self.module_path_input.delete(0, "end")
            self.module_path_input.insert(0, file_path)
            
    def install_module(self):
        """Arayüzden girilen yerel dosya yolunu modules klasörüne kopyalar."""
        path = self.module_path_input.get().strip()
        if not path:
            return
            
        self.log_write(f"\n[CORE] Yeni modül yükleme isteği alındı: {path}")
        
        # Eğer yerel bir .py dosyasıysa kopyalama işlemini yapalım
        if os.path.exists(path) and path.endswith(".py"):
            file_name = os.path.basename(path)
            dest_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "modules"))
            dest_path = os.path.join(dest_dir, file_name)
            
            try:
                shutil.copy(path, dest_path)
                self.log_write(f"[SUCCESS] {file_name} başarıyla DeltaVerse havuzuna eklendi.")
                self.module_path_input.delete(0, "end")
                self.refresh_module_list()
            except Exception as e:
                self.log_write(f"[ERROR] Modül yüklenemedi: {str(e)}")
        else:
            # Burası ileride git clone mantığı için geliştirilebilir
            self.log_write("[WARNING] Geçersiz dosya yolu! Git entegrasyonu yakında eklenecek.")

    def remove_custom_module(self, module_name_raw):
        """Seçilen modülü diskten kalıcı olarak siler."""
        module_name = module_name_raw.split(" ")[0]
        modules_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "modules"))
        
        py_file_path = os.path.join(modules_dir, f"{module_name}.py")
        dir_path = os.path.join(modules_dir, module_name)
        
        try:
            if os.path.exists(py_file_path):
                os.remove(py_file_path)
            elif os.path.exists(dir_path):
                shutil.rmtree(dir_path)
                
            self.log_write(f"[REMOVE] {module_name} modülü sistemden kaldırıldı.")
            self.refresh_module_list()
        except Exception as e:
            self.log_write(f"[ERROR] Modül silinirken hata oluştu: {str(e)}")

if __name__ == "__main__":
    # Önce beyni oluşturuyoruz
    core = TomirisCore()
    # Sonra beyni arayüze verip düğünü bitiriyoruz
    app = TomirisUI(core)
    app.mainloop()
