#!/bin/bash

echo "🧪 Instalando Home Assistant en entorno virtual..."

# Crear carpeta para HA
mkdir -p ~/homeassistant
cd ~/homeassistant

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Actualizar pip y wheel
pip install --upgrade pip wheel

# Instalar Home Assistant Core
pip install homeassistant

echo "✅ Instalación completa."
echo "👉 Para iniciar Home Assistant, ejecuta:"
echo "   source ~/homeassistant/venv/bin/activate && hass"

# Instrucción opcional:
echo "⚠️ Nota: El puerto por defecto es http://localhost:8123"
