--
-- PostgreSQL database dump
--

\restrict xNThddurgl3bWhw4jEMNn4GDYwx4fc3ZgVmETEoO3HenbJ3CDKxdA5RjPg83jvX

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

-- Started on 2026-02-08 22:24:14

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
-- TOC entry 6 (class 2615 OID 40970)
-- Name: nexus; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA nexus;


ALTER SCHEMA nexus OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 220 (class 1259 OID 40971)
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
    historico jsonb DEFAULT '[]'::jsonb,
    id_roteiro integer
);


ALTER TABLE nexus.pendencias OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 40982)
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
-- TOC entry 5084 (class 0 OID 0)
-- Dependencies: 221
-- Name: pendencias_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.pendencias_id_seq OWNED BY nexus.pendencias.id;


--
-- TOC entry 231 (class 1259 OID 49178)
-- Name: roteiro_setores; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.roteiro_setores (
    id integer NOT NULL,
    roteiro_id integer NOT NULL,
    id_setor integer NOT NULL,
    ordem integer NOT NULL
);


ALTER TABLE nexus.roteiro_setores OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 49177)
-- Name: roteiro_setores_id_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.roteiro_setores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.roteiro_setores_id_seq OWNER TO postgres;

--
-- TOC entry 5085 (class 0 OID 0)
-- Dependencies: 230
-- Name: roteiro_setores_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.roteiro_setores_id_seq OWNED BY nexus.roteiro_setores.id;


--
-- TOC entry 229 (class 1259 OID 49163)
-- Name: roteiros; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.roteiros (
    id integer NOT NULL,
    nome character varying(255) NOT NULL,
    descricao text,
    ativo boolean DEFAULT true NOT NULL,
    data_criacao timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE nexus.roteiros OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 49162)
-- Name: roteiros_id_seq; Type: SEQUENCE; Schema: nexus; Owner: postgres
--

CREATE SEQUENCE nexus.roteiros_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE nexus.roteiros_id_seq OWNER TO postgres;

--
-- TOC entry 5086 (class 0 OID 0)
-- Dependencies: 228
-- Name: roteiros_id_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.roteiros_id_seq OWNED BY nexus.roteiros.id;


--
-- TOC entry 222 (class 1259 OID 40990)
-- Name: setores; Type: TABLE; Schema: nexus; Owner: postgres
--

CREATE TABLE nexus.setores (
    id_setor integer NOT NULL,
    nome_setor text NOT NULL
);


ALTER TABLE nexus.setores OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 40997)
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
-- TOC entry 5087 (class 0 OID 0)
-- Dependencies: 223
-- Name: setores_id_setor_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.setores_id_setor_seq OWNED BY nexus.setores.id_setor;


--
-- TOC entry 224 (class 1259 OID 40998)
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
-- TOC entry 225 (class 1259 OID 41005)
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
-- TOC entry 5088 (class 0 OID 0)
-- Dependencies: 225
-- Name: usuarios_codigo_usuario_seq; Type: SEQUENCE OWNED BY; Schema: nexus; Owner: postgres
--

ALTER SEQUENCE nexus.usuarios_codigo_usuario_seq OWNED BY nexus.usuarios.codigo_usuario;


--
-- TOC entry 226 (class 1259 OID 41006)
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
-- TOC entry 227 (class 1259 OID 41011)
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
-- TOC entry 4885 (class 2604 OID 41015)
-- Name: pendencias id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendencias ALTER COLUMN id SET DEFAULT nextval('nexus.pendencias_id_seq'::regclass);


--
-- TOC entry 4894 (class 2604 OID 49181)
-- Name: roteiro_setores id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.roteiro_setores ALTER COLUMN id SET DEFAULT nextval('nexus.roteiro_setores_id_seq'::regclass);


--
-- TOC entry 4891 (class 2604 OID 49166)
-- Name: roteiros id; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.roteiros ALTER COLUMN id SET DEFAULT nextval('nexus.roteiros_id_seq'::regclass);


--
-- TOC entry 4889 (class 2604 OID 41017)
-- Name: setores id_setor; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.setores ALTER COLUMN id_setor SET DEFAULT nextval('nexus.setores_id_setor_seq'::regclass);


--
-- TOC entry 4890 (class 2604 OID 41018)
-- Name: usuarios codigo_usuario; Type: DEFAULT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.usuarios ALTER COLUMN codigo_usuario SET DEFAULT nextval('nexus.usuarios_codigo_usuario_seq'::regclass);


