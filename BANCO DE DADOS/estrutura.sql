--
-- PostgreSQL database dump
--

\restrict GHEbegflSW7mkDoUgLwI61KTd5GGBpvZ05DjTwMRFS7ARcYGH2aQgULutQ7f2oo

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: nexus; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA nexus;


ALTER SCHEMA nexus OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: pendencias; Type: TABLE; Schema: nexus; Owner: postgres
--

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
    id_setor integer
);


ALTER TABLE nexus.pendencias OWNER TO postgres;

--
-- Name: pendencias_id_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.pendencias_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.pendencias_id_seq OWNER TO postgres;

--
-- Name: pendencias_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.pendencias_id_seq OWNED BY nexus.pendencias.id;


--
-- Name: setores; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.setores (
    id_setor integer NOT NULL,
    nome_setor text NOT NULL
);


ALTER TABLE nexus.setores OWNER TO postgres;

--
-- Name: setores_id_setor_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.setores_id_setor_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.setores_id_setor_seq OWNER TO postgres;

--
-- Name: setores_id_setor_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.setores_id_setor_seq OWNED BY nexus.setores.id_setor;


--
-- Name: usuarios; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.usuarios (
    codigo_usuario integer NOT NULL,
    nome_usuario text NOT NULL,
    telefone_usuario text,
    email_usuario text,
    computador_usuario text,
    cargo_usuario text,
    nivel_usuario integer,
    id_setor integer
);


ALTER TABLE nexus.usuarios OWNER TO postgres;

--
-- Name: usuarios_codigo_usuario_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.usuarios_codigo_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.usuarios_codigo_usuario_seq OWNER TO postgres;

--
-- Name: usuarios_codigo_usuario_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.usuarios_codigo_usuario_seq OWNED BY nexus.usuarios.codigo_usuario;


--
-- Name: v_pendencias_com_detalhes; Type: VIEW; Schema: nexus; Owner: postgres
--

CREATE VIEW nexus.v_pendencias_com_detalhes AS
 SELECT p.id,
    p.numero,
    p.situacao,
    p.status,
    p.prioridade,
    u.nome_usuario,
    s.nome_setor,
    p.data_criacao,
    p.ultima_modificacao
   FROM ((nexus.pendencias p
     LEFT JOIN nexus.usuarios u ON ((u.codigo_usuario = p.id_usuario)))
     LEFT JOIN nexus.setores s ON ((s.id_setor = p.id_setor)));


ALTER VIEW nexus.v_pendencias_com_detalhes OWNER TO postgres;

--
-- Name: v_usuarios_com_setor; Type: VIEW; Schema: nexus; Owner: postgres
--

CREATE VIEW nexus.v_usuarios_com_setor AS
 SELECT u.codigo_usuario,
    u.nome_usuario,
    u.email_usuario,
    u.computador_usuario,
    s.nome_setor
   FROM (nexus.usuarios u
     LEFT JOIN nexus.setores s ON ((s.id_setor = u.id_setor)));


ALTER VIEW nexus.v_usuarios_com_setor OWNER TO postgres;

--
-- Name: pendencias id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendencias ALTER COLUMN id SET DEFAULT nextval('nexus.pendencias_id_seq'::regclass);


--
-- Name: setores id_setor; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.setores ALTER COLUMN id_setor SET DEFAULT nextval('nexus.setores_id_setor_seq'::regclass);


--
-- Name: usuarios codigo_usuario; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.usuarios ALTER COLUMN codigo_usuario SET DEFAULT nextval('nexus.usuarios_codigo_usuario_seq'::regclass);


--
-- Name: pendencias pendencias_numero_key; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendencias
    ADD CONSTRAINT pendencias_numero_key UNIQUE (numero);


--
-- Name: pendencias pendencias_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendencias
    ADD CONSTRAINT pendencias_pkey PRIMARY KEY (id);


--
-- Name: setores setores_nome_setor_key; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.setores
    ADD CONSTRAINT setores_nome_setor_key UNIQUE (nome_setor);


--
-- Name: setores setores_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.setores
    ADD CONSTRAINT setores_pkey PRIMARY KEY (id_setor);


--
-- Name: usuarios usuarios_email_usuario_key; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.usuarios
    ADD CONSTRAINT usuarios_email_usuario_key UNIQUE (email_usuario);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (codigo_usuario);


--
-- Name: pendencias fk_pend_setor; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendencias
    ADD CONSTRAINT fk_pend_setor FOREIGN KEY (id_setor) REFERENCES nexus.setores(id_setor);


--
-- Name: usuarios fk_usuario_setor; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.usuarios
    ADD CONSTRAINT fk_usuario_setor FOREIGN KEY (id_setor) REFERENCES nexus.setores(id_setor);


--
-- PostgreSQL database dump complete
--

\unrestrict GHEbegflSW7mkDoUgLwI61KTd5GGBpvZ05DjTwMRFS7ARcYGH2aQgULutQ7f2oo

