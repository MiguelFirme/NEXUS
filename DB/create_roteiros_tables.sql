-- Script para criar tabelas de roteiros
-- Execute este script no banco de dados PostgreSQL

-- Tabela de roteiros
CREATE TABLE IF NOT EXISTS nexus.roteiros (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    ativo BOOLEAN NOT NULL DEFAULT true,
    data_criacao TIMESTAMP WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de setores no roteiro (sequência)
CREATE TABLE IF NOT EXISTS nexus.roteiro_setores (
    id SERIAL PRIMARY KEY,
    roteiro_id INTEGER NOT NULL REFERENCES nexus.roteiros(id) ON DELETE CASCADE,
    id_setor INTEGER NOT NULL,
    ordem INTEGER NOT NULL,
    CONSTRAINT fk_roteiro_setor FOREIGN KEY (roteiro_id) REFERENCES nexus.roteiros(id) ON DELETE CASCADE,
    CONSTRAINT unique_roteiro_ordem UNIQUE (roteiro_id, ordem)
);

-- Adicionar coluna id_roteiro na tabela pendencias
ALTER TABLE nexus.pendencias 
ADD COLUMN IF NOT EXISTS id_roteiro INTEGER;

-- Criar índice para melhorar performance
CREATE INDEX IF NOT EXISTS idx_pendencias_id_roteiro ON nexus.pendencias(id_roteiro);
CREATE INDEX IF NOT EXISTS idx_roteiro_setores_roteiro_id ON nexus.roteiro_setores(roteiro_id);
CREATE INDEX IF NOT EXISTS idx_roteiro_setores_id_setor ON nexus.roteiro_setores(id_setor);
