import asyncio
import os
from dotenv import load_dotenv
from deepgram import Deepgram

# Cargar variables de entorno desde .env (dos niveles arriba)
load_dotenv('../../.env')
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')

# Verificar que la API key esté disponible
if not DEEPGRAM_API_KEY:
    print("❌ ERROR: DEEPGRAM_API_KEY no encontrada en archivo .env")
    print("💡 Asegúrate de tener DEEPGRAM_API_KEY=tu_clave en el archivo .env")
    exit(1)

print(f"✅ API Key cargada: ***{DEEPGRAM_API_KEY[-4:]}")

# Ruta del archivo de audio local (formato WAV preferido)
AUDIO_FILE = "audio_para_transcribir.wav"

async def transcribir():
    """
    Función principal de transcripción usando Deepgram
    """
    try:
        # Verificar que el archivo de audio existe
        if not os.path.exists(AUDIO_FILE):
            print(f"❌ ERROR: Archivo de audio '{AUDIO_FILE}' no encontrado")
            print("💡 Coloca un archivo WAV con ese nombre en esta carpeta")
            return
        
        print(f"🎵 Procesando archivo: {AUDIO_FILE}")
        
        # Inicializar cliente Deepgram
        dg = Deepgram(DEEPGRAM_API_KEY)
        
        # Leer archivo de audio
        with open(AUDIO_FILE, "rb") as audio:
            source = {
                "buffer": audio,
                "mimetype": "audio/wav"
            }
            
            # Configuración optimizada para español médico
            options = {
                "language": "es",
                "smart_format": True,
                "punctuate": True,
                "diarize": True,  # Separación de speakers
                "model": "nova-2",  # Modelo más reciente
                "tier": "enhanced"  # Mayor precisión
            }
            
            print("🔄 Enviando audio a Deepgram...")
            
            # Realizar transcripción
            response = await dg.transcription.prerecorded(source, options)
            
            # Mostrar resultados
            print("\n📄 TRANSCRIPCIÓN COMPLETA:")
            print("=" * 50)
            
            # Extraer transcripción principal
            main_transcript = response["results"]["channels"][0]["alternatives"][0]["transcript"]
            print(main_transcript)
            
            # Si hay separación de speakers, mostrarla
            if "paragraphs" in response["results"]["channels"][0]["alternatives"][0]:
                print("\n👥 TRANSCRIPCIÓN POR SPEAKERS:")
                print("=" * 30)
                
                paragraphs = response["results"]["channels"][0]["alternatives"][0]["paragraphs"]["paragraphs"]
                for i, paragraph in enumerate(paragraphs):
                    speaker = paragraph.get("speaker", "Desconocido")
                    text = paragraph["sentences"][0]["text"] if paragraph["sentences"] else ""
                    print(f"Speaker {speaker}: {text}")
            
            # Guardar transcripción en archivo
            output_file = "transcripcion_resultado.txt"
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("TRANSCRIPCIÓN DEEPGRAM\n")
                f.write("=" * 30 + "\n\n")
                f.write(f"Archivo: {AUDIO_FILE}\n")
                f.write(f"Modelo: {options['model']}\n")
                f.write(f"Idioma: {options['language']}\n\n")
                f.write("TRANSCRIPCIÓN:\n")
                f.write(main_transcript)
                
                if "paragraphs" in response["results"]["channels"][0]["alternatives"][0]:
                    f.write("\n\nPOR SPEAKERS:\n")
                    f.write("-" * 20 + "\n")
                    paragraphs = response["results"]["channels"][0]["alternatives"][0]["paragraphs"]["paragraphs"]
                    for paragraph in paragraphs:
                        speaker = paragraph.get("speaker", "Desconocido")
                        text = paragraph["sentences"][0]["text"] if paragraph["sentences"] else ""
                        f.write(f"Speaker {speaker}: {text}\n")
            
            print(f"\n💾 Transcripción guardada en: {output_file}")
            
            # Mostrar estadísticas
            confidence = response["results"]["channels"][0]["alternatives"][0].get("confidence", 0)
            print(f"📊 Confianza: {confidence:.2%}")
            
            return response
            
    except FileNotFoundError:
        print(f"❌ ERROR: Archivo '{AUDIO_FILE}' no encontrado")
        print("💡 Asegúrate de tener un archivo WAV en esta carpeta")
    except Exception as e:
        print(f"❌ ERROR durante la transcripción: {e}")
        print("💡 Verifica tu API key y conexión a internet")

def crear_audio_prueba():
    """
    Crear un archivo de audio simple para pruebas usando síntesis de voz de macOS
    """
    if not os.path.exists(AUDIO_FILE):
        print("🎤 Creando archivo de audio de prueba...")
        texto_prueba = "Hola, este es un archivo de prueba para transcripción médica. El paciente presenta síntomas de ansiedad y dificultades para dormir."
        
        # Usar comando 'say' de macOS para generar audio
        os.system(f'say "{texto_prueba}" -o {AUDIO_FILE} --data-format=LEF32@22050')
        print(f"✅ Archivo de prueba creado: {AUDIO_FILE}")
    else:
        print(f"📁 Archivo {AUDIO_FILE} ya existe")

# Ejecutar
if __name__ == "__main__":
    print("🏥 TRANSCRIPTOR MÉDICO DEEPGRAM")
    print("=" * 40)
    
    # Crear archivo de prueba si no existe
    crear_audio_prueba()
    
    # Ejecutar transcripción
    asyncio.run(transcribir())
