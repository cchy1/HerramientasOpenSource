import asyncio
import os
import subprocess
import glob
from datetime import datetime
from dotenv import load_dotenv
from deepgram import Deepgram

# Cargar variables de entorno
load_dotenv('../../.env')
DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')

# Verificar API key
if not DEEPGRAM_API_KEY:
    print("❌ ERROR: DEEPGRAM_API_KEY no encontrada en archivo .env")
    print("💡 Asegúrate de tener DEEPGRAM_API_KEY=tu_clave en el archivo .env")
    exit(1)

print(f"✅ API Key cargada: ***{DEEPGRAM_API_KEY[-4:]}")

class TranscriptorMedico:
    """
    Transcriptor médico optimizado usando nova-2
    """
    
    def __init__(self):
        self.dg = Deepgram(DEEPGRAM_API_KEY)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Configuración óptima basada en tests
        self.config_optima = {
            "language": "es",
            "model": "nova-2",          # Ganador de los tests (96.85%)
            "smart_format": True,
            "punctuate": True,
            "diarize": True,            # Separación médico/paciente
            "keywords": [               # Términos médicos priorizados
                "doctor", "médico", "paciente", "síntomas", "dolor",
                "medicamento", "tratamiento", "ansiedad", "depresión",
                "consulta", "diagnóstico", "terapia", "escala"
            ]
        }
        
        # Vocabulario médico para análisis
        self.vocabulario_medico = {
            "ROLES": ["doctor", "médico", "paciente", "doctora", "enfermera"],
            "SÍNTOMAS_FÍSICOS": ["dolor", "palpitaciones", "mareo", "fatiga", "insomnio", "náuseas"],
            "SÍNTOMAS_PSICOLÓGICOS": ["ansiedad", "depresión", "estrés", "nervioso", "preocupado", "tristeza"],
            "MEDICAMENTOS": ["medicamento", "medicina", "pastilla", "dosis", "miligramos", "tratamiento"],
            "ESCALAS": ["escala", "nivel", "intensidad", "grado", "puntuación"],
            "TEMPORALES": ["semana", "mes", "año", "día", "mañana", "noche", "ayer", "hoy"],
            "FRECUENCIA": ["siempre", "nunca", "frecuente", "ocasional", "diario", "semanal"]
        }

    def crear_segmento_optimizado(self, archivo_original, duracion_segundos=300):
        """
        Crear segmento con filtros de audio optimizados para voz médica
        """
        if not os.path.exists(archivo_original):
            print(f"❌ Archivo {archivo_original} no encontrado")
            return None
        
        nombre_base = archivo_original.replace('.wav', '')
        archivo_segmento = f"{nombre_base}_optimizado_{duracion_segundos}s.wav"
        
        print(f"✂️ Creando segmento optimizado de {duracion_segundos//60}:{duracion_segundos%60:02d} minutos...")
        
        try:
            # Comando ffmpeg optimizado para audio médico
            cmd = [
                'ffmpeg', 
                '-i', archivo_original,
                '-t', str(duracion_segundos),
                '-acodec', 'pcm_s16le',
                '-ar', '16000',                              # 16kHz sample rate
                '-ac', '1',                                  # Mono
                '-af', 'highpass=f=100,lowpass=f=8000,volume=1.2',  # Filtros para voz + amplificación
                '-y',
                archivo_segmento
            ]
            
            resultado = subprocess.run(cmd, capture_output=True, text=True)
            
            if resultado.returncode == 0:
                tamaño_original = os.path.getsize(archivo_original) / (1024 * 1024)
                tamaño_segmento = os.path.getsize(archivo_segmento) / (1024 * 1024)
                
                print(f"✅ Segmento optimizado creado")
                print(f"📊 Tamaño original: {tamaño_original:.1f} MB")
                print(f"📊 Tamaño segmento: {tamaño_segmento:.1f} MB")
                print(f"🎛️ Filtros aplicados: highpass + lowpass + amplificación")
                
                return archivo_segmento
            else:
                print(f"❌ Error con ffmpeg: {resultado.stderr}")
                return None
                
        except FileNotFoundError:
            print("❌ ffmpeg no encontrado. Instala con: brew install ffmpeg")
            return None
        except Exception as e:
            print(f"❌ Error creando segmento: {e}")
            return None

    async def transcribir_optimizado(self, archivo_audio, incluir_timestamps=True):
        """
        Transcripción médica con nova-2 y análisis completo
        """
        try:
            print(f"\n🎵 TRANSCRIPCIÓN MÉDICA OPTIMIZADA")
            print(f"📁 Archivo: {archivo_audio}")
            print(f"🤖 Modelo: nova-2 (calidad premium)")
            
            if not os.path.exists(archivo_audio):
                print(f"❌ Archivo no encontrado: {archivo_audio}")
                return None
            
            tamaño_mb = os.path.getsize(archivo_audio) / (1024 * 1024)
            print(f"📊 Tamaño: {tamaño_mb:.2f} MB")
            
            print("🔄 Enviando a Deepgram con configuración óptima...")
            
            with open(archivo_audio, "rb") as audio:
                source = {
                    "buffer": audio,
                    "mimetype": "audio/wav"
                }
                
                # Usar configuración óptima
                response = await self.dg.transcription.prerecorded(source, self.config_optima)
                
                if response and "results" in response:
                    return await self._procesar_respuesta_completa(response, archivo_audio, incluir_timestamps)
                else:
                    print("❌ No se recibió respuesta válida de Deepgram")
                    return None
                    
        except Exception as e:
            print(f"❌ Error durante transcripción: {e}")
            import traceback
            traceback.print_exc()
            return None

    async def _procesar_respuesta_completa(self, response, archivo_audio, incluir_timestamps):
        """
        Procesamiento completo de la respuesta con análisis médico
        """
        try:
            channels = response["results"]["channels"]
            if not channels or len(channels) == 0:
                print("❌ No se encontraron canales de audio")
                return None
            
            alternatives = channels[0]["alternatives"]
            if not alternatives or len(alternatives) == 0:
                print("❌ No se encontraron alternativas de transcripción")
                return None
            
            # Datos principales
            transcript = alternatives[0]["transcript"]
            confidence = alternatives[0].get("confidence", 0)
            words = alternatives[0].get("words", [])
            
            print(f"\n📄 TRANSCRIPCIÓN COMPLETA:")
            print("=" * 70)
            print(transcript)
            print(f"\n📊 Confianza general: {confidence:.2%}")
            
            # Crear resultado estructurado
            resultado = {
                "transcript": transcript,
                "confidence": confidence,
                "archivo": archivo_audio,
                "timestamp": datetime.now().isoformat(),
                "modelo": "nova-2",
                "analisis": await self._analizar_contenido_medico(transcript, words),
                "speakers": self._analizar_speakers(words) if words else None
            }
            
            # Guardar archivo completo
            output_file = await self._guardar_transcripcion_completa(resultado, incluir_timestamps)
            resultado["output_file"] = output_file
            
            # Mostrar resumen
            self._mostrar_resumen(resultado)
            
            return resultado
            
        except Exception as e:
            print(f"❌ Error procesando respuesta: {e}")
            return None

    async def _analizar_contenido_medico(self, transcript, words):
        """
        Análisis específico del contenido médico
        """
        texto_lower = transcript.lower()
        analisis = {}
        
        # Contar palabras por categoría
        for categoria, palabras_lista in self.vocabulario_medico.items():
            encontradas = {}
            for palabra in palabras_lista:
                count = texto_lower.count(palabra)
                if count > 0:
                    encontradas[palabra] = count
            if encontradas:
                analisis[categoria] = encontradas
        
        # Análisis de sentimiento básico
        palabras_positivas = ["bien", "mejor", "bueno", "tranquilo", "calmado", "relajado"]
        palabras_negativas = ["mal", "peor", "terrible", "horrible", "intenso", "fuerte"]
        
        sentiment_score = 0
        for palabra in palabras_positivas:
            sentiment_score += texto_lower.count(palabra)
        for palabra in palabras_negativas:
            sentiment_score -= texto_lower.count(palabra)
        
        analisis["SENTIMENT"] = {
            "score": sentiment_score,
            "interpretacion": "Positivo" if sentiment_score > 0 else "Negativo" if sentiment_score < 0 else "Neutro"
        }
        
        # Estadísticas generales
        analisis["ESTADISTICAS"] = {
            "palabras_totales": len(transcript.split()),
            "caracteres": len(transcript),
            "oraciones_aprox": transcript.count('.') + transcript.count('?') + transcript.count('!')
        }
        
        return analisis

    def _analizar_speakers(self, words):
        """
        Análisis detallado de speakers
        """
        if not words:
            return None
        
        speakers_info = {}
        
        for word in words:
            speaker = word.get("speaker", 0)
            if speaker not in speakers_info:
                speakers_info[speaker] = {
                    "palabras": 0,
                    "confianza_total": 0,
                    "texto_completo": []
                }
            
            speakers_info[speaker]["palabras"] += 1
            speakers_info[speaker]["confianza_total"] += word.get("confidence", 0)
            speakers_info[speaker]["texto_completo"].append(word.get("word", ""))
        
        # Calcular promedios y roles
        for speaker_id, info in speakers_info.items():
            info["confianza_promedio"] = info["confianza_total"] / info["palabras"]
            info["texto"] = " ".join(info["texto_completo"][:100])  # Primeras 100 palabras
            info["rol_estimado"] = "👨‍⚕️ MÉDICO/PROFESIONAL" if speaker_id == 0 else f"🧑‍🤝‍🧑 PACIENTE/CLIENTE"
            
            # Porcentaje de participación
            total_palabras = sum(s["palabras"] for s in speakers_info.values())
            info["participacion_porcentaje"] = (info["palabras"] / total_palabras) * 100
        
        return speakers_info

    async def _guardar_transcripcion_completa(self, resultado, incluir_timestamps):
        """
        Guardar transcripción con análisis completo
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"transcripcion_medica_optimizada_{timestamp}.txt"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("TRANSCRIPCIÓN MÉDICA OPTIMIZADA - NOVA-2\n")
            f.write("=" * 60 + "\n\n")
            
            # Información del archivo
            f.write("INFORMACIÓN DE LA SESIÓN:\n")
            f.write("-" * 30 + "\n")
            f.write(f"Archivo: {resultado['archivo']}\n")
            f.write(f"Timestamp: {resultado['timestamp']}\n")
            f.write(f"Modelo: {resultado['modelo']}\n")
            f.write(f"Confianza: {resultado['confidence']:.2%}\n")
            f.write(f"Sesión ID: {self.session_id}\n\n")
            
            # Transcripción principal
            f.write("TRANSCRIPCIÓN COMPLETA:\n")
            f.write("-" * 25 + "\n")
            f.write(resultado['transcript'])
            f.write("\n\n")
            
            # Análisis médico
            if resultado['analisis']:
                f.write("ANÁLISIS DE CONTENIDO MÉDICO:\n")
                f.write("-" * 35 + "\n")
                
                for categoria, contenido in resultado['analisis'].items():
                    if categoria == "ESTADISTICAS":
                        f.write(f"\n{categoria}:\n")
                        for key, value in contenido.items():
                            f.write(f"  • {key}: {value}\n")
                    elif categoria == "SENTIMENT":
                        f.write(f"\n{categoria}:\n")
                        f.write(f"  • Score: {contenido['score']}\n")
                        f.write(f"  • Interpretación: {contenido['interpretacion']}\n")
                    else:
                        f.write(f"\n{categoria}:\n")
                        for palabra, count in contenido.items():
                            f.write(f"  • {palabra}: {count} vez(es)\n")
            
            # Análisis de speakers
            if resultado['speakers']:
                f.write("\n\nANÁLISIS POR SPEAKERS:\n")
                f.write("-" * 25 + "\n")
                
                for speaker_id, info in resultado['speakers'].items():
                    f.write(f"\n{info['rol_estimado']} (Speaker {speaker_id}):\n")
                    f.write(f"  • Palabras: {info['palabras']}\n")
                    f.write(f"  • Participación: {info['participacion_porcentaje']:.1f}%\n")
                    f.write(f"  • Confianza promedio: {info['confianza_promedio']:.2%}\n")
                    f.write(f"  • Muestra de texto: {info['texto'][:200]}...\n")
            
            # Recomendaciones
            f.write("\n\nRECOMENDACIONES PARA MEJORA:\n")
            f.write("-" * 35 + "\n")
            if resultado['confidence'] >= 0.95:
                f.write("✅ Excelente calidad de audio - mantener configuración\n")
            elif resultado['confidence'] >= 0.90:
                f.write("✅ Buena calidad - considerar mejores micrófonos\n")
            else:
                f.write("⚠️ Calidad mejorable - revisar audio fuente\n")
            
            f.write("💡 Usar siempre modelo nova-2 para máxima precisión\n")
            f.write("💡 Mantener segmentos de 2-5 minutos para mejor costo/beneficio\n")
        
        return output_file

    def _mostrar_resumen(self, resultado):
        """
        Mostrar resumen en pantalla
        """
        print(f"\n📋 RESUMEN DE ANÁLISIS:")
        print("=" * 30)
        
        # Palabras clave encontradas
        total_medicas = 0
        for categoria, contenido in resultado['analisis'].items():
            if categoria not in ["ESTADISTICAS", "SENTIMENT"]:
                total_medicas += sum(contenido.values())
        
        print(f"🔍 Términos médicos detectados: {total_medicas}")
        print(f"📊 Confianza: {resultado['confidence']:.2%}")
        
        if resultado['speakers']:
            print(f"👥 Speakers detectados: {len(resultado['speakers'])}")
            for speaker_id, info in resultado['speakers'].items():
                print(f"   {info['rol_estimado']}: {info['participacion_porcentaje']:.1f}% participación")
        
        # Sentiment
        if "SENTIMENT" in resultado['analisis']:
            sentiment = resultado['analisis']["SENTIMENT"]
            print(f"😊 Sentimiento general: {sentiment['interpretacion']}")
        
        print(f"\n💾 Archivo guardado: {resultado['output_file']}")

    def seleccionar_archivo(self):
        """
        Seleccionar archivo de audio para transcribir
        """
        # Buscar archivos de audio
        archivos_audio = []
        extensiones = ['*.wav', '*.mp3', '*.m4a', '*.aiff', '*.flac']
        
        for extension in extensiones:
            archivos_audio.extend(glob.glob(extension))
        
        if not archivos_audio:
            print("📁 No se encontraron archivos de audio en esta carpeta")
            return None
        
        print("\n🎵 ARCHIVOS DE AUDIO DISPONIBLES:")
        print("=" * 40)
        
        for i, archivo in enumerate(archivos_audio, 1):
            tamaño = os.path.getsize(archivo) / (1024 * 1024)  # MB
            print(f"{i}. {archivo} ({tamaño:.1f} MB)")
        
        try:
            seleccion = int(input(f"\n🎯 Selecciona archivo (1-{len(archivos_audio)}): "))
            
            if 1 <= seleccion <= len(archivos_audio):
                return archivos_audio[seleccion - 1]
            else:
                print("❌ Selección inválida")
                return None
                
        except ValueError:
            print("❌ Por favor ingresa un número válido")
            return None

async def main():
    """
    Función principal del transcriptor médico optimizado
    """
    print("🏥 TRANSCRIPTOR MÉDICO OPTIMIZADO - NOVA-2")
    print("=" * 60)
    print("🤖 Configuración: nova-2 + keywords médicas + análisis completo")
    print("🎯 Optimizado para: Consultas médicas, entrevistas clínicas\n")
    
    transcriptor = TranscriptorMedico()
    
    # Seleccionar archivo
    archivo_seleccionado = transcriptor.seleccionar_archivo()
    
    if not archivo_seleccionado:
        print("❌ No se seleccionó archivo")
        return
    
    # Menú de duración
    print(f"\n⏱️ DURACIÓN DEL SEGMENTO:")
    print("1. 📊 2 minutos (rápido, $0.02)")
    print("2. 📊 5 minutos (balance, $0.05)")
    print("3. 📊 10 minutos (completo, $0.10)")
    print("4. 📊 Personalizado")
    
    try:
        opcion_duracion = int(input("\n🎯 Selecciona duración: "))
        
        duraciones = {1: 120, 2: 300, 3: 600}
        
        if opcion_duracion in duraciones:
            duracion = duraciones[opcion_duracion]
        elif opcion_duracion == 4:
            duracion = int(input("⏱️ Duración en segundos: "))
        else:
            print("❌ Opción inválida")
            return
            
    except ValueError:
        print("❌ Entrada inválida")
        return
    
    # Crear segmento optimizado
    archivo_segmento = transcriptor.crear_segmento_optimizado(archivo_seleccionado, duracion)
    
    if archivo_segmento:
        # Transcribir con análisis completo
        resultado = await transcriptor.transcribir_optimizado(archivo_segmento, incluir_timestamps=True)
        
        if resultado:
            print("\n🎉 ¡TRANSCRIPCIÓN COMPLETADA EXITOSAMENTE!")
            print(f"🎯 Calidad obtenida: {resultado['confidence']:.2%}")
            print("💡 Archivo listo para análisis médico avanzado")
        else:
            print("❌ Error en la transcripción")
    else:
        print("❌ No se pudo crear el segmento de audio")

if __name__ == "__main__":
    asyncio.run(main())
