--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.24
-- Dumped by pg_dump version 9.5.24

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: all_jobs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.all_jobs (
    id bigint NOT NULL,
    url character varying(100),
    run_time timestamp with time zone,
    status character varying(20),
    lambda_name character varying(100),
    lambda_description character varying(500)
);


ALTER TABLE public.all_jobs OWNER TO postgres;

--
-- Name: all_jobs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.all_jobs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.all_jobs_id_seq OWNER TO postgres;

--
-- Name: all_jobs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.all_jobs_id_seq OWNED BY public.all_jobs.id;


--
-- Name: apscheduler_jobs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.apscheduler_jobs (
    id bigint,
    url character varying(100),
    run_time timestamp with time zone,
    status character varying(20),
    lambda_name character varying(100),
    lambda_description character varying(500)
);


ALTER TABLE public.apscheduler_jobs OWNER TO postgres;

--
-- Name: credentials; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.credentials (
    username character varying(100) NOT NULL,
    password character(64) NOT NULL
);


ALTER TABLE public.credentials OWNER TO postgres;

--
-- Name: orchestrator_tasks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.orchestrator_tasks (
    id bigint NOT NULL,
    num integer NOT NULL,
    url character varying(100) NOT NULL,
    condition_check_url character varying(100),
    condition_check_delay integer,
    condition_check_retries integer,
    delay_between_retries integer,
    fallback_url character varying(100)
);


ALTER TABLE public.orchestrator_tasks OWNER TO postgres;

--
-- Name: scheduler_jobs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.scheduler_jobs (
    id character varying(191) NOT NULL,
    next_run_time double precision,
    job_state bytea NOT NULL
);


ALTER TABLE public.scheduler_jobs OWNER TO postgres;

--
-- Name: task_set; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.task_set (
    id bigint NOT NULL,
    status character varying(20) NOT NULL,
    username character varying(100) NOT NULL,
    initial_delay integer
);


ALTER TABLE public.task_set OWNER TO postgres;

--
-- Name: task_set_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.task_set_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.task_set_id_seq OWNER TO postgres;

