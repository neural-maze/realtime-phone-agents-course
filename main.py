from pathlib import Path

from openai import OpenAI

client = OpenAI()

with Path("audio.wav").open("rb") as audio_file:
    transcription = client.audio.transcriptions.create(model="Systran/faster-whisper-small", file=audio_file)

print(transcription.text)