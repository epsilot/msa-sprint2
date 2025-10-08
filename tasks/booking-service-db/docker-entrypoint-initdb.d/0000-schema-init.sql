--
-- PostgreSQL database dump
--

\restrict nljzcal91QRIehXMuBhi5lzUa6fxVGmeavEtHEvvpfLHfDfe7MuWaOgzZNuMmtQ

-- Dumped from database version 15.14 (Debian 15.14-1.pgdg13+1)
-- Dumped by pg_dump version 15.14 (Homebrew)

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
-- Name: booking; Type: TABLE; Schema: public; Owner: hotelio
--

CREATE TABLE public.booking (
                                discount_percent double precision,
                                price double precision NOT NULL,
                                created_at timestamp(6) with time zone,
                                id bigint NOT NULL,
                                hotel_id character varying(255),
                                promo_code character varying(255),
                                user_id character varying(255)
);


ALTER TABLE public.booking OWNER TO hotelio;

--
-- Name: booking_id_seq; Type: SEQUENCE; Schema: public; Owner: hotelio
--

CREATE SEQUENCE public.booking_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.booking_id_seq OWNER TO hotelio;

--
-- Name: booking_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hotelio
--

ALTER SEQUENCE public.booking_id_seq OWNED BY public.booking.id;


--
-- Name: booking id; Type: DEFAULT; Schema: public; Owner: hotelio
--

ALTER TABLE ONLY public.booking ALTER COLUMN id SET DEFAULT nextval('public.booking_id_seq'::regclass);


--
-- Name: booking booking_pkey; Type: CONSTRAINT; Schema: public; Owner: hotelio
--

ALTER TABLE ONLY public.booking
    ADD CONSTRAINT booking_pkey PRIMARY KEY (id);

--
-- PostgreSQL database dump complete
--

\unrestrict nljzcal91QRIehXMuBhi5lzUa6fxVGmeavEtHEvvpfLHfDfe7MuWaOgzZNuMmtQ





