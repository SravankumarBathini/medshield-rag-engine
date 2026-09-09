import sqlite3
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("providence_clinical.db")
cursor = conn.cursor()

print("?? Local SQLite Database Connection Opened.")

cursor.execute('''
CREATE TABLE IF NOT EXISTS patient_admissions (
    patient_id TEXT PRIMARY KEY,
    admission_date TEXT,
    discharge_date TEXT,
    department TEXT,
    billing_amount REAL,
    doctor_notes TEXT
)
''')
conn.commit()

departments = ['Cardiology', 'Neurology', 'Oncology', 'Gastroenterology', 'General Medicine']
symptoms = [
    "Patient presenting with acute chest pain radiating to the left arm. History of hypertension. Suspected myocardial infarction.",
    "Patient experiences progressive numbness in right lower extremity accompanied by mild slurred speech. Checking for stroke indicators.",
    "Routine follow-up for chronic stage 2 lymphoma. Patient reporting extreme fatigue but showing stable vital signs.",
    "Chronic abdominal pain localized in the lower right quadrant. Nausea present. Ruling out acute appendicitis.",
    "Persistent low-grade fever lasting 14 days. Accompanied by non-productive cough and joint pain. Initiating infectious disease panel."
]
medications = ["Aspirin 81mg, Metoprolol 25mg", "Clopidogrel 75mg, Atorvastatin 40mg", "Rituximab IV, Ondansetron 4mg", "Acetaminophen 500mg, Amoxicillin 500mg", "Ibuprofen 400mg, Azithromycin 250mg"]

np.random.seed(42)
random.seed(42)

data = []
start_date = datetime(2026, 1, 1)

for i in range(100):
    p_id = f"PRV-2026-{1000 + i}"
    days_add = random.randint(1, 180)
    add_dt = start_date + timedelta(days=days_add)
    stay_dur = random.randint(2, 14)
    dis_dt = add_dt + timedelta(days=stay_dur)
    
    idx = random.randint(0, 4)
    dept = departments[idx]
    note = f"{symptoms[idx]} Prescribed: {medications[idx]}. Patient advised strict bed rest."
    bill = round(random.uniform(15000.00, 185000.00), 2)
    
    data.append((p_id, add_dt.strftime('%Y-%m-%d'), dis_dt.strftime('%Y-%m-%d'), dept, bill, note))

cursor.executemany('''
INSERT OR REPLACE INTO patient_admissions (patient_id, admission_date, discharge_date, department, billing_amount, doctor_notes)
VALUES (?, ?, ?, ?, ?, ?)
''', data)

conn.commit()
conn.close()
print("? 100 Clinical Enterprise Records loaded cleanly into local warehouse table 'patient_admissions'.")
