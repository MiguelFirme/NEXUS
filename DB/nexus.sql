--
-- PostgreSQL database dump
--

\restrict qSikDaDQGTFrh8ZbCIszXo1u2vkozbhovXisBqd06zc3RGE8AaluyHRLiWMsF8S

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

-- Started on 2026-02-05 13:06:59

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
-- TOC entry 6 (class 2615 OID 16388)
-- Name: nexus; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA nexus;


ALTER SCHEMA nexus OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 220 (class 1259 OID 16389)
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
    id_setor integer,
    propostas_vinculadas jsonb DEFAULT '[]'::jsonb,
    cliente jsonb DEFAULT '{}'::jsonb,
    historico jsonb DEFAULT '[]'::jsonb
);


ALTER TABLE nexus.pendencias OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 16400)
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
-- TOC entry 5065 (class 0 OID 0)
-- Dependencies: 221
-- Name: pendencias_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.pendencias_id_seq OWNED BY nexus.pendencias.id;


--
-- TOC entry 222 (class 1259 OID 16401)
-- Name: rotina_passos; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.rotina_passos (
    id integer NOT NULL,
    rotina_id integer,
    ordem integer,
    id_setor integer,
    nome_pass character varying(255),
    instrucoes text
);


ALTER TABLE nexus.rotina_passos OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 16407)
-- Name: rotina_passos_id_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.rotina_passos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.rotina_passos_id_seq OWNER TO postgres;

--
-- TOC entry 5066 (class 0 OID 0)
-- Dependencies: 223
-- Name: rotina_passos_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.rotina_passos_id_seq OWNED BY nexus.rotina_passos.id;


--
-- TOC entry 224 (class 1259 OID 16408)
-- Name: setores; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.setores (
    id_setor integer NOT NULL,
    nome_setor text NOT NULL
);


ALTER TABLE nexus.setores OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 16415)
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
-- TOC entry 5067 (class 0 OID 0)
-- Dependencies: 225
-- Name: setores_id_setor_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.setores_id_setor_seq OWNED BY nexus.setores.id_setor;


--
-- TOC entry 226 (class 1259 OID 16416)
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
    id_setor integer,
    senha character varying
);


ALTER TABLE nexus.usuarios OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 16423)
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
-- TOC entry 5068 (class 0 OID 0)
-- Dependencies: 227
-- Name: usuarios_codigo_usuario_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.usuarios_codigo_usuario_seq OWNED BY nexus.usuarios.codigo_usuario;


--
-- TOC entry 228 (class 1259 OID 16424)
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
    p.data_atualizacao,
    p.ultima_modificacao,
    p.equipamento,
    p.observacoes
   FROM ((nexus.pendencias p
     LEFT JOIN nexus.usuarios u ON ((u.codigo_usuario = p.id_usuario)))
     LEFT JOIN nexus.setores s ON ((s.id_setor = p.id_setor)));


ALTER VIEW nexus.v_pendencias_com_detalhes OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 16429)
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
-- TOC entry 4880 (class 2604 OID 16433)
-- Name: pendencias id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendencias ALTER COLUMN id SET DEFAULT nextval('nexus.pendencias_id_seq'::regclass);


--
-- TOC entry 4884 (class 2604 OID 16434)
-- Name: rotina_passos id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.rotina_passos ALTER COLUMN id SET DEFAULT nextval('nexus.rotina_passos_id_seq'::regclass);


--
-- TOC entry 4885 (class 2604 OID 16435)
-- Name: setores id_setor; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.setores ALTER COLUMN id_setor SET DEFAULT nextval('nexus.setores_id_setor_seq'::regclass);


--
-- TOC entry 4886 (class 2604 OID 16436)
-- Name: usuarios codigo_usuario; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.usuarios ALTER COLUMN codigo_usuario SET DEFAULT nextval('nexus.usuarios_codigo_usuario_seq'::regclass);


