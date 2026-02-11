--
-- PostgreSQL - Schema Nexus (init para Docker)
-- Baseado em DB/nexus2.sql sem comandos \restrict/\unrestrict
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

CREATE SCHEMA IF NOT EXISTS nexus;
ALTER SCHEMA nexus OWNER TO postgres;

CREATE TABLE nexus.pendencias (
    id integer NOT NULL,
    numero character varying(20) NOT NULL,
    data_criacao timestamp without time zone NOT NULL,
    data_atualizacao timestamp without time zone,
    equipamento text,
    situacao character varying(100),
    status character varying(50),
    prioridade character varying(20),
    prazo_resposta integer,
    origem character varying(50),
    observacoes text,
    versao character varying(20),
    ultima_modificacao timestamp without time zone,
    modificado_por character varying(100),
    id_usuario integer,
    id_setor integer,
    propostas_vinculadas jsonb DEFAULT '[]'::jsonb,
    cliente jsonb DEFAULT '{}'::jsonb,
    historico jsonb DEFAULT '[]'::jsonb,
    id_roteiro integer
);
ALTER TABLE nexus.pendencias OWNER TO postgres;

CREATE SEQUENCE nexus.pendencias_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE nexus.pendencias_id_seq OWNER TO postgres;
ALTER SEQUENCE nexus.pendencias_id_seq OWNED BY nexus.pendencias.id;

CREATE TABLE nexus.roteiro_setores (
    id integer NOT NULL,
    roteiro_id integer NOT NULL,
    id_setor integer NOT NULL,
    ordem integer NOT NULL
);
ALTER TABLE nexus.roteiro_setores OWNER TO postgres;

CREATE SEQUENCE nexus.roteiro_setores_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE nexus.roteiro_setores_id_seq OWNER TO postgres;
ALTER SEQUENCE nexus.roteiro_setores_id_seq OWNED BY nexus.roteiro_setores.id;

CREATE TABLE nexus.roteiros (
    id integer NOT NULL,
    nome character varying(255) NOT NULL,
    descricao text,
    ativo boolean DEFAULT true NOT NULL,
    data_criacao timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);
ALTER TABLE nexus.roteiros OWNER TO postgres;

CREATE SEQUENCE nexus.roteiros_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE nexus.roteiros_id_seq OWNER TO postgres;
ALTER SEQUENCE nexus.roteiros_id_seq OWNED BY nexus.roteiros.id;

CREATE TABLE nexus.setores (
    id_setor integer NOT NULL,
    nome_setor text NOT NULL
);
ALTER TABLE nexus.setores OWNER TO postgres;

CREATE SEQUENCE nexus.setores_id_setor_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE nexus.setores_id_setor_seq OWNER TO postgres;
ALTER SEQUENCE nexus.setores_id_setor_seq OWNED BY nexus.setores.id_setor;

CREATE TABLE nexus.usuarios (
    codigo_usuario integer NOT NULL,
    nome_usuario text NOT NULL,
    telefone_usuario text,
    email_usuario text,
    computador_usuario text,
    cargo_usuario text,
    nivel_usuario integer,
    id_setor integer,
    senha character varying
);
ALTER TABLE nexus.usuarios OWNER TO postgres;

CREATE SEQUENCE nexus.usuarios_codigo_usuario_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE nexus.usuarios_codigo_usuario_seq OWNER TO postgres;
ALTER SEQUENCE nexus.usuarios_codigo_usuario_seq OWNED BY nexus.usuarios.codigo_usuario;

CREATE VIEW nexus.v_pendencias_com_detalhes AS
 SELECT p.id, p.numero, p.situacao, p.status, p.prioridade, u.nome_usuario, s.nome_setor,
    p.data_criacao, p.data_atualizacao, p.ultima_modificacao, p.equipamento, p.observacoes
 FROM nexus.pendencias p
 LEFT JOIN nexus.usuarios u ON u.codigo_usuario = p.id_usuario
 LEFT JOIN nexus.setores s ON s.id_setor = p.id_setor;
