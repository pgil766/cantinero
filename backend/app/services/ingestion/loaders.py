"""Extracción de texto por formato (AGENTS.md §13.1, RF-DOC-2).

Cada formato produce una lista de secciones con sus metadatos. Una sección `atomic` no se parte al
fragmentar: así una receta (una fila del CSV) siempre queda completa en un solo fragmento (§13.2).
"""

import csv
import io
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import docx2txt
from pypdf import PdfReader
from pypdf.errors import PdfReadError

from app.core.errors import AppError

MIME_TYPES = {
    ".pdf": "application/pdf",
    ".txt": "text/plain",
    ".md": "text/markdown",
    ".csv": "text/csv",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}
SUPPORTED_EXTENSIONS = frozenset(MIME_TYPES)

_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
_NAME_COLUMNS = ("nombre", "name", "coctel", "cóctel", "cocktail")


@dataclass(frozen=True)
class Section:
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)
    atomic: bool = False


class UnsupportedFormatError(AppError):
    def __init__(self, filename: str) -> None:
        allowed = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        super().__init__(f"Formato no soportado: '{filename}'. Formatos permitidos: {allowed}.",
                         code="unsupported_format", status_code=415)


class UnreadableDocumentError(AppError):
    def __init__(self, detail: str) -> None:
        super().__init__(detail, code="unreadable_document", status_code=422)


def extension_of(filename: str) -> str:
    return Path(filename).suffix.lower()


def load_document(path: Path, filename: str | None = None) -> list[Section]:
    """Extrae el texto de un archivo. `filename` es el nombre original (el archivo puede estar en un temporal)."""
    filename = filename or path.name
    ext = extension_of(filename)
    loaders = {".pdf": _load_pdf, ".docx": _load_docx, ".csv": _load_csv, ".md": _load_markdown, ".txt": _load_text}
    if ext not in loaders:
        raise UnsupportedFormatError(filename)

    sections = [s for s in loaders[ext](path) if s.text.strip()]
    if not sections:
        raise UnreadableDocumentError(f"El documento '{filename}' no tiene texto que se pueda extraer.")
    return sections


# --- Formatos ----------------------------------------------------------------------------------

def _load_pdf(path: Path) -> list[Section]:
    try:
        reader = PdfReader(str(path))
        pages = [(n, _clean(page.extract_text() or "")) for n, page in enumerate(reader.pages, start=1)]
    except (PdfReadError, ValueError, KeyError) as exc:
        raise UnreadableDocumentError("El PDF está dañado o protegido y no se puede leer.") from exc
    sections = [Section(text, {"page": n}) for n, text in pages if text]
    if not sections:
        raise UnreadableDocumentError(
            "El PDF no tiene texto extraíble (¿es una imagen escaneada?). Sube una versión con texto."
        )
    return sections


def _load_docx(path: Path) -> list[Section]:
    try:
        text = docx2txt.process(str(path))
    except Exception as exc:  # docx2txt lanza excepciones genéricas de zipfile/xml con archivos dañados
        raise UnreadableDocumentError("El DOCX está dañado y no se puede leer.") from exc
    return [Section(_clean(text or ""))]


def _load_text(path: Path) -> list[Section]:
    return [Section(_clean(_read_text(path)))]


def _load_markdown(path: Path) -> list[Section]:
    """Una sección por encabezado. Cada sección conserva la ruta de encabezados ("Tequila > Historia")
    en `heading`, que el fragmentador antepone a cada fragmento para darle contexto."""
    sections: list[Section] = []
    stack: list[str] = []
    buffer: list[str] = []

    def flush() -> None:
        text = _clean("\n".join(buffer))
        if text:
            sections.append(Section(text, {"heading": " > ".join(stack)} if stack else {}))
        buffer.clear()

    for line in _read_text(path).splitlines():
        match = _HEADING.match(line)
        if match:
            flush()
            level = len(match.group(1))
            stack[:] = stack[: level - 1] + [match.group(2)]
        else:
            buffer.append(line)
    flush()
    return sections


def _load_csv(path: Path) -> list[Section]:
    """Una fila → una sección atómica ("columna: valor" por línea). Para recetas: una receta, un fragmento."""
    raw = _read_text(path)
    try:
        dialect = csv.Sniffer().sniff(raw[:4096], delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(io.StringIO(raw), dialect=dialect)
    if not reader.fieldnames:
        return []

    name_column = next((c for c in reader.fieldnames if c and c.strip().lower() in _NAME_COLUMNS), None)
    sections = []
    for row_number, row in enumerate(reader, start=1):
        metadata: dict[str, Any] = {"row": row_number}
        lines = []
        for column, value in row.items():
            if not column or value is None or not str(value).strip():
                continue
            value = str(value).strip()
            if "url" in column.lower():
                metadata["source_url"] = value  # la URL no aporta al significado: va a metadatos
                continue
            lines.append(f"{column.strip()}: {value}")
        if name_column and row.get(name_column):
            metadata["item_name"] = row[name_column].strip()
        if lines:
            sections.append(Section("\n".join(lines), metadata, atomic=True))
    return sections


# --- Utilidades --------------------------------------------------------------------------------

def _read_text(path: Path) -> str:
    data = path.read_bytes()
    for encoding in ("utf-8-sig", "cp1252"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("latin-1")  # nunca falla


def _clean(text: str) -> str:
    text = text.replace("\x00", "").replace("\r\n", "\n").replace("\r", "\n")
    # Espacios repetidos (texto justificado de los PDF: "Métodos  de  preparación") → uno solo.
    text = "\n".join(re.sub(r"[ \t ]{2,}", " ", line).rstrip() for line in text.split("\n"))
    return re.sub(r"\n{3,}", "\n\n", text).strip()
