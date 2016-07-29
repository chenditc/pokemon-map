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
       encounter_id     DOUBLE PRECISION,
       expire           DOUBLE PRECISION,
       pokemon_id       INT,
       latitude         DOUBLE PRECISION,
       longitude        DOUBLE PRECISION,
       PRIMARY KEY (encounter_id, expire, pokemon_id, latitude, longitude)
);
CREATE INDEX expire_idx ON POKEMON_MAP (expire);
CREATE INDEX pokemon_id ON POKEMON_MAP (pokemon_id);
CREATE INDEX pokemon_latitude_idx ON POKEMON_MAP (latitude);
CREATE INDEX pokemon_longitude_idx ON POKEMON_MAP (longitude);


CREATE TABLE spawn_point_map(
       cellid       DOUBLE PRECISION,
       latitude     DOUBLE PRECISION,
       longitude    DOUBLE PRECISION,
       last_check   DOUBLE PRECISION,
       PRIMARY KEY (latitude, longitude)
);
CREATE INDEX spawn_last_check_idx ON spawn_point_map (last_check);
CREATE INDEX spawn_cellid_idx ON spawn_point_map (cellid);

CREATE TABLE searcher_account(
       username       VARCHAR(64) PRIMARY KEY,
       password       VARCHAR(64) ,
       lastused     DOUBLE PRECISION,
       failcount    INT
);
CREATE INDEX searcher_account_lastused_idx ON searcher_account (lastused);
CREATE INDEX searcher_account_failcount_idx ON searcher_account (failcount);
ALTER TABLE searcher_account ADD column logininfo VARCHAR(250);

