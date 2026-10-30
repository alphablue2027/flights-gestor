# SPDX-License-Identifier: AGPL-3.0-with-Commons-Clause
# Copyright (C) 2025 Ordnay Perez Hernandez - ¡Uso comercial prohibido sin permiso!
from .flights import NationalFly, InternationalFly
from .airline import Airline
from datetime import date, datetime, timedelta
from psycopg.rows import dict_row
import os
import psycopg

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql:///flights_gestor")

FLIGHTS_QUERY = """
    SELECT f.code, f.is_inbound, a.name AS airline, f.init_city, f.end_city, f.departure,
        f.plane_mark, f.plane_model, f.plane_matricule, f.plane_capacity,
        i.destiny, i.scale, i.scale_number
    FROM flights f
    JOIN airlines a ON a.code = f.airline_code
    LEFT JOIN international_flights i ON i.flight_code = f.code
"""
NATIONALS_QUERY = FLIGHTS_QUERY + " WHERE i.flight_code IS NULL"
INTERNATIONALS_QUERY = FLIGHTS_QUERY + " WHERE i.flight_code IS NOT NULL"
INSERT_FLIGHT = """
    INSERT INTO flights (code, is_inbound, airline_code, init_city, end_city, departure,
        plane_mark, plane_model, plane_matricule, plane_capacity)
    VALUES (%s, %s, (SELECT code FROM airlines WHERE name = %s), %s, %s, %s, %s, %s, %s, %s)
"""

def to_national(row : dict) -> NationalFly:
    return NationalFly(row['code'], row['is_inbound'], row['airline'], row['init_city'], row['end_city'], row['departure'],
                       row['plane_mark'], row['plane_model'], row['plane_matricule'], row['plane_capacity'])

def to_international(row : dict) -> InternationalFly:
    return InternationalFly(row['code'], row['is_inbound'], row['airline'], row['init_city'], row['end_city'], row['departure'],
                            row['plane_mark'], row['plane_model'], row['plane_matricule'], row['plane_capacity'],
                            row['destiny'], row['scale'], row['scale_number'])

def to_airline(row : dict) -> Airline:
    return Airline(row['name'], row['code'], row['planes_number'], row['nationality'])

def day_range(day : date) -> tuple[datetime, datetime]:
    start = datetime.combine(day, datetime.min.time())
    return start, start + timedelta(days=1)


