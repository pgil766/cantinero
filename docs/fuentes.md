# Fuentes de la base de conocimiento

Fuentes **realmente usadas** en el *seed* (`data/seed/`, 37 archivos) y en el documento de la demo
(`data/demo/`). Recopiladas el 2026-09-23 (tarea **T3.1**). Los scripts que generan todo están en
`data/tools/`.

> ⚠️ Citar todas las fuentes usadas en el README (T9.1). Wikipedia se publica bajo licencia
> **CC BY-SA 4.0**: al reutilizar su texto hay que atribuirlo y mantener la misma licencia. Cada archivo
> Markdown del seed lleva al inicio su bloque de atribución (título, URL, licencia y fecha de descarga), y
> los PDF/DOCX derivados citan sus fuentes y declaran la misma licencia.

## Convenciones

- **Medidas:** las recetas se guardan en **ml** con su equivalente en **oz** entre paréntesis
  (1 oz ≈ 30 ml; decimales con coma, redondeados a dos cifras). Ej.: `22,5 ml (0,75 oz) de jugo fresco de lima`.
  Las medidas que la IBA no da en ml (cucharaditas, *dashes*, piezas) se traducen tal cual.
- **Traducción de ingredientes:** *lime* → lima; *lemon* → limón; *mint* → hierbabuena (menta);
  *gin* → gin; *sweet red vermouth* → vermut rojo dulce; *cocktail glass* → copa de cóctel.
- **Sin viche en el seed:** el downloader descarta cualquier párrafo que contenga la subcadena
  `viche`/`biche` (lo que también quita, por ejemplo, menciones de «ceviche»), y
  `generar_documentos.py` verifica el texto de todos los archivos del seed, incluidos PDF y DOCX.

## Recetas

| Fuente | URL | Uso | Licencia / notas |
|--------|-----|-----|------------------|
| IBA — cócteles oficiales | https://iba-world.com/cocktails/all-cocktails/ (y `https://iba-world.com/iba-cocktail/<cóctel>/`) | `recetas_iba.csv`: **94 recetas** (33 *Unforgettables*, 30 *Contemporary Classics*, 31 *New Era*), traducidas al español; cada fila cita la URL de su receta | El sitio no publica una licencia abierta; se usan los datos de las recetas (ingredientes, medidas, método), traducidos y citados. Revisar antes de publicar el repositorio. |

Cócteles de la lista IBA **no incluidos** (8 de 102): Bellini, Mimosa, Kir, Spritz, Champagne Cocktail,
Sherry Cobbler y Porto Flip (su base es un vino, espumoso o vino fortificado; los vinos están fuera del
alcance, §3.2), e IBA Tiki (la página oficial da dos medidas sin unidad).

TheCocktailDB **no se usó** (las 94 recetas de la IBA cubren las preguntas de evaluación).

## Artículos de Wikipedia en español (CC BY-SA 4.0) — un Markdown por artículo

| Archivo | Artículo |
|---------|----------|
| `coctel_general.md` | https://es.wikipedia.org/wiki/Cóctel |
| `coctel_terminologia.md` | https://es.wikipedia.org/wiki/Terminología_en_coctelería |
| `coctel_negroni.md` | https://es.wikipedia.org/wiki/Negroni |
| `coctel_mojito.md` | https://es.wikipedia.org/wiki/Mojito |
| `coctel_daiquiri.md` | https://es.wikipedia.org/wiki/Daiquirí |
| `coctel_margarita.md` | https://es.wikipedia.org/wiki/Margarita_(cóctel) |
| `coctel_martini.md` | https://es.wikipedia.org/wiki/Martini_(cóctel) |
| `coctel_manhattan.md` | https://es.wikipedia.org/wiki/Manhattan_(cóctel) |
| `coctel_pina_colada.md` | https://es.wikipedia.org/wiki/Piña_colada |
| `coctel_caipirinha.md` | https://es.wikipedia.org/wiki/Caipiriña |
| `coctel_moscow_mule.md` | https://es.wikipedia.org/wiki/Moscow_mule |
| `destilado_tequila.md` | https://es.wikipedia.org/wiki/Tequila |
| `destilado_mezcal.md` | https://es.wikipedia.org/wiki/Mezcal |
| `destilado_ginebra.md` | https://es.wikipedia.org/wiki/Ginebra_(bebida) |
| `destilado_whisky.md` | https://es.wikipedia.org/wiki/Whisky |
| `destilado_bourbon.md` | https://es.wikipedia.org/wiki/Whisky_de_Bourbon |
| `destilado_ron.md` | https://es.wikipedia.org/wiki/Ron |
| `destilado_vodka.md` | https://es.wikipedia.org/wiki/Vodka |
| `destilado_pisco.md` | https://es.wikipedia.org/wiki/Pisco_(aguardiente) |
| `destilado_aguardiente.md` | https://es.wikipedia.org/wiki/Aguardiente |
| `colombia_aguardiente_antioqueno.md` | https://es.wikipedia.org/wiki/Aguardiente_Antioqueño |
| `colombia_canelazo.md` | https://es.wikipedia.org/wiki/Canelazo |
| `colombia_refajo.md` | https://es.wikipedia.org/wiki/Refajo_(bebida) |
| `colombia_chicha.md` | https://es.wikipedia.org/wiki/Chicha |
| `licor_vermut.md` | https://es.wikipedia.org/wiki/Vermú |
| `licor_campari.md` | https://es.wikipedia.org/wiki/Campari |
| `licor_biter.md` | https://es.wikipedia.org/wiki/Bíter |
| `licor_amargo_de_angostura.md` | https://es.wikipedia.org/wiki/Amargo_de_Angostura |
| `herramienta_coctelera.md` | https://es.wikipedia.org/wiki/Coctelera |
| `cristaleria_general.md` | https://es.wikipedia.org/wiki/Cristalería |
| `cristaleria_copa_de_coctel.md` | https://es.wikipedia.org/wiki/Copa_martinera (redirige desde «Copa de cóctel») |
| `cristaleria_copa_coupe.md` | https://es.wikipedia.org/wiki/Copa_champañera (redirige desde «Copa de champán»; es la copa coupé) |
| `cristaleria_vaso_highball.md` | https://es.wikipedia.org/wiki/Vaso_Highball |
| `cristaleria_vaso_old_fashioned.md` | https://es.wikipedia.org/wiki/Vaso_de_rocas (redirige desde «Vaso Old-Fashioned») |

