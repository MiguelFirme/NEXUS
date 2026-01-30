-- Adiciona coluna senha na tabela usuarios (hash BCrypt, até 255 caracteres).
-- Execute este script no banco Nexus_DB se a coluna ainda não existir.
ALTER TABLE nexus.usuarios ADD COLUMN IF NOT EXISTS senha VARCHAR(255);
