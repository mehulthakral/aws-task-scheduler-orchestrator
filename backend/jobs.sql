--
-- PostgreSQL database dump
--

-- Dumped from database version 13.1
-- Dumped by pg_dump version 13.1

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: apscheduler_jobs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.apscheduler_jobs (
    url character varying(100),
    run_time timestamp with time zone,
    status character varying(20),
    lambda_name character varying(100),
    lambda_description character varying(500),
    id bigint NOT NULL,
    execution_time numeric(10,2),
    username character varying(50),
    scheduling_type character varying(10)
);


ALTER TABLE public.apscheduler_jobs OWNER TO postgres;

--
-- Name: apscheduler_jobs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.apscheduler_jobs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.apscheduler_jobs_id_seq OWNER TO postgres;

--
-- Name: apscheduler_jobs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.apscheduler_jobs_id_seq OWNED BY public.apscheduler_jobs.id;


--
-- Name: credentials; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.credentials (
    username character varying(100) NOT NULL,
    password character(64) NOT NULL
);


ALTER TABLE public.credentials OWNER TO postgres;

--
-- Name: function_data; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.function_data (
    id integer,
    code character varying(1000),
    requirements character varying(500)
);


ALTER TABLE public.function_data OWNER TO postgres;

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
-- Name: apscheduler_jobs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.apscheduler_jobs ALTER COLUMN id SET DEFAULT nextval('public.apscheduler_jobs_id_seq'::regclass);


--
-- Name: task_set id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_set ALTER COLUMN id SET DEFAULT nextval('public.task_set_id_seq'::regclass);


--
-- Data for Name: apscheduler_jobs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.apscheduler_jobs (url, run_time, status, lambda_name, lambda_description, id, execution_time, username, scheduling_type) FROM stdin;
https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-04-04 00:32:04.603857+05:30	Completed	Lambda Function	Sample Description	8	1401.33	user01	url
https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-04-04 01:09:06.329673+05:30	Cancelled	Lambda Function	Sample Description	9	0.00	user01	url
https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-04-04 01:25:14.207998+05:30	Failed	Lambda Function	Sample Description	10	1416.61	user01	url
https://iiiy1ms67f.execute-api.us-east-1.amazonaws.com/v1?num=1	2021-04-04 01:47:12.004753+05:30	Failed	Lambda Function	Sample Description	11	1440.14	user01	url
\.


--
-- Data for Name: credentials; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.credentials (username, password) FROM stdin;
user	a1159e9df3670d549d04524532629f5477ceb7deec9b45e47e8c009506ecb2c8
user01	5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
\.


--
-- Data for Name: function_data; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.function_data (id, code, requirements) FROM stdin;
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
-- Name: apscheduler_jobs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.apscheduler_jobs_id_seq', 11, true);


--
-- Name: task_set_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.task_set_id_seq', 16, true);


--
-- Name: credentials credentials_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.credentials
    ADD CONSTRAINT credentials_pkey PRIMARY KEY (username);


--
-- Name: scheduler_jobs scheduler_jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scheduler_jobs
    ADD CONSTRAINT scheduler_jobs_pkey PRIMARY KEY (id);


--
-- Name: task_set task_set_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.task_set
    ADD CONSTRAINT task_set_pkey PRIMARY KEY (id);


--
-- Name: ix_scheduler_jobs_next_run_time; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_scheduler_jobs_next_run_time ON public.scheduler_jobs USING btree (next_run_time);


--
-- PostgreSQL database dump complete
--

