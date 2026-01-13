# 🎓 English Tutor - AI-Powered Language Learning System

> Sistema completo de tutoría de inglés con IA totalmente local usando Gradio + LangGraph + Ollama

---

## 📚 Índice de Documentación

**Empieza aquí:**

1. **[INDICE_ENGLISH_TUTOR.txt](INDICE_ENGLISH_TUTOR.txt)** - Navegación de todos los archivos
2. **[RESUMEN_ENGLISH_TUTOR.txt](RESUMEN_ENGLISH_TUTOR.txt)** - Resumen ejecutivo del proyecto
3. **[QUICKSTART_ENGLISH_TUTOR.txt](QUICKSTART_ENGLISH_TUTOR.txt)** - Guía de inicio rápido

**Documentación completa:**

- **[ENGLISH_TUTOR_README.md](ENGLISH_TUTOR_README.md)** - Documentación detallada
- **[ARCHITECTURE_ENGLISH_TUTOR.txt](ARCHITECTURE_ENGLISH_TUTOR.txt)** - Diagramas de arquitectura
- **[ENGLISH_TUTOR_FILES.txt](ENGLISH_TUTOR_FILES.txt)** - Lista completa de archivos

---

## 🚀 Instalación Rápida

### Paso 1: Generar el Proyecto

```bash
python setup_english_tutor_master.py
```

Este script creará automáticamente toda la estructura del proyecto.

### Paso 2: Configurar

```bash
cd english_tutor
cp .env.example .env
# Edita .env con tus configuraciones
```

### Paso 3: Instalar y Ejecutar

```bash
pip install -e .
python scripts/run_tutor.py
```

Abre tu navegador en `http://localhost:7860`

---

## ✨ Características

- 🎯 **Aprendizaje Personalizado** - Ejercicios adaptativos basados en competencias
- 🗣️ **Práctica de Speaking** - Retroalimentación de pronunciación en tiempo real
- ✍️ **Ejercicios Escritos** - Gramática y vocabulario
- 👂 **Comprensión Auditiva** - Ejercicios con audio
- 📊 **Tracking de Progreso** - Seguimiento de 6 áreas de competencia
- 🤖 **IA Conversacional** - Agente LangGraph que se adapta a tu nivel
- 🔒 **100% Local** - Ollama + TTS/STT locales

---

## 🏗️ Arquitectura

- **LLM**: Ollama (llama3.2, qwen2.5, etc.)
- **Agent**: LangGraph (workflows con estado)
- **TTS**: Kokoro (inglés local), Together AI, Edge
- **STT**: Whisper-Groq, Moonshine, Faster Whisper
- **UI**: Gradio (chat + voz)
- **DB**: SQLite (progreso del estudiante)

---

## 📊 Competencias Trackeadas

1. **Grammar** - Gramática, tiempos verbales, estructura
2. **Vocabulary** - Vocabulario, sinónimos, colocaciones
3. **Pronunciation** - Pronunciación, fonética, entonación
4. **Listening** - Comprensión auditiva
5. **Speaking** - Fluidez conversacional
6. **Writing** - Expresión escrita

---

## 📦 Scripts de Setup

| Script | Descripción |
|--------|-------------|
| `setup_english_tutor_master.py` | ⭐ **PRINCIPAL** - Ejecuta todo |
| `setup_english_tutor_full.py` | Parte 1: Core modules |
| `setup_english_tutor_full_part2.py` | Parte 2: Agent & UI |
| `verify_english_tutor_setup.py` | Verificación de archivos |

---

## 🎯 Uso

### Modo Texto
```
Usuario: "Can you help me with grammar?"
Tutor: "Let's practice! Fill in the blank: I ___ to the store."
```

### Modo Voz
1. Haz clic en el micrófono
2. Habla tu respuesta
3. Recibe feedback en audio

---

## 🔧 Configuración Recomendada

```env
OLLAMA_MODEL=llama3.2          # O qwen2.5
STT_MODEL=whisper-groq         # Rápido, requiere API key
TTS_MODEL=kokoro               # TTS local en inglés
GROQ_API_KEY=tu_api_key
```

---

## 📁 Estructura del Proyecto

```
english_tutor/
├── src/english_tutor/
│   ├── agent/              # LangGraph tutor agent
│   ├── competencies/       # Sistema de tracking
│   ├── exercises/          # Generador de ejercicios
│   ├── models/             # STT/TTS wrappers
│   ├── database/           # SQLite persistence
│   ├── ui/                 # Gradio interface
│   └── tutor.py            # Clase principal
├── scripts/
│   └── run_tutor.py        # Entry point
└── data/
    └── students.db         # Base de datos
```

---

## 🐛 Troubleshooting

**"Ollama not running"**
```bash
ollama serve
```

**"GROQ_API_KEY not found"**
```bash
# Añade tu API key a .env o usa STT local
STT_MODEL=moonshine
```

**"Port already in use"**
```env
# Cambia en .env
SERVER_PORT=7861
```

---

## 💡 Modelos Recomendados

### LLM (Ollama)
- `llama3.2` - Rápido, ideal para principiantes (3B)
- `qwen2.5` - Excelente para enseñanza (3B)
- `llama3.1:8b` - Mejor razonamiento (8B)

### STT
- `whisper-groq` - Rápido, cloud (gratis)
- `moonshine` - Local, ligero
- `faster-whisper` - Local, optimizado

### TTS
- `kokoro` - ⭐ Local, voz nativa en inglés
- `together` - Alta calidad (requiere API key)
- `edge` - Gratis, requiere internet

---

## 🎓 Ejemplos

```python
from english_tutor import EnglishTutor

# Crear tutor
tutor = EnglishTutor(
    student_name="Juan",
    llm_model="llama3.2",
    stt_model_name="whisper-groq",
    tts_model_name="kokoro"
)

# Lanzar interfaz
tutor.launch()

# Obtener respuesta
response = tutor.agent.process_student_input("Help me with grammar")

# Ver progreso
progress = tutor.tracker.get_progress_summary()

# Guardar
tutor.save_progress()
```

---

## 📖 Documentación Completa

Para más detalles, consulta:

- **[ENGLISH_TUTOR_README.md](ENGLISH_TUTOR_README.md)** - Guía completa
- **[QUICKSTART_ENGLISH_TUTOR.txt](QUICKSTART_ENGLISH_TUTOR.txt)** - Inicio rápido
- **[ARCHITECTURE_ENGLISH_TUTOR.txt](ARCHITECTURE_ENGLISH_TUTOR.txt)** - Arquitectura técnica

---

## 🤝 Integración con Proyecto Padre

Este proyecto reutiliza la infraestructura TTS/STT del proyecto padre:

```
realtime-phone-agents-course/
├── src/realtime_phone_agents/
│   ├── stt/              → Usado por tutor
│   └── tts/              → Usado por tutor
└── english_tutor/        ← Nuevo proyecto separado
    └── src/english_tutor/
```

---

## 📄 Licencia

MIT License - Libre para uso educativo y comercial

---

## 🙏 Créditos

- **Proyecto Padre**: realtime-phone-agents-course
- **LangChain/LangGraph**: Framework de agentes
- **Gradio**: Interfaz de usuario
- **Ollama**: LLMs locales

---

**¡Empieza ahora!**

```bash
python setup_english_tutor_master.py
```

**¡Feliz aprendizaje de inglés! 🎓🚀**
