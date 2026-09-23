# Fuentes de la base de conocimiento

Fuentes candidatas para el *seed* (`data/seed/`) y para el documento de la demo (`data/demo/`).
Todas se verificaron accesibles el 2026-09-23. La recopilación y conversión se hace en la tarea **T3.1**.

> ⚠️ Citar todas las fuentes usadas en el README (T9.1). Wikipedia se publica bajo licencia
> **CC BY-SA 4.0**: al reutilizar su texto hay que atribuirlo y mantener la misma licencia.

## Recetas

| Fuente | URL | Uso | Formato destino |
|--------|-----|-----|-----------------|
| IBA — cócteles oficiales | https://iba-world.com/cocktails/all-cocktails/ | ~90 recetas oficiales (*Unforgettables*, *Contemporary Classics*, *New Era*) | CSV (una fila por cóctel, medidas en ml + oz) |
| TheCocktailDB (API pública) | https://www.thecocktaildb.com/api.php | Recetas complementarias (revisar sus términos de uso) | CSV |

## Artículos (Wikipedia en español)

| Tema | Artículo |
|------|----------|
| Cócteles en general | https://es.wikipedia.org/wiki/Cóctel |
| Negroni | https://es.wikipedia.org/wiki/Negroni |
| Mojito | https://es.wikipedia.org/wiki/Mojito |
| Daiquiri | https://es.wikipedia.org/wiki/Daiquiri |
| Tequila | https://es.wikipedia.org/wiki/Tequila |
| Mezcal | https://es.wikipedia.org/wiki/Mezcal |
| Ginebra (gin) | https://es.wikipedia.org/wiki/Ginebra |
| Whisky | https://es.wikipedia.org/wiki/Whisky |
| Ron | https://es.wikipedia.org/wiki/Ron |
| Vodka | https://es.wikipedia.org/wiki/Vodka |
| Pisco | https://es.wikipedia.org/wiki/Pisco |
| Aguardiente | https://es.wikipedia.org/wiki/Aguardiente |
| Aguardiente Antioqueño | https://es.wikipedia.org/wiki/Aguardiente_Antioqueño |
| Canelazo | https://es.wikipedia.org/wiki/Canelazo |
| Refajo | https://es.wikipedia.org/wiki/Refajo |
| Chicha | https://es.wikipedia.org/wiki/Chicha |

Faltan por buscar en T3.1: artículos de técnicas (*shake*, *stir*, *muddle*), cristalería, herramientas de bar,
*bitters*, vermut, Campari y bourbon.

## Documento de la demo (NO va al seed)

| Tema | Fuente | Destino |
|------|--------|---------|
| Viche | https://es.wikipedia.org/wiki/Viche_(bebida) (más otras fuentes sobre su uso en coctelería) | `data/demo/guia_destilados_colombianos_viche.pdf` |

> Antes de la demo, verificar que **ningún** documento del seed mencione el viche (por ejemplo, el artículo
> de aguardiente o el de chicha podrían nombrarlo; si es así, quitar ese párrafo).
