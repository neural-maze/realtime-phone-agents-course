# 🎓 English Tutor - AI-Powered Language Learning System

Sistema completo de tutoría de inglés con IA totalmente local usando Gradio + LangGraph + Ollama.

## 🌟 Características

- **🎯 Aprendizaje Personalizado**: Ejercicios adaptativos basados en tus competencias
- **🗣️ Práctica de Speaking**: Retroalimentación de pronunciación en tiempo real
- **✍️ Ejercicios Escritos**: Gramática y vocabulario
- **👂 Comprensión Auditiva**: Ejercicios basados en audio
- **📊 Seguimiento de Progreso**: Monitorea tu mejora en todas las áreas
- **🤖 IA Tutor Conversacional**: Agente que se adapta a tu nivel
- **🔒 100% Local**: Todos los modelos corren localmente (Ollama + STT/TTS locales)

## 🏗️ Arquitectura

- **LLM**: Ollama (llama3.2, qwen2.5, o cualquier modelo que tengas)
- **TTS**: Kokoro (TTS local en inglés) o Together AI
- **STT**: Whisper-based (Groq, Moonshine, Faster Whisper)
- **Framework de Agente**: LangGraph para workflows conversacionales con estado
- **UI**: Gradio con streaming de audio + chat de texto
- **Base de Datos**: SQLite para seguimiento de progreso
- **Integración**: Reutiliza modelos TTS/STT del proyecto padre

## 📦 Instalación Rápida

### Paso 1: Generar el Proyecto

Desde el directorio raíz del repositorio:

```bash
python setup_english_tutor_master.py
```

Este script generará automáticamente:
- ✅ Estructura de directorios completa
- ✅ Todos los módulos Python
- ✅ Configuración base
- ✅ Sistema de competencias
- ✅ Generador de ejercicios
- ✅ Agente LangGraph
- ✅ Interfaz Gradio

### Paso 2: Configurar

```bash
cd english_tutor
cp .env.example .env
```

Edita `.env` con tus configuraciones:

```env
OLLAMA_MODEL=llama3.2          # o qwen2.5, mistral, etc.
STT_MODEL=whisper-groq         # o moonshine, faster-whisper
GROQ_API_KEY=tu_api_key        # Para Whisper Groq
TTS_MODEL=kokoro               # o together, edge, gtts
```

### Paso 3: Instalar Dependencias

```bash
pip install -e .
```

O con uv:

```bash
uv pip install -e .
```

### Paso 4: Ejecutar

```bash
python scripts/run_tutor.py
```

La aplicación se abrirá en `http://localhost:7860`

## 🎮 Uso

### Modo Texto
1. Escribe tu pregunta o solicita un ejercicio
2. El tutor responderá adaptándose a tu nivel
3. Completa ejercicios y recibe retroalimentación

### Modo Voz
1. Haz clic en el micrófono y habla
2. Tu voz se transcribirá automáticamente
3. El tutor responderá con audio sintetizado

### Comandos Útiles

- **"Can we practice grammar?"** - Solicita ejercicios de gramática
- **"I want to practice speaking"** - Inicia conversación
- **"Give me a vocabulary exercise"** - Ejercicio de vocabulario
- **"What should I focus on?"** - Obtén recomendaciones personalizadas

## 📊 Competencias Seguidas

El sistema rastrea 6 áreas de competencia:

1. **Grammar** - Estructura de oraciones, tiempos verbales, artículos
2. **Vocabulary** - Conocimiento de palabras, sinónimos, colocaciones
3. **Pronunciation** - Fonética, entonación, fluidez
4. **Listening** - Comprensión auditiva, dictado
5. **Speaking** - Fluidez conversacional, espontaneidad
6. **Writing** - Expresión escrita, ortografía, coherencia

## 🗂️ Estructura del Proyecto

```
english_tutor/
├── src/english_tutor/
│   ├── __init__.py
│   ├── config.py              # Configuración con Pydantic
│   ├── tutor.py               # Clase principal EnglishTutor
│   │
│   ├── agent/                 # Agente LangGraph
│   │   ├── __init__.py
│   │   ├── state.py           # Definición de estado
│   │   └── tutor_agent.py     # Lógica del agente
│   │
│   ├── competencies/          # Sistema de competencias
│   │   ├── __init__.py
│   │   ├── models.py          # Modelos de datos
│   │   └── tracker.py         # Lógica de seguimiento
│   │
│   ├── exercises/             # Generador de ejercicios
│   │   ├── __init__.py
│   │   ├── types.py           # Tipos de ejercicios
│   │   └── generator.py       # Generación con LLM
│   │
│   ├── models/                # Integración TTS/STT
│   │   ├── __init__.py
│   │   ├── stt.py             # Speech-to-Text
│   │   └── tts.py             # Text-to-Speech
│   │
│   ├── database/              # Persistencia
│   │   ├── __init__.py
│   │   └── storage.py         # SQLite
│   │
│   └── ui/                    # Interfaz Gradio
│       ├── __init__.py
│       └── app.py             # Aplicación Gradio
│
├── scripts/
│   └── run_tutor.py           # Punto de entrada
│
├── data/                      # Base de datos (auto-generada)
│   └── students.db
│
├── pyproject.toml
├── .env.example
├── .gitignore
└── README.md
```

