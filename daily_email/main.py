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
from groq import Groq

load_dotenv()

# Fecha estimada de parto
DUE_DATE = date(2026, 12, 28)
GESTATION_WEEKS = 40


def get_current_week():
    conception_start = DUE_DATE - timedelta(weeks=GESTATION_WEEKS)
    today = date.today()
    # Suma 1 día para que el domingo (inicio de semana) muestre la semana que comienza
    days_pregnant = (today - conception_start).days + 1
    week = days_pregnant // 7
    return max(1, min(week, GESTATION_WEEKS))


def generate_content(week):
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    next_week = week + 1 if week < GESTATION_WEEKS else week

    prompt = (
        f"Eres una experta en maternidad y embarazo. Hoy es {date.today().strftime('%d/%m/%Y')}. "
        f"Una pareja esta en la semana {week} de embarazo. Redacta un correo CONCISO en español con EXACTAMENTE esta estructura:\n\n"
        f"1. UN parrafo (4-5 lineas) con informacion general de la semana {week}\n"
        f"2. UN parrafo (4-5 lineas) sobre los cambios mas significativos del feto esta semana\n"
        f"3. PROPUESTAS DE NOMBRES:\n"
        f"   - 3 nombres de niña originales, cortos (estilo: Naia, Vera, Luna)\n"
        f"   - 3 nombres de niño originales, cortos (estilo: Gael, Oliver, Leo)\n"
        f"   - Incluye el significado breve de cada nombre\n"
        f"4. RECOMENDACIONES (3-4 puntos concretos sobre alimentacion, ejercicio, cuidados)\n"
        f"5. MENSAJE DE ANIMO (2-3 lineas motivadoras para la pareja)\n\n"
        f"Usa un tono cercano y calido. NO uses formato markdown, negritas ni asteriscos. Usa mayusculas para los titulos."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1200
    )
    return response.choices[0].message.content


def send_email(subject, body):
    msg = MIMEMultipart("alternative")
    msg["From"] = os.environ["EMAIL_FROM"]
    
    # Soporta múltiples destinatarios separados por coma
    recipients = [email.strip() for email in os.environ["EMAIL_TO"].split(",")]
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain", "utf-8"))

    with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ["SMTP_PORT"])) as server:
        server.starttls()
        server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        server.sendmail(msg["From"], recipients, msg.as_string())

def main():
    week = get_current_week()
    print(f"Semana actual de gestacion: {week}")
    print("Generando contenido...")

    content = generate_content(week)
    print("Contenido generado. Enviando correo...")

    subject = f"🤰 Semana {week} de embarazo - Tu resumen semanal"
    send_email(subject, content)
    print("Correo enviado exitosamente!")


if __name__ == "__main__":
    main()
