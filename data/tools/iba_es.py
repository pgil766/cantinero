"""Traducción al español de las recetas oficiales de la IBA (iba-world.com).

Cada entrada: slug -> (ingredientes, preparación, cristalería, guarnición).
En los ingredientes, una tupla (ml, texto) es una medida en mililitros tal como la da la IBA;
el generador añade el equivalente en onzas (1 oz ≈ 30 ml). Una cadena se copia tal cual
(medidas que no están en ml: cucharaditas, golpes o "dashes", piezas, etc.).

Fuente de cada receta: https://iba-world.com/iba-cocktail/<slug>/ (consultada el 2026-09-23).
"""

# Cócteles de la lista de la IBA que NO se incluyen en el seed:
EXCLUIDOS = {
    # Su base es un vino, espumoso o vino fortificado (los vinos están fuera del alcance, §3.2).
    "bellini": "base de vino espumoso (Prosecco)",
    "mimosa": "base de vino espumoso (Prosecco)",
    "kir": "base de vino blanco",
    "spritz": "base de vino espumoso (Prosecco)",
    "champagne-cocktail": "base de Champagne",
    "sherry-cobbler": "base de jerez",
    "porto-flip": "base de vino de Oporto",
    # Medidas incompletas en la página oficial (dos ingredientes sin unidad).
    "iba-tiki": "medidas sin unidad en la fuente (90 y 30 sin 'ml')",
}

CATEGORIAS = {
    "The unforgettables": "The Unforgettables (Inolvidables)",
    "Contemporary Classics": "Contemporary Classics (Clásicos contemporáneos)",
    "New Era": "New Era Drinks (Bebidas de la nueva era)",
}

