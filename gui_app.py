import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os
from assembler import create_doc_from_plan

class AutoDocGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AIFTeam - SAP B1 Dokümantasyon Aracı")
        self.root.geometry("600x450")
        
        # Variables
        self.video_path = tk.StringVar()
        self.plan_path = tk.StringVar()
        self.output_path = tk.StringVar()
        
        # UI Elements
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header = tk.Label(self.root, text="Otomatik Doküman Oluşturucu (v7)", font=("Arial", 14, "bold"))
        header.pack(pady=20)
        
        # File Selection Frame
        frame = tk.Frame(self.root)
        frame.pack(padx=20, fill="x")
        
        # Video Selection
        tk.Label(frame, text="Video Dosyası (.mp4):").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(frame, textvariable=self.video_path, width=50).grid(row=0, column=1, padx=5)
        tk.Button(frame, text="Seç", command=self.select_video).grid(row=0, column=2)
        
        # Plan Selection
        tk.Label(frame, text="Plan Dosyası (.json):").grid(row=1, column=0, sticky="w", pady=5)
        tk.Entry(frame, textvariable=self.plan_path, width=50).grid(row=1, column=1, padx=5)
        tk.Button(frame, text="Seç", command=self.select_plan).grid(row=1, column=2)
        
        # Output Selection
        tk.Label(frame, text="Çıktı Dosyası (.docx):").grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(frame, textvariable=self.output_path, width=50).grid(row=2, column=1, padx=5)
        
        # Generate Button
        self.btn_generate = tk.Button(self.root, text="Dokümanı Oluştur", command=self.start_generation, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), height=2)
        self.btn_generate.pack(pady=30, fill="x", padx=100)
        
        # Status
        self.status = tk.Label(self.root, text="Hazır", fg="gray")
        self.status.pack(side="bottom", pady=10)

    def select_video(self):
        filename = filedialog.askopenfilename(title="Video Seç", filetypes=[("MP4 Files", "*.mp4")])
        if filename:
            self.video_path.set(filename)
            
    def select_plan(self):
        filename = filedialog.askopenfilename(title="Plan Seç", filetypes=[("JSON Files", "*.json")])
        if filename:
            self.plan_path.set(filename)

    def start_generation(self):
        video = self.video_path.get()
        plan = self.plan_path.get()
        output = self.output_path.get()
        
        if not output:
             output = os.path.join(os.path.dirname(video), "Olusturulan_Dokuman.docx")
             self.output_path.set(output)
        
        if not video or not plan:
            messagebox.showerror("Hata", "Lütfen Video ve Plan dosyalarını seçin.")
            return
            
        self.btn_generate.config(state="disabled")
        self.status.config(text="İşleniyor... Lütfen bekleyin.")
        
        # Run in thread to not freeze GUI
        threading.Thread(target=self.run_process, args=(video, plan, output)).start()
        
    def run_process(self, video, plan, output):
        try:
            create_doc_from_plan(video, plan, output)
            self.root.after(0, lambda: messagebox.showinfo("Başarılı", f"Doküman oluşturuldu:\n{output}"))
            self.root.after(0, lambda: self.status.config(text="Tamamlandı."))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Hata", str(e)))
            self.root.after(0, lambda: self.status.config(text="Hata oluştu."))
        finally:
             self.root.after(0, lambda: self.btn_generate.config(state="normal"))

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoDocGUI(root)
    root.mainloop()
