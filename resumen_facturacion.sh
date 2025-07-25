#!/bin/bash

# Nombre del script Python a ejecutar
SCRIPT="resumen_facturacion.py"

# Nombre del entorno virtual
VENV_DIR="venv-facturas"

# 1. Crear entorno virtual si no existe, usando paquetes del sistema
if [ ! -d "$VENV_DIR" ]; then
    echo "⏳ Creando entorno virtual con acceso a paquetes del sistema..."
    python3 -m venv "$VENV_DIR" --system-site-packages
fi

# 2. Activar entorno virtual
source "$VENV_DIR/bin/activate"

# 3. Verificar si las dependencias necesarias están disponibles
MISSING=()

for pkg in pandas openpyxl; do
    if ! python3 -c "import $pkg" 2>/dev/null; then
        MISSING+=("$pkg")
    fi
done

# 4. Si faltan dependencias, informar y abortar
if [ ${#MISSING[@]} -ne 0 ]; then
    echo "❌ Faltan dependencias: ${MISSING[*]}"
    echo "Este entorno no permite instalar con pip. Por favor, instalalas con apt u otro medio."
    deactivate
    exit 1
fi

# 5. Ejecutar el script Python si existe
if [ -f "$SCRIPT" ]; then
    echo "🚀 Ejecutando $SCRIPT..."
    python3 "$SCRIPT"
else
    echo "❌ Archivo $SCRIPT no encontrado."
fi

# 6. Desactivar entorno virtual
deactivate
