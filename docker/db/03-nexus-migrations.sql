--
-- Migrações adicionais para o app (roteiro_passos, colunas de transferência)
-- Executado após 01-nexus-schema.sql e 02-nexus-data.sql
--

-- Colunas de transferência em pendencias
ALTER TABLE nexus.pendencias ADD COLUMN IF NOT EXISTS status_transferencia VARCHAR(20);
ALTER TABLE nexus.pendencias ADD COLUMN IF NOT EXISTS id_setor_anterior INTEGER;
ALTER TABLE nexus.pendencias ADD COLUMN IF NOT EXISTS id_usuario_anterior INTEGER;

-- Tabela roteiro_passos (passos do roteiro: setor ou usuário)
CREATE TABLE IF NOT EXISTS nexus.roteiro_passos (
    id SERIAL PRIMARY KEY,
    roteiro_id INTEGER NOT NULL REFERENCES nexus.roteiros(id) ON DELETE CASCADE,
    ordem INTEGER NOT NULL,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('SETOR', 'USUARIO')),
    id_setor INTEGER NULL,
    id_usuario INTEGER NULL,
    CONSTRAINT chk_passos_tipo_setor CHECK (
        (tipo = 'SETOR' AND id_setor IS NOT NULL AND id_usuario IS NULL) OR
        (tipo = 'USUARIO' AND id_usuario IS NOT NULL AND id_setor IS NULL)
    ),
    CONSTRAINT unique_roteiro_passos_ordem UNIQUE (roteiro_id, ordem)
);
ALTER TABLE nexus.roteiro_passos OWNER TO postgres;
CREATE INDEX IF NOT EXISTS idx_roteiro_passos_roteiro_id ON nexus.roteiro_passos(roteiro_id);
