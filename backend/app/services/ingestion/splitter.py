"""Fragmentación (AGENTS.md §13.2, RF-DOC-3).

- Secciones atómicas (recetas): un fragmento por sección, sin partir.
- Texto largo: RecursiveCharacterTextSplitter con CHUNK_SIZE / CHUNK_OVERLAP. Si la sección tiene un
  encabezado ("Tequila > Historia"), se antepone a cada fragmento para que no pierda su contexto.
- Se descartan los fragmentos demasiado cortos para aportar algo.
"""

import logging
from dataclasses import dataclass, field
from typing import Any

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.services.ingestion.loaders import Section

logger = logging.getLogger(__name__)

MIN_CHUNK_CHARS = 30


@dataclass(frozen=True)
class Chunk:
    index: int
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)


def split_sections(sections: list[Section], chunk_size: int, chunk_overlap: int,
                   min_chars: int = MIN_CHUNK_CHARS) -> list[Chunk]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", "; ", ", ", " ", ""],
    )
    chunks: list[Chunk] = []
    for section in sections:
        heading = section.metadata.get("heading")
        if section.atomic:
            pieces = [section.text.strip()]
            if len(pieces[0]) > chunk_size * 3:
                logger.warning("Sección atómica de %d caracteres (%s): se indexa completa",
                               len(pieces[0]), section.metadata)
        else:
            pieces = splitter.split_text(section.text)
        for piece in pieces:
            piece = piece.strip()
            if len(piece) < min_chars:
                continue
            content = f"{heading}\n{piece}" if heading else piece
            chunks.append(Chunk(index=len(chunks), content=content, metadata=dict(section.metadata)))
    return chunks
