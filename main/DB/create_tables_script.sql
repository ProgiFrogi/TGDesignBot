--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET default_tablespace = '';

SET default_with_oids = false;

---
--- drop tables
---
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Fonts;
DROP TABLE IF EXISTS Templates;
DROP TABLE IF EXISTS Images;
DROP TABLE IF EXISTS Slides;

--
-- Name: Users; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE Users (
    user_id BIGINT PRIMARY KEY,
    role VARCHAR(10) CHECK (role IN ('user', 'admin'))
);

--
-- Name: Templates; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE Templates (
	template_id SERIAL PRIMARY KEY,
	link text not null,
	path text not null,
	name text not null
);
--
-- Name: Fonts; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE Fonts (
	font_id SERIAL PRIMARY KEY,
	link text not null,
	business_unit text not null,
	template_id int,
	FOREIGN KEY (template_id) REFERENCES Templates(template_id) ON DELETE CASCADE
);

--
-- Name: Slides; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE Slides (
	slide_id int PRIMARY KEY,
	template_id int,
	FOREIGN KEY (template_id) REFERENCES Templates(template_id) ON DELETE CASCADE,
	"link" text not null,
	business_unit text not null,
	tags text
);
--
-- Name: Images; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE Images (
	image_id int PRIMARY KEY,
	template_id int,
	FOREIGN KEY (template_id) REFERENCES Templates(template_id) ON DELETE CASCADE,
	business_unit text not null,
	"link" text not null
);
--
-- Data for Name: Users; Type: TABLE DATA; Schema: public; Owner: -
--
INSERT INTO Users VALUES (2114778573, 'admin');
INSERT INTO Users VALUES (5592902615, 'admin');
INSERT INTO Users VALUES (928962436, 'admin');