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
-- Name: scheduler_jobs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.scheduler_jobs (
    id character varying(191) NOT NULL,
    next_run_time double precision,
    job_state bytea NOT NULL
);


ALTER TABLE public.scheduler_jobs OWNER TO postgres;

--
-- Name: all_jobs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.all_jobs ALTER COLUMN id SET DEFAULT nextval('public.all_jobs_id_seq'::regclass);


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
\.


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
\.


--
-- Data for Name: scheduler_jobs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.scheduler_jobs (id, next_run_time, job_state) FROM stdin;
\.


--
-- Name: all_jobs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.all_jobs_id_seq', 25, true);


--
-- Name: all_jobs all_jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.all_jobs
    ADD CONSTRAINT all_jobs_pkey PRIMARY KEY (id);


--
-- Name: scheduler_jobs scheduler_jobs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.scheduler_jobs
    ADD CONSTRAINT scheduler_jobs_pkey PRIMARY KEY (id);


--
-- Name: ix_scheduler_jobs_next_run_time; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_scheduler_jobs_next_run_time ON public.scheduler_jobs USING btree (next_run_time);


--
-- PostgreSQL database dump complete
--

