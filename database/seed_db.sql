-- Seed judgement table

INSERT INTO judgement
(judgement_favour)
VALUES
('Defendant'),
('Plaintiff');

-- Seed placeholder judge

INSERT INTO judge
    (title_id, first_name, middle_name, last_name, appointment_date)
VALUES
    (NULL, 'X', 'Y', 'Unknown', TO_TIMESTAMP('0001-01-01', 'YYYY-MM-DD'))