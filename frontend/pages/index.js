import { useEffect, useState } from "react";

export default function Dashboard() {
  const [emails, setEmails] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/emails")
      .then(res => res.json())
      .then(data => setEmails(data));
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>📩 AI Support Assistant Dashboard</h1>
      {emails.map(email => (
        <div key={email.id} style={{ border: "1px solid #ccc", padding: "15px", margin: "10px 0", borderRadius: "8px" }}>
          <h2>{email.subject}</h2>
          <p><b>From:</b> {email.sender}</p>
          <p><b>Date:</b> {email.date}</p>
          <p><b>Sentiment:</b> {email.sentiment}</p>
          <p><b>Priority:</b> {email.priority}</p>
          <p><b>Body:</b> {email.body}</p>
          <h3>🤖 AI Draft Response</h3>
          <p style={{ background: "#f4f4f4", padding: "10px", borderRadius: "5px" }}>{email.ai_response}</p>
          <button style={{ marginTop: "10px", padding: "8px 12px" }}>Send Reply</button>
        </div>
      ))}
    </div>
  );
}