class FlightsGestor:
    __conn : psycopg.Connection

    @classmethod
    def connect(cls):
        cls.__conn = psycopg.connect(DATABASE_URL, row_factory=dict_row, autocommit=True)

    @classmethod
    def get_nationals(cls) -> list[NationalFly]:
        rows = cls.__conn.execute(NATIONALS_QUERY + " ORDER BY f.departure").fetchall()
        return list(map(to_national, rows))

    @classmethod
    def get_internationals(cls) -> list[InternationalFly]:
        rows = cls.__conn.execute(INTERNATIONALS_QUERY + " ORDER BY f.departure").fetchall()
        return list(map(to_international, rows))

    @classmethod
    def get_airlines(cls) -> list[Airline]:
        rows = cls.__conn.execute("SELECT * FROM airlines ORDER BY name").fetchall()
        return list(map(to_airline, rows))

    @classmethod
    def add_ifly(cls, code : str, inner: bool, airline : str, init_city : str, end_city : str, datetime : datetime, mark : str, model : str, matr : str, capacity : int, destiny : str, scale : bool, number : int):
        with cls.__conn.transaction():
            cls.__conn.execute(INSERT_FLIGHT, (code, inner, airline, init_city, end_city, datetime, mark, model, matr, capacity))
            cls.__conn.execute(
                "INSERT INTO international_flights (flight_code, destiny, scale, scale_number) VALUES (%s, %s, %s, %s)",
                (code, destiny, scale, number)
            )

    @classmethod
    def add_nfly(cls, code : str, inner: bool, airline : str, init_city : str, end_city : str, datetime : datetime, mark : str, model : str, matr : str, capacity : int):
        cls.__conn.execute(INSERT_FLIGHT, (code, inner, airline, init_city, end_city, datetime, mark, model, matr, capacity))

    @classmethod
    def del_fly(cls, code: str) -> bool:
        return cls.__conn.execute("DELETE FROM flights WHERE code = %s", (code.upper(),)).rowcount > 0

    @classmethod
    def add_airline(cls, code : str, name : str, nation : str, planes : int):
        cls.__conn.execute(
            "INSERT INTO airlines (code, name, planes_number, nationality) VALUES (%s, %s, %s, %s)",
            (code, name, planes, nation)
        )

    @classmethod
    def del_airline(cls, code : str) -> bool:
        return cls.__conn.execute("DELETE FROM airlines WHERE code = %s", (code.upper(),)).rowcount > 0

    @classmethod
    def get_airline(cls, code : str) -> Airline | None:
        row = cls.__conn.execute(
            "SELECT a.* FROM airlines a JOIN flights f ON f.airline_code = a.code WHERE f.code = %s",
            (code.upper(),)
        ).fetchone()
        return to_airline(row) if row else None

    @classmethod
    def get_airline_code(cls, name : str) -> str:
        return cls.__conn.execute("SELECT code FROM airlines WHERE name = %s", (name,)).fetchone()['code']

    @classmethod
    def airline_name_exists(cls, name : str) -> bool:
        return cls.__conn.execute("SELECT EXISTS (SELECT 1 FROM airlines WHERE name = %s)", (name,)).fetchone()['exists']

    @classmethod
    def airline_code_exists(cls, code : str) -> bool:
        return cls.__conn.execute("SELECT EXISTS (SELECT 1 FROM airlines WHERE code = %s)", (code,)).fetchone()['exists']

    @classmethod
    def flight_code_exists(cls, code : str) -> bool:
        return cls.__conn.execute("SELECT EXISTS (SELECT 1 FROM flights WHERE code = %s)", (code,)).fetchone()['exists']

    @classmethod
    def get_internationals_porcent(cls, mark : str, name : str) -> tuple[int, int, int]:
        row = cls.__conn.execute(
            """
            SELECT count(*) FILTER (WHERE f.plane_mark = %s) AS marked, count(*) AS total
            FROM flights f
            JOIN international_flights i ON i.flight_code = f.code
            JOIN airlines a ON a.code = f.airline_code
            WHERE a.name = %s
            """,
            (mark, name)
        ).fetchone()
        if not row['total']:
            return 0, 0, 0
        return row['marked'], row['total'], row['marked']*100//row['total']

    @classmethod
    def get_passagers_avg(cls, destiny: str) -> tuple[int, list[InternationalFly]]:
        rows = cls.__conn.execute(INTERNATIONALS_QUERY + " AND i.destiny = %s ORDER BY f.departure", (destiny,)).fetchall()
        flights = list(map(to_international, rows))
        if not flights:
            return 0, flights
        return sum(map(lambda f : f.plane.capacity, flights))//len(flights), flights

    @classmethod
    def get_outers_nflights(cls, date: date) -> list[NationalFly]:
        rows = cls.__conn.execute(
            NATIONALS_QUERY + " AND NOT f.is_inbound AND f.departure >= %s AND f.departure < %s ORDER BY f.departure",
            day_range(date)
        ).fetchall()
        return list(map(to_national, rows))

    @classmethod
    def get_scalest_fly(cls, date: date) -> InternationalFly | None:
        row = cls.__conn.execute(
            INTERNATIONALS_QUERY + " AND NOT f.is_inbound AND f.departure >= %s AND f.departure < %s ORDER BY i.scale_number DESC LIMIT 1",
            day_range(date)
        ).fetchone()
        return to_international(row) if row else None

    @classmethod
    def close(cls):
        cls.__conn.close()
