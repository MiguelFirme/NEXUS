--
-- PostgreSQL database dump
--

\restrict ytnHWLBfpdJgQAuCLePvfsZez5ODdltsYZ1oTw6filfkqbOSALa2JZRaYlBEmBE

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
    vendedor character varying(100),
    setor character varying(100),
    equipamento text,
    situacao character varying(100),
    status character varying(50),
    prioridade character varying(20),
    prazo_resposta integer,
    origem character varying(50),
    observacoes text,
    versao character varying(20),
    ultima_modificacao timestamp without time zone,
    modificado_por character varying(100)
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
-- Name: usuarios; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.usuarios (
    codigo_usuario integer NOT NULL,
    nome_usuario text NOT NULL,
    telefone_usuario text,
    email_usuario text,
    computador_usuario text,
    setor_usuario text,
    cargo_usuario text,
    nivel_usuario integer
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
-- Name: pendencias id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendencias ALTER COLUMN id SET DEFAULT nextval('nexus.pendencias_id_seq'::regclass);


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
-- PostgreSQL database dump complete
--

\unrestrict ytnHWLBfpdJgQAuCLePvfsZez5ODdltsYZ1oTw6filfkqbOSALa2JZRaYlBEmBE

