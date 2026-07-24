"""
Genera el index.html FINAL de produccion con:
- V4 (menu completo + platos reales + paleta violeta/amarillo/turquesa)
- Sellos con logo Grupo Cotorreo (Opcion A)
- JavaScript de la app real (login, get-mis-sellos, canje)
- PWA integrado
- Fotos y logos empaquetados como assets estaticos (no data URI para no inflar HTML)

Este es el archivo que se sube a rewards.grupocotorreo.com/
"""
import os, shutil, base64, io
from PIL import Image

FRONTEND = r"C:\Users\vicente benitez2\cotorreo-rewards\frontend"
ASSETS = os.path.join(FRONTEND, "assets")

# 1. Copiar fotos reales al proyecto assets/
FOTOS_SRC = [
    (r"C:\Users\vicente benitez2\OneDrive\Escritorio\REDES COTORREO\ASSETS-DROPBOX\CARPETA_01\Fotos Local\KSNS cotorreo desayuno-08.jpg", "hero-local.jpg", 1400),
    (r"C:\Users\vicente benitez2\OneDrive\Escritorio\REDES COTORREO\ASSETS-DROPBOX\CARPETA_01\Fotos Cotorreo\Fotos Platos Menú Cotorreo\DSC02116.jpg", "plato-1.jpg", 900),
    (r"C:\Users\vicente benitez2\OneDrive\Escritorio\REDES COTORREO\ASSETS-DROPBOX\CARPETA_01\Fotos Cotorreo\Fotos Platos Menú Cotorreo\DSC02117.jpg", "plato-2.jpg", 900),
    (r"C:\Users\vicente benitez2\OneDrive\Escritorio\REDES COTORREO\ASSETS-DROPBOX\CARPETA_01\Fotos bebidas Cotorreo\BUBBLE TEA CHOCOLATE.jpg", "bebida.jpg", 900),
    (r"C:\Users\vicente benitez2\OneDrive\Escritorio\REDES COTORREO\ASSETS-DROPBOX\CARPETA_01\Fotos Alpadel Octubre\NSM_4944.jpg", "alpadel.jpg", 900),
    (r"C:\Users\vicente benitez2\Downloads\Menú_GrupoCotorreo-01.jpg.jpeg", "menu-p1.jpg", 1600),
    (r"C:\Users\vicente benitez2\Downloads\Menú_GrupoCotorreo-02.jpg.jpeg", "menu-p2.jpg", 1600),
]

os.makedirs(ASSETS, exist_ok=True)
print("=== Copiando + comprimiendo fotos ===")
for src, dst_name, max_w in FOTOS_SRC:
    if not os.path.exists(src):
        print(f"  ! No existe: {src}")
        continue
    img = Image.open(src)
    if img.mode != "RGB": img = img.convert("RGB")
    w, h = img.size
    if w > max_w:
        img = img.resize((max_w, int(h * max_w / w)), Image.LANCZOS)
    out = os.path.join(ASSETS, dst_name)
    img.save(out, "JPEG", quality=82, optimize=True, progressive=True)
    print(f"  + {dst_name}: {os.path.getsize(out)//1024}KB")

# 2. Copiar logos SVG (ya deben estar pero por si acaso)
LOGOS = [
    (r"C:\Users\vicente benitez2\Logos-Grupo-Cotorreo\Grupo Cotorreo\grupo-cotorreo-vertical-blanco.svg", "logo-grupo-blanco.svg"),
    (r"C:\Users\vicente benitez2\Logos-Grupo-Cotorreo\Grupo Cotorreo\grupo-cotorreo-vertical-color.svg", "logo-grupo-color.svg"),
    (r"C:\Users\vicente benitez2\Logos-Grupo-Cotorreo\Cotorreo Plaza\cotorreo-plaza-color.svg", "logo-plaza.svg"),
    (r"C:\Users\vicente benitez2\Logos-Grupo-Cotorreo\Cotorreo Taqueria\cotorreo-taqueria-color.svg", "logo-taqueria.svg"),
    (r"C:\Users\vicente benitez2\Logos-Grupo-Cotorreo\Alpadel\alpadel-vertical-color.svg", "logo-alpadel.svg"),
    (r"C:\Users\vicente benitez2\Logos-Grupo-Cotorreo\Bebros\bebros-color.svg", "logo-bebros.svg"),
    (r"C:\Users\vicente benitez2\Logos-Grupo-Cotorreo\Pits Burger Grill\pits-color.svg", "logo-pits.svg"),
    (r"C:\Users\vicente benitez2\Logos-Grupo-Cotorreo\Nube Suites Motel\nube-color.svg", "logo-nube.svg"),
]
print("\n=== Copiando logos ===")
for src, dst in LOGOS:
    if os.path.exists(src):
        shutil.copy(src, os.path.join(ASSETS, dst))
        print(f"  + {dst}")
    else:
        print(f"  ! No existe: {src}")

print("\nOK todos los assets en frontend/assets/")
