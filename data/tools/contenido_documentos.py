"""Contenido de los documentos PDF y DOCX del seed y del documento de la demo.

Todo el texto está redactado (resumido, reordenado o traducido) a partir de las fuentes citadas en cada
documento. No se añaden datos que no estén en ellas. Los textos de Wikipedia se reutilizan bajo
CC BY-SA 4.0, por lo que estos documentos derivados se distribuyen bajo la misma licencia.
"""

WIKI_LICENCIA = (
    "Este documento es una obra derivada de artículos de Wikipedia (textos bajo licencia Creative Commons "
    "Atribución-CompartirIgual 4.0, CC BY-SA 4.0, https://creativecommons.org/licenses/by-sa/4.0/deed.es; "
    "autores: colaboradores de Wikipedia) y se distribuye bajo la misma licencia."
)

# ---------------------------------------------------------------------------------------------
# 1. Guía de técnicas de bar (PDF, va al seed)
# ---------------------------------------------------------------------------------------------
GUIA_TECNICAS = {
    "archivo": "guia_tecnicas_de_bar.pdf",
    "titulo": "Guía de técnicas de bar",
    "subtitulo": "Métodos de preparación, herramientas, medidas, hielo y cristalería para coctelería",
    "intro": (
        "Guía de consulta del proyecto Cantinero. Resume, a partir de las fuentes citadas al final, las técnicas "
        "básicas para preparar cócteles (agitar, remover, construir, macerar, colar, licuar y hacer capas), las "
        "herramientas de la barra, las medidas habituales y el tipo de vaso o copa que se usa en cada caso. "
        "Convención de medidas del proyecto: 1 onza (oz) equivale aproximadamente a 30 ml."
    ),
    "secciones": [
        ("1. Métodos de preparación", [
            ("Agitado (shake o shaken)",
             "Los cócteles agitados se preparan mezclando los ingredientes en una coctelera con hielo. Este método "
             "integra los sabores y enfría la bebida rápidamente, y además le da cierta espuma o textura. Se emplea "
             "especialmente en cócteles que incluyen jugos de frutas, cremas o ingredientes densos. La coctelera es "
             "necesaria porque hay ingredientes que, si no se agitan, no se mezclan bien, como el jugo de tomate y el "
             "vodka de un Bloody Mary. Se agitan los cócteles con jugos, siropes (jarabes), productos lácteos, "
             "ingredientes de diferentes densidades o de textura cremosa. Ejemplos de la IBA que se agitan: Daiquiri, "
             "Margarita, Sidecar, Whiskey Sour y Pisco Sour."),
            ("Removido o mezclado (stir o stirred)",
             "Los cócteles mezclados o revueltos (stirred) se elaboran removiendo suavemente los ingredientes en un "
             "vaso mezclador con hielo, normalmente con una cuchara de bar. Este método mantiene la claridad y la "
             "suavidad de la bebida y es el indicado para licores puros o cócteles que no llevan jugos ni cremas. "
             "Ejemplos de la IBA que se preparan en vaso mezclador y se remueven: Dry Martini, Manhattan, "
             "Boulevardier, Martinez y Vieux Carré. Sobre el Martini existe una discusión conocida en la cultura "
             "popular: el personaje James Bond lo pide «agitado, no revuelto»."),
            ("Cuándo agitar y cuándo remover",
             "Regla práctica que se desprende de las fuentes: se agita en coctelera cuando la receta lleva jugos de "
             "frutas, jarabes, lácteos o cremas, huevo o ingredientes de densidades distintas, porque la agitación "
             "los integra, los enfría y les da espuma o textura; se remueve en vaso mezclador cuando el cóctel está "
             "hecho solo de destilados, licores o vermut (sin jugos ni cremas), para que quede claro y suave."),
            ("Directo o construido (build o built)",
             "Se habla de un cóctel «construido» cuando se sirve en el mismo vaso en el que se prepara: no se agita en "
             "coctelera, sino que se vierten los ingredientes y se mezclan en el vaso con la cuchara de bar. Para "
             "construir un cóctel primero se agrega el hielo, luego las bebidas alcohólicas y finalmente los "
             "ingredientes sin alcohol; se termina removiendo levemente con la cuchara de bar y añadiendo la "
             "decoración. Es el método más sencillo y se usa en bebidas largas y refrescantes. La mayoría de los "
             "tragos largos servidos en vaso de tubo son construidos, por ejemplo el Cuba Libre, el John Collins, la "
             "Caipiriña, el Black Russian, el Moscow Mule y el Mint Julep."),
            ("Macerado (muddle)",
             "Macerar (en inglés, muddle) es machacar frutas, hierbas o especias en el fondo del vaso para liberar sus "
             "aromas y sabores. Se hace con el macerador o muddler, una herramienta con forma de pequeño bate que debe "
             "ser lo bastante larga para tocar el fondo del vaso; puede ser de madera, plástico o acero inoxidable y su "
             "extremo puede ser liso, texturizado o dentado. Los ingredientes se maceran en el fondo del vaso antes de "
             "añadir cualquier líquido. Cócteles que usan macerador: Mojito (con ron blanco), Caipiriña (con cachaça), "
             "Caipiroska (con vodka), Mint Julep (con bourbon) y Old Fashioned (con whisky o brandy). En la receta "
             "IBA de la Caipiriña, por ejemplo, la lima y el azúcar se maceran suavemente en el vaso antes de añadir "
             "el hielo picado y la cachaça."),
            ("Colado (strain), doble colado y colado fino",
             "Los cócteles colados se filtran al servirlos para eliminar restos de hielo o pulpa y lograr una textura "
             "limpia y uniforme. Suele aplicarse a los cócteles agitados o removidos antes de servirlos en la copa. El "
             "doble colado (double strain) combina el colador Hawthorne con un colador fino adicional para evitar "
             "cualquier resto de pulpa o de hielo triturado."),
            ("En capas (layered o pousse-café)",
             "Los cócteles por capas se consiguen con ingredientes de diferentes densidades, vertiéndolos lentamente "
             "uno sobre otro con ayuda de una cucharilla (o del dorso de una cuchara) para que no se mezclen. Hay "
             "cócteles de dos hasta siete capas. También reciben el nombre de pousse-café. En la receta IBA del "
             "Irish Coffee, la crema fría se vierte sobre el dorso de una cuchara para que flote sobre el café."),
            ("Licuado o frozen (blend)",
             "Los cócteles frozen (por ejemplo, Frozen Daiquiri o Frozen Caipiriña) no son una familia, sino otra forma "
             "de preparación: se hacen con hielo picado en lugar de hielo en cubos. En las recetas IBA de la Piña "
             "Colada y del Zombie los ingredientes se licúan con hielo en una licuadora eléctrica."),
            ("Flambeado",
             "Algunos cócteles se encienden antes de servirlos, sobre todo por el efecto visual de las llamas, aunque "
             "con ciertos alcoholes también se modifica el sabor y se aporta un matiz tostado. Las fuentes advierten "
             "que esta técnica solo debe hacerla un experto."),
        ]),
        ("2. Herramientas de la barra", [
            ("Coctelera (shaker)",
             "Recipiente diseñado para mezclar bebidas. Se colocan los ingredientes (jugos de fruta, licores, cubitos "
             "de hielo, etc.) y se bate agitadamente durante algunos segundos. La mayoría de las modernas son de acero. "
             "Tipos: Boston shaker, formado por dos vasos (uno de metal y otro de vidrio o metal) que se encajan y se "
             "agitan juntos, con colador por separado; Cobbler shaker, de tres piezas (vaso, colador incorporado y "
             "tapa); y French shaker, de dos piezas metálicas, similar al Boston pero sin colador incorporado."),
            ("Vaso mezclador (mixing glass)",
             "Vaso grande de vidrio o acero donde se mezclan los ingredientes removiéndolos; es el ideal para los "
             "cócteles que no requieren agitación vigorosa."),
            ("Cuchara de bar (bar spoon)",
             "Cuchara larga y delgada que permite remover con precisión y llegar al fondo del vaso mezclador o del vaso "
             "más alto. Contiene unos 5 ml (como una cucharadita) y sirve también para medir pequeños volúmenes y para "
             "hacer capas. Su mango suele ser delgado y retorcido para girarla fácilmente con los dedos."),
            ("Jigger (medidor)",
             "Vaso medidor de doble punta, con dos lados de distinta capacidad (por ejemplo, 30 ml y 60 ml), que "
             "permite medir con precisión los licores y otros ingredientes líquidos. Tiene forma de pequeño diábolo "
             "(dos conos unidos por la punta); generalmente mide 2 onzas (u onza y media) por un lado y 3/4 de onza "
             "(o 1 onza) por el otro."),
            ("Pourer (vertedor)",
             "Pico que se coloca en la boca de la botella y restringe el flujo a una tasa estándar, lo que permite "
             "medir contando: contar hasta 6 equivale aproximadamente a 1,5 oz, hasta 4 a 1 oz (un pony) y hasta 3 a "
             "3/4 oz. No es un método exacto, porque los líquidos de distinta viscosidad fluyen a distinta velocidad."),
            ("Colador (strainer)",
             "Accesorio metálico que se coloca sobre la boca de la coctelera o del vaso mezclador para retener el hielo, "
             "la pulpa o las semillas al servir. Colador Hawthorne: disco con mango y un muelle (resorte) en el borde "
             "que se ajusta al recipiente; es el más usado en la coctelería profesional y debe su nombre al Hawthorne "
             "Café de Boston. Colador Julep: con forma de cuenco o cazo pequeño con agujeros; fue el primer colador "
             "diseñado para cócteles (1868). Colador fino o chinois: malla muy fina para separar partículas pequeñas."),
            ("Macerador (muddler)",
             "Instrumento de madera, plástico o acero para machacar frutas, hierbas o especias en el fondo del vaso "
             "(véase «Macerado»)."),
            ("Otras herramientas",
             "Cuchillo de bar y tabla de cortar (para gajos, rodajas y cubos de fruta), pelador o zester (para tiras de "
             "cáscara de cítricos o twists), mortero, exprimidores de cítricos, ralladores (nuez moscada, chocolate), "
             "pinzas para guarniciones y batidor o licuadora eléctrica."),
        ]),
        ("3. Medidas", [
            ("Onza, pony, shot y jigger",
             "La onza líquida estadounidense (US fl oz) es la medida estándar en coctelería. Un pony equivale a 1 oz "
             "(unos 30 ml); un shot o jigger estándar, a 1,5 oz (44 ml); y un doble, a 3 oz (89 ml). En el proyecto "
             "Cantinero las recetas se expresan en ml con su equivalente en oz (1 oz ≈ 30 ml)."),
            ("Dash (golpe)",
             "Medida imprecisa muy común en la coctelería anglosajona; equivale a «una pizca» o «un chorrito». Se usa "
             "sobre todo con los bitters (amargos), por ejemplo «2 dashes de Angostura»."),
            ("Cucharada de bar",
             "Alrededor de 5 ml."),
        ]),
        ("4. Hielo y dilución", [
            ("Dilución",
             "Es la cantidad de agua que aporta el hielo al derretirse. No es un defecto: el agua fría suaviza el "
             "sabor fuerte del alcohol y realza los sabores secundarios. Cuanto más pequeños los trozos de hielo, más "
             "rápido se derriten; y cuanto más hielo, más tarda en fundirse, por eso se llenan los vasos hasta arriba. "
             "En la coctelera se usan trozos grandes, que resisten mejor los golpes del shake."),
            ("Tipos de hielo",
             "Hielo en cubos: el más versátil, preferido para servir on the rocks. Hielo picado o frappé: se derrite "
             "rápido; se recomienda para cócteles dulces y tropicales como el mojito o el daiquirí y para los frozen. "
             "Hielo bola: esfera de 3 a 5 cm de radio que se derrite muy lentamente. Hielo cobbler: variante del "
             "picado que mantiene el frío más tiempo; se usa, por ejemplo, en el Bramble. Hielo seco: dióxido de "
             "carbono sólido que produce un efecto de niebla; no se debe tocar ni ingerir."),
        ]),
        ("5. Formas de servir", [
            ("Straight up / up",
             "Bebida que se agita o mezcla con hielo y luego se cuela y se sirve sin hielo."),
            ("Neat",
             "Licor sin mezclar, sin enfriar y sin agua ni hielo."),
            ("On the rocks (en las rocas)",
             "Servido sobre cubos de hielo, típicamente en vaso old fashioned y a veces en vaso Collins."),
            ("Trago largo y trago corto",
             "Los tragos largos (long drinks) están pensados para beberse lentamente; suelen llevar dos tercios de "
             "bebida sin alcohol y un tercio de bebida alcohólica. Los tragos cortos (short drinks) llevan menos "
             "líquido y se beben más rápido."),
        ]),
        ("6. Cristalería", [
            ("Copa de cóctel o copa martini",
             "Copa con tallo (fuste) y cáliz en forma de cono invertido, usada principalmente para cócteles servidos "
             "sin hielo (straight up). El tallo permite sostenerla sin calentar la bebida y la boca ancha acerca los "
             "aromas a la nariz. Contiene de 90 a 300 ml. Se usa para el Martini y sus variantes, el Manhattan, el "
             "Brandy Alexander, el Pisco Sour, el Cosmopolitan, el Gimlet y el Grasshopper. La copa de cóctel es algo "
             "más pequeña y redondeada que la copa martini, que es puramente cónica."),
            ("Copa coupé (copa champañera o de champán)",
             "Copa de boca ancha y cáliz poco profundo, con capacidad de 180 a 240 ml. Aunque nació para el champán, hoy "
             "su uso se está reorientando hacia cócteles como el daiquirí y otros tragos con hielo picado, y a menudo "
             "se usa como sustituta de la copa martini porque esta tiende a derramar su contenido. Entre las recetas "
             "oficiales de la IBA, el Remember the Maine se sirve expresamente en copa coupé; y, según la Wikipedia en "
             "inglés, la coupé se usa a veces en lugar de la copa de cóctel para los cócteles que se sirven en ella."),
            ("Vaso highball (vaso alto o de trago largo)",
             "Vaso alto para cócteles de trago largo, que se beben lentamente, generalmente con hielo. Contiene entre "
             "24 y 35 cl (8 a 12 oz). Es más alto que el vaso old fashioned y más corto y ancho que el vaso Collins. "
             "Ejemplos: gin tonic, Cuba Libre y, en las recetas IBA, Tequila Sunrise, Garibaldi, Horse's Neck y "
             "Dark 'N' Stormy."),
            ("Vaso old fashioned (vaso de rocas o lowball)",
             "Vaso corto de borde ancho y base gruesa, para destilados solos o con hielo y para cócteles como el Old "
             "Fashioned, del que recibe su nombre, y el Negroni. Su base gruesa permite macerar ingredientes en él. "
             "Contiene 180 a 300 ml; el old fashioned doble, 350 a 470 ml."),
            ("Vaso Collins",
             "Vaso alto, similar al highball pero más largo y estrecho, de paredes completamente verticales, para "
             "cócteles largos con abundante hielo."),
            ("Copa flauta",
             "Copa estrecha y alargada para bebidas espumosas, que conserva las burbujas más tiempo (por ejemplo, el "
             "French 75 de la IBA)."),
        ]),
    ],
    "fuentes": [
        "Wikipedia en español, «Cóctel»: https://es.wikipedia.org/wiki/Cóctel",
        "Wikipedia en español, «Terminología en coctelería»: https://es.wikipedia.org/wiki/Terminología_en_coctelería",
        "Wikipedia en español, «Coctelera»: https://es.wikipedia.org/wiki/Coctelera",
        "Wikipedia en español, «Martini (cóctel)»: https://es.wikipedia.org/wiki/Martini_(cóctel)",
        "Wikipedia en español, «Copa martinera»: https://es.wikipedia.org/wiki/Copa_martinera",
        "Wikipedia en español, «Copa champañera»: https://es.wikipedia.org/wiki/Copa_champañera",
        "Wikipedia en español, «Vaso Highball»: https://es.wikipedia.org/wiki/Vaso_Highball",
        "Wikipedia en español, «Vaso de rocas»: https://es.wikipedia.org/wiki/Vaso_de_rocas",
        "Wikipedia en inglés, «Muddler» (traducción): https://en.wikipedia.org/wiki/Muddler",
        "Wikipedia en inglés, «Cocktail strainer» (traducción): https://en.wikipedia.org/wiki/Cocktail_strainer",
        "Wikipedia en inglés, «Bar spoon» (traducción): https://en.wikipedia.org/wiki/Bar_spoon",
        "Wikipedia en inglés, «Cocktail glass» (traducción): https://en.wikipedia.org/wiki/Cocktail_glass",
        "International Bartenders Association (IBA), recetas oficiales: https://iba-world.com/cocktails/all-cocktails/",
    ],
}