Correcciones respecto a la lista candidata anterior: `Ginebra` es el artículo de la **ciudad** suiza (se usa
`Ginebra (bebida)`); `Refajo` es la **prenda de vestir** (se usa `Refajo (bebida)`); `Pisco` es una página de
desambiguación (se usa `Pisco (aguardiente)`); `Bitter` es un **tipo de cerveza** inglesa (se usa `Bíter`).
Descartados: `Maceración` (general/culinario), `Mixología` (redirige a `Cóctel`), `Barman` (esbozo sin contenido)
y `Colador` (utensilio de cocina). No existe artículo en español sobre el *jigger*, el colador de cóctel ni el
removido: esa información sale de `Cóctel` y `Terminología en coctelería`.

## Documentos propios derivados (seed)

| Archivo | Contenido | Fuentes (todas citadas dentro del documento) |
|---------|-----------|----------------------------------------------|
| `guia_tecnicas_de_bar.pdf` | Guía de técnicas de bar: métodos (agitado, removido, construido, macerado, colado, capas, licuado), cuándo agitar y cuándo remover, herramientas, medidas, hielo, formas de servir y cristalería | Wikipedia en español: Cóctel, Terminología en coctelería, Coctelera, Martini (cóctel), Copa martinera, Copa champañera, Vaso Highball, Vaso de rocas. Wikipedia en inglés (traducción, CC BY-SA 4.0): [Muddler](https://en.wikipedia.org/wiki/Muddler), [Cocktail strainer](https://en.wikipedia.org/wiki/Cocktail_strainer), [Bar spoon](https://en.wikipedia.org/wiki/Bar_spoon), [Cocktail glass](https://en.wikipedia.org/wiki/Cocktail_glass). Recetas IBA (ejemplos). Licencia del documento: CC BY-SA 4.0 |
| `glosario_cocteleria.docx` | Glosario A–Z (36 términos) | Las anteriores, más Wikipedia en español: Bíter, Amargo de Angostura, Campari, Vermú, Caipiriña y [Cachaza](https://es.wikipedia.org/wiki/Cachaza). Licencia del documento: CC BY-SA 4.0 |

## Documento de la demo (NO va al seed)

`data/demo/guia_destilados_colombianos_viche.pdf` (qué es, origen y región, elaboración, cultura y ley,
uso en coctelería):

| Fuente | URL | Licencia |
|--------|-----|----------|
| Wikipedia en español, «Viche (bebida)» | https://es.wikipedia.org/wiki/Viche_(bebida) | CC BY-SA 4.0 |
| Wikipedia en inglés, «Viche (drink)» | https://en.wikipedia.org/wiki/Viche_(drink) | CC BY-SA 4.0 (traducción) |
| 7 Caníbales, «Viche, destilado histórico del Pacífico colombiano» (Erin Rose) | https://www.7canibales.com/beber/destilados/viche-el-destilado-patrimonial-del-pacifico-colombiano/ | Prensa: datos resumidos con palabras propias y citados |
| Colombia Visible, «En Cali puede probar coctelería con licores como viche, tomaseca y arrechón» (Susana Serrano Arango) | https://colombiavisible.com/en-cali-puede-probar-cocteleria-con-licores-como-viche-tomaseca-y-arrechon/ | Prensa: ídem |
| El Tiempo, «El viche irrumpe en la alta coctelería» (Liliana Martínez Polo, 6-feb-2023) | https://www.eltiempo.com/cultura/gastronomia/el-viche-irrumpe-en-la-alta-cocteleria-guia-de-lugares-donde-disfrutarlo-739764 | Prensa: ídem |

El artículo de Wikipedia sobre el viche no trata su uso en coctelería (y su párrafo de etimología está
corrupto); por eso la sección de coctelería del PDF se apoya en las tres fuentes de prensa.

> Antes de la demo, verificar que **ningún** documento del seed mencione el viche:
> `generar_documentos.py` lo comprueba al final (resultado actual: 0 coincidencias).
