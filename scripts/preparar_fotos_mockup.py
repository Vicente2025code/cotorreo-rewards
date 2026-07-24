"""
Selecciona ~5 fotos representativas de Cotorreo, las comprime y arma un HTML mockup pro.
Usa Pillow para redimensionar (max 1000px) + JPEG quality 78 para peso razonable.
"""
import os, base64, io
from PIL import Image

FOTOS = [
    # (path, nombre_uso, ancho_max)
    (r"C:\Users\vicente benitez2\OneDrive\Escritorio\REDES COTORREO\ASSETS-DROPBOX\CARPETA_01\Fotos Local\KSNS cotorreo desayuno-08.jpg", "hero_local", 1200),
    (r"C:\Users\vicente benitez2\OneDrive\Escritorio\REDES COTORREO\ASSETS-DROPBOX\CARPETA_01\Fotos Cotorreo\Fotos Platos Menú Cotorreo\DSC02116.jpg", "plato_1", 800),
    (r"C:\Users\vicente benitez2\OneDrive\Escritorio\REDES COTORREO\ASSETS-DROPBOX\CARPETA_01\Fotos Cotorreo\Fotos Platos Menú Cotorreo\DSC02117.jpg", "plato_2", 800),
    (r"C:\Users\vicente benitez2\OneDrive\Escritorio\REDES COTORREO\ASSETS-DROPBOX\CARPETA_01\Fotos bebidas Cotorreo\BUBBLE TEA CHOCOLATE.jpg", "bebida", 800),
    (r"C:\Users\vicente benitez2\OneDrive\Escritorio\REDES COTORREO\ASSETS-DROPBOX\CARPETA_01\Fotos Alpadel Octubre\NSM_4944.jpg", "alpadel", 800),
]

def redim_a_data_uri(src, max_w, quality=78):
    img = Image.open(src)
    if img.mode != "RGB":
        img = img.convert("RGB")
    w, h = img.size
    if w > max_w:
        new_h = int(h * max_w / w)
        img = img.resize((max_w, new_h), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=quality, optimize=True, progressive=True)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/jpeg;base64,{b64}", len(buf.getvalue())

resultados = {}
total_kb = 0
for path, nombre, max_w in FOTOS:
    if not os.path.exists(path):
        print(f"  ! No existe: {path}")
        continue
    uri, size = redim_a_data_uri(path, max_w)
    resultados[nombre] = uri
    total_kb += size // 1024
    print(f"  + {nombre}: {size//1024}KB")

print(f"\nTotal fotos: {total_kb}KB")

# Logos SVG (color) para cada negocio
LOGOS = [
    ("cotorreo_plaza", r"C:\Users\vicente benitez2\Logos-Grupo-Cotorreo\Cotorreo Plaza\cotorreo-plaza-color.svg"),
    ("cotorreo_taqueria", r"C:\Users\vicente benitez2\Logos-Grupo-Cotorreo\Cotorreo Taqueria\cotorreo-taqueria-color.svg"),
    ("alpadel", r"C:\Users\vicente benitez2\Logos-Grupo-Cotorreo\Alpadel\alpadel-vertical-color.svg"),
    ("bebros", r"C:\Users\vicente benitez2\Logos-Grupo-Cotorreo\Bebros\bebros-color.svg"),
    ("pits", r"C:\Users\vicente benitez2\Logos-Grupo-Cotorreo\Pits Burger Grill\pits-color.svg"),
    ("nube", r"C:\Users\vicente benitez2\Logos-Grupo-Cotorreo\Nube Suites Motel\nube-color.svg"),
    ("grupo_vertical_blanco", r"C:\Users\vicente benitez2\Logos-Grupo-Cotorreo\Grupo Cotorreo\grupo-cotorreo-vertical-blanco.svg"),
]

logos_data = {}
for nombre, path in LOGOS:
    if not os.path.exists(path):
        print(f"  ! Logo no existe: {path}")
        continue
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    logos_data[nombre] = f"data:image/svg+xml;base64,{b64}"
    print(f"  + logo {nombre}: {len(b64)//1024}KB")

# Guardar mapa a JSON para usar en el HTML
import json
out = r"C:\Users\VICENT~1\AppData\Local\Temp\claude\C--Users-vicente-benitez2\9638ccb6-fcd5-4b92-b05b-dd6c7ef1c6e2\scratchpad\assets-mockup.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump({"fotos": resultados, "logos": logos_data}, f)
print(f"\nAssets guardados en: {out}")
