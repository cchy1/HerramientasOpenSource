# 🏥 Medical-AI - Módulo de IA Médica

Módulo especializado para transcripción y análisis de consultas médicas, optimizado para el proyecto **TDAH Workflow Optimization Strategy**.

## 🎯 Características Principales

- **Transcripción de alta precisión** (>99% confianza) usando Deepgram nova-2
- **Análisis médico automatizado** con vocabulario especializado
- **Separación automática** médico/paciente 
- **Optimización TDAH-friendly** para flujos de trabajo eficientes
- **Integración completa** con Google Workspace y n8n

## 📁 Estructura del Módulo

```
medical-ai/
├── transcription/           # Transcripción médica
├── analysis/               # Análisis con IA (futuro)
└── workflows/              # Workflows n8n (futuro)
```

## 🚀 Inicio Rápido

### Prerrequisitos

1. **ffmpeg** instalado:
   ```bash
   brew install ffmpeg
   ```

2. **API Key de Deepgram** configurada en `.env`:
   ```bash
   DEEPGRAM_API_KEY=tu_clave_aqui
   ```

### Instalación

```bash
cd medical-ai/transcription
pip install -r requirements.txt
```

### Uso Básico

```bash
python transcriptor_medico_final.py
```

## 📊 Resultados Comprobados

| Configuración | Confianza | Uso Recomendado |
|---------------|-----------|-----------------|
| Nova-2 Optimizada | 99.99% | ✅ **Producción** |
| Nova-2 + Keywords | 96.85% | ✅ Estándar |
| General + Keywords | 93.75% | ⚠️ Básico |

## 🔬 Análisis Automático

El sistema detecta automáticamente:

### Categorías Médicas
- **ROLES**: doctor, médico, paciente, doctora
- **SÍNTOMAS FÍSICOS**: dolor, palpitaciones, mareo, fatiga
- **SÍNTOMAS PSICOLÓGICOS**: ansiedad, depresión, estrés
- **MEDICAMENTOS**: medicamento, dosis, tratamiento
- **ESCALAS**: nivel, intensidad, grado
- **TEMPORALES**: semana, mes, día, frecuencia

### Métricas de Calidad
- Confianza por speaker
- Participación porcentual 
- Análisis de sentimiento básico
- Estadísticas de sesión

## 💰 Costos Aproximados

| Duración | Costo | Uso Recomendado |
|----------|-------|-----------------|
| 2 minutos | $0.02 | 🔄 Pruebas rápidas |
| 5 minutos | $0.05 | ⚖️ Balance óptimo |
| 10 minutos | $0.10 | 📋 Análisis completo |

## 🎛️ Configuración Óptima

```python
config_optima = {
    "language": "es",
    "model": "nova-2",          # Máxima calidad
    "smart_format": True,
    "punctuate": True,
    "diarize": True,            # Separación speakers
    "keywords": [               # Términos médicos priorizados
        "doctor", "médico", "paciente", "síntomas", 
        "dolor", "medicamento", "tratamiento", 
        "ansiedad", "depresión"
    ]
}
```

## 🔧 Optimizaciones de Audio

El sistema aplica automáticamente:
- **Filtro pasa-altos**: 100Hz (elimina ruido de fondo)
- **Filtro pasa-bajos**: 8kHz (optimiza rango de voz)
- **Amplificación**: +20% (mejora audibilidad)
- **Conversión**: 16kHz mono (formato óptimo)

## 📁 Archivos de Salida

Cada transcripción genera:
- **Transcripción principal** con alta precisión
- **Análisis médico categorizado** por términos
- **Separación por speakers** con estadísticas
- **Recomendaciones** para mejoras futuras
- **Metadatos de sesión** para seguimiento

## 🧠 Integración TDAH

Optimizaciones específicas para profesionales con TDAH:
- **Segmentación automática** (evita archivos largos)
- **Análisis inmediato** (feedback rápido)
- **Archivos estructurados** (fácil navegación)
- **Resúmenes visuales** (información clara)
- **Flujo no interrumpible** (mantiene concentración)

## 🔄 Workflow Típico

1. **Selección de archivo** automática
2. **Segmentación optimizada** con filtros
3. **Transcripción nova-2** de alta calidad
4. **Análisis médico** automatizado
5. **Archivo estructurado** listo para revisión

## 🛠️ Troubleshooting

### Error: ffmpeg no encontrado
```bash
brew install ffmpeg
```

### Error: API Key no válida
Verificar en `.env`:
```bash
cat ../../.env | grep DEEPGRAM
```

### Baja calidad de audio
- Usar archivos WAV de 16kHz
- Verificar que el micrófono funcione bien
- Evitar ruido de fondo durante grabación

## 📈 Roadmap

### ✅ Completado
- [x] Transcripción de alta calidad (nova-2)
- [x] Análisis médico automatizado
- [x] Separación de speakers
- [x] Optimizaciones TDAH

### 🔄 En Desarrollo
- [ ] Streaming en tiempo real
- [ ] Integración con n8n workflows
- [ ] Análisis avanzado con IA
- [ ] Dashboard en Home Assistant

### 🎯 Futuro
- [ ] Detección automática de síntomas
- [ ] Sugerencias de diagnóstico
- [ ] Integración con historiales clínicos
- [ ] Análisis de patrones TDAH

## 🤝 Contribución

Este módulo es parte del proyecto **HerramientasOpenSource** bajo licencia MIT.

### Autores
- Juan Carlos Sánchez ([@cchy1](https://github.com/cchy1))
- Agrícola López Sánchez Limitada

### Contacto
- Proyecto: [HerramientasOpenSource](https://github.com/cchy1/HerramientasOpenSource)
- Documentación: Ver archivos de ejemplo en `/examples/`

---

*Optimizado para profesionales de salud mental con TDAH de alto funcionamiento*
