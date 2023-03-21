--
-- PostgreSQL database dump
--

-- Dumped from database version 14.7 (Debian 14.7-1.pgdg110+1)
-- Dumped by pg_dump version 14.7 (Debian 14.7-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: state; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.state AS ENUM (
    'NEW',
    'PARSED',
    'VERIFIED'
);


ALTER TYPE public.state OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: clients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clients (
    id integer NOT NULL,
    username character varying(60) NOT NULL,
    email character varying(255) NOT NULL,
    password_hash character varying(255) NOT NULL,
    activated boolean,
    created_at timestamp without time zone,
    unique_id character varying(36)
);


ALTER TABLE public.clients OWNER TO postgres;

--
-- Name: clients_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clients_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.clients_id_seq OWNER TO postgres;

--
-- Name: clients_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clients_id_seq OWNED BY public.clients.id;


--
-- Name: email_site; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.email_site (
    id integer NOT NULL,
    site_id integer,
    email_id integer
);


ALTER TABLE public.email_site OWNER TO postgres;

--
-- Name: email_site_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.email_site_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.email_site_id_seq OWNER TO postgres;

--
-- Name: email_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.email_site_id_seq OWNED BY public.email_site.id;


--
-- Name: emails; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.emails (
    id integer NOT NULL,
    email character varying(256) NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.emails OWNER TO postgres;

--
-- Name: emails_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.emails_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.emails_id_seq OWNER TO postgres;

--
-- Name: emails_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.emails_id_seq OWNED BY public.emails.id;


--
-- Name: phone_site; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.phone_site (
    id integer NOT NULL,
    site_id integer,
    phone_id integer
);


ALTER TABLE public.phone_site OWNER TO postgres;

--
-- Name: phone_site_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.phone_site_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.phone_site_id_seq OWNER TO postgres;

--
-- Name: phone_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.phone_site_id_seq OWNED BY public.phone_site.id;


--
-- Name: phones; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.phones (
    id integer NOT NULL,
    number character varying(256) NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.phones OWNER TO postgres;

--
-- Name: phones_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.phones_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.phones_id_seq OWNER TO postgres;

--
-- Name: phones_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.phones_id_seq OWNED BY public.phones.id;


--
-- Name: sites; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sites (
    id integer NOT NULL,
    url character varying(256) NOT NULL,
    state public.state,
    created_at timestamp without time zone,
    parsed_at timestamp without time zone
);


ALTER TABLE public.sites OWNER TO postgres;

--
-- Name: sites_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sites_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sites_id_seq OWNER TO postgres;

--
-- Name: sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sites_id_seq OWNED BY public.sites.id;


--
-- Name: clients id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients ALTER COLUMN id SET DEFAULT nextval('public.clients_id_seq'::regclass);


--
-- Name: email_site id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.email_site ALTER COLUMN id SET DEFAULT nextval('public.email_site_id_seq'::regclass);


--
-- Name: emails id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emails ALTER COLUMN id SET DEFAULT nextval('public.emails_id_seq'::regclass);


--
-- Name: phone_site id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phone_site ALTER COLUMN id SET DEFAULT nextval('public.phone_site_id_seq'::regclass);


--
-- Name: phones id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phones ALTER COLUMN id SET DEFAULT nextval('public.phones_id_seq'::regclass);


--
-- Name: sites id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sites ALTER COLUMN id SET DEFAULT nextval('public.sites_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
869d35ddd173
\.


--
-- Data for Name: clients; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clients (id, username, email, password_hash, activated, created_at, unique_id) FROM stdin;
1	admin	admin@simple2b.net	pbkdf2:sha256:260000$NVmbjWWmnEejKvqN$e9bc389dce80eb9b15102361804f31e9763f6135859f098f4c7424d130ed236c	f	2023-03-21 07:39:42.53737	1c03517e-ef9f-4365-ba52-43371890a829
\.


--
-- Data for Name: email_site; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.email_site (id, site_id, email_id) FROM stdin;
\.


--
-- Data for Name: emails; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.emails (id, email, created_at) FROM stdin;
\.


--
-- Data for Name: phone_site; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.phone_site (id, site_id, phone_id) FROM stdin;
\.


--
-- Data for Name: phones; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.phones (id, number, created_at) FROM stdin;
\.


--
-- Data for Name: sites; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sites (id, url, state, created_at, parsed_at) FROM stdin;
1	https://www.riserealtyca.com/	NEW	2023-03-21 07:47:47.424764	9999-12-31 23:59:59.999999
2	https://www.luxurysocalrealty.com/	NEW	2023-03-21 07:47:48.406934	9999-12-31 23:59:59.999999
3	https://www.rubyhome.com/	NEW	2023-03-21 08:51:17.918979	9999-12-31 23:59:59.999999
4	https://www.texasrealestatesource.com/	NEW	2023-03-21 08:51:18.961152	9999-12-31 23:59:59.999999
5	https://www.yourathometeam.com/	NEW	2023-03-21 08:51:20.070123	9999-12-31 23:59:59.999999
6	https://www.kittlerealestate.com/	NEW	2023-03-21 08:51:25.994156	9999-12-31 23:59:59.999999
7	https://www.trecmoves.com/	NEW	2023-03-21 08:51:29.698139	9999-12-31 23:59:59.999999
8	https://www.villarealestate.com/	NEW	2023-03-21 08:51:32.322604	9999-12-31 23:59:59.999999
9	https://www.sarasotafloridarealestate.com/	NEW	2023-03-21 08:51:33.700427	9999-12-31 23:59:59.999999
10	https://www.palmshome.com/	NEW	2023-03-21 08:51:35.475958	9999-12-31 23:59:59.999999
11	https://www.lipplyrealestate.com/	NEW	2023-03-21 08:51:36.549886	9999-12-31 23:59:59.999999
12	https://www.totalvegasrealestate.com/	NEW	2023-03-21 08:51:37.422884	9999-12-31 23:59:59.999999
13	https://www.shepherdhomesgroup.com/	NEW	2023-03-21 08:51:40.645763	9999-12-31 23:59:59.999999
14	https://www.thecaliforniahomefinder.com/	NEW	2023-03-21 08:51:41.936171	9999-12-31 23:59:59.999999
15	https://www.1kbb.com/	NEW	2023-03-21 08:51:43.126687	9999-12-31 23:59:59.999999
16	https://www.oceancitycondosandhomes.com/	NEW	2023-03-21 08:51:44.165323	9999-12-31 23:59:59.999999
17	https://www.bighelpergroup.com/	NEW	2023-03-21 08:51:45.271758	9999-12-31 23:59:59.999999
18	https://www.wexlerrealestate.com/	NEW	2023-03-21 08:51:46.294191	9999-12-31 23:59:59.999999
19	https://www.mnpropertygroup.com/	NEW	2023-03-21 08:51:47.358039	9999-12-31 23:59:59.999999
20	https://www.dayhometeam.com/	NEW	2023-03-21 08:51:50.196756	9999-12-31 23:59:59.999999
21	https://www.homepagerealty.com/	NEW	2023-03-21 08:51:56.83436	9999-12-31 23:59:59.999999
22	https://www.thegrishamgroup.com/	NEW	2023-03-21 08:51:57.793885	9999-12-31 23:59:59.999999
23	https://www.chartaylorrealestate.com/	NEW	2023-03-21 08:51:58.801675	9999-12-31 23:59:59.999999
24	https://www.greentreerealestate.com/	NEW	2023-03-21 08:51:59.693329	9999-12-31 23:59:59.999999
25	https://www.livingingreatercharlotte.com/	NEW	2023-03-21 09:15:31.821577	9999-12-31 23:59:59.999999
26	https://www.matinrealestate.com/	NEW	2023-03-21 09:15:38.592827	9999-12-31 23:59:59.999999
27	https://www.supremerealestatekc.com/	NEW	2023-03-21 09:15:39.65538	9999-12-31 23:59:59.999999
28	https://www.virga-realty.com/	NEW	2023-03-21 09:15:44.686044	9999-12-31 23:59:59.999999
29	https://www.tiffanyholtz.com/	NEW	2023-03-21 09:15:47.473239	9999-12-31 23:59:59.999999
30	https://www.shilostorey.com/	NEW	2023-03-21 09:15:48.483556	9999-12-31 23:59:59.999999
31	https://www.trgmove.com/	NEW	2023-03-21 09:15:49.442752	9999-12-31 23:59:59.999999
32	https://www.pepinerealty.com/	NEW	2023-03-21 09:15:50.62605	9999-12-31 23:59:59.999999
33	https://www.nowrealestategroup.ca/	NEW	2023-03-21 09:15:51.787485	9999-12-31 23:59:59.999999
34	https://www.thelestergroup.com/	NEW	2023-03-21 09:15:52.894121	9999-12-31 23:59:59.999999
35	https://www.portlandrealestate.com/	NEW	2023-03-21 09:15:53.889679	9999-12-31 23:59:59.999999
36	https://www.anvilreinc.com/	NEW	2023-03-21 09:15:55.515243	9999-12-31 23:59:59.999999
37	https://www.tracyestates.com/	NEW	2023-03-21 09:15:58.588177	9999-12-31 23:59:59.999999
38	https://www.affinityrealestate.ca/	NEW	2023-03-21 09:15:59.568603	9999-12-31 23:59:59.999999
39	https://www.edmontonrealtyexperts.com/	NEW	2023-03-21 09:16:00.594127	9999-12-31 23:59:59.999999
40	https://www.thestillergroup.com/	NEW	2023-03-21 09:16:01.616034	9999-12-31 23:59:59.999999
41	https://www.teamgoran.com/	NEW	2023-03-21 09:16:02.684821	9999-12-31 23:59:59.999999
42	https://www.greatertorontohomepros.com/	NEW	2023-03-21 09:16:03.741421	9999-12-31 23:59:59.999999
43	https://www.effective.realestate/	NEW	2023-03-21 09:16:04.77066	9999-12-31 23:59:59.999999
44	https://www.ixlrealestate.com/	NEW	2023-03-21 09:16:05.93628	9999-12-31 23:59:59.999999
45	https://www.liveutah.com/	NEW	2023-03-21 09:16:08.028744	9999-12-31 23:59:59.999999
46	https://www.dawkinsresidential.com/	NEW	2023-03-21 09:16:11.205357	9999-12-31 23:59:59.999999
47	https://www.kessingerrealestate.com/	NEW	2023-03-21 09:16:12.670813	9999-12-31 23:59:59.999999
48	https://www.reallivinghomes.ca/	NEW	2023-03-21 09:16:13.768401	9999-12-31 23:59:59.999999
49	https://www.truerealestateminnesota.com/	NEW	2023-03-21 09:16:14.788472	9999-12-31 23:59:59.999999
50	https://www.woodrealestategroup.com/	NEW	2023-03-21 09:16:15.754628	9999-12-31 23:59:59.999999
51	https://www.omegahome.com/	NEW	2023-03-21 09:16:16.663925	9999-12-31 23:59:59.999999
52	https://www.brgut.com/	NEW	2023-03-21 09:16:17.658773	9999-12-31 23:59:59.999999
53	https://www.jimblacksellshomes.com/	NEW	2023-03-21 09:16:18.683137	9999-12-31 23:59:59.999999
54	https://www.zokoeteam.com/	NEW	2023-03-21 09:16:19.815435	9999-12-31 23:59:59.999999
55	https://www.lonniebush.com/	NEW	2023-03-21 09:16:22.64842	9999-12-31 23:59:59.999999
56	https://www.edmonton-real-estate.com/	NEW	2023-03-21 09:16:23.639987	9999-12-31 23:59:59.999999
57	https://www.weknowottawa.com/	NEW	2023-03-21 09:16:24.769291	9999-12-31 23:59:59.999999
58	https://www.gristrealestate.com/	NEW	2023-03-21 09:16:25.875688	9999-12-31 23:59:59.999999
59	https://www.rzteamkc.com/	NEW	2023-03-21 09:16:27.139946	9999-12-31 23:59:59.999999
60	https://www.atkinsonteam.ca/	NEW	2023-03-21 09:16:28.134917	9999-12-31 23:59:59.999999
61	https://www.katrinaandtheteam.com/	NEW	2023-03-21 09:16:29.215629	9999-12-31 23:59:59.999999
62	https://www.elliottreteam.com/	NEW	2023-03-21 09:16:30.742869	9999-12-31 23:59:59.999999
63	https://www.dolanre.com/	NEW	2023-03-21 09:16:31.85477	9999-12-31 23:59:59.999999
64	https://www.carbuttirealestate.com/	NEW	2023-03-21 09:16:32.866049	9999-12-31 23:59:59.999999
65	https://www.dwellingsmi.com/	NEW	2023-03-21 09:16:35.647975	9999-12-31 23:59:59.999999
66	https://www.ronsellsthebeach.com/	NEW	2023-03-21 09:16:36.659507	9999-12-31 23:59:59.999999
67	https://manausa.com/	NEW	2023-03-21 09:16:38.095242	9999-12-31 23:59:59.999999
68	https://www.lyvrealty.com/	NEW	2023-03-21 09:16:39.162849	9999-12-31 23:59:59.999999
69	https://www.acolerealty.com/	NEW	2023-03-21 09:16:40.284354	9999-12-31 23:59:59.999999
70	https://www.sierracrestrealestate.com/	NEW	2023-03-21 09:16:41.410707	9999-12-31 23:59:59.999999
71	https://www.johnhillhomesearch.com/	NEW	2023-03-21 09:16:42.906838	9999-12-31 23:59:59.999999
72	https://www.mattoneillrealestate.com/	NEW	2023-03-21 09:16:44.128615	9999-12-31 23:59:59.999999
73	https://www.niceagents.ca/	NEW	2023-03-21 09:16:49.123325	9999-12-31 23:59:59.999999
74	https://www.graywaltrealty.com/	NEW	2023-03-21 09:16:50.132719	9999-12-31 23:59:59.999999
75	https://www.markdietel.com/	NEW	2023-03-21 09:16:51.066799	9999-12-31 23:59:59.999999
76	https://www.palmparadiserealestate.com/	NEW	2023-03-21 09:16:52.042561	9999-12-31 23:59:59.999999
77	https://www.listwithron.com/	NEW	2023-03-21 09:16:53.413817	9999-12-31 23:59:59.999999
78	https://www.yegpropertypros.com/	NEW	2023-03-21 09:16:54.638353	9999-12-31 23:59:59.999999
79	https://www.firstsaturdayre.com/	NEW	2023-03-21 09:16:55.622378	9999-12-31 23:59:59.999999
80	https://www.elainekochgroup.com/	NEW	2023-03-21 09:16:56.707986	9999-12-31 23:59:59.999999
81	https://www.cityandfieldhomes.com/	NEW	2023-03-21 09:16:57.715717	9999-12-31 23:59:59.999999
82	https://www.clearviewep.com/	NEW	2023-03-21 09:16:58.696961	9999-12-31 23:59:59.999999
83	https://www.hansenteampensacola.com/	NEW	2023-03-21 09:17:01.632232	9999-12-31 23:59:59.999999
84	https://www.walidmrealtor.com/	NEW	2023-03-21 09:17:02.854486	9999-12-31 23:59:59.999999
85	https://www.elamre.com/	NEW	2023-03-21 09:17:03.858723	9999-12-31 23:59:59.999999
86	https://www.lauriereader.com/	NEW	2023-03-21 09:17:04.911567	9999-12-31 23:59:59.999999
87	https://www.trilliantrealty.ca/	NEW	2023-03-21 09:17:05.96337	9999-12-31 23:59:59.999999
88	https://www.indianahomesfirst.com/	NEW	2023-03-21 09:17:07.114807	9999-12-31 23:59:59.999999
89	https://www.performance-realestate.com/about/	NEW	2023-03-21 09:17:08.188406	9999-12-31 23:59:59.999999
90	https://www.richbassford.com/	NEW	2023-03-21 09:17:09.099095	9999-12-31 23:59:59.999999
91	https://www.therussellteam.com/	NEW	2023-03-21 09:17:10.146522	9999-12-31 23:59:59.999999
92	https://www.oakandstonerealestate.com/	NEW	2023-03-21 09:17:11.127706	9999-12-31 23:59:59.999999
93	https://www.lincolnselectrealestategroup.com/	NEW	2023-03-21 09:17:14.190485	9999-12-31 23:59:59.999999
94	https://www.brealthomasville.com/	NEW	2023-03-21 09:17:15.187393	9999-12-31 23:59:59.999999
95	https://www.keetonandcompany.com/	NEW	2023-03-21 09:17:16.372801	9999-12-31 23:59:59.999999
96	https://www.jacobsandco.com/	NEW	2023-03-21 09:17:17.392228	9999-12-31 23:59:59.999999
97	https://www.maddenrealestate.com/	NEW	2023-03-21 09:17:18.32798	9999-12-31 23:59:59.999999
98	https://www.avenueret.com/	NEW	2023-03-21 09:17:19.500231	9999-12-31 23:59:59.999999
99	https://www.ryandobbsteam.com/	NEW	2023-03-21 09:17:20.822958	9999-12-31 23:59:59.999999
100	https://www.thebrileyteam.com/	NEW	2023-03-21 09:17:21.946778	9999-12-31 23:59:59.999999
101	https://www.liveankeny.com/	NEW	2023-03-21 09:17:22.841786	9999-12-31 23:59:59.999999
102	https://www.nassargrouprealty.com/	NEW	2023-03-21 09:17:26.394784	9999-12-31 23:59:59.999999
103	https://www.cantrellre.com/	NEW	2023-03-21 09:17:27.431775	9999-12-31 23:59:59.999999
104	https://www.dustonleddy.com/	NEW	2023-03-21 09:17:28.483339	9999-12-31 23:59:59.999999
105	https://www.costellorei.com/	NEW	2023-03-21 09:17:29.620118	9999-12-31 23:59:59.999999
106	https://www.bradfordudouj.com/	NEW	2023-03-21 09:17:30.63612	9999-12-31 23:59:59.999999
107	https://www.mkrealestatesales.com/	NEW	2023-03-21 09:17:32.412171	9999-12-31 23:59:59.999999
108	https://www.goodmorningrealty.com/	NEW	2023-03-21 09:17:33.48887	9999-12-31 23:59:59.999999
109	https://www.allgoodsoldit.com/	NEW	2023-03-21 09:17:34.921057	9999-12-31 23:59:59.999999
110	https://www.sellwithmoore.com/	NEW	2023-03-21 09:17:36.202871	9999-12-31 23:59:59.999999
111	https://www.gustygulasgroup.com/	NEW	2023-03-21 09:17:37.244371	9999-12-31 23:59:59.999999
112	https://www.symbiodenver.com/	NEW	2023-03-21 09:17:40.354946	9999-12-31 23:59:59.999999
113	https://www.realtallrealestate.com/	NEW	2023-03-21 09:17:41.379107	9999-12-31 23:59:59.999999
114	https://www.homesweethomegroup.com/	NEW	2023-03-21 09:17:42.377137	9999-12-31 23:59:59.999999
115	https://www.parkcityluxuryrealestate.com/	NEW	2023-03-21 09:17:43.368609	9999-12-31 23:59:59.999999
116	https://www.robenrealestate.com/	NEW	2023-03-21 09:17:44.489373	9999-12-31 23:59:59.999999
117	https://www.tylerhousehunters.com/	NEW	2023-03-21 09:17:45.64369	9999-12-31 23:59:59.999999
118	https://www.longitudebcs.com/	NEW	2023-03-21 09:17:46.89016	9999-12-31 23:59:59.999999
119	https://www.thehollyritchieteam.com/	NEW	2023-03-21 09:17:47.910036	9999-12-31 23:59:59.999999
120	https://www.fortmcmurrayrealestate.com/	NEW	2023-03-21 09:17:48.889334	9999-12-31 23:59:59.999999
121	https://www.simpsonrealtygrouprva.com/	NEW	2023-03-21 09:17:49.981794	9999-12-31 23:59:59.999999
122	https://www.therivlingroup.com/	NEW	2023-03-21 09:17:53.806605	9999-12-31 23:59:59.999999
123	https://www.leetessier.com/	NEW	2023-03-21 09:17:54.794099	9999-12-31 23:59:59.999999
124	https://www.searchallcharlottenchomes.com/	NEW	2023-03-21 09:17:55.883396	9999-12-31 23:59:59.999999
125	https://www.mogul-realestate.com/	NEW	2023-03-21 09:17:56.918776	9999-12-31 23:59:59.999999
126	https://www.everydoorrealestate.com/	NEW	2023-03-21 09:17:57.946239	9999-12-31 23:59:59.999999
127	https://www.daubyrealestate.com/	NEW	2023-03-21 09:17:58.974545	9999-12-31 23:59:59.999999
128	https://www.abanksrealestate.com/	NEW	2023-03-21 09:17:59.99217	9999-12-31 23:59:59.999999
129	https://www.goldcountrymodern.com/	NEW	2023-03-21 09:18:00.936068	9999-12-31 23:59:59.999999
130	https://www.resmarion.com/	NEW	2023-03-21 09:18:01.860954	9999-12-31 23:59:59.999999
131	https://www.tailoredreg.com/	NEW	2023-03-21 09:18:02.88664	9999-12-31 23:59:59.999999
132	https://www.exitjusticerealty.com/	NEW	2023-03-21 09:18:06.279364	9999-12-31 23:59:59.999999
133	https://www.fivemarkrealtygroupllc.com/	NEW	2023-03-21 09:18:07.450587	9999-12-31 23:59:59.999999
134	https://www.nlhomefinder.ca/	NEW	2023-03-21 09:18:08.660444	9999-12-31 23:59:59.999999
135	https://www.oneteamct.com/	NEW	2023-03-21 09:18:09.809175	9999-12-31 23:59:59.999999
136	https://www.atlaspremierrealty.com/	NEW	2023-03-21 09:18:11.159307	9999-12-31 23:59:59.999999
137	https://www.cincinkyrealestate.com/	NEW	2023-03-21 09:18:12.027404	9999-12-31 23:59:59.999999
138	https://www.findedmontonhomes.ca/	NEW	2023-03-21 09:18:13.1369	9999-12-31 23:59:59.999999
139	https://www.welcomehomepa.com/	NEW	2023-03-21 09:18:14.312949	9999-12-31 23:59:59.999999
140	https://www.kennarealestate.com/	NEW	2023-03-21 09:18:15.381233	9999-12-31 23:59:59.999999
141	https://www.yegismoving.com/	NEW	2023-03-21 09:18:16.617232	9999-12-31 23:59:59.999999
\.


--
-- Name: clients_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clients_id_seq', 1, true);


--
-- Name: email_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.email_site_id_seq', 1, false);


--
-- Name: emails_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.emails_id_seq', 1, false);


--
-- Name: phone_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.phone_site_id_seq', 1, false);


--
-- Name: phones_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.phones_id_seq', 1, false);


--
-- Name: sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sites_id_seq', 141, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: clients clients_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_email_key UNIQUE (email);


--
-- Name: clients clients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_pkey PRIMARY KEY (id);


--
-- Name: clients clients_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clients
    ADD CONSTRAINT clients_username_key UNIQUE (username);


--
-- Name: email_site email_site_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.email_site
    ADD CONSTRAINT email_site_pkey PRIMARY KEY (id);


--
-- Name: emails emails_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emails
    ADD CONSTRAINT emails_email_key UNIQUE (email);


--
-- Name: emails emails_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emails
    ADD CONSTRAINT emails_pkey PRIMARY KEY (id);


--
-- Name: phone_site phone_site_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phone_site
    ADD CONSTRAINT phone_site_pkey PRIMARY KEY (id);


--
-- Name: phones phones_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phones
    ADD CONSTRAINT phones_number_key UNIQUE (number);


--
-- Name: phones phones_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phones
    ADD CONSTRAINT phones_pkey PRIMARY KEY (id);


--
-- Name: sites sites_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sites
    ADD CONSTRAINT sites_pkey PRIMARY KEY (id);


--
-- Name: sites sites_url_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sites
    ADD CONSTRAINT sites_url_key UNIQUE (url);


--
-- Name: email_site email_site_email_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.email_site
    ADD CONSTRAINT email_site_email_id_fkey FOREIGN KEY (email_id) REFERENCES public.emails(id);


--
-- Name: email_site email_site_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.email_site
    ADD CONSTRAINT email_site_site_id_fkey FOREIGN KEY (site_id) REFERENCES public.sites(id);


--
-- Name: phone_site phone_site_phone_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phone_site
    ADD CONSTRAINT phone_site_phone_id_fkey FOREIGN KEY (phone_id) REFERENCES public.phones(id);


--
-- Name: phone_site phone_site_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.phone_site
    ADD CONSTRAINT phone_site_site_id_fkey FOREIGN KEY (site_id) REFERENCES public.sites(id);


--
-- PostgreSQL database dump complete
--