# ---------------------------------------------------------------------------------------------
# 2. Glosario de coctelería (DOCX, va al seed)
# ---------------------------------------------------------------------------------------------
GLOSARIO = {
    "archivo": "glosario_cocteleria.docx",
    "titulo": "Glosario de coctelería",
    "intro": (
        "Glosario de términos de bar del proyecto Cantinero, ordenado alfabéticamente. Las definiciones están "
        "redactadas a partir de las fuentes citadas al final. Convención de medidas: 1 onza (oz) ≈ 30 ml."
    ),
    "terminos": [
        ("Agitado (shake, shaken)", "Técnica que mezcla los ingredientes en una coctelera con hielo; integra sabores, enfría rápido y da espuma o textura. Se usa con jugos de frutas, jarabes, lácteos, cremas o ingredientes densos."),
        ("Amargo (bitter o bíter)", "Bebida alcohólica aromatizada con esencias de hierbas y de sabor amargo. Se prepara por infusión o destilación de hierbas aromáticas, cortezas, raíces y frutas (angostura, cascarilla, genciana, cáscara de naranja, quina). Los bitters aromáticos se usan en pequeñas cantidades (dashes) para aromatizar cócteles; otros, como el Campari, se usan como aperitivo y también en cócteles."),
        ("Amargo de Angostura", "Bitter aromático de sabor amargo con un 44,7 % de alcohol en volumen, elaborado por primera vez en Venezuela en 1824 por el médico alemán Johann Gottlieb Benjamin Siegert. En las recetas de la IBA aparece, por ejemplo, en el Old Fashioned, el Manhattan, el Singapore Sling y el Zombie."),
        ("Build, built (construido)", "Cóctel que se prepara y se sirve en el mismo vaso: primero el hielo, luego las bebidas alcohólicas y al final los ingredientes sin alcohol; se remueve levemente con la cuchara de bar. Ejemplos: Cuba Libre, John Collins, Moscow Mule."),
        ("Cachaça (cachaza)", "Bebida alcohólica destilada de Brasil que se obtiene destilando el jugo de caña de azúcar fermentado, exprimido fresco; se diferencia del ron, que se obtiene a partir de la melaza. Es el ingrediente principal de la Caipiriña (caipirinha), que además lleva lima o limón, azúcar y hielo."),
        ("Campari", "Bebida alcohólica de grado medio, calificable como aperitivo, de característico color rojo y sabor amargo. Es uno de los tres ingredientes del Negroni, junto con el gin y el vermut rojo."),
        ("Chaser", "Bebida suave que se toma justo después de un chupito para compensar la fuerza del alcohol."),
        ("Coctelera (shaker)", "Recipiente para mezclar bebidas agitándolas. Tipos: Boston (dos vasos que encajan, colador aparte), Cobbler (tres piezas con colador incorporado y tapa) y French (dos piezas metálicas sin colador)."),
        ("Colador (strainer)", "Accesorio que retiene el hielo, la pulpa o las semillas al servir. El Hawthorne tiene un muelle en el borde; el Julep tiene forma de cazo con agujeros; el colador fino o chinois es de malla muy fina."),
        ("Copa coupé (copa champañera)", "Copa de boca ancha y cáliz poco profundo (180 a 240 ml). Hoy se usa para cócteles como el daiquirí y como sustituta de la copa martini. En la IBA, el Remember the Maine se sirve en copa coupé."),
        ("Copa de cóctel (copa martini)", "Copa con tallo y cáliz en forma de cono invertido para cócteles servidos sin hielo (straight up): Martini, Manhattan, Cosmopolitan, Grasshopper, entre otros."),
        ("Cuchara de bar (bar spoon)", "Cuchara larga y delgada, de unos 5 ml, para remover en el vaso mezclador, medir pequeñas cantidades y hacer capas."),
        ("Dash", "Golpe o chorrito: medida imprecisa, equivalente a «una pizca», muy usada con los bitters."),
        ("Dilución", "Agua que aporta el hielo al derretirse; suaviza el alcohol y realza los sabores secundarios."),
        ("Doble colado (double strain)", "Colar con el colador Hawthorne y, a la vez, con un colador fino, para no dejar pulpa ni hielo triturado."),
        ("Frozen", "Forma de preparar un cóctel con hielo picado en lugar de cubos, normalmente licuado (Frozen Daiquiri, Frozen Caipiriña)."),
        ("Garnish (guarnición)", "Decoración que se agrega al cóctel; su función es sobre todo estética, pero puede aportar aroma. Ejemplos: gajo de naranja y cereza en el Sex on the Beach, borde de sal en la Margarita, aceituna en el Martini."),
        ("Hielo picado o frappé", "Hielo en trozos pequeños que se derrite rápido; recomendado para cócteles dulces y tropicales como el mojito o el daiquirí y para los frozen."),
        ("Highball (vaso alto)", "Vaso alto de 24 a 35 cl para tragos largos con hielo, como el Cuba Libre o el gin tonic."),
        ("Jigger", "Medidor de doble punta con dos capacidades (por ejemplo, 30 ml y 60 ml; o 2 oz y 3/4 oz) que sirve para medir con precisión los licores y demás ingredientes líquidos."),
        ("Layered (en capas, pousse-café)", "Cóctel de capas separadas que se logra vertiendo con cuidado ingredientes de distinta densidad sobre una cucharilla."),
        ("Macerar (muddle)", "Machacar frutas, hierbas o especias en el fondo del vaso con el macerador (muddler) para liberar sus aromas y sabores, antes de añadir los líquidos. Se usa en el Mojito, la Caipiriña, el Mint Julep y el Old Fashioned."),
        ("Neat", "Licor servido solo, sin enfriar y sin agua ni hielo."),
        ("Old fashioned (vaso de rocas o lowball)", "Vaso corto, de borde ancho y base gruesa, de 180 a 300 ml; se usa para destilados solos o con hielo y para cócteles como el Old Fashioned y el Negroni."),
        ("On the rocks (en las rocas)", "Servido sobre cubos de hielo."),
        ("Pony", "Medida de 1 onza líquida estadounidense (unos 30 ml)."),
        ("Pourer", "Pico vertedor que se pone en la botella y permite medir contando el tiempo de vertido."),
        ("Removido o mezclado (stir, stirred)", "Técnica que mezcla los ingredientes removiéndolos suavemente con hielo en un vaso mezclador; mantiene la bebida clara y suave. Indicada para cócteles de solo destilados, licores o vermut, sin jugos ni cremas (Dry Martini, Manhattan)."),
        ("Shot", "Medida estándar de 1,5 oz (44 ml); también, el vaso pequeño para servirla."),
        ("Sour", "Familia de cócteles con un licor base, jugo de limón o de lima y un endulzante (azúcar, triple sec, jarabe, granadina o jugo de piña). Por ejemplo, el Whiskey Sour de la IBA lleva bourbon, jugo fresco de limón y jarabe de azúcar."),
        ("Straight up / up", "Bebida agitada o mezclada con hielo que se cuela y se sirve sin hielo."),
        ("Tiki", "Familia de cócteles de origen estadounidense (California) cuyo ingrediente estrella es el ron, con sabores dulces y afrutados y decoración llamativa."),
        ("Trago largo / trago corto", "El trago largo (long drink) se bebe lentamente y suele llevar dos tercios de bebida sin alcohol; el trago corto (short drink) lleva menos líquido y se bebe más rápido."),
        ("Twist", "Guarnición que consiste en torcer la cáscara de una naranja, lima o limón en espiral, liberando aromas cítricos."),
        ("Vaso mezclador (mixing glass)", "Vaso grande de vidrio o acero donde se remueven los cócteles que no requieren agitación vigorosa."),
        ("Vermut (vermú)", "Bebida alcohólica categorizada como vino fortificado: una base de vino con un destilado y una mezcla de hierbas, cuyo nombre viene del alemán wermut, «ajenjo». El vermut rojo dulce y el seco son ingredientes del Negroni, el Manhattan y el Dry Martini."),
    ],
    "fuentes": [
        "Wikipedia en español, «Cóctel»: https://es.wikipedia.org/wiki/Cóctel",
        "Wikipedia en español, «Terminología en coctelería»: https://es.wikipedia.org/wiki/Terminología_en_coctelería",
        "Wikipedia en español, «Bíter»: https://es.wikipedia.org/wiki/Bíter",
        "Wikipedia en español, «Amargo de Angostura»: https://es.wikipedia.org/wiki/Amargo_de_Angostura",
        "Wikipedia en español, «Campari»: https://es.wikipedia.org/wiki/Campari",
        "Wikipedia en español, «Vermú»: https://es.wikipedia.org/wiki/Vermú",
        "Wikipedia en español, «Caipiriña»: https://es.wikipedia.org/wiki/Caipiriña",
        "Wikipedia en español, «Cachaza»: https://es.wikipedia.org/wiki/Cachaza",
        "Wikipedia en español, «Coctelera»: https://es.wikipedia.org/wiki/Coctelera",
        "Wikipedia en español, «Copa martinera»: https://es.wikipedia.org/wiki/Copa_martinera",
        "Wikipedia en español, «Copa champañera»: https://es.wikipedia.org/wiki/Copa_champañera",
        "Wikipedia en español, «Vaso Highball»: https://es.wikipedia.org/wiki/Vaso_Highball",
        "Wikipedia en español, «Vaso de rocas»: https://es.wikipedia.org/wiki/Vaso_de_rocas",
        "Wikipedia en inglés, «Muddler», «Cocktail strainer» y «Bar spoon» (traducción): https://en.wikipedia.org/wiki/Muddler",
        "International Bartenders Association (IBA), recetas oficiales: https://iba-world.com/cocktails/all-cocktails/",
    ],
}

