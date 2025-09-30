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
    title_name VARCHAR NOT NULL
);

CREATE TABLE judge (
    judge_id BIGSERIAL PRIMARY KEY,
    title_id BIGINT REFERENCES title (title_id),
    first_name VARCHAR NOT NULL,
    middle_name VARCHAR,
    last_name VARCHAR NOT NULL,
    appointment_date TIMESTAMP
);

CREATE TABLE judgement (
    judgement_id BIGSERIAL PRIMARY KEY,
    judgement_favour VARCHAR
);

CREATE TABLE court (
    court_id BIGSERIAL PRIMARY KEY,
    court_name VARCHAR NOT NULL
);

CREATE TABLE hearing (
    hearing_id BIGSERIAL PRIMARY KEY,
    judgement_id BIGINT REFERENCES judgement (judgement_id),
    court_id BIGINT REFERENCES court (court_id),
    case_number VARCHAR NOT NULL,
    hearing_date TIMESTAMP,
    description VARCHAR
);

CREATE TABLE judge_hearing (
    judge_hearing_id BIGSERIAL PRIMARY KEY,
    judge_id BIGINT REFERENCES judge (judge_id),
    hearing_id BIGINT REFERENCES hearing (hearing_id)
);
