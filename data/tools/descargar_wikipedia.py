"""Descarga artículos de Wikipedia en español (texto plano) y los guarda como Markdown en data/seed/.

Uso:
    py data/tools/descargar_wikipedia.py            # descarga y escribe todos los artículos de ARTICULOS
    py data/tools/descargar_wikipedia.py --crudo DIR # además guarda el JSON crudo en DIR

Usa la API de MediaWiki (action=query&prop=extracts&explaintext=1). El texto de Wikipedia se publica
bajo licencia CC BY-SA 4.0: cada archivo lleva un bloque de atribución al inicio.
Se quitan las secciones sin valor para el RAG (Referencias, Enlaces externos, Bibliografía, etc.) y
cualquier párrafo que mencione el viche (reservado para la demo, AGENTS.md §3.3).
"""
import datetime
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SEED = os.path.join(RAIZ, "data", "seed")
API = "https://es.wikipedia.org/w/api.php"
UA = "CantineroSeed/1.0 (proyecto universitario; saracorreacarvajal@gmail.com)"

# archivo destino -> título exacto del artículo en es.wikipedia.org
ARTICULOS = {
    # Cócteles
    "coctel_general.md": "Cóctel",
    "coctel_terminologia.md": "Terminología en coctelería",
    "coctel_negroni.md": "Negroni",
    "coctel_mojito.md": "Mojito",
    "coctel_daiquiri.md": "Daiquiri",
    "coctel_margarita.md": "Margarita (cóctel)",
    "coctel_martini.md": "Martini (cóctel)",
    "coctel_manhattan.md": "Manhattan (cóctel)",
    "coctel_pina_colada.md": "Piña colada",
    "coctel_caipirinha.md": "Caipiriña",
    "coctel_moscow_mule.md": "Moscow mule",
    # Destilados
    "destilado_tequila.md": "Tequila",
    "destilado_mezcal.md": "Mezcal",
    "destilado_ginebra.md": "Ginebra (bebida)",
    "destilado_whisky.md": "Whisky",
    "destilado_bourbon.md": "Whisky de Bourbon",
    "destilado_ron.md": "Ron",
    "destilado_vodka.md": "Vodka",
    "destilado_pisco.md": "Pisco (aguardiente)",
    "destilado_aguardiente.md": "Aguardiente",
    # Coctelería colombiana
    "colombia_aguardiente_antioqueno.md": "Aguardiente Antioqueño",
    "colombia_canelazo.md": "Canelazo",
    "colombia_refajo.md": "Refajo (bebida)",
    "colombia_chicha.md": "Chicha",
    # Licores y modificadores
    "licor_vermut.md": "Vermú",
    "licor_campari.md": "Campari",
    "licor_biter.md": "Bíter",
    "licor_amargo_de_angostura.md": "Amargo de Angostura",
    # Herramientas y cristalería
    "herramienta_coctelera.md": "Coctelera",
    "cristaleria_general.md": "Cristalería",
    "cristaleria_copa_de_coctel.md": "Copa de cóctel",
    "cristaleria_copa_coupe.md": "Copa de champán",
    "cristaleria_vaso_highball.md": "Vaso Highball",
    "cristaleria_vaso_old_fashioned.md": "Vaso Old-Fashioned",
}

SECCIONES_FUERA = {
    "referencias", "enlaces externos", "bibliografía", "véase también", "vease también",
    "notas", "notas y referencias", "fuentes", "lecturas adicionales", "otras lecturas",
    "bibliografía adicional", "citas", "referencias y notas",
}
# Subcadena, no palabra completa: también descarta, por ejemplo, párrafos que dicen "ceviche".
PROHIBIDO = re.compile(r"[vb]iche", re.I)


