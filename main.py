import os
import subprocess

def run_step(script_name):
    print(f"--- Running {script_name} ---")
    subprocess.run(["python", script_name], check=True)

if __name__ == "__main__":
    # The Order of Operations
    run_step("data_gen.py")     # 1. Create Data
    run_step("db_setup.py")     # 2. Setup SQL
    run_step("train_model.py")  # 3. Train AI
    
    print("\n✅ All systems ready! Launch the dashboard with:")
    print("streamlit run dashboard.py")