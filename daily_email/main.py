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
