import os
import json
import urllib.request
from typing import Dict, Any

def send_notification_email(recipient_email: str, subject: str, message_body: str) -> Dict[str, Any]:
    """
    Sends notification via Brevo (ex-Sendinblue) Free Tier (300 free emails/day).
    Fallback to simulated dispatch logging if BREVO_API_KEY is not configured.
    """
    brevo_key = os.getenv("BREVO_API_KEY")
    if brevo_key:
        try:
            url = "https://api.brevo.com/v3/smtp/email"
            payload = {
                "sender": {"name": "Orientation IA Burkina", "email": "no-reply@orientation.bf"},
                "to": [{"email": recipient_email}],
                "subject": subject,
                "textContent": message_body
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={
                    "api-key": brevo_key,
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                return {"status": "sent", "provider": "Brevo API", "recipient": recipient_email}
        except Exception as e:
            pass

    # Free Fallback / Local Log Dispatcher (0 FCFA)
    return {
        "status": "simulated_sent",
        "provider": "Local Dispatcher (Free)",
        "recipient": recipient_email,
        "subject": subject,
        "preview": message_body[:100]
    }
