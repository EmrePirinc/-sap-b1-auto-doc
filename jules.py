
import os
import sys
import time
import subprocess
from datetime import datetime
from assembler import create_doc_from_plan

class JulesAgent:
    def __init__(self):
        self.name = "Jules"
        self.version = "v7.2"
        self.work_dir = os.path.dirname(os.path.abspath(__file__))
        
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{self.name} {timestamp}]: {message}")

    def run_task(self):
        self.log(f"Initializing... (Version {self.version})")
        self.log("Reading configuration...")
        
        video_file = os.path.join(os.path.dirname(self.work_dir), "1-El-Terminali-E-itimi-20250623-092431-Toplant-Kayd-mp4-6e84e604-09f0.vtt").replace('.vtt', '.mp4')
        # Check if mp4 extraction name is different
        if not os.path.exists(video_file):
             # Try other name
             video_file = os.path.join(os.path.dirname(self.work_dir), "1-El Terminali Eğitimi-20250623_092431-Toplantı Kaydı.mp4")

        plan_file = "content_plan.json"
        output_file = os.path.join(os.path.dirname(self.work_dir), "El_Terminali_Kullanim_Kilavuzu_Jules_Auto.docx")

        if not os.path.exists(video_file):
            self.log(f"Error: Video file not found at {video_file}")
            return

        self.log("Starting Phase 1: Visual Analysis & RedBox Detection...")
        # assembler.py logic is imported
        try:
            create_doc_from_plan(video_file, plan_file, output_file)
            self.log("Phase 1 Complete. Document Generated.")
        except Exception as e:
            self.log(f"Critical Error during generation: {e}")
            return

        self.log("Starting Phase 2: Version Control (Git)...")
        self.git_sync()

        self.log("Phase 3: Delivery...")
        self.open_file(output_file)
        
        self.log("Task Completed Successfully.")

    def git_sync(self):
        try:
            subprocess.run(["git", "add", "."], cwd=self.work_dir, check=True, stdout=subprocess.DEVNULL)
            commit_msg = f"Jules Auto-Exec: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=self.work_dir, check=False, stdout=subprocess.DEVNULL) # fail silently if nothing to commit
            subprocess.run(["git", "push", "origin", "main"], cwd=self.work_dir, check=True, stdout=subprocess.DEVNULL)
            self.log("Code and artifacts synced to GitHub.")
        except Exception as e:
            self.log(f"Git sync warning: {e}")

    def open_file(self, path):
        self.log(f"Opening {path}...")
        os.startfile(path)

if __name__ == "__main__":
    agent = JulesAgent()
    agent.run_task()