--
-- TOC entry 5069 (class 0 OID 40971)
-- Dependencies: 220
-- Data for Name: pendencias; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.pendencias (id, numero, data_criacao, data_atualizacao, equipamento, situacao, status, prioridade, prazo_resposta, origem, observacoes, versao, ultima_modificacao, modificado_por, id_usuario, id_setor, propostas_vinculadas, cliente, historico, id_roteiro) FROM stdin;
27	721831	2026-02-08 22:21:03.134227	\N	\N	Aberta	\N	Média	15	\N	Demonstrar as ultimas atualizações	\N	2026-02-08 22:21:31.011553	\N	6	3	\N	\N	[{"acao": "Criação", "idSetor": 3, "situacao": "Aberta", "observacoes": "Demonstrar as ultimas atualizações", "dataAlteracao": "2026-02-08T22:21:03.134227400"}, {"acao": "Atribuição", "idSetor": 3, "situacao": "Aberta", "descricao": "Usuário: — → 6", "idUsuario": 6, "dataAlteracao": "2026-02-08T22:21:31.012906800", "idSetorAnterior": 3, "situacaoAnterior": "Aberta"}]	\N
28	741037	2026-02-08 22:21:58.454649	\N	\N	Aberta	\N	Alta	40	\N	\N	\N	2026-02-08 22:21:58.454649	\N	\N	3	\N	\N	[{"acao": "Criação", "idSetor": 3, "situacao": "Aberta", "dataAlteracao": "2026-02-08T22:21:58.454649200"}]	\N
\.


--
-- TOC entry 5078 (class 0 OID 49178)
-- Dependencies: 231
-- Data for Name: roteiro_setores; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.roteiro_setores (id, roteiro_id, id_setor, ordem) FROM stdin;
1	1	3	1
2	1	1	2
3	1	3	3
\.


--
-- TOC entry 5076 (class 0 OID 49163)
-- Dependencies: 229
-- Data for Name: roteiros; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.roteiros (id, nome, descricao, ativo, data_criacao) FROM stdin;
1	Roteiro teste	\N	t	2026-02-08 22:10:42.581168
\.


--
-- TOC entry 5071 (class 0 OID 40990)
-- Dependencies: 222
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
-- TOC entry 5073 (class 0 OID 40998)
-- Dependencies: 224
-- Data for Name: usuarios; Type: TABLE DATA; Schema: nexus; Owner: postgres
--

COPY nexus.usuarios (codigo_usuario, nome_usuario, telefone_usuario, email_usuario, computador_usuario, cargo_usuario, nivel_usuario, id_setor, senha) FROM stdin;
4	Lucas Bava	+554896718572	projetos2@olivo.ind.br	DESKTOP-QBCIUNQ	ENGENHEIRO	3	1	$2a$10$m3pNj.UNhFIO2Uwg4RiGIejJM.29aqsWRsdcceofVkGXz4nCUpU.K
3	Pedro Luz	+554896870346	projetos14@olivo.ind.br	DESKTOP-TC5VAN1	DEVELOPER	4	3	$2a$10$k2UJDWZeUh8R4hjkFj6v2eXJMjvkfLcnoeeHXQdSIpVE7jRsKBrLO
1	Thalita Costa	+554898430122	vendas06@olivoguindastes.com.br	VENDINTERNA03	VENDEDOR	1	2	$2a$10$AJJmY3u90vR1ry8z.2P11umWrezgwREd7qFcuQRG8Wz1Jrs6.k4Gy
5	Sabino	+554899290029	engenharia08@olivoimplementos.com.br	\N	ENGENHEIRO	3	1	$2a$10$aw3o5FnXZke4dTvCZJ.aiOj3mF6y4khSYwSV/YEV7daUupOcDZQYS
2	Ricardo Feltrin	+554896006593	supervisao01@olivoguindastes.com.br	DESKTOP-M81U9SG	VENDEDOR	1	2	$2a$10$sQ2miwq1X2D8bML03qjKQ.hksmqhyCZJvBo2Iy5/joCwU6GkNGWL2
7	Dimitri	+554896989630	\N	\N	LIDER	3	4	\N
8	Leanderson	+554891817184	ger.custos@olivoimplementos.com.br	\N	GERENTE	3	5	\N
9	Fabiano	+554884528863	\N	\N	ENGENHEIRO	3	1	\N
6	Miguel Firme	+554898036211	projetos13@olivo.ind.br	MIGUELFIRME	DEVELOPER	4	3	$2a$10$ByZsWkEucvJUMNX3fJVNTefsFWTkXLb3m8g3RpRhwfrNhaHNN3T3K
10	Leonardo Bettiol				ENGENHEIRO	2	1	\N
\.


--
-- TOC entry 5089 (class 0 OID 0)
-- Dependencies: 221
-- Name: pendencias_id_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.pendencias_id_seq', 28, true);


--
-- TOC entry 5090 (class 0 OID 0)
-- Dependencies: 230
-- Name: roteiro_setores_id_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.roteiro_setores_id_seq', 3, true);


--
-- TOC entry 5091 (class 0 OID 0)
-- Dependencies: 228
-- Name: roteiros_id_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.roteiros_id_seq', 1, true);


