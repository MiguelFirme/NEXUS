-- Script para adicionar colunas JSON necessárias para o funcionamento da interface
-- Sistema NEXUS - Olivo Guindastes

ALTER TABLE nexus.pendencias ADD COLUMN IF NOT EXISTS cliente jsonb DEFAULT '{}';
ALTER TABLE nexus.pendencias ADD COLUMN IF NOT EXISTS historico jsonb DEFAULT '[]';
ALTER TABLE nexus.pendencias ADD COLUMN IF NOT EXISTS propostas_vinculadas jsonb DEFAULT '[]';

-- Comentários para documentação
COMMENT ON COLUMN nexus.pendencias.cliente IS 'Dados do cliente em formato JSON (razao_social, cnpj, telefone, etc)';
COMMENT ON COLUMN nexus.pendencias.historico IS 'Histórico de alterações da pendência em formato JSON';
COMMENT ON COLUMN nexus.pendencias.propostas_vinculadas IS 'Lista de propostas vinculadas em formato JSON';
