"""
Script de correo diario sobre embarazo y maternidad.
Calcula la semana de gestacion segun la FPP y genera contenido personalizado.
Uso: python main.py
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date, timedelta

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

# Fecha estimada de parto
DUE_DATE = date(2026, 12, 28)
GESTATION_WEEKS = 40


def get_current_week():
    conception_start = DUE_DATE - timedelta(weeks=GESTATION_WEEKS)
    today = date.today()
    days_pregnant = (today - conception_start).days
    week = days_pregnant // 7
    return max(1, min(week, GESTATION_WEEKS))


def generate_content(week):
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    next_week = week + 1 if week < GESTATION_WEEKS else week

    prompt = (
        f"Eres una experta en maternidad y embarazo. "
        f"Hoy es {date.today().strftime('%d/%m/%Y')}. "
        f"Una madre primeriza esta en la semana {week} de embarazo. "
        f"Escribe un correo amigable y calido en espanol que incluya:\n"
        f"1. Datos curiosos sobre el desarrollo del bebe en la semana {week}\n"
        f"2. Consejos practicos para padres y madres primerizos en esta etapa\n"
        f"3. Que esperar en la semana {next_week} (siguiente semana)\n"
        f"4. Un dato curioso o tip extra que sea util\n\n"
        f"Usa un tono cercano, positivo y reconfortante. No uses formato markdown."
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents=prompt
    )
    return response.text


def send_email(subject, body):
    msg = MIMEMultipart("alternative")
    msg["From"] = os.environ["EMAIL_FROM"]
    msg["To"] = os.environ["EMAIL_TO"]
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ["SMTP_PORT"])) as server:
        server.starttls()
        server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        server.sendmail(msg["From"], msg["To"], msg.as_string())


def main():
    week = get_current_week()
    print(f"Semana actual de gestacion: {week}")
    print("Generando contenido...")

    content = generate_content(week)
    print("Contenido generado. Enviando correo...")

    subject = f"Semana {week} de embarazo - Tu resumen diario"
    send_email(subject, content)
    print("Correo enviado exitosamente!")


if __name__ == "__main__":
    main()
