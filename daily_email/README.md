# Daily Email - Correo diario con IA

Script de Python que genera contenido diario sobre un tema usando OpenAI y lo envía por correo electrónico.

## Configuración

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Copia `.env.example` a `.env` y rellena tus datos:
   ```bash
   cp .env.example .env
   ```

3. Configura las variables en `.env`:
   - `OPENAI_API_KEY` — tu clave de API de OpenAI
   - `TOPIC` — el tema sobre el que quieres recibir contenido
   - `SMTP_*` — credenciales de tu servidor de correo
   - `EMAIL_FROM` / `EMAIL_TO` — remitente y destinatario

> **Gmail**: si tienes 2FA activado, genera una [contraseña de aplicación](https://myaccount.google.com/apppasswords).

## Ejecución manual

```bash
python main.py
```

## Programar envío diario

### Windows (Task Scheduler)

1. Abre **Task Scheduler** → Crear tarea básica
2. Trigger: Diariamente, a la hora que prefieras
3. Acción: Iniciar programa
   - Programa: `python`
   - Argumentos: `main.py`
   - Iniciar en: `C:\ruta\a\daily_email`

### Linux/Mac (cron)

```bash
crontab -e
```

Añade (ejemplo: todos los días a las 8:00):
```
0 8 * * * cd /ruta/a/daily_email && python main.py
```