--
-- TOC entry 5052 (class 0 OID 16389)
-- Dependencies: 220
-- Data for Name: pendencias; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.pendencias (id, numero, data_criacao, data_atualizacao, equipamento, situacao, status, prioridade, prazo_resposta, origem, observacoes, versao, ultima_modificacao, modificado_por, id_usuario, id_setor, propostas_vinculadas, cliente, historico) FROM stdin;
21	PEN-1770126523593	2026-02-03 10:48:43.622259	\N	\N	Em Andamento	\N	Baixa	15	\N	Testando...	\N	2026-02-03 10:50:37.44581	\N	\N	1	\N	\N	[{"acao": "Criação", "idSetor": 3, "situacao": "Aberta", "idUsuario": 6, "observacoes": "Testando...", "dataAlteracao": "2026-02-03T10:48:43.622259100"}, {"acao": "Mudança de situação", "idSetor": 3, "situacao": "Em Andamento", "descricao": "Situação: Aberta → Em Andamento", "idUsuario": 6, "dataAlteracao": "2026-02-03T10:48:55.207475700", "idSetorAnterior": 3, "situacaoAnterior": "Aberta", "idUsuarioAnterior": 6}, {"acao": "Transferência", "idSetor": 1, "situacao": "Em Andamento", "descricao": "Setor: 3 → 1. Usuário: 6 → —", "dataAlteracao": "2026-02-03T10:50:37.445809600", "idSetorAnterior": 3, "situacaoAnterior": "Em Andamento", "idUsuarioAnterior": 6}]
11	Pendencia Front end	2026-01-30 11:29:54.428146	\N	Pendencia Front end	\N	\N	\N	\N	\N	Essa pendencia foi criada com o front end	\N	2026-01-30 11:29:54.428146	\N	\N	\N	\N	\N	\N
15	PEN-1769784546605	2026-01-30 11:49:06.629194	\N	\N	Aberta	\N	Média	4	\N	aaaaaaa	\N	2026-01-30 11:49:06.629194	\N	4	2	\N	\N	\N
22	PEN-1770130692938	2026-02-03 11:58:12.994669	\N	\N	Aberta	\N	Média	\N	\N	TESTE	\N	2026-02-03 11:58:36.30389	\N	6	3	\N	\N	[{"acao": "Criação", "idSetor": 3, "situacao": "Aberta", "observacoes": "TESTE", "dataAlteracao": "2026-02-03T11:58:12.995670800"}, {"acao": "Atribuição", "idSetor": 3, "situacao": "Aberta", "descricao": "Usuário: — → 6", "idUsuario": 6, "dataAlteracao": "2026-02-03T11:58:36.303889900", "idSetorAnterior": 3, "situacaoAnterior": "Aberta"}]
23	PEN-1770135224534	2026-02-03 13:13:44.576657	\N	\N	Aberta	\N	Média	15	\N	Teste	\N	2026-02-03 13:13:44.576657	\N	\N	3	\N	\N	[{"acao": "Criação", "idSetor": 3, "situacao": "Aberta", "observacoes": "Teste", "dataAlteracao": "2026-02-03T13:13:44.576656900"}]
\.


--
-- TOC entry 5054 (class 0 OID 16401)
-- Dependencies: 222
-- Data for Name: rotina_passos; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.rotina_passos (id, rotina_id, ordem, id_setor, nome_pass, instrucoes) FROM stdin;
\.


--
-- TOC entry 5056 (class 0 OID 16408)
-- Dependencies: 224
-- Data for Name: setores; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.setores (id_setor, nome_setor) FROM stdin;
1	ENGENHARIA
2	COMERCIAL
3	DESENVOLVIMENTO
4	PCP
5	CUSTOS
\.