ALTER VIEW nexus.v_pendencias_com_detalhes OWNER TO postgres;

CREATE VIEW nexus.v_usuarios_com_setor AS
 SELECT u.codigo_usuario, u.nome_usuario, u.email_usuario, u.computador_usuario, s.nome_setor
 FROM nexus.usuarios u LEFT JOIN nexus.setores s ON s.id_setor = u.id_setor;
ALTER VIEW nexus.v_usuarios_com_setor OWNER TO postgres;

ALTER TABLE ONLY nexus.pendencias ALTER COLUMN id SET DEFAULT nextval('nexus.pendencias_id_seq'::regclass);
ALTER TABLE ONLY nexus.roteiro_setores ALTER COLUMN id SET DEFAULT nextval('nexus.roteiro_setores_id_seq'::regclass);
ALTER TABLE ONLY nexus.roteiros ALTER COLUMN id SET DEFAULT nextval('nexus.roteiros_id_seq'::regclass);
ALTER TABLE ONLY nexus.setores ALTER COLUMN id_setor SET DEFAULT nextval('nexus.setores_id_setor_seq'::regclass);
ALTER TABLE ONLY nexus.usuarios ALTER COLUMN codigo_usuario SET DEFAULT nextval('nexus.usuarios_codigo_usuario_seq'::regclass);

ALTER TABLE ONLY nexus.pendencias ADD CONSTRAINT pendencias_numero_key UNIQUE (numero);
ALTER TABLE ONLY nexus.pendencias ADD CONSTRAINT pendencias_pkey PRIMARY KEY (id);
ALTER TABLE ONLY nexus.roteiro_setores ADD CONSTRAINT roteiro_setores_pkey PRIMARY KEY (id);
ALTER TABLE ONLY nexus.roteiros ADD CONSTRAINT roteiros_pkey PRIMARY KEY (id);
ALTER TABLE ONLY nexus.setores ADD CONSTRAINT setores_nome_setor_key UNIQUE (nome_setor);
ALTER TABLE ONLY nexus.setores ADD CONSTRAINT setores_pkey PRIMARY KEY (id_setor);
ALTER TABLE ONLY nexus.roteiro_setores ADD CONSTRAINT unique_roteiro_ordem UNIQUE (roteiro_id, ordem);
ALTER TABLE ONLY nexus.usuarios ADD CONSTRAINT usuarios_email_usuario_key UNIQUE (email_usuario);
ALTER TABLE ONLY nexus.usuarios ADD CONSTRAINT usuarios_pkey PRIMARY KEY (codigo_usuario);

CREATE INDEX idx_pendencias_id_roteiro ON nexus.pendencias USING btree (id_roteiro);
CREATE INDEX idx_roteiro_setores_id_setor ON nexus.roteiro_setores USING btree (id_setor);
CREATE INDEX idx_roteiro_setores_roteiro_id ON nexus.roteiro_setores USING btree (roteiro_id);

ALTER TABLE ONLY nexus.pendencias ADD CONSTRAINT fk_pend_setor FOREIGN KEY (id_setor) REFERENCES nexus.setores(id_setor);
ALTER TABLE ONLY nexus.roteiro_setores ADD CONSTRAINT fk_roteiro_setor FOREIGN KEY (roteiro_id) REFERENCES nexus.roteiros(id) ON DELETE CASCADE;
ALTER TABLE ONLY nexus.usuarios ADD CONSTRAINT fk_usuario_setor FOREIGN KEY (id_setor) REFERENCES nexus.setores(id_setor);
ALTER TABLE ONLY nexus.roteiro_setores ADD CONSTRAINT roteiro_setores_roteiro_id_fkey FOREIGN KEY (roteiro_id) REFERENCES nexus.roteiros(id) ON DELETE CASCADE;
