"""Genera data/seed/recetas_iba.csv a partir de las páginas oficiales de la IBA.

Uso:
    py data/tools/generar_csv_iba.py <carpeta_con_html>

<carpeta_con_html> contiene las páginas descargadas de https://iba-world.com/iba-cocktail/<slug>/
(una por cóctel, nombradas <slug>.html). El script:
  1. extrae de cada página el nombre, la categoría y las medidas en ml de la receta original (inglés);
  2. toma la traducción al español de iba_es.py;
  3. verifica que las medidas en ml de la traducción coincidan exactamente con las de la página;
  4. escribe el CSV (UTF-8, separador coma) con medidas en ml y su equivalente en oz (1 oz ≈ 30 ml).
"""
import csv
import glob
import html
import os
import re
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(__file__))
from iba_es import CATEGORIAS, EXCLUIDOS, R  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
NOMBRES = {"pina-colada": "Piña Colada"}  # la IBA escribe "Pina Colada" sin tilde
SALIDA = os.path.join(RAIZ, "data", "seed", "recetas_iba.csv")


def num_es(x: float) -> str:
    s = f"{x:.2f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


def medida(ml: float, texto: str) -> str:
    return f"{num_es(ml)} ml ({num_es(ml / 30)} oz) de {texto}"


def leer_pagina(ruta: str):
    s = open(ruta, encoding="utf-8").read()
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", "\n", t))
    lineas = [l.strip() for l in t.split("\n") if l.strip()]
    i = lineas.index("Ingredients")
    j = lineas.index("Method", i)
    # Migas de pan: Nombre / Categoría / Nombre / N views
    k = next(n for n in range(i, 0, -1) if lineas[n].endswith("views"))
    nombre, categoria = lineas[k - 5], lineas[k - 3]
    ingredientes = " ".join(lineas[i + 1 : j])
    mls = sorted(float(m) for m in re.findall(r"(\d+(?:\.\d+)?)\s*ml", ingredientes, flags=re.I))
    return nombre, categoria, mls


def main(carpeta: str) -> None:
    filas, errores = [], []
    for ruta in sorted(glob.glob(os.path.join(carpeta, "*.html"))):
        slug = os.path.basename(ruta)[:-5]
        if slug in EXCLUIDOS:
            continue
        nombre, categoria, mls = leer_pagina(ruta)
        if slug not in R:
            errores.append(f"{slug}: sin traducción")
            continue
        ings, prep, vaso, guarn = R[slug]
        mls_es = sorted(float(x[0]) for x in ings if isinstance(x, tuple))
        # Ingredientes cuya cantidad en la fuente viene en ml pero traducimos como texto: ninguno.
        if Counter(mls) != Counter(mls_es):
            errores.append(f"{slug}: ml fuente {mls} != traducción {mls_es}")
        texto_ings = "; ".join(medida(*x) if isinstance(x, tuple) else x for x in ings)
        filas.append({
            "nombre": NOMBRES.get(slug) or nombre.replace("’", "'").replace("‘", "'"),
            "categoria_iba": CATEGORIAS[categoria],
            "ingredientes": texto_ings,
            "preparacion": prep,
            "cristaleria": vaso,
            "guarnicion": guarn,
            "fuente_url": f"https://iba-world.com/iba-cocktail/{slug}/",
        })
    faltan = set(R) - {os.path.basename(p)[:-5] for p in glob.glob(os.path.join(carpeta, "*.html"))}
    errores += [f"{s}: traducción sin página" for s in faltan]
    if errores:
        print("\n".join(errores))
        sys.exit(1)
    filas.sort(key=lambda f: f["nombre"].lower())
    os.makedirs(os.path.dirname(SALIDA), exist_ok=True)
    with open(SALIDA, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]), quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(filas)
    print(f"{len(filas)} recetas escritas en {SALIDA}")
    print(Counter(f["categoria_iba"] for f in filas))


if __name__ == "__main__":
    main(sys.argv[1])
