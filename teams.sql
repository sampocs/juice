CREATE TABLE teams(
    team_id TEXT,
    org_id TEXT,
    city TEXT,
    mascot TEXT,
    start_year TEXT,
    active BOOLEAN,
    pfr_name TEXT
);

COPY teams(
    team_id,
    org_id,
    city,
    mascot,
    start_year,
    active,
    pfr_name
)
FROM '/opt/juice_data/teams.csv'
DELIMITER ','
CSV HEADER;