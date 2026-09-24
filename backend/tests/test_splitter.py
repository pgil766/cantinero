"""Fragmentación (T3.3): una receta por fragmento, texto largo partido con solapamiento."""

from app.services.ingestion.loaders import Section
from app.services.ingestion.splitter import split_sections

RECIPE = "nombre: Negroni\ningredientes: " + "; ".join(["30 ml (1 oz) de ingrediente"] * 40)


def test_atomic_recipe_is_never_split_even_if_longer_than_chunk_size():
    assert len(RECIPE) > 900
    chunks = split_sections([Section(RECIPE, {"row": 1}, atomic=True)], chunk_size=300, chunk_overlap=50)
    assert len(chunks) == 1
    assert chunks[0].content == RECIPE
    assert chunks[0].metadata == {"row": 1}


def test_long_text_is_split_within_size_with_overlap():
    sentences = [f"Frase número {i} sobre la historia del ron en el Caribe." for i in range(60)]
    chunks = split_sections([Section(" ".join(sentences))], chunk_size=300, chunk_overlap=80)
    assert len(chunks) > 5
    assert all(len(c.content) <= 300 for c in chunks)
    # solapamiento: el final de un fragmento reaparece al inicio del siguiente
    first_words = chunks[1].content.split()[:3]
    assert " ".join(first_words) in chunks[0].content


def test_heading_is_prepended_to_every_piece_of_its_section():
    text = " ".join(["El tequila se elabora con agave azul de Jalisco."] * 30)
    chunks = split_sections([Section(text, {"heading": "Tequila > Elaboración"})], chunk_size=200, chunk_overlap=20)
    assert len(chunks) > 1
    assert all(c.content.startswith("Tequila > Elaboración\n") for c in chunks)


def test_tiny_fragments_are_discarded_and_indexes_are_consecutive():
    sections = [
        Section("ok"),  # demasiado corto
        Section("El Mojito es un cóctel cubano con ron, lima y hierbabuena.", {"row": 1}, atomic=True),
        Section("El Daiquiri lleva ron blanco, jugo de lima y jarabe de azúcar.", {"row": 2}, atomic=True),
    ]
    chunks = split_sections(sections, chunk_size=900, chunk_overlap=150)
    assert [c.index for c in chunks] == [0, 1]
    assert [c.metadata["row"] for c in chunks] == [1, 2]


def test_no_empty_chunks():
    chunks = split_sections([Section("\n\n\n" + "Texto útil sobre coctelería clásica. " * 50 + "\n\n")],
                            chunk_size=200, chunk_overlap=30)
    assert chunks and all(c.content.strip() for c in chunks)