--
-- TOC entry 5058 (class 0 OID 16416)
-- Dependencies: 226
-- Data for Name: usuarios; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.usuarios (codigo_usuario, nome_usuario, telefone_usuario, email_usuario, computador_usuario, cargo_usuario, nivel_usuario, id_setor, senha) FROM stdin;
6	Miguel Firme	+554898036211	projetos13@olivo.ind.br	MIGUELFIRME	DEVELOPER	4	3	$2a$10$JQNvCUkNglJSK7rlpCDQ.O1nu75VanCy.m8VMHOezwL.iguVsPRoW
4	Lucas Bava	+554896718572	projetos2@olivo.ind.br	DESKTOP-QBCIUNQ	ENGENHEIRO	3	1	$2a$10$m3pNj.UNhFIO2Uwg4RiGIejJM.29aqsWRsdcceofVkGXz4nCUpU.K
3	Pedro Luz	+554896870346	projetos14@olivo.ind.br	DESKTOP-TC5VAN1	DEVELOPER	4	3	$2a$10$k2UJDWZeUh8R4hjkFj6v2eXJMjvkfLcnoeeHXQdSIpVE7jRsKBrLO
1	Thalita Costa	+554898430122	vendas06@olivoguindastes.com.br	VENDINTERNA03	VENDEDOR	1	2	$2a$10$AJJmY3u90vR1ry8z.2P11umWrezgwREd7qFcuQRG8Wz1Jrs6.k4Gy
5	Sabino	+554899290029	engenharia08@olivoimplementos.com.br	\N	ENGENHEIRO	3	1	$2a$10$aw3o5FnXZke4dTvCZJ.aiOj3mF6y4khSYwSV/YEV7daUupOcDZQYS
2	Ricardo Feltrin	+554896006593	supervisao01@olivoguindastes.com.br	DESKTOP-M81U9SG	VENDEDOR	1	2	$2a$10$sQ2miwq1X2D8bML03qjKQ.hksmqhyCZJvBo2Iy5/joCwU6GkNGWL2
7	Dimitri	+554896989630	\N	\N	LIDER	3	4	\N
8	Leanderson	+554891817184	ger.custos@olivoimplementos.com.br	\N	GERENTE	3	5	\N
9	Fabiano	+554884528863	\N	\N	ENGENHEIRO	3	1	\N
10	Leonardo Bettiol	+554891218600	\N	\N	ENGENHEIRO	3	1	\N
\.


--
-- TOC entry 5069 (class 0 OID 0)
-- Dependencies: 221
-- Name: pendencias_id_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.pendencias_id_seq', 23, true);


--
-- TOC entry 5070 (class 0 OID 0)
-- Dependencies: 223
-- Name: rotina_passos_id_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.rotina_passos_id_seq', 1, false);


--
-- TOC entry 5071 (class 0 OID 0)
-- Dependencies: 225
-- Name: setores_id_setor_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.setores_id_setor_seq', 5, true);


--
-- TOC entry 5072 (class 0 OID 0)
-- Dependencies: 227
-- Name: usuarios_codigo_usuario_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.usuarios_codigo_usuario_seq', 10, true);


--
-- TOC entry 4888 (class 2606 OID 16438)
-- Name: pendencias pendencias_numero_key; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendencias
    ADD CONSTRAINT pendencias_numero_key UNIQUE (numero);


--
-- TOC entry 4890 (class 2606 OID 16440)
-- Name: pendencias pendencias_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendencias
    ADD CONSTRAINT pendencias_pkey PRIMARY KEY (id);


--
-- TOC entry 4892 (class 2606 OID 16442)
-- Name: rotina_passos rotina_passos_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.rotina_passos
    ADD CONSTRAINT rotina_passos_pkey PRIMARY KEY (id);


--
-- TOC entry 4894 (class 2606 OID 16444)
-- Name: setores setores_nome_setor_key; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.setores
    ADD CONSTRAINT setores_nome_setor_key UNIQUE (nome_setor);


--
-- TOC entry 4896 (class 2606 OID 16446)
-- Name: setores setores_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.setores
    ADD CONSTRAINT setores_pkey PRIMARY KEY (id_setor);


--
-- TOC entry 4898 (class 2606 OID 16448)
-- Name: usuarios usuarios_email_usuario_key; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.usuarios
    ADD CONSTRAINT usuarios_email_usuario_key UNIQUE (email_usuario);


--
-- TOC entry 4900 (class 2606 OID 16450)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (codigo_usuario);


--
-- TOC entry 4901 (class 2606 OID 16451)
-- Name: pendencias fk_pend_setor; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendencias
    ADD CONSTRAINT fk_pend_setor FOREIGN KEY (id_setor) REFERENCES nexus.setores(id_setor);


--
-- TOC entry 4902 (class 2606 OID 16456)
-- Name: usuarios fk_usuario_setor; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.usuarios
    ADD CONSTRAINT fk_usuario_setor FOREIGN KEY (id_setor) REFERENCES nexus.setores(id_setor);


-- Completed on 2026-02-05 13:07:00

--
-- PostgreSQL database dump complete
--

\unrestrict qSikDaDQGTFrh8ZbCIszXo1u2vkozbhovXisBqd06zc3RGE8AaluyHRLiWMsF8S

