-- Drop tables in reverse order of dependencies
DROP TABLE IF EXISTS judge_hearing CASCADE;
DROP TABLE IF EXISTS hearing CASCADE;
DROP TABLE IF EXISTS judge CASCADE;
DROP TABLE IF EXISTS court CASCADE;
DROP TABLE IF EXISTS judgement CASCADE;
DROP TABLE IF EXISTS title CASCADE;

-- Recreate schema

CREATE TABLE title (
    title_id BIGSERIAL PRIMARY KEY,
    title_name VARCHAR(60) NOT NULL
);

CREATE TABLE judge (
    judge_id BIGSERIAL PRIMARY KEY,
    title_id BIGINT REFERENCES title (title_id),
    first_name VARCHAR(30) NOT NULL,
    middle_name VARCHAR(30),
    last_name VARCHAR(30) NOT NULL,
    appointment_date TIMESTAMP
);

CREATE TABLE judgement (
    judgement_id BIGSERIAL PRIMARY KEY,
    judgement_favour VARCHAR(30)
);

CREATE TABLE court (
    court_id BIGSERIAL PRIMARY KEY,
    court_name VARCHAR(80) NOT NULL
);

CREATE TABLE hearing (
    hearing_id BIGSERIAL PRIMARY KEY,
    judgement_id BIGINT REFERENCES judgement (judgement_id),
    court_id BIGINT REFERENCES court (court_id),
    hearing_citation VARCHAR(20) NOT NULL,
    hearing_title VARCHAR(50),
    hearing_date TIMESTAMP,
    hearing_description VARCHAR(1000),
    hearing_anomaly VARCHAR(1000),
    hearing_url VARCHAR(100)
);

CREATE TABLE judge_hearing (
    judge_hearing_id BIGSERIAL PRIMARY KEY,
    judge_id BIGINT REFERENCES judge (judge_id),
    hearing_id BIGINT REFERENCES hearing (hearing_id)
);
