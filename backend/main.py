from fastapi import FastAPI
import sqlite3
from transformers import pipeline
import pandas as pd
from queue import PriorityQueue

app = FastAPI()

# Sentiment Analysis model (HuggingFace)
sentiment_model = pipeline("sentiment-analysis")

# DB Setup
conn = sqlite3.connect("emails.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    subject TEXT,
    body TEXT,
    date TEXT,
    sentiment TEXT,
    priority TEXT,
    ai_response TEXT
)""")
conn.commit()

# Priority Queue
email_queue = PriorityQueue()

# Simple AI Draft Response Generator
def generate_response(subject, body, sentiment):
    if "urgent" in subject.lower() or "critical" in body.lower():
        return f"Hello, we understand your concern. Our team is treating this as URGENT. We’ll update you soon regarding: {subject}"
    elif "billing" in subject.lower():
        return f"Hello, thank you for reaching out. Regarding billing, we will check and resolve this issue. Subject: {subject}"
    else:
        return f"Hello, thank you for your query. We will get back shortly. Subject: {subject}"

# Insert Email
def insert_email(sender, subject, body, date):
    sentiment = sentiment_model(body[:512])[0]["label"]

    urgent_keywords = ["urgent", "immediate", "critical", "blocked", "cannot access"]
    priority = "Urgent" if any(w in subject.lower() for w in urgent_keywords) else "Normal"

    ai_response = generate_response(subject, body, sentiment)

    cursor.execute("INSERT INTO emails (sender, subject, body, date, sentiment, priority, ai_response) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (sender, subject, body, date, sentiment, priority, ai_response))
    conn.commit()

    priority_value = 0 if priority == "Urgent" else 1
    email_queue.put((priority_value, subject))

# API: Get Emails
@app.get("/emails")
def get_emails():
    cursor.execute("SELECT * FROM emails ORDER BY priority DESC")
    rows = cursor.fetchall()
    return [
        {
            "id": row[0],
            "sender": row[1],
            "subject": row[2],
            "body": row[3],
            "date": row[4],
            "sentiment": row[5],
            "priority": row[6],
            "ai_response": row[7],
        }
        for row in rows
    ]