--
-- TOC entry 5092 (class 0 OID 0)
-- Dependencies: 223
-- Name: setores_id_setor_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.setores_id_setor_seq', 5, true);


--
-- TOC entry 5093 (class 0 OID 0)
-- Dependencies: 225
-- Name: usuarios_codigo_usuario_seq; Type: SEQUENCE SET; Schema: nexus; Owner: postgres
--

SELECT pg_catalog.setval('nexus.usuarios_codigo_usuario_seq', 13, true);


--
-- TOC entry 4897 (class 2606 OID 41020)
-- Name: pendencias pendencias_numero_key; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendencias
    ADD CONSTRAINT pendencias_numero_key UNIQUE (numero);


--
-- TOC entry 4899 (class 2606 OID 41022)
-- Name: pendencias pendencias_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendencias
    ADD CONSTRAINT pendencias_pkey PRIMARY KEY (id);


--
-- TOC entry 4913 (class 2606 OID 49187)
-- Name: roteiro_setores roteiro_setores_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.roteiro_setores
    ADD CONSTRAINT roteiro_setores_pkey PRIMARY KEY (id);


--
-- TOC entry 4909 (class 2606 OID 49176)
-- Name: roteiros roteiros_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.roteiros
    ADD CONSTRAINT roteiros_pkey PRIMARY KEY (id);


--
-- TOC entry 4901 (class 2606 OID 41026)
-- Name: setores setores_nome_setor_key; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.setores
    ADD CONSTRAINT setores_nome_setor_key UNIQUE (nome_setor);


--
-- TOC entry 4903 (class 2606 OID 41028)
-- Name: setores setores_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.setores
    ADD CONSTRAINT setores_pkey PRIMARY KEY (id_setor);


--
-- TOC entry 4915 (class 2606 OID 49189)
-- Name: roteiro_setores unique_roteiro_ordem; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.roteiro_setores
    ADD CONSTRAINT unique_roteiro_ordem UNIQUE (roteiro_id, ordem);


--
-- TOC entry 4905 (class 2606 OID 41030)
-- Name: usuarios usuarios_email_usuario_key; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.usuarios
    ADD CONSTRAINT usuarios_email_usuario_key UNIQUE (email_usuario);


--
-- TOC entry 4907 (class 2606 OID 41032)
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (codigo_usuario);


--
-- TOC entry 4895 (class 1259 OID 49200)
-- Name: idx_pendencias_id_roteiro; Type: INDEX; Schema: nexus; Owner: postgres
--

CREATE INDEX idx_pendencias_id_roteiro ON nexus.pendencias USING btree (id_roteiro);


--
-- TOC entry 4910 (class 1259 OID 49202)
-- Name: idx_roteiro_setores_id_setor; Type: INDEX; Schema: nexus; Owner: postgres
--

CREATE INDEX idx_roteiro_setores_id_setor ON nexus.roteiro_setores USING btree (id_setor);


--
-- TOC entry 4911 (class 1259 OID 49201)
-- Name: idx_roteiro_setores_roteiro_id; Type: INDEX; Schema: nexus; Owner: postgres
--

CREATE INDEX idx_roteiro_setores_roteiro_id ON nexus.roteiro_setores USING btree (roteiro_id);


--
-- TOC entry 4916 (class 2606 OID 41033)
-- Name: pendencias fk_pend_setor; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.pendencias
    ADD CONSTRAINT fk_pend_setor FOREIGN KEY (id_setor) REFERENCES nexus.setores(id_setor);


--
-- TOC entry 4918 (class 2606 OID 49195)
-- Name: roteiro_setores fk_roteiro_setor; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.roteiro_setores
    ADD CONSTRAINT fk_roteiro_setor FOREIGN KEY (roteiro_id) REFERENCES nexus.roteiros(id) ON DELETE CASCADE;


--
-- TOC entry 4917 (class 2606 OID 41038)
-- Name: usuarios fk_usuario_setor; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.usuarios
    ADD CONSTRAINT fk_usuario_setor FOREIGN KEY (id_setor) REFERENCES nexus.setores(id_setor);


--
-- TOC entry 4919 (class 2606 OID 49190)
-- Name: roteiro_setores roteiro_setores_roteiro_id_fkey; Type: FK CONSTRAINT; Schema: nexus; Owner: postgres
--

ALTER TABLE ONLY nexus.roteiro_setores
    ADD CONSTRAINT roteiro_setores_roteiro_id_fkey FOREIGN KEY (roteiro_id) REFERENCES nexus.roteiros(id) ON DELETE CASCADE;


-- Completed on 2026-02-08 22:24:14

--
-- PostgreSQL database dump complete
--

\unrestrict xNThddurgl3bWhw4jEMNn4GDYwx4fc3ZgVmETEoO3HenbJ3CDKxdA5RjPg83jvX

