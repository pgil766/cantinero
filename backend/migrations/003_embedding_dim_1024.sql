-- 003: el modelo de embeddings pasa a "bge-m3" (1024 dimensiones, lee hasta 8192 tokens), en lugar de
-- "paraphrase-multilingual" (768), que solo leía ~500 caracteres de cada fragmento (ver docs/bitacora.md).
-- Cambiar la dimensión invalida los vectores existentes: se borran los fragmentos y los documentos
-- quedan en 'failed' para reingestarlos (scripts/reindex.py). Al momento de esta migración no había datos.

DROP INDEX IF EXISTS ix_chunks_embedding;
DELETE FROM chunks;
UPDATE documents
   SET status = 'failed', chunk_count = 0,
       error = 'Reindexar: cambió el modelo de embeddings (migración 003).'
 WHERE status <> 'failed';

ALTER TABLE chunks ALTER COLUMN embedding TYPE VECTOR(1024);
CREATE INDEX ix_chunks_embedding ON chunks USING hnsw (embedding vector_cosine_ops);
