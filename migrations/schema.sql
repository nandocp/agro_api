--
-- PostgreSQL database dump
--

\restrict hSNAtvTbNcVEStVPjw1IlEiBTUEhdTxbszWudWO5NrNXyd8DCtvnA75s4XLqnb9

-- Dumped from database version 18.3
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
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: accounts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.accounts (
    address_id uuid,
    name character varying(128) NOT NULL,
    document character varying(32) NOT NULL,
    plan character varying(32) NOT NULL,
    archived_at timestamp with time zone,
    id uuid DEFAULT uuidv7() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: activities; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.activities (
    activity_type character varying(50) NOT NULL,
    field_id uuid NOT NULL,
    creator_id uuid NOT NULL,
    kind character varying(50) NOT NULL,
    started_at date NOT NULL,
    finished_at date,
    total_area_m2 numeric(12,2),
    status character varying(64) NOT NULL,
    id uuid DEFAULT uuidv7() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT activities_check CHECK (((finished_at IS NULL) OR (finished_at >= started_at))),
    CONSTRAINT ck_activity_area_positive CHECK (((total_area_m2 IS NULL) OR (total_area_m2 > (0)::numeric)))
);


--
-- Name: addresses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.addresses (
    street character varying(200),
    number character varying(20),
    complement character varying(100),
    neighborhood character varying(100),
    city character varying(100) NOT NULL,
    state character varying(8) NOT NULL,
    country character varying(2) NOT NULL,
    postal_code character varying(10),
    reference character varying(300),
    id uuid DEFAULT uuidv7() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


--
-- Name: estate_registries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.estate_registries (
    estate_id uuid NOT NULL,
    code character varying(100) NOT NULL,
    source character varying(128) NOT NULL,
    submitted_at date,
    issued_at date,
    expires_at date,
    notes character varying(500),
    status character varying(32) NOT NULL,
    id uuid DEFAULT uuidv7() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_registry_code_not_empty CHECK ((length(TRIM(BOTH FROM code)) > 0))
);


--
-- Name: estates; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.estates (
    account_id uuid NOT NULL,
    address_id uuid,
    opened_at date,
    archived_at date,
    label character varying(96) NOT NULL,
    slug character varying(64) NOT NULL,
    description character varying(200),
    timezone character varying(64) NOT NULL,
    zone character varying(16) NOT NULL,
    usage character varying(50),
    status character varying(50) NOT NULL,
    ownership_type character varying(50) NOT NULL,
    declared_area_m2 numeric(14,2),
    entrance_point public.geometry(Point,4326),
    boundary public.geometry(MultiPolygon,4326),
    boundary_source character varying(32),
    perimeter_m numeric(14,2) GENERATED ALWAYS AS (
CASE
    WHEN (boundary IS NOT NULL) THEN public.st_perimeter((boundary)::public.geography)
    ELSE NULL::double precision
END) STORED,
    calculated_area_m2 numeric(14,2) GENERATED ALWAYS AS (
CASE
    WHEN (boundary IS NOT NULL) THEN public.st_area((boundary)::public.geography)
    ELSE NULL::double precision
END) STORED,
    id uuid DEFAULT uuidv7() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_estate_positive_declared_area CHECK (((declared_area_m2 IS NULL) OR (declared_area_m2 > (0)::numeric)))
);


--
-- Name: field_protections; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.field_protections (
    field_id uuid NOT NULL,
    created_by_id uuid NOT NULL,
    kind character varying(32) NOT NULL,
    reason character varying(256),
    expires_at date,
    started_at date DEFAULT CURRENT_DATE NOT NULL,
    id uuid DEFAULT uuidv7() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_field_protection_expiry CHECK (((expires_at IS NULL) OR (expires_at > started_at)))
);


--
-- Name: field_soil_analyses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.field_soil_analyses (
    field_id uuid NOT NULL,
    collected_at date NOT NULL,
    analyzed_at date,
    sampling_depth_cm integer NOT NULL,
    ph_h2o numeric(3,1),
    base_saturation_percent numeric(5,2),
    organic_matter_g_dm3 numeric(5,2),
    texture_class character varying(50),
    chemical jsonb,
    physical jsonb,
    biological jsonb,
    collector_name character varying(255) NOT NULL,
    collector_registry character varying(64) NOT NULL,
    laboratory_name character varying(255) NOT NULL,
    laboratory_protocol character varying(128),
    id uuid DEFAULT uuidv7() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_analysis_date_after_collection CHECK (((analyzed_at IS NULL) OR (analyzed_at >= collected_at))),
    CONSTRAINT ck_dsampling_epth_positive CHECK ((sampling_depth_cm > 0)),
    CONSTRAINT ck_ph_h2o_range CHECK (((ph_h2o IS NULL) OR ((ph_h2o >= (0)::numeric) AND (ph_h2o <= (14)::numeric))))
);


--
-- Name: field_soil_classifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.field_soil_classifications (
    field_id uuid NOT NULL,
    soil_classification_id uuid NOT NULL
);


--
-- Name: field_transitions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.field_transitions (
    predecessor_id uuid NOT NULL,
    successor_id uuid NOT NULL,
    kind character varying(64) NOT NULL,
    transitioned_at date DEFAULT CURRENT_DATE NOT NULL,
    transitioned_by_id uuid NOT NULL,
    reason character varying(500),
    id uuid DEFAULT uuidv7() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_field_transition_no_self_reference CHECK ((predecessor_id <> successor_id))
);


--
-- Name: fields; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.fields (
    estate_id uuid NOT NULL,
    creator_id uuid NOT NULL,
    slug character varying(64) NOT NULL,
    label character varying(96) NOT NULL,
    notes character varying(500),
    boundary public.geometry(Polygon,4326),
    boundary_source character varying(32),
    calculated_area_m2 numeric(12,2) GENERATED ALWAYS AS (public.st_area((boundary)::public.geography)) STORED,
    perimeter_m numeric(12,2) GENERATED ALWAYS AS (public.st_perimeter((boundary)::public.geography)) STORED,
    active_from date DEFAULT CURRENT_DATE NOT NULL,
    active_to date,
    id uuid DEFAULT uuidv7() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    slope_percent numeric(5,2),
    slope_class character varying(50)
);


--
-- Name: journal_entries; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.journal_entries (
    entity_type character varying(50) NOT NULL,
    entity_id uuid NOT NULL,
    author_id uuid NOT NULL,
    logged_at timestamp with time zone NOT NULL,
    title character varying(200),
    content text NOT NULL,
    is_pinned boolean NOT NULL,
    id uuid DEFAULT uuidv7() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL,
    CONSTRAINT ck_journal_entry_content_not_empty CHECK ((length(TRIM(BOTH FROM content)) > 0))
);


--
-- Name: organism_common_names; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.organism_common_names (
    organism_id uuid NOT NULL,
    name character varying(100) NOT NULL,
    region character varying(64),
    language character varying(10) NOT NULL,
    is_preferred boolean NOT NULL,
    id uuid DEFAULT uuidv7() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: organism_synonyms; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.organism_synonyms (
    organism_id uuid NOT NULL,
    scientific_name character varying(200) NOT NULL,
    taxonomy jsonb,
    authorship character varying(200),
    id uuid DEFAULT uuidv7() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: organism_traits; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.organism_traits (
    name character varying(100) NOT NULL,
    category character varying(50) NOT NULL,
    id uuid DEFAULT uuidv7() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: organisms; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.organisms (
    organism_type character varying(50) NOT NULL,
    taxonomy jsonb,
    scientific_name character varying(200) NOT NULL,
    authorship character varying(200),
    external_ids jsonb,
    id uuid DEFAULT uuidv7() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.permissions (
    resource character varying(50) NOT NULL,
    action character varying(50) NOT NULL,
    id uuid DEFAULT uuidv7() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: plants; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.plants (
    id uuid NOT NULL,
    plant_cycle character varying(50),
    growth_habit character varying(50),
    max_height_cm integer,
    min_temperature_c numeric(3,1),
    max_temperature_c numeric(3,1),
    water_requirement character varying(50),
    drought_tolerance character varying(32),
    days_to_germination integer,
    days_to_maturity integer,
    frost_tolerance character varying(32),
    flood_tolerance character varying(32),
    soil_ph_min numeric(3,1),
    soil_ph_max numeric(3,1),
    recommended_altitude_min_m numeric(5,2),
    recommended_altitude_max_m numeric(5,2),
    nitrogen_fixing boolean NOT NULL,
    allelopathic boolean NOT NULL,
    CONSTRAINT ck_plant_altitude_order CHECK (((recommended_altitude_min_m IS NULL) OR (recommended_altitude_max_m IS NULL) OR (recommended_altitude_max_m >= recommended_altitude_min_m))),
    CONSTRAINT ck_plant_ph_max_range CHECK (((soil_ph_max IS NULL) OR ((soil_ph_max >= (0)::numeric) AND (soil_ph_max <= (14)::numeric)))),
    CONSTRAINT ck_plant_ph_min_range CHECK (((soil_ph_min IS NULL) OR ((soil_ph_min >= (0)::numeric) AND (soil_ph_min <= (14)::numeric)))),
    CONSTRAINT ck_plant_ph_order CHECK (((soil_ph_min IS NULL) OR (soil_ph_max IS NULL) OR (soil_ph_max >= soil_ph_min))),
    CONSTRAINT ck_plant_temperature_order CHECK (((min_temperature_c IS NULL) OR (max_temperature_c IS NULL) OR (max_temperature_c >= min_temperature_c)))
);


--
-- Name: role_permissions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.role_permissions (
    role_id uuid NOT NULL,
    permission_id uuid NOT NULL
);


--
-- Name: roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.roles (
    name character varying(50) NOT NULL,
    description character varying(200),
    id uuid DEFAULT uuidv7() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: soil_classifications; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.soil_classifications (
    name character varying(100) NOT NULL,
    source character varying(50) NOT NULL,
    parent_id uuid,
    id uuid DEFAULT uuidv7() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: user_roles; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.user_roles (
    user_id uuid NOT NULL,
    role_id uuid NOT NULL
);


--
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    account_id uuid NOT NULL,
    name character varying(255) NOT NULL,
    email character varying(254) NOT NULL,
    password character varying(255) NOT NULL,
    is_active boolean NOT NULL,
    deactivated_at timestamp with time zone,
    reset_password_token character varying,
    reset_password_sent_at timestamp without time zone,
    jti uuid,
    current_sign_in_at timestamp with time zone,
    last_sign_in_at timestamp with time zone,
    failed_attempts integer NOT NULL,
    locked_at timestamp with time zone,
    unlock_token uuid,
    id uuid DEFAULT uuidv7() NOT NULL,
    created_at timestamp with time zone DEFAULT now() NOT NULL,
    updated_at timestamp with time zone DEFAULT now() NOT NULL
);


--
-- Name: accounts accounts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_pkey PRIMARY KEY (id);


--
-- Name: activities activities_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_pkey PRIMARY KEY (id);


--
-- Name: addresses addresses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.addresses
    ADD CONSTRAINT addresses_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: estate_registries estate_registries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estate_registries
    ADD CONSTRAINT estate_registries_pkey PRIMARY KEY (id);


--
-- Name: estates estates_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estates
    ADD CONSTRAINT estates_pkey PRIMARY KEY (id);


--
-- Name: field_protections field_protections_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.field_protections
    ADD CONSTRAINT field_protections_pkey PRIMARY KEY (id);


--
-- Name: field_soil_analyses field_soil_analyses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.field_soil_analyses
    ADD CONSTRAINT field_soil_analyses_pkey PRIMARY KEY (id);


--
-- Name: field_soil_classifications field_soil_classifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.field_soil_classifications
    ADD CONSTRAINT field_soil_classifications_pkey PRIMARY KEY (field_id, soil_classification_id);


--
-- Name: field_transitions field_transitions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.field_transitions
    ADD CONSTRAINT field_transitions_pkey PRIMARY KEY (id);


--
-- Name: fields fields_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fields
    ADD CONSTRAINT fields_pkey PRIMARY KEY (id);


--
-- Name: journal_entries journal_entries_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.journal_entries
    ADD CONSTRAINT journal_entries_pkey PRIMARY KEY (id);


--
-- Name: organism_common_names organism_common_names_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organism_common_names
    ADD CONSTRAINT organism_common_names_pkey PRIMARY KEY (id);


--
-- Name: organism_synonyms organism_synonyms_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organism_synonyms
    ADD CONSTRAINT organism_synonyms_pkey PRIMARY KEY (id);


--
-- Name: organism_traits organism_traits_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organism_traits
    ADD CONSTRAINT organism_traits_pkey PRIMARY KEY (id);


--
-- Name: organisms organisms_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organisms
    ADD CONSTRAINT organisms_pkey PRIMARY KEY (id);


--
-- Name: permissions permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT permissions_pkey PRIMARY KEY (id);


--
-- Name: plants plants_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plants
    ADD CONSTRAINT plants_pkey PRIMARY KEY (id);


--
-- Name: role_permissions role_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_pkey PRIMARY KEY (role_id, permission_id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: soil_classifications soil_classifications_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.soil_classifications
    ADD CONSTRAINT soil_classifications_pkey PRIMARY KEY (id);


--
-- Name: accounts uq_account_document; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT uq_account_document UNIQUE (document);


--
-- Name: users uq_account_email; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT uq_account_email UNIQUE (account_id, email);


--
-- Name: estates uq_account_estate_slug; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estates
    ADD CONSTRAINT uq_account_estate_slug UNIQUE (account_id, slug);


--
-- Name: fields uq_estate_field_slug; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fields
    ADD CONSTRAINT uq_estate_field_slug UNIQUE (estate_id, slug);


--
-- Name: estate_registries uq_estate_registry_code; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estate_registries
    ADD CONSTRAINT uq_estate_registry_code UNIQUE (estate_id, source, code);


--
-- Name: field_transitions uq_field_transition; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.field_transitions
    ADD CONSTRAINT uq_field_transition UNIQUE (predecessor_id, successor_id, kind);


--
-- Name: organism_common_names uq_organism_name_lang; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organism_common_names
    ADD CONSTRAINT uq_organism_name_lang UNIQUE (organism_id, name, language);


--
-- Name: organisms uq_organism_scientific_name; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organisms
    ADD CONSTRAINT uq_organism_scientific_name UNIQUE (scientific_name);


--
-- Name: organism_synonyms uq_organism_synonym; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organism_synonyms
    ADD CONSTRAINT uq_organism_synonym UNIQUE (organism_id, scientific_name);


--
-- Name: organism_traits uq_organism_trait_name; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organism_traits
    ADD CONSTRAINT uq_organism_trait_name UNIQUE (name);


--
-- Name: permissions uq_permission_resource_action; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.permissions
    ADD CONSTRAINT uq_permission_resource_action UNIQUE (resource, action);


--
-- Name: roles uq_role_name; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT uq_role_name UNIQUE (name);


--
-- Name: soil_classifications uq_soil_name_source; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.soil_classifications
    ADD CONSTRAINT uq_soil_name_source UNIQUE (name, source);


--
-- Name: user_roles user_roles_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_pkey PRIMARY KEY (user_id, role_id);


--
-- Name: users users_jti_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_jti_key UNIQUE (jti);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_reset_password_token_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_reset_password_token_key UNIQUE (reset_password_token);


--
-- Name: users users_unlock_token_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_unlock_token_key UNIQUE (unlock_token);


--
-- Name: idx_common_name_search; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_common_name_search ON public.organism_common_names USING btree (name);


--
-- Name: ix_activities_field_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activities_field_id ON public.activities USING btree (field_id);


--
-- Name: ix_activities_started_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_activities_started_at ON public.activities USING btree (started_at);


--
-- Name: ix_estate_registries_estate_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_estate_registries_estate_id ON public.estate_registries USING btree (estate_id);


--
-- Name: ix_estate_registry_code; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_estate_registry_code ON public.estate_registries USING btree (code);


--
-- Name: ix_estates_slug; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_estates_slug ON public.estates USING btree (slug);


--
-- Name: ix_field_active_protection; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX ix_field_active_protection ON public.field_protections USING btree (field_id) WHERE (expires_at IS NULL);


--
-- Name: ix_field_soil_analyses_collected_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_field_soil_analyses_collected_at ON public.field_soil_analyses USING btree (collected_at);


--
-- Name: ix_field_soil_analyses_field_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_field_soil_analyses_field_id ON public.field_soil_analyses USING btree (field_id);


--
-- Name: ix_field_transitions_predecessor_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_field_transitions_predecessor_id ON public.field_transitions USING btree (predecessor_id);


--
-- Name: ix_field_transitions_successor_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_field_transitions_successor_id ON public.field_transitions USING btree (successor_id);


--
-- Name: ix_journal_entries_author_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_journal_entries_author_id ON public.journal_entries USING btree (author_id);


--
-- Name: ix_journal_entries_entity_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_journal_entries_entity_id ON public.journal_entries USING btree (entity_id);


--
-- Name: ix_journal_entries_logged_at; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_journal_entries_logged_at ON public.journal_entries USING btree (logged_at);


--
-- Name: ix_journal_entry_entity; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_journal_entry_entity ON public.journal_entries USING btree (entity_type, entity_id);


--
-- Name: ix_organism_synonyms_organism_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_organism_synonyms_organism_id ON public.organism_synonyms USING btree (organism_id);


--
-- Name: ix_organisms_scientific_name; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX ix_organisms_scientific_name ON public.organisms USING btree (scientific_name);


--
-- Name: accounts accounts_address_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.accounts
    ADD CONSTRAINT accounts_address_id_fkey FOREIGN KEY (address_id) REFERENCES public.addresses(id) ON DELETE SET NULL;


--
-- Name: activities activities_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: activities activities_field_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.activities
    ADD CONSTRAINT activities_field_id_fkey FOREIGN KEY (field_id) REFERENCES public.fields(id) ON DELETE CASCADE;


--
-- Name: estate_registries estate_registries_estate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estate_registries
    ADD CONSTRAINT estate_registries_estate_id_fkey FOREIGN KEY (estate_id) REFERENCES public.estates(id) ON DELETE CASCADE;


--
-- Name: estates estates_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estates
    ADD CONSTRAINT estates_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.accounts(id) ON DELETE CASCADE;


--
-- Name: estates estates_address_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.estates
    ADD CONSTRAINT estates_address_id_fkey FOREIGN KEY (address_id) REFERENCES public.addresses(id) ON DELETE SET NULL;


--
-- Name: field_protections field_protections_created_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.field_protections
    ADD CONSTRAINT field_protections_created_by_id_fkey FOREIGN KEY (created_by_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: field_protections field_protections_field_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.field_protections
    ADD CONSTRAINT field_protections_field_id_fkey FOREIGN KEY (field_id) REFERENCES public.fields(id);


--
-- Name: field_soil_analyses field_soil_analyses_field_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.field_soil_analyses
    ADD CONSTRAINT field_soil_analyses_field_id_fkey FOREIGN KEY (field_id) REFERENCES public.fields(id) ON DELETE RESTRICT;


--
-- Name: field_soil_classifications field_soil_classifications_field_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.field_soil_classifications
    ADD CONSTRAINT field_soil_classifications_field_id_fkey FOREIGN KEY (field_id) REFERENCES public.fields(id) ON DELETE CASCADE;


--
-- Name: field_soil_classifications field_soil_classifications_soil_classification_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.field_soil_classifications
    ADD CONSTRAINT field_soil_classifications_soil_classification_id_fkey FOREIGN KEY (soil_classification_id) REFERENCES public.soil_classifications(id) ON DELETE RESTRICT;


--
-- Name: field_transitions field_transitions_predecessor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.field_transitions
    ADD CONSTRAINT field_transitions_predecessor_id_fkey FOREIGN KEY (predecessor_id) REFERENCES public.fields(id) ON DELETE RESTRICT;


--
-- Name: field_transitions field_transitions_successor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.field_transitions
    ADD CONSTRAINT field_transitions_successor_id_fkey FOREIGN KEY (successor_id) REFERENCES public.fields(id) ON DELETE RESTRICT;


--
-- Name: field_transitions field_transitions_transitioned_by_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.field_transitions
    ADD CONSTRAINT field_transitions_transitioned_by_id_fkey FOREIGN KEY (transitioned_by_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- Name: fields fields_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fields
    ADD CONSTRAINT fields_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: fields fields_estate_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.fields
    ADD CONSTRAINT fields_estate_id_fkey FOREIGN KEY (estate_id) REFERENCES public.estates(id) ON DELETE CASCADE;


--
-- Name: journal_entries journal_entries_author_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.journal_entries
    ADD CONSTRAINT journal_entries_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users(id) ON DELETE RESTRICT;


--
-- Name: organism_common_names organism_common_names_organism_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organism_common_names
    ADD CONSTRAINT organism_common_names_organism_id_fkey FOREIGN KEY (organism_id) REFERENCES public.organisms(id);


--
-- Name: organism_synonyms organism_synonyms_organism_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.organism_synonyms
    ADD CONSTRAINT organism_synonyms_organism_id_fkey FOREIGN KEY (organism_id) REFERENCES public.organisms(id) ON DELETE CASCADE;


--
-- Name: plants plants_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.plants
    ADD CONSTRAINT plants_id_fkey FOREIGN KEY (id) REFERENCES public.organisms(id);


--
-- Name: role_permissions role_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permissions(id) ON DELETE CASCADE;


--
-- Name: role_permissions role_permissions_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.role_permissions
    ADD CONSTRAINT role_permissions_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE CASCADE;


--
-- Name: soil_classifications soil_classifications_parent_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.soil_classifications
    ADD CONSTRAINT soil_classifications_parent_id_fkey FOREIGN KEY (parent_id) REFERENCES public.soil_classifications(id) ON DELETE SET NULL;


--
-- Name: user_roles user_roles_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE CASCADE;


--
-- Name: user_roles user_roles_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.user_roles
    ADD CONSTRAINT user_roles_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE CASCADE;


--
-- Name: users users_account_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_account_id_fkey FOREIGN KEY (account_id) REFERENCES public.accounts(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict hSNAtvTbNcVEStVPjw1IlEiBTUEhdTxbszWudWO5NrNXyd8DCtvnA75s4XLqnb9