## 🔧 Configuración Avanzada

### Modelos Ollama Recomendados

Para mejores resultados en tutoría de inglés:

```bash
# Modelos pequeños y rápidos
ollama pull llama3.2        # 3B - Rápido, bueno para gramática básica
ollama pull qwen2.5         # 3B - Excelente para ESL

# Modelos medianos
ollama pull llama3.1:8b     # Mejor razonamiento
ollama pull mistral         # Bueno para feedback detallado

# Modelos grandes (requieren más RAM)
ollama pull llama3.1:70b    # Máxima calidad
```

### Configuración de STT

**Opción 1: Groq (Recomendado - Rápido y gratis)**
```env
STT_MODEL=whisper-groq
GROQ_API_KEY=tu_api_key_de_groq
```

**Opción 2: Moonshine (Local, sin API)**
```env
STT_MODEL=moonshine
```

**Opción 3: Faster Whisper (Local optimizado)**
```env
STT_MODEL=faster-whisper
```

### Configuración de TTS

**Opción 1: Kokoro (Local, inglés nativo)**
```env
TTS_MODEL=kokoro
```

**Opción 2: Together AI (Mejor calidad)**
```env
TTS_MODEL=together
TOGETHER_API_KEY=tu_api_key
```

**Opción 3: Edge TTS (Gratis, requiere internet)**
```env
TTS_MODEL=edge
```

## 🐛 Troubleshooting

### Error: "Ollama not running"
```bash
# Inicia Ollama
ollama serve
```

### Error: "No module named 'realtime_phone_agents'"
Asegúrate de que el proyecto padre está en el path. El tutor importa modelos STT/TTS desde allí.

### Error: "GROQ_API_KEY not found"
Si usas `whisper-groq`, necesitas una API key de Groq (gratis en groq.com)

### La UI no carga
Verifica que el puerto 7860 esté libre:
```bash
# Windows
netstat -ano | findstr :7860

# Linux/Mac
lsof -i :7860
```

Cambia el puerto en `.env`:
```env
SERVER_PORT=7861
```

## 💡 Ejemplos de Uso

### Uso Programático

```python
from english_tutor import EnglishTutor

# Crear tutor personalizado
tutor = EnglishTutor(
    student_name="Juan",
    llm_model="llama3.2",
    stt_model_name="whisper-groq",
    tts_model_name="kokoro"
)

# Lanzar interfaz
tutor.launch(share=True)  # share=True para Gradio sharing

# Guardar progreso manualmente
tutor.save_progress()
```

### Interacción Directa con el Agente

```python
# Procesar entrada de texto
response = tutor.agent.process_student_input(
    "Can you help me with present perfect tense?"
)
print(response)

# Obtener recomendación
recommendation = tutor.tracker.get_recommendation()
print(recommendation)

# Ver progreso
progress = tutor.tracker.get_progress_summary()
print(progress)
```

## 🚀 Características Futuras (Roadmap)

- [ ] Reconocimiento de pronunciación con scoring
- [ ] Ejercicios de listening con audio pregrabado
- [ ] Sistema de niveles (A1, A2, B1, B2, C1, C2)
- [ ] Flashcards de vocabulario
- [ ] Certificados de logros
- [ ] Modo examen (TOEFL, IELTS prep)
- [ ] Integración con Anki
- [ ] Multi-usuario con autenticación
- [ ] Estadísticas detalladas y gráficos
- [ ] Export de progreso (PDF, CSV)

## 📝 Notas de Desarrollo

### Testing
```bash
# Instalar dependencias de desarrollo
pip install pytest pytest-asyncio

# Ejecutar tests (cuando estén implementados)
pytest tests/
```

### Linting
```bash
pip install ruff
ruff check src/
ruff format src/
```

## 🤝 Contribuir

Este es un proyecto educativo. Mejoras bienvenidas:

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit cambios (`git commit -am 'Añade mejora'`)
4. Push (`git push origin feature/mejora`)
5. Abre un Pull Request

## 📄 Licencia

MIT License - Libre para uso educativo y comercial

## 🙏 Agradecimientos

- **Proyecto Padre**: realtime-phone-agents-course (modelos STT/TTS)
- **LangChain/LangGraph**: Framework de agentes
- **Gradio**: Interfaz de usuario
- **Ollama**: LLMs locales

---

**¿Preguntas o problemas?** Abre un issue en GitHub

**¡Disfruta aprendiendo inglés con IA! 🎓🚀**
