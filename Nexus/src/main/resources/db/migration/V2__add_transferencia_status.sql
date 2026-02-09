-- Adiciona colunas para rastrear status de transferência
ALTER TABLE nexus.pendencias 
ADD COLUMN IF NOT EXISTS status_transferencia VARCHAR(20),
ADD COLUMN IF NOT EXISTS id_setor_anterior INTEGER,
ADD COLUMN IF NOT EXISTS id_usuario_anterior INTEGER;

-- Comentários para documentação
COMMENT ON COLUMN nexus.pendencias.status_transferencia IS 'Status da transferência: PENDENTE (aguardando aceitação), ACEITA, DEVOLVIDA, ou NULL (sem transferência pendente)';
COMMENT ON COLUMN nexus.pendencias.id_setor_anterior IS 'ID do setor anterior (usado para devolução de transferência)';
COMMENT ON COLUMN nexus.pendencias.id_usuario_anterior IS 'ID do usuário anterior (usado para devolução de transferência)';
