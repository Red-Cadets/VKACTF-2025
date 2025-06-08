






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

SET default_tablespace = '';

SET default_table_access_method = heap;





CREATE TABLE public."Model" (
    id integer NOT NULL,
    name text NOT NULL,
    combat boolean DEFAULT false NOT NULL
);


ALTER TABLE public."Model" OWNER TO postgres;





CREATE SEQUENCE public."Model_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Model_id_seq" OWNER TO postgres;





ALTER SEQUENCE public."Model_id_seq" OWNED BY public."Model".id;






CREATE TABLE public."Order" (
    id integer NOT NULL,
    message text NOT NULL,
    "modelId" integer DEFAULT 1 NOT NULL
);


ALTER TABLE public."Order" OWNER TO postgres;





CREATE SEQUENCE public."Order_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Order_id_seq" OWNER TO postgres;





ALTER SEQUENCE public."Order_id_seq" OWNED BY public."Order".id;






CREATE TABLE public."Robot" (
    id integer NOT NULL,
    name text NOT NULL,
    password text NOT NULL,
    bio text,
    "modelId" integer DEFAULT 1 NOT NULL
);


ALTER TABLE public."Robot" OWNER TO postgres;





CREATE SEQUENCE public."Robot_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Robot_id_seq" OWNER TO postgres;





ALTER SEQUENCE public."Robot_id_seq" OWNED BY public."Robot".id;






CREATE TABLE public."User" (
    id integer NOT NULL,
    login text NOT NULL,
    password text NOT NULL
);


ALTER TABLE public."User" OWNER TO postgres;





CREATE SEQUENCE public."User_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."User_id_seq" OWNER TO postgres;





ALTER SEQUENCE public."User_id_seq" OWNED BY public."User".id;






CREATE TABLE public._prisma_migrations (
    id character varying(36) NOT NULL,
    checksum character varying(64) NOT NULL,
    finished_at timestamp with time zone,
    migration_name character varying(255) NOT NULL,
    logs text,
    rolled_back_at timestamp with time zone,
    started_at timestamp with time zone DEFAULT now() NOT NULL,
    applied_steps_count integer DEFAULT 0 NOT NULL
);


ALTER TABLE public._prisma_migrations OWNER TO postgres;





ALTER TABLE ONLY public."Model" ALTER COLUMN id SET DEFAULT nextval('public."Model_id_seq"'::regclass);






ALTER TABLE ONLY public."Order" ALTER COLUMN id SET DEFAULT nextval('public."Order_id_seq"'::regclass);






ALTER TABLE ONLY public."Robot" ALTER COLUMN id SET DEFAULT nextval('public."Robot_id_seq"'::regclass);






ALTER TABLE ONLY public."User" ALTER COLUMN id SET DEFAULT nextval('public."User_id_seq"'::regclass);








COPY public._prisma_migrations (id, checksum, finished_at, migration_name, logs, rolled_back_at, started_at, applied_steps_count) FROM stdin;
592d3b22-a907-472f-a9da-083552b9ff01    2b67c61af4febd78c24417ba6cba7eeba6b35d614e51ace65cb287ca920faea7        2025-04-06 14:56:09.299574+00   20250405130958_init   \N      \N      2025-04-06 14:56:09.291588+00   1
\.






SELECT pg_catalog.setval('public."Model_id_seq"', 1, true);






SELECT pg_catalog.setval('public."Order_id_seq"', 1, true);






SELECT pg_catalog.setval('public."Robot_id_seq"', 1, false);






SELECT pg_catalog.setval('public."User_id_seq"', 1, true);






ALTER TABLE ONLY public."Model"
    ADD CONSTRAINT "Model_pkey" PRIMARY KEY (id);






ALTER TABLE ONLY public."Order"
    ADD CONSTRAINT "Order_pkey" PRIMARY KEY (id);






ALTER TABLE ONLY public."Robot"
    ADD CONSTRAINT "Robot_pkey" PRIMARY KEY (id);






ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (id);






ALTER TABLE ONLY public._prisma_migrations
    ADD CONSTRAINT _prisma_migrations_pkey PRIMARY KEY (id);






CREATE UNIQUE INDEX "Model_name_key" ON public."Model" USING btree (name);






CREATE UNIQUE INDEX "Robot_name_key" ON public."Robot" USING btree (name);






CREATE UNIQUE INDEX "User_login_key" ON public."User" USING btree (login);






ALTER TABLE ONLY public."Order"
    ADD CONSTRAINT "Order_modelId_fkey" FOREIGN KEY ("modelId") REFERENCES public."Model"(id) ON UPDATE CASCADE ON DELETE RESTRICT;






ALTER TABLE ONLY public."Robot"
    ADD CONSTRAINT "Robot_modelId_fkey" FOREIGN KEY ("modelId") REFERENCES public."Model"(id) ON UPDATE CASCADE ON DELETE RESTRICT;
