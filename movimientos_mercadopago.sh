#!/bin/bash

# Nombre del entorno virtual
ENTORNO="mp_env"

# Verificar que se haya pasado un parámetro
if [ -z "$1" ]; then
  echo "❌ Debes indicar el nombre del script Python a ejecutar."
  echo "👉 Uso: ./crear_y_ejecutar.sh nombre_script.py"
  exit 1
fi

PYTHON_SCRIPT="$1"

# Verificar si Python3 está instalado
if ! command -v python3 &>/dev/null; then
  echo "❌ Python3 no está instalado."
  exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "$ENTORNO" ]; then
  echo "📦 Creando entorno virtual '$ENTORNO'..."
  python3 -m venv "$ENTORNO"
fi

# Activar entorno virtual
source "$ENTORNO/bin/activate"

# Asegurar pip y actualizar herramientas
echo "⬆️  Actualizando pip y setuptools..."
"$ENTORNO/bin/python" -m ensurepip --upgrade
"$ENTORNO/bin/python" -m pip install --upgrade pip setuptools

# Instalar SDK de Mercado Pago
echo "📥 Instalando SDK de Mercado Pago..."
"$ENTORNO/bin/pip" install mercadopago

# Instalar Librerías para Excel
echo "📥 Instalando Librerías para Excel..."
"$ENTORNO/bin/pip" install openpyxl

# Verificar que el script Python existe
if [ ! -f "$PYTHON_SCRIPT" ]; then
  echo "❌ El archivo '$PYTHON_SCRIPT' no existe."
  exit 1
fi

# Ejecutar el script Python
echo "🚀 Ejecutando '$PYTHON_SCRIPT'..."
"$ENTORNO/bin/python" "$PYTHON_SCRIPT"