def pedir(params: dict) -> dict:
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def extracto(titulo: str) -> tuple[str, str]:
    d = pedir({"action": "query", "prop": "extracts|info", "inprop": "url", "explaintext": 1,
               "exsectionformat": "wiki", "redirects": 1, "format": "json", "titles": titulo})
    pagina = next(iter(d["query"]["pages"].values()))
    if "missing" in pagina:
        raise SystemExit(f"No existe el artículo: {titulo}")
    return pagina["title"], pagina["extract"]


def a_markdown(texto: str) -> tuple[str, list[str]]:
    """Convierte '== Sección ==' en encabezados Markdown, quita secciones sin valor y párrafos prohibidos."""
    salida, quitados = [], []
    saltar_nivel = None
    for linea in texto.split("\n"):
        m = re.match(r"^(=+)\s*(.*?)\s*=+\s*$", linea)
        if m:
            nivel = len(m.group(1))  # '==' -> 2
            if saltar_nivel is not None and nivel > saltar_nivel:
                continue
            saltar_nivel = None
            if m.group(2).lower() in SECCIONES_FUERA:
                saltar_nivel = nivel
                continue
            salida.append("")
            salida.append("#" * nivel + " " + m.group(2))
            salida.append("")
            continue
        if saltar_nivel is not None:
            continue
        if PROHIBIDO.search(linea):
            quitados.append(linea)
            continue
        salida.append(linea.replace("​", "").rstrip())  # quita los espacios de ancho cero de las notas
    md = "\n".join(quitar_encabezados_vacios(salida))
    md = re.sub(r"\n{3,}", "\n\n", md).strip()
    return md, quitados


def quitar_encabezados_vacios(lineas: list[str]) -> list[str]:
    """Quita encabezados sin contenido (seguidos solo de otro encabezado de igual o mayor nivel)."""
    cambiado = True
    while cambiado:
        cambiado = False
        utiles = [i for i, l in enumerate(lineas) if l.strip()]
        for pos, i in enumerate(utiles):
            m = re.match(r"^(#+) ", lineas[i])
            if not m:
                continue
            sig = lineas[utiles[pos + 1]] if pos + 1 < len(utiles) else None
            ms = re.match(r"^(#+) ", sig) if sig else None
            if sig is None or (ms and len(ms.group(1)) <= len(m.group(1))):
                del lineas[i]
                cambiado = True
                break
    return lineas


def main() -> None:
    crudo = sys.argv[sys.argv.index("--crudo") + 1] if "--crudo" in sys.argv else None
    hoy = datetime.date.today().isoformat()
    os.makedirs(SEED, exist_ok=True)
    for archivo, titulo in ARTICULOS.items():
        titulo_real, texto = extracto(titulo)
        if crudo:
            os.makedirs(crudo, exist_ok=True)
            with open(os.path.join(crudo, archivo + ".txt"), "w", encoding="utf-8") as f:
                f.write(texto)
        cuerpo, quitados = a_markdown(texto)
        url = "https://es.wikipedia.org/wiki/" + urllib.parse.quote(titulo_real.replace(" ", "_"), safe="()")
        cabecera = (
            f"# {titulo_real}\n\n"
            f"> **Fuente:** artículo «{titulo_real}» de Wikipedia en español — {url}  \n"
            f"> **Licencia:** Texto de Wikipedia en español bajo licencia CC BY-SA 4.0 "
            f"(https://creativecommons.org/licenses/by-sa/4.0/deed.es). Autores: colaboradores de Wikipedia.  \n"
            f"> **Fecha de descarga:** {hoy}. Se omitieron las secciones de referencias, enlaces externos, "
            f"bibliografía y véase también.\n\n"
        )
        with open(os.path.join(SEED, archivo), "w", encoding="utf-8", newline="\n") as f:
            f.write(cabecera + cuerpo + "\n")
        print(f"{archivo}: {titulo_real} ({len(cuerpo)} caracteres; párrafos quitados por viche: {len(quitados)})")
        time.sleep(1)


if __name__ == "__main__":
    main()
