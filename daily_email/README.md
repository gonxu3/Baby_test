# Daily Email - Correo diario con IA

Script de Python que genera contenido diario sobre un tema usando Groq (cliente LLM) y lo envía por correo electrónico.

## Resumen

Este proyecto genera un correo semanal sobre embarazo/maternidad (resumen por semana de gestación) utilizando el cliente Groq para generar el contenido y lo envía vía SMTP. El flujo principal está en `daily_email/main.py`.

> Nota: originalmente se consideró OpenAI, pero actualmente el código utiliza Groq (GROQ_API_KEY).

## Configuración

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

2. Copia `.env.example` a `.env` y rellena tus datos:
   ```bash
   cp .env.example .env
   ```

3. Configura las variables en `.env` (principales):
   - `GROQ_API_KEY` — tu clave de API de Groq
   - `TOPIC` — el tema sobre el que quieres recibir contenido (opcional)
   - `SMTP_*` — credenciales de tu servidor de correo (SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD)
   - `EMAIL_FROM` / `EMAIL_TO` — remitente y destinatario(s) (EMAIL_TO acepta una lista separada por comas)

> Si usas Gmail con 2FA activa, genera una contraseña de aplicación para SMTP (https://myaccount.google.com/apppasswords).

## Fecha estimada de parto (FPP)

El script calcula la semana de gestación en función de la fecha estimada de parto definida en `daily_email/main.py` (constante `DUE_DATE`). Actualmente está hardcodeada en `date(2026, 12, 28)`.

Si quieres cambiar la FPP rápida y manualmente, edita esa constante en `daily_email/main.py`. Si prefieres que lo haga por ti, puedo hacer que la fecha sea configurable vía variable de entorno (por ejemplo `DUE_DATE=YYYY-MM-DD`) en un próximo cambio.

## Ejecución manual

```bash
python main.py
```

Al ejecutarlo verás en consola la semana actual calculada:
```
Semana actual de gestacion: <n>
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

## GitHub Actions

Hay un workflow (`.github/workflows/daily_email.yml`) que ejecuta el script de forma programada. El workflow espera los secretos `GROQ_API_KEY`, `SMTP_USER`, y `SMTP_PASSWORD`. Revisa la configuración del workflow antes de usarlo y cambia `EMAIL_TO` si no quieres esos destinatarios por defecto.

## Estado actual y próximos pasos recomendados

- El script genera y envía correo en texto plano (MIME text/plain). Si más adelante quieres HTML o imágenes, se puede extender.
- La FPP está hardcodeada; recomendable convertirla en variable de entorno para facilitar uso por múltiples usuarios.
- README actualizado para reflejar el uso de Groq en lugar de OpenAI.

Si quieres, aplico alguno de los siguientes cambios ahora:
- Hacer `DUE_DATE` configurable vía `.env` y documentarlo.
- Añadir tests unitarios para el cálculo de la semana.
- Convertir `EMAIL_SUBJECT` en plantilla configurable.
