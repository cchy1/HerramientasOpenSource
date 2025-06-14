import asyncio
from deepgram import Deepgram
import os

# 🔑 Reemplaza con tu clave API de Deepgram
DEEPGRAM_API_KEY = "TU_API_KEY"

# Ruta del archivo de audio local (formato WAV preferido)
AUDIO_FILE = "audio_para_transcribir.wav"

async def transcribir():
    dg = Deepgram(DEEPGRAM_API_KEY)

    with open(AUDIO_FILE, "rb") as audio:
        source = {
            "buffer": audio,
            "mimetype": "audio/wav"
        }
        response = await dg.transcription.prerecorded(
            source,
            {
                "language": "es",
                "smart_format": True,
                "punctuate": True
            }
        )

    print("\n📄 TRANSCRIPCIÓN COMPLETA:\n")
    print(response["results"]["channels"][0]["alternatives"][0]["transcript"])

# Ejecutar
if __name__ == "__main__":
    asyncio.run(transcribir())