R = {
"alexander": (
    [(30, "coñac (cognac)"), (30, "crema de cacao oscura"), (30, "crema de leche fresca")],
    "Verter todos los ingredientes en una coctelera con cubos de hielo. Agitar (shake) y colar en una copa de cóctel fría.",
    "copa de cóctel", "Nuez moscada recién rallada espolvoreada por encima."),
"americano": (
    [(30, "Campari (bitter Campari)"), (30, "vermut rojo dulce"), "un chorrito de agua con gas (soda)"],
    "Mezclar los ingredientes directamente en un vaso old fashioned lleno de cubos de hielo. Añadir un chorrito de agua con gas. Remover suavemente.",
    "vaso old fashioned", "Media rodaja de naranja y una piel (zest) de limón."),
"angel-face": (
    [(30, "gin"), (30, "brandy de albaricoque (apricot brandy)"), (30, "calvados")],
    "Verter todos los ingredientes en una coctelera con cubos de hielo. Agitar y colar en una copa de cóctel fría.",
    "copa de cóctel", "Sin guarnición."),
"aviation": (
    [(45, "gin"), (15, "licor marrasquino Luxardo"), (15, "jugo fresco de limón"), "1 cucharada de bar de crème de violette (licor de violeta)"],
    "Poner todos los ingredientes en una coctelera. Agitar con hielo picado y colar en una copa de cóctel fría.",
    "copa de cóctel", "Opcional: una cereza marrasquino."),
"bees-knees": (
    [(52.5, "gin seco (dry gin)"), "2 cucharaditas de jarabe de miel", (22.5, "jugo fresco de limón"), (22.5, "jugo fresco de naranja")],
    "Remover la miel con los jugos de limón y de naranja hasta que se disuelva; añadir el gin y agitar con hielo. Colar en una copa de cóctel fría.",
    "copa de cóctel", "Opcional: una piel (zest) de limón o de naranja."),
"between-the-sheets": (
    [(30, "ron blanco"), (30, "coñac (cognac)"), (30, "triple sec"), (20, "jugo fresco de limón")],
    "Poner todos los ingredientes en una coctelera. Agitar con hielo y colar en una copa de cóctel fría.",
    "copa de cóctel", "Sin guarnición."),
"black-russian": (
    [(50, "vodka"), (20, "licor de café")],
    "Verter los ingredientes en un vaso old fashioned lleno de cubos de hielo y remover suavemente. Nota: para el White Russian, hacer flotar crema de leche fresca por encima y removerla lentamente.",
    "vaso old fashioned", "Sin guarnición."),
"bloody-mary": (
    [(45, "vodka"), (90, "jugo de tomate"), (15, "jugo fresco de limón"), "2 golpes (dashes) de salsa Worcestershire", "Tabasco, sal de apio y pimienta al gusto"],
    "Remover suavemente todos los ingredientes en un vaso mezclador con hielo y verter en un vaso rocks. Nota: si se pide con hielo, servir en un vaso highball.",
    "vaso rocks (o vaso highball si se sirve con hielo)", "Apio y una cuña de limón (opcional)."),
"boulevardier": (
    [(45, "bourbon o whiskey de centeno (rye)"), (30, "Campari (bitter Campari)"), (30, "vermut rojo dulce")],
    "Verter todos los ingredientes en un vaso mezclador con cubos de hielo. Remover bien (stir) y colar en una copa de cóctel fría.",
    "copa de cóctel", "Una piel (zest) de naranja u, opcionalmente, de limón."),
"bramble": (
    [(50, "gin"), (25, "jugo fresco de limón"), (12.5, "jarabe de azúcar"), (15, "crème de mûre (licor de mora)")],
    "Verter todos los ingredientes en la coctelera excepto la crème de mûre, agitar bien con hielo y colar en un vaso old fashioned frío lleno de hielo picado; luego verter el licor de mora (crème de mûre) sobre la bebida con un movimiento circular.",
    "vaso old fashioned", "Opcional: una rodaja de limón y moras."),
"brandy-crusta": (
    [(52.5, "brandy"), (7.5, "licor marrasquino Luxardo"), "1 cucharada de bar de curaçao", (15, "jugo fresco de limón"), "1 cucharada de bar de jarabe simple", "2 golpes (dashes) de bitters aromáticos"],
    "Mezclar todos los ingredientes con cubos de hielo en un vaso mezclador y colar en una copa de cóctel estrecha previamente preparada.",
    "copa de cóctel estrecha", "Frotar el borde de la copa con una rodaja de naranja (o limón) y pasarlo por azúcar blanca pulverizada para que se adhiera; colocar con cuidado la piel de naranja o limón enroscada en el interior de la copa."),
"caipirinha": (
    [(60, "cachaça"), "1 lima cortada en cuñas pequeñas", "4 cucharaditas de azúcar blanca de caña"],
    "Poner la lima y el azúcar en un vaso old fashioned doble y macerar (muddle) suavemente. Llenar el vaso con hielo picado y añadir la cachaça. Remover suavemente para integrar los ingredientes. Nota: Caipiroska, con vodka en lugar de cachaça; Caipirissima, con ron en lugar de cachaça; Caipirão, con Licor Beirão en lugar de cachaça.",
    "vaso old fashioned doble", "Sin guarnición."),
"canchanchara": (
    [(60, "aguardiente cubano"), (15, "jugo fresco de lima"), (15, "miel cruda"), (50, "agua")],
    "Mezclar la miel con el agua y el jugo de lima y extender la mezcla en el fondo y las paredes del vaso. Añadir hielo picado y luego el ron (aguardiente cubano). Terminar removiendo enérgicamente de abajo hacia arriba.",
    "vaso (tipo no especificado por la IBA)", "Una cuña de lima."),
"cardinale": (
    [(40, "gin"), (20, "vermut seco"), (10, "Campari (bitter Campari)")],
    "Verter todos los ingredientes en un vaso mezclador con cubos de hielo. Remover bien y colar en una copa de cóctel fría.",
    "copa de cóctel", "Una piel (zest) de limón."),
"casino": (
    [(40, "gin Old Tom"), (10, "licor marrasquino Luxardo"), (10, "jugo fresco de limón"), "2 golpes (dashes) de bitter de naranja"],
    "Verter todos los ingredientes en la coctelera, agitar bien con hielo y colar en un vaso rocks frío con hielo.",
    "vaso rocks", "Una piel (zest) de limón y una cereza marrasquino."),
"chartreuse-swizzle": (
    [(45, "Chartreuse verde"), (30, "jugo fresco de piña"), (22.5, "jugo fresco de lima"), (15, "falernum")],
    "Verter todos los ingredientes en un vaso alto y añadir hielo granizado (pebble ice). Con ayuda de un swizzle stick (o una cuchara de bar) mezclar vigorosamente y terminar llenando el vaso con más hielo granizado.",
    "vaso alto", "Hojas de hierbabuena (menta) y nuez moscada rallada."),
"clover-club": (
    [(45, "gin"), (15, "jarabe de frambuesa"), (15, "jugo fresco de limón"), "unas gotas de clara de huevo"],
    "Verter todos los ingredientes en la coctelera, agitar bien con hielo y colar en una copa de cóctel fría.",
    "copa de cóctel", "Frambuesas frescas."),
"corpse-reviver-2": (
    [(30, "gin"), (30, "Cointreau"), (30, "Lillet Blanc"), (30, "jugo fresco de limón"), "1 golpe (dash) de absenta"],
    "Verter todos los ingredientes en una coctelera con hielo. Agitar bien y colar en una copa de cóctel fría.",
    "copa de cóctel", "Una piel (zest) de naranja."),
"cosmopolitan": (
    [(40, "vodka cítrico (vodka citron)"), (15, "Cointreau"), (15, "jugo fresco de lima"), (30, "jugo de arándano rojo")],
    "Poner todos los ingredientes en una coctelera con hielo. Agitar bien y colar en una copa de cóctel grande.",
    "copa de cóctel grande", "Un twist de limón."),
"cuba-libre": (
    [(50, "ron blanco"), (120, "cola"), (10, "jugo fresco de lima")],
    "Construir (build) todos los ingredientes directamente en un vaso highball lleno de hielo.",
    "vaso highball", "Una cuña de lima."),
"daiquiri": (
    [(60, "ron blanco cubano"), (20, "jugo fresco de lima"), "2 cucharadas de bar de azúcar superfina"],
    "En una coctelera poner todos los ingredientes y remover bien para disolver el azúcar. Añadir hielo y agitar. Colar en una copa de cóctel fría.",
    "copa de cóctel", "Sin guarnición."),
"dark-n-stormy": (
    [(60, "ron Goslings"), (100, "ginger beer (cerveza de jengibre)")],
    "En un vaso highball lleno de hielo verter la ginger beer y completar haciendo flotar el ron por encima.",
    "vaso highball", "Una cuña o rodaja de lima."),
"dons-special-daiquiri": (
    [(30, "ron dorado de Jamaica"), (15, "ron cubano"), (15, "jarabe de maracuyá (fruta de la pasión)"), (15, "jugo fresco de lima"), (15, "jarabe de miel")],
    "Licuar (blend) unos segundos en una batidora de malteadas con hielo picado y verter en un vaso copo con pie. Llenar el vaso con más hielo picado.",
    "vaso copo con pie", "Medio maracuyá (fruta de la pasión)."),
"dry-martini": (
    [(60, "gin"), (10, "vermut seco")],
    "Verter todos los ingredientes en un vaso mezclador con cubos de hielo. Remover bien (stir) y colar en una copa martini fría.",
    "copa martini", "Exprimir los aceites de una piel de limón sobre la bebida o, si se pide, decorar con aceitunas verdes."),
"espresso-martini": (
    [(50, "vodka"), (30, "Kahlúa (licor de café)"), (10, "jarabe de azúcar"), "1 café espresso fuerte"],
    "Verter todos los ingredientes en la coctelera, agitar bien con hielo y colar en una copa de cóctel fría.",
    "copa de cóctel", "3 granos de café."),
"fernandito": (
    [(50, "Fernet Branca"), "completar con cola"],
    "Verter el Fernet Branca en un vaso old fashioned doble con hielo y completar el vaso con cola. Remover suavemente.",
    "vaso old fashioned doble", "Sin guarnición."),
"french-75": (
    [(30, "gin"), (15, "jugo fresco de limón"), (15, "jarabe de azúcar"), (60, "champaña (Champagne)")],
    "Verter todos los ingredientes excepto la champaña en una coctelera. Agitar bien y colar en una copa flauta de champaña. Completar con champaña y remover suavemente.",
    "copa flauta", "Sin guarnición."),
"french-connection": (
    [(35, "coñac (cognac)"), (35, "amaretto")],
    "Verter todos los ingredientes directamente en un vaso old fashioned lleno de cubos de hielo. Remover suavemente.",
    "vaso old fashioned", "Sin guarnición."),
"french-martini": (
    [(45, "vodka"), (15, "licor de frambuesa"), (15, "jugo fresco de piña")],
    "Verter todos los ingredientes en la coctelera, agitar bien con hielo y colar en una copa de cóctel fría.",
    "copa de cóctel", "Exprimir los aceites de una piel de limón sobre la bebida."),
"garibaldi": (
    [(45, "Campari (bitter Campari)"), (120, "jugo de naranja recién exprimido")],
    "Construir (build) todos los ingredientes en un vaso highball lleno de hielo.",
    "vaso highball", "Una cuña de naranja."),
"gin-basil-smash": (
    [(60, "gin"), (22.5, "jugo de limón recién exprimido"), (22.5, "jarabe de azúcar"), "10 hojas de albahaca italiana"],
    "Poner todos los ingredientes en una coctelera con hielo. Agitar vigorosamente y verter en una copa de cóctel fría.",
    "copa de cóctel", "Sin guarnición."),
"gin-fizz": (
    [(45, "gin"), (30, "jugo fresco de limón"), (10, "jarabe simple"), "un chorrito de agua con gas (soda)"],
    "Agitar todos los ingredientes con hielo excepto el agua con gas. Verter en un vaso tumbler alto y delgado y completar con un chorrito de agua con gas. Nota: se sirve sin hielo.",
    "vaso tumbler alto", "Una rodaja de limón; opcionalmente, una piel (zest) de limón."),
"grand-margarita": (
    [(45, "tequila 100 % de agave"), (30, "Grand Marnier"), (15, "jugo fresco de lima")],
    "Escarchar el borde de un vaso rocks con sal marina de buena calidad. Verter los ingredientes en la coctelera. Poner hielo en el vaso y en la coctelera. Agitar con fuerza durante 10 segundos y colar la bebida en el vaso.",
    "vaso rocks", "Una rodaja de lima."),
"grasshopper": (
    [(20, "crema de cacao blanca"), (20, "crema de menta verde"), (20, "crema de leche fresca")],
    "Verter todos los ingredientes en una coctelera llena de hielo. Agitar enérgicamente durante unos segundos y colar en una copa de cóctel fría.",
    "copa de cóctel", "Sin guarnición; opcional, una hoja de menta."),
"hanky-panky": (
    [(45, "gin London Dry"), (45, "vermut rojo dulce"), (7.5, "Fernet")],
    "Verter todos los ingredientes en un vaso mezclador con cubos de hielo. Remover bien y colar en una copa de cóctel fría.",
    "copa de cóctel", "Una piel (zest) de naranja."),
"hemingway-special": (
    [(60, "ron"), (40, "jugo de toronja (pomelo)"), (15, "licor marrasquino Luxardo"), (15, "jugo fresco de lima")],
    "Verter todos los ingredientes en una coctelera con hielo. Agitar bien y colar en una copa de cóctel grande.",
    "copa de cóctel grande", "Sin guarnición."),
"horses-neck": (
    [(40, "coñac (cognac)"), (120, "ginger ale"), "un golpe (dash) de amargo de Angostura (opcional)"],
    "Verter el coñac y el ginger ale directamente en un vaso highball con cubos de hielo. Remover suavemente. Si se prefiere, añadir unos golpes de Angostura.",
    "vaso highball", "La cáscara de un limón entero cortada en espiral."),
"illegal": (
    [(30, "mezcal espadín"), (15, "ron blanco overproof de Jamaica"), (15, "falernum"), "1 cucharada de bar de licor marrasquino Luxardo", (22.5, "jugo fresco de lima"), (15, "jarabe simple"), "unas gotas de clara de huevo (opcional)"],
    "Verter todos los ingredientes en la coctelera. Agitar vigorosamente con hielo. Colar en una copa de cóctel fría, o servir con hielo (on the rocks) en una taza tradicional de barro o terracota.",
    "copa de cóctel (o taza de barro o terracota)", "Sin guarnición."),
"irish-coffee": (
    [(50, "whiskey irlandés"), (120, "café caliente"), (50, "crema de leche fresca fría"), "1 cucharadita de azúcar"],
    "Verter el café negro caliente en una copa de Irish coffee precalentada. Añadir el whiskey y al menos una cucharadita de azúcar y remover hasta disolver. Verter con cuidado la crema fresca, espesa y fría, sobre el dorso de una cuchara sostenida justo encima de la superficie del café; la capa de crema flotará sobre el café sin mezclarse. El azúcar puede sustituirse por jarabe de azúcar.",
    "copa de Irish coffee", "Sin guarnición."),
"john-collins": (
    [(45, "gin"), (30, "jugo fresco de limón"), (15, "jarabe simple"), (60, "agua con gas (soda)")],
    "Verter todos los ingredientes directamente en un vaso highball lleno de hielo. Remover suavemente. Nota: con gin Old Tom se convierte en Tom Collins.",
    "vaso highball", "Una rodaja de limón y una cereza marrasquino."),
"jungle-bird": (
    [(45, "ron blackstrap"), (22.5, "Campari"), (45, "jugo de piña"), (15, "jugo de lima recién exprimido"), (15, "jarabe de azúcar demerara")],
    "Verter todos los ingredientes en una coctelera con hielo y agitar. Colar en un vaso rocks lleno de hielo.",
    "vaso rocks", "Una cuña de piña."),
"last-word": (
    [(22.5, "gin"), (22.5, "Chartreuse verde"), (22.5, "licor marrasquino Luxardo"), (22.5, "jugo fresco de lima")],
    "Poner todos los ingredientes en una coctelera. Agitar con hielo y colar en una copa de cóctel fría.",
    "copa de cóctel", "Sin guarnición."),
"lemon-drop-martini": (
    [(30, "vodka"), (20, "triple sec"), (15, "jugo de limón recién exprimido")],
    "Verter todos los ingredientes en una coctelera con hielo. Agitar bien y colar en una copa de cóctel fría.",
    "copa de cóctel", "Sin guarnición."),
"long-island-iced-tea": (
    [(15, "vodka"), (15, "tequila"), (15, "ron blanco"), (15, "gin"), (15, "Cointreau"), (25, "jugo de limón"), (30, "jarabe simple"), "completar con cola"],
    "Poner todos los ingredientes en un vaso highball lleno de hielo. Remover suavemente.",
    "vaso highball", "Una rodaja de limón (opcional)."),
"mai-tai": (
    [(30, "ron ámbar de Jamaica"), (30, "rhum de melaza de Martinica*"), (15, "curaçao de naranja"), (15, "jarabe de orgeat (almendra)"), (30, "jugo de lima recién exprimido"), (7.5, "jarabe simple")],
    "Poner todos los ingredientes en una coctelera con hielo. Agitar y verter en un vaso rocks doble o en un vaso highball. *El ron de melaza de Martinica que usaba Trader Vic no era un rhum agrícola, sino un tipo de ron de melaza.",
    "vaso rocks doble o vaso highball", "Una lanza de piña, hojas de hierbabuena (menta) y piel de lima."),
"manhattan": (
    [(50, "whiskey de centeno (rye)"), (20, "vermut rojo dulce"), "1 golpe (dash) de amargo de Angostura"],
    "Verter todos los ingredientes en un vaso mezclador con cubos de hielo. Remover bien (stir) y colar en una copa de cóctel fría.",
    "copa de cóctel", "Una cereza de cóctel."),
"margarita": (
    [(50, "tequila 100 % de agave"), (20, "triple sec"), (15, "jugo de lima recién exprimido")],
    "Poner todos los ingredientes en una coctelera con hielo. Agitar y colar en una copa de cóctel fría.",
    "copa de cóctel", "Medio borde escarchado con sal (opcional)."),
"martinez": (
    [(45, "gin London Dry"), (45, "vermut rojo dulce"), "1 cucharada de bar de licor marrasquino Luxardo", "2 golpes (dashes) de bitter de naranja"],
    "Verter todos los ingredientes en un vaso mezclador con cubos de hielo. Remover bien y colar en una copa de cóctel fría.",
    "copa de cóctel", "Una piel (zest) de limón."),
"mary-pickford": (
    [(45, "ron blanco"), (45, "jugo fresco de piña"), (7.5, "licor marrasquino Luxardo"), (5, "jarabe de granadina")],
    "Verter todos los ingredientes en la coctelera, agitar bien con hielo y colar en una copa de cóctel fría.",
    "copa de cóctel", "Sin guarnición."),
"mint-julep": (
    [(60, "bourbon"), "4 ramitas frescas de hierbabuena (menta)", "1 cucharadita de azúcar glas", "2 cucharaditas de agua"],
    "En una copa julep de acero inoxidable, macerar (muddle) suavemente la hierbabuena con el azúcar y el agua. Llenar la copa con hielo picado, añadir el bourbon y remover bien hasta que la copa se escarche.",
    "copa julep de acero inoxidable", "Una ramita de hierbabuena (menta)."),
"missionarys-downfall": (
    [(30, "ron blanco"), (15, "brandy de durazno (melocotón)"), (15, "jugo fresco de lima"), (30, "mezcla de miel (honey mix)"), "10 hojas de hierbabuena (menta)", "3 o 4 trozos de piña"],
    "Licuar (blend) todos los ingredientes con media taza de hielo picado. Servir en una copa grande (coppa grande).",
    "copa grande", "Una ramita de hierbabuena (menta) y una rodaja de piña."),
"mojito": (
    [(45, "ron blanco cubano"), (20, "jugo fresco de lima"), "6 ramitas de hierbabuena (menta)", "2 cucharaditas de azúcar blanca de caña", "agua con gas (soda)"],
    "Mezclar las ramitas de hierbabuena con el azúcar y el jugo de lima. Añadir un chorrito de agua con gas y llenar el vaso con hielo. Verter el ron y completar con agua con gas. Remover ligeramente para integrar todos los ingredientes.",
    "vaso (tipo no especificado por la IBA)", "Ramitas de hierbabuena (menta) y una rodaja de lima."),
"monkey-gland": (
    [(45, "gin seco (dry gin)"), (45, "jugo fresco de naranja"), "1 cucharada de absenta", "1 cucharada de jarabe de granadina"],
    "Verter todos los ingredientes en la coctelera, agitar bien con hielo y colar en una copa de cóctel fría.",
    "copa de cóctel", "Sin guarnición."),
"moscow-mule": (
    [(45, "vodka Smirnoff"), (120, "ginger beer (cerveza de jengibre)"), (10, "jugo fresco de lima")],
    "En una taza Mule (mule cup) o en un vaso rocks, combinar el vodka y la ginger beer. Añadir el jugo de lima y remover suavemente para integrar todos los ingredientes.",
    "taza Mule (mule cup) o vaso rocks", "Una rodaja de lima."),
"naked-and-famous": (
    [(22.5, "mezcal"), (22.5, "Chartreuse amarillo"), (22.5, "Aperol"), (22.5, "jugo fresco de lima")],
    "Verter todos los ingredientes en la coctelera, agitar bien con hielo y colar en una copa de cóctel fría.",
    "copa de cóctel", "Sin guarnición."),
"negroni": (
    [(30, "gin"), (30, "Campari (bitter Campari)"), (30, "vermut rojo dulce")],
    "Verter todos los ingredientes directamente en un vaso old fashioned frío lleno de hielo. Remover suavemente.",
    "vaso old fashioned", "Media rodaja de naranja."),
"new-york-sour": (
    [(60, "whiskey de centeno (rye) o bourbon"), (22.5, "jarabe simple"), (30, "jugo fresco de limón"), "unas gotas de clara de huevo", (15, "vino tinto (Shiraz o Malbec)")],
    "Verter todos los ingredientes en la coctelera. Agitar vigorosamente con hielo. Colar en un vaso rocks frío lleno de hielo. Hacer flotar el vino por encima.",
    "vaso rocks", "Una piel (zest) de limón o de naranja con una cereza."),
"old-cuban": (
    ["6 a 8 hojas de hierbabuena (menta)", (45, "ron añejo"), (22.5, "jugo fresco de lima"), (30, "jarabe simple"), "2 golpes (dashes) de amargo de Angostura", (60, "champaña brut o Prosecco")],
    "Verter todos los ingredientes en la coctelera excepto el vino espumoso, agitar bien con hielo y colar en una copa de cóctel elegante y fría. Completar con el vino espumoso.",
    "copa de cóctel", "Ramitas de hierbabuena (menta)."),
"old-fashioned": (
    [(45, "bourbon o whiskey de centeno (rye)"), "1 terrón de azúcar", "unos golpes (dashes) de amargo de Angostura", "unos golpes de agua natural"],
    "Poner el terrón de azúcar en un vaso old fashioned y empaparlo con el bitter (Angostura); añadir unos golpes de agua natural. Macerar (muddle) hasta disolverlo. Llenar el vaso con cubos de hielo y añadir el whisky. Remover suavemente.",
    "vaso old fashioned", "Una rodaja o piel (zest) de naranja y una cereza de cóctel."),
"paloma": (
    [(50, "tequila 100 % de agave"), (5, "jugo fresco de lima"), "una pizca de sal", (100, "soda de toronja rosada (pomelo rosado)")],
    "Verter el tequila en un vaso highball y exprimir el jugo de lima. Añadir hielo y sal y completar con la soda de toronja rosada. Remover suavemente.",
    "vaso highball", "Una rodaja de lima."),
"paper-plane": (
    [(30, "bourbon"), (30, "Amaro Nonino"), (30, "Aperol"), (30, "jugo fresco de limón")],
    "Verter todos los ingredientes en la coctelera, agitar bien con hielo y colar en una copa de cóctel fría.",
    "copa de cóctel", "Sin guarnición."),
"paradise": (
    [(30, "gin"), (20, "brandy de albaricoque (apricot brandy)"), (15, "jugo fresco de naranja")],
    "Verter todos los ingredientes en la coctelera, agitar bien con hielo y colar en una copa de cóctel fría.",
    "copa de cóctel", "Sin guarnición."),
"penicillin": (
    [(60, "whisky escocés de mezcla (blended scotch)"), (7.5, "whisky Lagavulin 16 años (single malt de Islay)"), (22.5, "jugo fresco de limón"), (22.5, "jarabe de miel"), "2 o 3 rodajas de jengibre fresco del tamaño de una moneda"],
    "Macerar (muddle) el jengibre fresco en una coctelera y añadir los demás ingredientes excepto el whisky single malt de Islay. Llenar la coctelera con hielo y agitar. Colar con colador fino (doble colado) en un vaso old fashioned frío con hielo. Hacer flotar el whisky single malt por encima.",
    "vaso old fashioned", "Rodajas de jengibre confitado."),
"pina-colada": (
    [(50, "ron blanco"), (30, "crema de coco"), (50, "jugo fresco de piña")],
    "Licuar (blend) todos los ingredientes con hielo en una licuadora eléctrica, verter en un vaso grande y servir con pajitas. Nota: históricamente se añadían al gusto unas gotas de jugo fresco de lima. Se pueden usar 4 rodajas de piña fresca en lugar del jugo.",
    "vaso grande", "Una rodaja de piña con una cereza de cóctel."),
"pisco-punch": (
    [(60, "pisco"), (22.5, "jugo fresco de piña"), (15, "jarabe simple"), (15, "jugo fresco de limón"), (30, "vino blanco seco"), "3 clavos de olor"],
    "Machacar suavemente el jarabe simple con los clavos de olor y añadir los demás ingredientes excepto el vino. Agitar vigorosamente y colar dos veces (doble colado) en una copa goblet grande. Añadir el vino por encima y remover suavemente.",
    "copa goblet grande", "Sin guarnición."),
"pisco-sour": (
    [(60, "pisco"), (30, "jugo fresco de limón"), (20, "jarabe simple"), "1 clara de huevo cruda entera"],
    "Poner todos los ingredientes en una coctelera con hielo. Agitar y colar en una copa goblet fría.",
    "copa goblet", "Unos golpes de amargo (bitters) por encima como guarnición aromática."),
"planters-punch": (
    [(45, "ron de Jamaica"), (15, "jugo de lima"), (30, "jugo de caña de azúcar")],
    "Verter todos los ingredientes directamente en un vaso tumbler pequeño o en un vaso típico de terracota. Nota: diluir al gusto con agua, hielo o jugos frescos.",
    "vaso tumbler pequeño o vaso de terracota", "Una piel (zest) de naranja."),
"porn-star-martini": (
    [(50, "vodka de vainilla"), (20, "licor de maracuyá (fruta de la pasión)"), (50, "puré de maracuyá (fruta de la pasión)"), "2 cucharadas de bar de azúcar de vainilla", (50, "champaña, servida aparte")],
    "Verter todos los ingredientes en la coctelera, agitar bien con hielo y colar dos veces (doble colado) en una copa de cóctel grande y fría. Acompañar con un shot de champaña.",
    "copa de cóctel grande", "Media fruta de maracuyá y azúcar."),
"rabo-de-galo": (
    [(60, "cachaça"), (20, "vermut dulce Cinzano Rosso"), (15, "Cynar"), "2 gotas de Angostura (opcional)"],
    "Combinar todos los ingredientes en un vaso rocks, añadir hielo y remover brevemente.",
    "vaso rocks", "Un twist de naranja."),
"ramos-fizz": (
    [(45, "gin"), (15, "jugo fresco de lima"), (15, "jugo fresco de limón"), (30, "jarabe de azúcar"), (60, "crema de leche"), (30, "clara de huevo"), "3 golpes (dashes) de agua de azahar", "2 gotas de extracto de vainilla", "agua con gas (soda)"],
    "Verter todos los ingredientes excepto el agua con gas en una coctelera con hielo. Agitar durante dos minutos, colar dos veces en un vaso, devolver la bebida a la coctelera y agitar con fuerza sin hielo durante un minuto. Colar en un vaso highball y completar con agua con gas. Nota: la bebida la inventó Henry Ramos en 1888 en su bar Meyer's Table d'Hôtel Internationale de Nueva Orleans; originalmente se agitaba durante 12 minutos por un equipo de 30 bartenders que se pasaban la coctelera de uno a otro.",
    "vaso highball", "Sin guarnición."),
"remember-the-maine": (
    [(60, "whiskey de centeno (rye)"), (22.5, "vermut dulce"), (15, "Cherry Brandy Luxardo"), (7.5, "absenta")],
    "Verter la absenta en una copa coupé y hacerla girar para cubrir por completo el interior. Desechar la absenta y reservar la copa. Poner los demás ingredientes en un vaso mezclador y llenarlo con hielo hasta 3/4. Remover hasta enfriar y colar en la copa enjuagada con absenta.",
    "copa coupé", "Una piel (zest) de limón."),
"russian-spring-punch": (
    [(25, "vodka"), (25, "jugo fresco de limón"), (15, "crème de cassis (licor de grosella negra)"), (10, "jarabe de azúcar"), "completar con vino espumoso"],
    "Verter todos los ingredientes en la coctelera excepto el vino espumoso, agitar bien con hielo, colar en un vaso tumbler alto y frío lleno de hielo y completar con vino espumoso.",
    "vaso tumbler alto", "Moras y, opcionalmente, una rodaja de limón."),
"rusty-nail": (
    [(45, "whisky escocés (scotch)"), (25, "Drambuie")],
    "Verter todos los ingredientes directamente en un vaso old fashioned lleno de hielo. Remover suavemente.",
    "vaso old fashioned", "Una piel (zest) de limón."),
"sazerac": (
    [(50, "coñac (cognac)"), (10, "absenta"), "1 terrón de azúcar", "2 golpes (dashes) de Peychaud's Bitters"],
    "Enjuagar un vaso old fashioned frío con la absenta, añadir hielo picado y reservar. Remover los demás ingredientes con hielo en un vaso mezclador. Desechar el hielo y el exceso de absenta del vaso preparado y colar en él la bebida. Nota: la receta original cambió tras la guerra de Secesión estadounidense; el whiskey de centeno (rye) sustituyó al coñac porque este se volvió difícil de conseguir.",
    "vaso old fashioned", "Una piel (zest) de limón."),
"sea-breeze": (
    [(40, "vodka"), (120, "jugo de arándano rojo"), (30, "jugo de toronja (pomelo)")],
    "Construir (build) todos los ingredientes en un vaso highball lleno de hielo.",
    "vaso highball", "Una piel (zest) de naranja y una cereza."),
"sex-on-the-beach": (
    [(40, "vodka"), (20, "licor de durazno (peach schnapps)"), (40, "jugo fresco de naranja"), (40, "jugo de arándano rojo")],
    "Construir (build) todos los ingredientes en un vaso highball lleno de hielo.",
    "vaso highball", "Media rodaja de naranja."),
"sidecar": (
    [(50, "coñac (cognac)"), (20, "triple sec"), (20, "jugo fresco de limón")],
    "Verter todos los ingredientes en la coctelera, agitar bien con hielo y colar en una copa de cóctel fría.",
    "copa de cóctel", "Sin guarnición."),
"singapore-sling": (
    [(30, "gin"), (15, "licor de cereza Sangue Morlacco"), (7.5, "Cointreau"), (7.5, "DOM Bénédictine"), (120, "jugo fresco de piña"), (15, "jugo fresco de lima"), (10, "jarabe de granadina"), "un golpe (dash) de amargo de Angostura"],
    "Verter todos los ingredientes en una coctelera llena de cubos de hielo. Agitar bien y colar en una copa Hurricane.",
    "copa Hurricane", "Piña y una cereza marrasquino."),
"south-side": (
    [(60, "gin London Dry"), (30, "jugo fresco de limón"), (15, "jarabe simple"), "5 o 6 hojas de hierbabuena (menta)", "unas gotas de clara de huevo (opcional)"],
    "Verter todos los ingredientes en una coctelera, agitar bien con hielo y colar dos veces (doble colado) en una copa de cóctel fría. Nota: si se usa clara de huevo, agitar vigorosamente.",
    "copa de cóctel", "Ramitas de hierbabuena (menta)."),
"spicy-fifty": (
    [(50, "vodka de vainilla"), (15, "cordial de flor de saúco"), (15, "jugo fresco de lima"), (10, "jarabe de miel Monin"), "2 rodajas finas de ají (chile) rojo"],
    "Verter todos los ingredientes en una coctelera, agitar bien con hielo y colar dos veces (doble colado) en una copa de cóctel fría.",
    "copa de cóctel", "Un ají (chile) rojo."),
"stinger": (
    [(50, "coñac (cognac)"), (20, "crema de menta blanca")],
    "Verter todos los ingredientes en un vaso mezclador con cubos de hielo. Remover bien y colar en una copa martini fría.",
    "copa martini", "Opcional: una hoja de menta."),
"suffering-bastard": (
    [(30, "coñac o brandy"), (30, "gin"), (15, "jugo fresco de lima"), "2 golpes (dashes) de amargo de Angostura", "completar con ginger beer (cerveza de jengibre)"],
    "Verter todos los ingredientes en la coctelera excepto la ginger beer y agitar bien con hielo. Verter sin colar en un vaso Collins o en la taza original Suffering Bastard y completar con ginger beer.",
    "vaso Collins (o taza Suffering Bastard)", "Una ramita de hierbabuena (menta) y, opcionalmente, una rodaja de naranja."),
"tequila-sunrise": (
    [(45, "tequila"), (90, "jugo fresco de naranja"), (15, "jarabe de granadina")],
    "Verter el tequila y el jugo de naranja directamente en un vaso highball lleno de cubos de hielo. Añadir el jarabe de granadina para crear el efecto cromático (amanecer o sunrise); no remover.",
    "vaso highball", "Media rodaja de naranja o una piel (zest) de naranja."),
"three-dots-and-a-dash": (
    [(45, "rhum agrícola de Martinica"), (15, "ron añejo de mezcla (blended aged rum)"), (7.5, "falernum"), (7.5, "licor de pimienta de Jamaica (Allspice Saint Elizabeth)"), (15, "jugo fresco de lima"), (15, "jugo fresco de naranja"), (15, "jarabe de miel"), "2 golpes (dashes) de amargo de Angostura"],
    "Verter todos los ingredientes en una licuadora con 12 onzas de hielo picado, licuar brevemente (flash blend) y verter la bebida en un vaso copo con pie. Llenar el vaso con más hielo picado.",
    "vaso copo con pie", "Tres cerezas y un trozo rectangular de piña."),
"tipperary": (
    [(50, "whiskey irlandés"), (25, "vermut rojo dulce"), (15, "Chartreuse verde"), "2 golpes (dashes) de amargo de Angostura"],
    "Verter todos los ingredientes en un vaso mezclador con cubos de hielo. Remover bien y colar en una copa martini fría.",
    "copa martini", "Una rodaja de naranja."),
"tommys-margarita": (
    [(60, "tequila 100 % de agave"), (30, "jugo fresco de lima"), (30, "néctar (sirope) de agave")],
    "Verter todos los ingredientes en una coctelera, agitar bien con hielo y colar en un vaso rocks frío lleno de hielo.",
    "vaso rocks", "Una rodaja de lima."),
"trinidad-sour": (
    [(45, "amargo de Angostura"), (30, "jarabe de orgeat"), (22.5, "jugo fresco de limón"), (15, "whiskey de centeno (rye)")],
    "Verter todos los ingredientes en una coctelera y agitar bien con hielo. Colar en una copa de cóctel fría.",
    "copa de cóctel", "Sin guarnición."),
"tuxedo": (
    [(30, "gin Old Tom"), (30, "vermut seco"), "1/2 cucharada de bar de licor marrasquino Luxardo", "1/4 de cucharada de bar de absenta", "3 golpes (dashes) de bitter de naranja"],
    "Verter todos los ingredientes en un vaso mezclador con cubos de hielo. Remover bien y colar en una copa martini fría.",
    "copa martini", "Una cereza y una piel (zest) de limón."),
"ve-n-to": (
    [(45, "grappa blanca suave"), (22.5, "jugo fresco de limón"), (15, "mezcla de miel (honey mix; el agua puede sustituirse por manzanilla)*"), (15, "cordial de manzanilla"), "unas gotas de clara de huevo (opcional)"],
    "Verter todos los ingredientes en la coctelera. Agitar vigorosamente con hielo. Colar en un vaso tumbler pequeño y frío lleno de hielo. *Si se desea, el agua de la mezcla de miel puede reemplazarse por infusión de manzanilla.",
    "vaso tumbler pequeño", "Una piel (zest) de limón y uvas blancas."),
"vesper": (
    [(45, "gin"), (15, "vodka"), (7.5, "Lillet Blanc")],
    "Verter todos los ingredientes en una coctelera llena de cubos de hielo. Agitar y colar en una copa de cóctel fría.",
    "copa de cóctel", "Una piel (zest) de limón."),
"vieux-carre": (
    [(30, "whiskey de centeno (rye)"), (30, "coñac (cognac)"), (30, "vermut dulce"), "1 cucharada de bar de Bénédictine", "2 golpes (dashes) de Peychaud's Bitters"],
    "Verter todos los ingredientes en un vaso mezclador con cubos de hielo. Remover bien y colar en una copa de cóctel fría.",
    "copa de cóctel", "Una piel (zest) de naranja y una cereza marrasquino."),
"whiskey-sour": (
    [(45, "bourbon"), (25, "jugo fresco de limón"), (20, "jarabe de azúcar"), "unas gotas de clara de huevo (opcional)"],
    "Verter todos los ingredientes en una coctelera llena de hielo y agitar bien. Colar en un vaso cobbler. Si se sirve con hielo (on the rocks), colar en un vaso old fashioned lleno de hielo. Nota: si se usa clara de huevo, agitar un poco más fuerte para liberar e incorporar la espuma de la clara.",
    "vaso cobbler (o vaso old fashioned si se sirve con hielo)", "Media rodaja de naranja y una cereza marrasquino; opcionalmente, una piel (zest) de naranja."),
"white-lady": (
    [(40, "gin"), (30, "triple sec"), (20, "jugo fresco de limón")],
    "Verter todos los ingredientes en la coctelera, agitar bien con hielo y colar en una copa de cóctel fría.",
    "copa de cóctel", "Sin guarnición."),
"zombie": (
    [(45, "ron oscuro de Jamaica"), (45, "ron dorado de Puerto Rico"), (30, "ron Demerara"), (20, "jugo fresco de lima"), (15, "falernum"), (15, "Donn's Mix*"), "1 cucharadita de jarabe de granadina", "1 golpe (dash) de amargo de Angostura", "6 gotas de Pernod"],
    "Poner todos los ingredientes en una licuadora eléctrica con 170 gramos de hielo picado. Licuar a pulsos durante unos segundos. Servir en un vaso tumbler alto. *Donn's Mix: 2 partes de jugo fresco de toronja amarilla y 1 parte de jarabe de canela.",
    "vaso tumbler alto", "Hojas de hierbabuena (menta)."),
}

R = {k: v for k, v in R.items() if v is not None}
