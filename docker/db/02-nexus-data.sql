-- Dados iniciais: setores e usuário admin (senha: admin123)
INSERT INTO nexus.setores (id_setor, nome_setor) VALUES
(1, 'ENGENHARIA'),
(2, 'COMERCIAL'),
(3, 'DESENVOLVIMENTO'),
(4, 'PCP'),
(5, 'CUSTOS')
ON CONFLICT (id_setor) DO NOTHING;

-- Sequência dos setores (evitar conflito em próximos inserts)
SELECT setval('nexus.setores_id_setor_seq', (SELECT COALESCE(MAX(id_setor), 1) FROM nexus.setores));

-- Usuário admin: nome_usuario=admin, senha=admin123 (BCrypt)
INSERT INTO nexus.usuarios (codigo_usuario, nome_usuario, cargo_usuario, nivel_usuario, id_setor, senha)
VALUES (1, 'admin', 'Administrador', 4, 1, '$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy')
ON CONFLICT (codigo_usuario) DO NOTHING;

SELECT setval('nexus.usuarios_codigo_usuario_seq', (SELECT COALESCE(MAX(codigo_usuario), 1) FROM nexus.usuarios));
