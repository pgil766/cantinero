-- 001: esquema inicial de Cantinero (AGENTS.md §10.2)

CREATE EXTENSION IF NOT EXISTS vector;

-- Documentos de la base de conocimiento.
-- is_global = TRUE  → seed de solo lectura (owner_id NULL).
-- is_global = FALSE → documento privado del usuario (owner_id = 'sub' de Keycloak).
CREATE TABLE documents (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  filename      TEXT NOT NULL,
  mime_type     TEXT NOT NULL,
  size_bytes    BIGINT NOT NULL CHECK (size_bytes >= 0),
  sha256        TEXT NOT NULL,
  is_global     BOOLEAN NOT NULL DEFAULT FALSE,
  owner_id      TEXT,
  status        TEXT NOT NULL DEFAULT 'processing'
                CHECK (status IN ('processing', 'ready', 'failed')),
  error         TEXT,
  chunk_count   INT NOT NULL DEFAULT 0,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK ((is_global AND owner_id IS NULL) OR (NOT is_global AND owner_id IS NOT NULL))
);

-- Evita subir dos veces el mismo archivo por usuario (y en el seed). Los documentos con
-- status 'failed' no cuentan, para que el usuario pueda reintentar la subida.
CREATE UNIQUE INDEX uq_documents_owner_sha ON documents (COALESCE(owner_id, 'GLOBAL'), sha256)
  WHERE status <> 'failed';
CREATE INDEX ix_documents_owner ON documents (owner_id);

-- Fragmentos con su embedding (dimensión = EMBEDDING_DIM).
CREATE TABLE chunks (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id   UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
  chunk_index   INT NOT NULL,
  content       TEXT NOT NULL,
  metadata      JSONB NOT NULL DEFAULT '{}',
  embedding     VECTOR(384) NOT NULL,
  UNIQUE (document_id, chunk_index)
);
CREATE INDEX ix_chunks_embedding ON chunks USING hnsw (embedding vector_cosine_ops);
CREATE INDEX ix_chunks_document ON chunks (document_id);

-- Historial de conversaciones (siempre privado de cada usuario).
CREATE TABLE conversations (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     TEXT NOT NULL,
  title       TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ix_conversations_user ON conversations (user_id, created_at DESC);

CREATE TABLE messages (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id  UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  role             TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
  content          TEXT NOT NULL,
  status           TEXT CHECK (status IN ('answered', 'rejected', 'clarify', 'greeting', 'responsible')),
  sources          JSONB NOT NULL DEFAULT '[]',
  created_at       TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX ix_messages_conversation ON messages (conversation_id, created_at);
