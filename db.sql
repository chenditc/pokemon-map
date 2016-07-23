CREATE TABLE FORT_MAP(
       fortid       VARCHAR(64) PRIMARY KEY,
       cellid       VARCHAR(64) ,
       enabled      BOOLEAN,
       latitude     DOUBLE PRECISION,
       longitude    DOUBLE PRECISION,
       forttype     INT,
       gymteam      INT 
);


ALTER TABLE FORT_MAP ADD column lure_expire DOUBLE PRECISION;
ALTER TABLE FORT_MAP ADD column last_update DOUBLE PRECISION;

CREATE INDEX latitude_idx ON fort_map (latitude);
CREATE INDEX longitude_idx ON fort_map (longitude);
CREATE INDEX cellid_idx ON fort_map (cellid);
CREATE INDEX lure_idx ON fort_map (lure_expire);
CREATE INDEX last_update_idx ON fort_map (last_update);


CREATE TABLE POKEMON_MAP(
       encounter_id     DOUBLE PRECISION PRIMARY KEY,
       expire           DOUBLE PRECISION,
       pokemon_id       INT,
       latitude         DOUBLE PRECISION,
       longitude        DOUBLE PRECISION
);


CREATE TABLE spawn_point_map(
       cellid       DOUBLE PRECISION,
       latitude     DOUBLE PRECISION,
       longitude    DOUBLE PRECISION,
       last_check   DOUBLE PRECISION,
       PRIMARY KEY (latitude, longitude)
);

CREATE INDEX last_check_idx ON spawn_point_map (last_check);
CREATE INDEX cellid_idx ON spawn_point_map (cellid);

CREATE TABLE map_visit_record(
       timestamp            DOUBLE PRECISION,
       cellid               DOUBLE PRECISION
);