--
-- Name: task_set_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.task_set_id_seq OWNED BY public.task_set.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.all_jobs ALTER COLUMN id SET DEFAULT nextval('public.all_jobs_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_set ALTER COLUMN id SET DEFAULT nextval('public.task_set_id_seq'::regclass);


--
-- Data for Name: all_jobs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.all_jobs (id, url, run_time, status, lambda_name, lambda_description) FROM stdin;
1	www.crio.do	2021-03-13 12:36:43.008351+05:30	Added	\N	\N
2	www.crio.do	2021-03-13 12:38:38.501876+05:30	Added	\N	\N
3	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 12:40:01.750793+05:30	Added	\N	\N
4	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 12:41:41.201526+05:30	Added	\N	\N
5	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 12:51:30.114407+05:30	Added	\N	\N
6	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 12:51:51.513751+05:30	Added	\N	\N
7	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 13:03:39.763184+05:30	Added	\N	\N
8	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 13:07:38.565335+05:30	Added	\N	\N
9	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 13:09:08.766372+05:30	Added	\N	\N
10	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 13:09:54.503239+05:30	Added	\N	\N
11	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 13:13:33.549616+05:30	Added	\N	\N
12	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	2021-03-13 13:27:02.587168+05:30	Added	\N	\N
13	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	2021-03-13 14:59:33.147154+05:30	Added	\N	\N
14	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	2021-03-13 15:00:33.366349+05:30	Added	\N	\N
15	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 15:00:53.095325+05:30	Added	\N	\N
16	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-16 18:59:33.913711+05:30	Added	\N	\N
17	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-22 21:40:30.536902+05:30	Added	\N	\N
18	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 07:08:38+05:30	Added	\N	\N
19	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-22 22:58:00+05:30	Added	\N	\N
20	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-22 23:05:00+05:30	Added	\N	\N
21	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	2021-03-25 12:34:27.551657+05:30	Added	\N	\N
22	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	2021-03-25 12:38:04.622956+05:30	Added	\N	\N
23	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	2021-03-25 12:39:53.836711+05:30	Added	\N	\N
24	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	2021-03-25 13:20:36.767547+05:30	Added	Lambda Function	Sample Description
25	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	2021-03-25 13:25:24.848206+05:30	Added	Lambda Function	Sample Description
26	https://dhzactc0r5.execute-api.us-east-1.amazonaws.com/dev/we/are/done	2021-03-27 01:31:17.702737+05:30	Added	65IT01R	
27	https://dhzactc0r5.execute-api.us-east-1.amazonaws.com/dev/we/are/done	2021-03-27 01:42:14.152319+05:30	Added	O9LL6SK	
28	https://dhzactc0r5.execute-api.us-east-1.amazonaws.com/dev/we/are/done	2021-03-27 01:50:13.91689+05:30	Added	M8BI9E4	
29	https://dhzactc0r5.execute-api.us-east-1.amazonaws.com/dev/we/are/done	2021-03-27 14:42:21.208097+05:30	Added	D60B31C	
30	https://dhzactc0r5.execute-api.us-east-1.amazonaws.com/dev/we/are/done	2021-03-27 14:45:22.329159+05:30	Added	WMHOB0B	
31	https://dhzactc0r5.execute-api.us-east-1.amazonaws.com/dev/we/are/done	2021-03-27 14:49:30.868172+05:30	Added	OSD8E0V	
\.


--
-- Name: all_jobs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.all_jobs_id_seq', 31, true);


--
-- Data for Name: apscheduler_jobs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.apscheduler_jobs (id, url, run_time, status, lambda_name, lambda_description) FROM stdin;
69	www.crio.do	2021-03-13 12:38:38.501876+05:30	Scheduled	\N	\N
3	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 12:40:01.750793+05:30	Scheduled	\N	\N
4	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 12:41:41.201526+05:30	Scheduled	\N	\N
5	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 12:51:30.114407+05:30	Scheduled	\N	\N
6	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 12:51:51.513751+05:30	Scheduled	\N	\N
7	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 13:03:39.763184+05:30	Scheduled	\N	\N
8	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 13:07:38.565335+05:30	Scheduled	\N	\N
9	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 13:09:08.766372+05:30	Scheduled	\N	\N
10	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 13:09:54.503239+05:30	Cancelled	\N	\N
11	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 13:13:33.549616+05:30	Completed	\N	\N
12	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	2021-03-13 13:27:02.587168+05:30	Failed	\N	\N
13	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	2021-03-13 14:59:33.147154+05:30	Cancelled	\N	\N
14	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	2021-03-13 15:00:33.366349+05:30	Failed	\N	\N
15	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 15:00:53.095325+05:30	Completed	\N	\N
16	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-16 18:59:33.913711+05:30	Completed	\N	\N
17	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-22 21:40:30.536902+05:30	Completed	\N	\N
18	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-13 07:08:38+05:30	Scheduled	\N	\N
19	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-22 22:58:00+05:30	Completed	\N	\N
23	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	2021-03-25 12:39:53.836711+05:30	Failed	\N	\N
20	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-03-22 23:05:00+05:30	Completed	\N	\N
21	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	2021-03-25 12:34:27.551657+05:30	Failed	\N	\N
25	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	2021-03-25 13:25:24.848206+05:30	Failed	Lambda Function	Sample Description
22	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	2021-03-25 12:38:04.622956+05:30	Failed	\N	\N
26	https://dhzactc0r5.execute-api.us-east-1.amazonaws.com/dev/we/are/done	2021-03-27 01:31:17.702737+05:30	Running	65IT01R	
27	https://dhzactc0r5.execute-api.us-east-1.amazonaws.com/dev/we/are/done	2021-03-27 01:42:14.152319+05:30	Running	O9LL6SK	
28	https://dhzactc0r5.execute-api.us-east-1.amazonaws.com/dev/we/are/done	2021-03-27 01:50:13.91689+05:30	Completed	M8BI9E4	
29	https://dhzactc0r5.execute-api.us-east-1.amazonaws.com/dev/we/are/done	2021-03-27 14:42:21.208097+05:30	Completed	D60B31C	
30	https://dhzactc0r5.execute-api.us-east-1.amazonaws.com/dev/we/are/done	2021-03-27 14:45:22.329159+05:30	Completed	WMHOB0B	
31	https://dhzactc0r5.execute-api.us-east-1.amazonaws.com/dev/we/are/done	2021-03-27 14:49:30.868172+05:30	Completed	OSD8E0V	
\.


--
-- Data for Name: credentials; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.credentials (username, password) FROM stdin;
user	a1159e9df3670d549d04524532629f5477ceb7deec9b45e47e8c009506ecb2c8
\.


--
-- Data for Name: orchestrator_tasks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.orchestrator_tasks (id, num, url, condition_check_url, condition_check_delay, condition_check_retries, delay_between_retries, fallback_url) FROM stdin;
4	1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	0	0	0	
4	2	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	0	0	0	
5	1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	0	0	0	
5	2	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	0	0	0	
6	1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	5000	0	0	
6	2	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	5000	0	0	
7	1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	5000	0	0	
7	2	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	5000	0	0	
8	1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	5000	2	5000	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1
8	2	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	5000	0	0	
9	1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	5000	2	5000	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1
9	2	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	5000	0	0	
10	1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	5000	2	5000	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1
10	2	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	5000	2	5000	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1
11	1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	5000	2	5000	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1
11	2	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	5000	2	5000	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1
12	1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	5000	2	5000	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1
12	2	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	5000	2	5000	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1
13	1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	5000	2	5000	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1
13	2	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	5000	2	5000	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1
14	1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	5000	2	5000	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1
14	2	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	5000	2	5000	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1
15	1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	5000	2	5000	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1
15	2	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	5000	2	5000	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1
16	1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	5000	2	5000	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1
16	2	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=0	5000	2	5000	https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1
\.


--
-- Data for Name: scheduler_jobs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.scheduler_jobs (id, next_run_time, job_state) FROM stdin;
\.


--
-- Data for Name: task_set; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.task_set (id, status, username, initial_delay) FROM stdin;
1	Scheduled	user	\N
2	Scheduled	user	\N
3	Scheduled	user	\N
4	Running	user	\N
5	Running	user	\N
6	Running	user	\N
7	Completed	user	\N
8	Running	user	\N
9	Failed	user	\N
10	Failed	user	\N
11	Completed	user	\N
12	Failed	user	5000
13	Scheduled	user	20000
14	Cancelled	user	20000
15	Failed	user	20000
16	Failed	user	20000
\.


--
-- Name: task_set_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_set_id_seq', 16, true);


--
-- Name: all_jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.all_jobs
    ADD CONSTRAINT all_jobs_pkey PRIMARY KEY (id);


--
-- Name: credentials_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.credentials
    ADD CONSTRAINT credentials_pkey PRIMARY KEY (username);


--
-- Name: scheduler_jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scheduler_jobs
    ADD CONSTRAINT scheduler_jobs_pkey PRIMARY KEY (id);


--
-- Name: task_set_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_set
    ADD CONSTRAINT task_set_pkey PRIMARY KEY (id);


--
-- Name: ix_scheduler_jobs_next_run_time; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_scheduler_jobs_next_run_time ON public.scheduler_jobs USING btree (next_run_time);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