# ---------------------------------------------------------------------------------------------
# 3. Documento de la demo (PDF, va a data/demo/, NUNCA al seed)
# ---------------------------------------------------------------------------------------------
DEMO_VICHE = {
    "archivo": "guia_destilados_colombianos_viche.pdf",
    "titulo": "Guía de destilados colombianos: el viche",
    "subtitulo": "El destilado ancestral de caña del Pacífico colombiano",
    "intro": (
        "Documento de apoyo del proyecto Cantinero sobre el viche (también escrito biche), la bebida destilada "
        "tradicional de las comunidades afrocolombianas del Pacífico. Resume las fuentes citadas al final."
    ),
    "secciones": [
        ("1. ¿Qué es el viche?", [
            (None,
             "El viche o biche es una bebida alcohólica artesanal, destilada a partir del jugo de la caña de azúcar, "
             "típica y originaria de la región del Pacífico colombiano. Es elaborada tradicionalmente por las "
             "comunidades negras o afrocolombianas de esa región. Su contenido de alcohol es similar al de otros "
             "destilados como el aguardiente: ronda el 35 % (entre 30 % y 35 %, según la fuente)."),
        ]),
        ("2. Origen y región", [
            (None,
             "El viche es originario de la región del Pacífico colombiano: Valle del Cauca (Buenaventura), Chocó, "
             "Nariño y Cauca. Se elabora principalmente en las zonas de los ríos Naya (Valle del Cauca), Saija y Micay "
             "(Cauca), y también en algunos municipios del norte de Antioquia. Durante siglos los habitantes de la "
             "región lo usaron como remedio tradicional, y también se le atribuyeron efectos afrodisíacos, una "
             "creencia que, según la fuente, ha servido para exotizar a las comunidades negras."),
            (None,
             "Sobre el nombre, la fuente relaciona la palabra «viche» con voces de lenguas bantúes que significan "
             "verde, crudo o fresco (por ejemplo, «bichi» en suajili), en referencia a que la caña se corta cruda, "
             "antes de su maduración."),
        ]),
        ("3. Elaboración", [
            (None,
             "Las mujeres han sido las protagonistas de su preparación, un oficio que se hereda de generación en "
             "generación dentro de las familias; a estas mujeres se les llama «sacadoras». El viche se fabrica a partir "
             "del jugo de caña de azúcar cortada antes de su maduración y de diversas mieles; según quien lo elabore, "
             "se le agregan distintos ingredientes para darle un sabor agradable. Primero se extrae la materia prima "
             "(la caña se corta cruda, lo que le da un sabor diferente al de bebidas similares como el aguardiente) y "
             "después se destila. Otra fuente describe el proceso así: se corta caña fresca, se prensa el jugo en un "
             "trapiche de madera o de metal, el jugo (guarapo) se fermenta con las levaduras naturales de la caña y "
             "del entorno, y una destilación convierte ese guarapo en viche."),
            (None,
             "Del viche se derivan otras bebidas típicas del Pacífico, como el arrechón (con clavos y especias "
             "aromáticas), el tumbacatre (con esencia de borojó y chontaduro) y la tomaseca."),
        ]),
        ("4. Cultura y reconocimiento legal", [
            (None,
             "Los lugares donde se consume viche se llaman «vicheras», y en ellos se escucha música en torno a la "
             "bebida. El viche forma parte de la economía y la práctica cultural de Cali, gracias a eventos como el "
             "Festival de Música del Pacífico Petronio Álvarez, que se realiza desde 1997."),
            (None,
             "Como otras bebidas de comunidades no europeas en América Latina, el viche fue perseguido desde la "
             "Colonia, y en 1923 la llamada «ley antialcohólica» dejó en la ilegalidad las bebidas artesanales. En "
             "2021, la Ley 2158, conocida como Ley del Viche, lo reconoció como patrimonio cultural colectivo de las "
             "comunidades negras afrocolombianas del Pacífico colombiano y del norte de Antioquia, y dictó los "
             "mecanismos para su reglamentación sanitaria, protección y promoción; la ley permitió también su "
             "producción comercial."),
        ]),
        ("5. El viche en la coctelería", [
            (None,
             "El viche puede tomarse solo, pero a menudo se mezcla con jugos de frutas azucarados. En los últimos años "
             "ha entrado en la alta coctelería y en los bares de coctelería de autor de Cali y de Bogotá. Según la "
             "prensa, el objetivo es que algún día llegue a ser tan valorado en el mundo como el mezcal, el vodka o "
             "la ginebra."),
            (None,
             "En Cali, bartenders como Ronal Ordoñez (Papagayo Gastrobar), Juan Ramírez (891 bar) y Carlos Alberto "
             "Gaitán (Viches Bailadores) usan el viche, la tomaseca y el arrechón para versionar cócteles básicos como "
             "el mojito, el moscow mule o el «gaviota», con el argumento de ofrecer una coctelería de alto nivel con "
             "sabores propios del Pacífico."),
            (None,
             "En Bogotá, la prensa ha reseñado cócteles como el «Manhattan del Pacífico», con viche curado, y el "
             "«Puerto Sour», con tomaseca (La Sala de Laura, bar del restaurante Leo); el «Negroni del Pacífico» "
             "(Humo Negro), con jerez, vermut blanco y viche; y el «Yo soy Pacífico» (Tres Cuatro Cinco), una "
             "combinación de viche, chontaduro y limón mandarino. En resumen, en coctelería el viche se usa como "
             "destilado de base en versiones de clásicos (mojito, moscow mule, manhattan, negroni) y en cócteles de "
             "autor con ingredientes del Pacífico y de Colombia."),
        ]),
    ],
    "fuentes": [
        "Wikipedia en español, «Viche (bebida)» (CC BY-SA 4.0): https://es.wikipedia.org/wiki/Viche_(bebida)",
        "Wikipedia en inglés, «Viche (drink)» (CC BY-SA 4.0, traducción): https://en.wikipedia.org/wiki/Viche_(drink)",
        "7 Caníbales, «Viche, destilado histórico del Pacífico colombiano» (Erin Rose): "
        "https://www.7canibales.com/beber/destilados/viche-el-destilado-patrimonial-del-pacifico-colombiano/",
        "Colombia Visible, «En Cali puede probar coctelería con licores como viche, tomaseca y arrechón» "
        "(Susana Serrano Arango): https://colombiavisible.com/en-cali-puede-probar-cocteleria-con-licores-como-viche-tomaseca-y-arrechon/",
        "El Tiempo, «El viche irrumpe en la alta coctelería: guía de lugares donde disfrutarlo» (Liliana Martínez "
        "Polo, 6 de febrero de 2023): https://www.eltiempo.com/cultura/gastronomia/el-viche-irrumpe-en-la-alta-cocteleria-guia-de-lugares-donde-disfrutarlo-739764",
    ],
    "nota_licencia": (
        "Las secciones basadas en Wikipedia son obra derivada bajo CC BY-SA 4.0. Los datos tomados de artículos de "
        "prensa se resumen con palabras propias y se citan arriba; sus textos originales pertenecen a sus autores."
    ),
}
