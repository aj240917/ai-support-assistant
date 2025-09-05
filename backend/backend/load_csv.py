import pandas as pd
import sqlite3
from main import insert_email

# Load dataset
df = pd.read_csv("../dataset/sample_support_emails.csv")

# Insert emails into DB
for _, row in df.iterrows():
    insert_email(row["sender"], row["subject"], row["body"], row["sent_date"])

print("✅ Emails loaded from CSV into database")
