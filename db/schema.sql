DROP TABLE IF EXISTS international_flights;
DROP TABLE IF EXISTS flights;
DROP TABLE IF EXISTS airlines;

CREATE TABLE airlines (
    code          CHAR(2)     PRIMARY KEY CHECK (code ~ '^[A-Z]{2}$'),
    name          VARCHAR(80) NOT NULL UNIQUE,
    planes_number INTEGER     NOT NULL CHECK (planes_number >= 0),
    nationality   VARCHAR(60) NOT NULL
);

CREATE TABLE flights (
    code            VARCHAR(8)  PRIMARY KEY,
    is_inbound      BOOLEAN     NOT NULL,
    airline_code    CHAR(2)     NOT NULL REFERENCES airlines (code) ON DELETE CASCADE,
    init_city       VARCHAR(60) NOT NULL,
    end_city        VARCHAR(60) NOT NULL,
    departure       TIMESTAMP   NOT NULL,
    plane_mark      VARCHAR(40) NOT NULL,
    plane_model     VARCHAR(40) NOT NULL,
    plane_matricule VARCHAR(20) NOT NULL,
    plane_capacity  INTEGER     NOT NULL CHECK (plane_capacity > 0),
    CHECK (left(code, 2) = airline_code AND substring(code FROM 3) ~ '^[0-9]+$')
);

CREATE TABLE international_flights (
    flight_code  VARCHAR(8)  PRIMARY KEY REFERENCES flights (code) ON DELETE CASCADE,
    destiny      VARCHAR(60) NOT NULL,
    scale        BOOLEAN     NOT NULL,
    scale_number INTEGER     NOT NULL CHECK (scale_number >= 0),
    CHECK (scale OR scale_number = 0)
);

CREATE INDEX flights_airline_code_idx ON flights (airline_code);
CREATE INDEX flights_departure_idx ON flights (departure);
