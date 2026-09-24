"""Extracción de texto por formato (T3.2)."""

import pytest

from app.services.ingestion.loaders import (
    UnreadableDocumentError,
    UnsupportedFormatError,
    load_document,
)
from tests.document_factory import make_docx, make_pdf


def write(tmp_path, name: str, data: bytes | str):
    path = tmp_path / name
    path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))
    return path


def test_pdf_keeps_page_numbers_and_accents(tmp_path):
    path = write(tmp_path, "guia.pdf", make_pdf(["Técnica de agitado.", "", "Cristalería: copa coupé."]))
    sections = load_document(path)
    assert [s.metadata["page"] for s in sections] == [1, 3]  # la página 2 no tiene texto
    assert "Técnica de agitado" in sections[0].text
    assert "coupé" in sections[1].text


def test_pdf_without_text_is_rejected_as_scanned(tmp_path):
    path = write(tmp_path, "escaneado.pdf", make_pdf(["", ""]))
    with pytest.raises(UnreadableDocumentError, match="escaneada"):
        load_document(path)


def test_corrupted_pdf_is_rejected(tmp_path):
    path = write(tmp_path, "roto.pdf", b"%PDF-1.4 esto no es un pdf")
    with pytest.raises(UnreadableDocumentError):
        load_document(path)


def test_docx_extracts_paragraphs(tmp_path):
    path = write(tmp_path, "glosario.docx", make_docx(["Jigger: medidor de líquidos.", "Muddler: macerador."]))
    [section] = load_document(path)
    assert "Jigger: medidor de líquidos." in section.text
    assert "Muddler" in section.text


def test_corrupted_docx_is_rejected(tmp_path):
    path = write(tmp_path, "roto.docx", b"no es un zip")
    with pytest.raises(UnreadableDocumentError):
        load_document(path)


def test_csv_row_becomes_one_atomic_section_with_url_in_metadata(tmp_path):
    csv_text = (
        "nombre,ingredientes,cristaleria,fuente_url\n"
        "Negroni,30 ml (1 oz) de gin; 30 ml (1 oz) de vermut rojo; 30 ml (1 oz) de Campari,old fashioned,https://iba.example/negroni\n"
        "Mojito,45 ml de ron blanco,highball,\n"
    )
    sections = load_document(write(tmp_path, "recetas.csv", csv_text))
    assert len(sections) == 2
    negroni = sections[0]
    assert negroni.atomic
    assert negroni.metadata == {"row": 1, "item_name": "Negroni", "source_url": "https://iba.example/negroni"}
    assert "ingredientes: 30 ml (1 oz) de gin" in negroni.text
    assert "http" not in negroni.text


def test_csv_with_semicolon_delimiter_is_detected(tmp_path):
    sections = load_document(write(tmp_path, "r.csv", "nombre;cristaleria\nDaiquiri;copa coupé\n"))
    assert sections[0].text == "nombre: Daiquiri\ncristaleria: copa coupé"


def test_markdown_splits_by_heading_and_keeps_heading_path(tmp_path):
    md = "# Tequila\nIntro del tequila.\n## Historia\nNació en Jalisco.\n## Tipos\nBlanco y reposado.\n"
    sections = load_document(write(tmp_path, "tequila.md", md))
    assert [(s.metadata.get("heading"), s.text) for s in sections] == [
        ("Tequila", "Intro del tequila."),
        ("Tequila > Historia", "Nació en Jalisco."),
        ("Tequila > Tipos", "Blanco y reposado."),
    ]


def test_text_in_windows_encoding_is_decoded(tmp_path):
    path = write(tmp_path, "notas.txt", "Caña de azúcar y ñame".encode("cp1252"))
    assert load_document(path)[0].text == "Caña de azúcar y ñame"


def test_original_filename_decides_the_format(tmp_path):
    path = write(tmp_path, "upload_tmp_1234", "Texto de prueba suficiente.")
    assert load_document(path, filename="notas.txt")[0].text == "Texto de prueba suficiente."


@pytest.mark.parametrize("name", ["foto.jpg", "hoja.xlsx", "sin_extension"])
def test_unsupported_formats_are_rejected_with_415(tmp_path, name):
    with pytest.raises(UnsupportedFormatError) as exc:
        load_document(write(tmp_path, name, "x"))
    assert exc.value.status_code == 415


def test_empty_document_is_rejected(tmp_path):
    with pytest.raises(UnreadableDocumentError, match="no tiene texto"):
        load_document(write(tmp_path, "vacio.txt", "   \n\n  "))
