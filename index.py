import os
import sys
import subprocess

# Función para instalar paquetes si no están
def ensure_package(pkg):
    try:
        __import__(pkg)
    except ImportError:
        print(f"📦 Instalando '{pkg}'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

# Verificar e instalar dependencias
ensure_package("rembg")
ensure_package("onnxruntime")

from rembg import remove
from PIL import Image

# Carpetas
input_dir = "inputs"
output_dir = "exports"

# Crear carpeta de exports si no existe
os.makedirs(output_dir, exist_ok=True)

# Extensiones permitidas
valid_exts = (".png", ".jpg", ".jpeg", ".webp", ".bmp")

# Obtener lista de imágenes
images = [f for f in os.listdir(input_dir) if f.lower().endswith(valid_exts)]

if not images:
    print("❌ No se encontraron imágenes en la carpeta 'input'.")
    sys.exit(1)

print(f"🔄 Procesando {len(images)} imagen(es)...")

# Procesar cada imagen
for img_name in images:
    input_path = os.path.join(input_dir, img_name)
    base_name = os.path.splitext(img_name)[0]  # nombre sin extensión
    output_path = os.path.join(output_dir, base_name + ".png")  # siempre PNG

    try:
        inp = Image.open(input_path)
        output = remove(inp)
        output.save(output_path, format="PNG")
        print(f"✅ Procesada: {img_name} → {base_name}.png")
    except Exception as e:
        print(f"❌ Error con {img_name}: {e}")

print("\n🎉 Proceso completado. Archivos guardados en 'exports'.")
