-- 002: los embeddings pasan a servirse por Ollama con "paraphrase-multilingual" (768 dimensiones),
-- en lugar de sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 (384).
-- Cambiar la dimensión invalida los vectores existentes: se borran los fragmentos y los documentos
-- quedan en 'failed' para reingestarlos (scripts/reindex.py). Al momento de esta migración no había datos.

DROP INDEX IF EXISTS ix_chunks_embedding;
DELETE FROM chunks;
UPDATE documents
   SET status = 'failed', chunk_count = 0,
       error = 'Reindexar: cambió el modelo de embeddings (migración 002).'
 WHERE status <> 'failed';

ALTER TABLE chunks ALTER COLUMN embedding TYPE VECTOR(768);
CREATE INDEX ix_chunks_embedding ON chunks USING hnsw (embedding vector_cosine_ops);
