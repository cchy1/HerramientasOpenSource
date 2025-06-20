import os
import sys
import asyncio
import subprocess
from dotenv import load_dotenv
from deepgram import Deepgram
import json

# Cargar la clave API desde el archivo .env.deepgram
load_dotenv('.env.deepgram')
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')

if not DEEPGRAM_API_KEY:
    print("❌ No se encontró la clave API de Deepgram en el entorno.")
    sys.exit(1)

if len(sys.argv) < 2:
    print("❗ Debes indicar un archivo de audio como argumento. Ej: python transcriptor_deepgram.py archivo.mp3")
    sys.exit(1)

input_file = sys.argv[1]
wav_file = "audio_reconvertido_deepgram.wav"

# Convertir automáticamente a WAV mono, 16 bits, 16kHz si no lo está
def convertir_a_wav_si_es_necesario(origen, destino):
    print("🔄 Verificando formato de audio...")
    comando = [
        "ffmpeg", "-y", "-i", origen,
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", destino
    ]
    try:
        subprocess.run(comando, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Conversión exitosa o ya en formato correcto.")
    except subprocess.CalledProcessError:
        print("❌ Error al convertir el archivo de audio.")
        sys.exit(1)

# Transcripción usando SDK v2 de Deepgram
async def transcribir():
    convertir_a_wav_si_es_necesario(input_file, wav_file)

    with open(wav_file, "rb") as f:
        audio = f.read()

    deepgram = Deepgram(DEEPGRAM_API_KEY)

    try:
        print("🎙️ Transcribiendo con Deepgram...")
        response = await deepgram.transcription.prerecorded(
            {"buffer": audio, "mimetype": "audio/wav"},
            {"punctuate": True, "language": "es"}
        )
        texto = response["results"]["channels"][0]["alternatives"][0]["transcript"]
        print("\n🧠 TRANSCRIPCIÓN:")
        print(texto)

        # Guardar transcripción en archivo
        with open("transcripcion_deepgram.txt", "w") as out:
            out.write(texto)
        print("📝 Guardado en 'transcripcion_deepgram.txt'.")

    except Exception as e:
        print(f"❌ Error en la transcripción: {e}")

if __name__ == "__main__":
    asyncio.run(transcribir())
