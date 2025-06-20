#!/usr/bin/env python3
"""
Ejemplo de uso básico del Transcriptor Médico Optimizado

Este ejemplo muestra cómo usar el transcriptor médico de forma 
programática para integrar en otros sistemas.
"""

import asyncio
import sys
import os

# Agregar el path del módulo médico
sys.path.append('../')
from transcriptor_medico_final import TranscriptorMedico

async def ejemplo_transcripcion_simple():
    """
    Ejemplo básico de transcripción médica
    """
    print("🏥 EJEMPLO - TRANSCRIPCIÓN MÉDICA BÁSICA")
    print("=" * 50)
    
    # Inicializar transcriptor
    transcriptor = TranscriptorMedico()
    
    # Archivo de prueba (debe existir)
    archivo_prueba = "consulta_ejemplo.wav"
    
    if not os.path.exists(archivo_prueba):
        print(f"❌ Archivo {archivo_prueba} no encontrado")
        print("💡 Coloca un archivo WAV de ejemplo en esta carpeta")
        return
    
    try:
        # Crear segmento de 2 minutos
        print("✂️ Creando segmento de prueba...")
        segmento = transcriptor.crear_segmento_optimizado(archivo_prueba, 120)
        
        if segmento:
            # Transcribir
            print("🎵 Transcribiendo con nova-2...")
            resultado = await transcriptor.transcribir_optimizado(segmento)
            
            if resultado:
                print(f"\n✅ TRANSCRIPCIÓN EXITOSA")
                print(f"📊 Confianza: {resultado['confidence']:.2%}")
                print(f"💾 Archivo: {resultado['output_file']}")
                
                # Mostrar primeros 200 caracteres
                texto = resultado['transcript'][:200]
                print(f"📄 Muestra: {texto}...")
                
                return resultado
            else:
                print("❌ Error en transcripción")
        else:
            print("❌ Error creando segmento")
            
    except Exception as e:
        print(f"❌ Error: {e}")

async def ejemplo_analisis_batch():
    """
    Ejemplo de análisis en lote de múltiples archivos
    """
    print("\n🔬 EJEMPLO - ANÁLISIS EN LOTE")
    print("=" * 40)
    
    transcriptor = TranscriptorMedico()
    
    # Buscar archivos WAV
    import glob
    archivos = glob.glob("*.wav")
    
    if not archivos:
        print("❌ No se encontraron archivos WAV")
        return
    
    resultados = []
    
    for archivo in archivos[:3]:  # Máximo 3 archivos
        print(f"\n📁 Procesando: {archivo}")
        
        # Crear segmento pequeño para demo
        segmento = transcriptor.crear_segmento_optimizado(archivo, 60)
        
        if segmento:
            resultado = await transcriptor.transcribir_optimizado(segmento)
            if resultado:
                resultados.append(resultado)
                print(f"✅ {archivo}: {resultado['confidence']:.2%}")
    
    # Resumen de resultados
    if resultados:
        print(f"\n📊 RESUMEN DE LOTE:")
        print(f"Archivos procesados: {len(resultados)}")
        
        confianza_promedio = sum(r['confidence'] for r in resultados) / len(resultados)
        print(f"Confianza promedio: {confianza_promedio:.2%}")
        
        mejor = max(resultados, key=lambda x: x['confidence'])
        print(f"Mejor resultado: {mejor['archivo']} ({mejor['confidence']:.2%})")

def ejemplo_integracion_n8n():
    """
    Ejemplo de cómo integrar con n8n workflows
    """
    print("\n🔄 EJEMPLO - INTEGRACIÓN N8N")
    print("=" * 35)
    
    # Configuración para webhook n8n
    webhook_config = {
        "url": "http://localhost:5678/webhook/transcripcion-medica",
        "metodo": "POST",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": "Bearer tu_token_n8n"
        }
    }
    
    # Ejemplo de payload que enviarías a n8n
    payload_ejemplo = {
        "action": "transcribir",
        "archivo": "consulta_paciente_001.wav",
        "duracion_segmento": 300,
        "incluir_analisis": True,
        "notificar_completion": True,
        "patient_id": "P001",
        "session_type": "consulta_inicial"
    }
    
    print("📋 Configuración webhook n8n:")
    print(f"URL: {webhook_config['url']}")
    print(f"Método: {webhook_config['metodo']}")
    
    print("\n📤 Payload de ejemplo:")
    import json
    print(json.dumps(payload_ejemplo, indent=2, ensure_ascii=False))
    
    print("\n💡 En n8n, crear workflow que:")
    print("1. Reciba webhook con datos del archivo")
    print("2. Ejecute transcriptor médico")
    print("3. Guarde resultado en Google Drive")
    print("4. Envíe notificación por Gmail")
    print("5. Actualice Google Tasks con seguimiento")

async def ejemplo_uso_programatico():
    """
    Ejemplo de uso programático avanzado
    """
    print("\n🤖 EJEMPLO - USO PROGRAMÁTICO")
    print("=" * 38)
    
    # Configuración personalizada
    configuracion_custom = {
        "duracion_segmento": 180,  # 3 minutos
        "aplicar_filtros": True,
        "analisis_completo": True,
        "guardar_metadatos": True
    }
    
    print("⚙️ Configuración personalizada:")
    for key, value in configuracion_custom.items():
        print(f"  • {key}: {value}")
    
    # Ejemplo de procesamiento automático
    print("\n🔄 Flujo automático:")
    print("1. ✅ Detectar archivos nuevos")
    print("2. ✅ Aplicar filtros de audio")
    print("3. ✅ Transcribir con nova-2")
    print("4. ✅ Analizar contenido médico")
    print("5. ✅ Generar reportes")
    print("6. ✅ Notificar completion")
    
    # Simulación de integración con otros sistemas
    integraciones = {
        "Google Drive": "✅ Guardar transcripciones",
        "Google Calendar": "✅ Agendar seguimientos",
        "Gmail": "✅ Enviar resúmenes",
        "Home Assistant": "✅ Dashboard médico",
        "n8n": "✅ Workflows automatizados"
    }
    
    print("\n🔗 Integraciones disponibles:")
    for sistema, funcion in integraciones.items():
        print(f"  {funcion} via {sistema}")

async def main():
    """
    Ejecutar todos los ejemplos
    """
    print("🏥 EJEMPLOS DE USO - TRANSCRIPTOR MÉDICO")
    print("=" * 60)
    print("🎯 Mostrando diferentes formas de usar el módulo\n")
    
    # Ejecutar ejemplos
    await ejemplo_transcripcion_simple()
    await ejemplo_analisis_batch()
    ejemplo_integracion_n8n()
    await ejemplo_uso_programatico()
    
    print("\n" + "=" * 60)
    print("✅ EJEMPLOS COMPLETADOS")
    print("💡 Para uso real, consulta la documentación completa")
    print("📁 Archivo: medical-ai/transcription/README.md")

if __name__ == "__main__":
    asyncio.run(main())
