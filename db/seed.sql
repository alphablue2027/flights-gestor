INSERT INTO airlines (code, name, planes_number, nationality) VALUES
    ('CU', 'Cubana de Aviación', 12, 'Cuba'),
    ('KG', 'Aerogaviota', 8, 'Cuba'),
    ('IB', 'Iberia', 140, 'España'),
    ('CM', 'Copa Airlines', 110, 'Panamá'),
    ('UX', 'Air Europa', 55, 'España');

INSERT INTO flights (code, is_inbound, airline_code, init_city, end_city, departure, plane_mark, plane_model, plane_matricule, plane_capacity) VALUES
    ('CU101', FALSE, 'CU', 'La Habana', 'Santiago de Cuba', '2026-11-10 07:30', 'Antonov', 'AN158', 'CU1701', 99),
    ('CU102', TRUE, 'CU', 'Santiago de Cuba', 'La Habana', '2026-11-10 12:15', 'Antonov', 'AN158', 'CU1701', 99),
    ('CU210', FALSE, 'CU', 'La Habana', 'Holguín', '2026-11-10 16:40', 'Ilyushin', 'IL96', 'CU1250', 262),
    ('KG301', FALSE, 'KG', 'La Habana', 'Cayo Coco', '2026-11-10 09:00', 'ATR', 'ATR72', 'CU1550', 68),
    ('KG302', TRUE, 'KG', 'Cayo Coco', 'La Habana', '2026-11-11 14:20', 'ATR', 'ATR72', 'CU1550', 68),
    ('KG315', FALSE, 'KG', 'Varadero', 'Cayo Largo', '2026-11-11 08:10', 'ATR', 'ATR42', 'CU1552', 46),
    ('IB6621', FALSE, 'IB', 'La Habana', 'Madrid', '2026-11-10 21:05', 'Airbus', 'A350', 'ECNBE', 348),
    ('IB6620', TRUE, 'IB', 'Madrid', 'La Habana', '2026-11-11 15:50', 'Airbus', 'A330', 'ECLUB', 288),
    ('CM217', FALSE, 'CM', 'La Habana', 'Lima', '2026-11-10 10:45', 'Boeing', 'B737', 'HP1849', 160),
    ('CM218', TRUE, 'CM', 'Panamá', 'La Habana', '2026-11-11 06:30', 'Boeing', 'B737', 'HP1850', 166),
    ('UX052', FALSE, 'UX', 'La Habana', 'Roma', '2026-11-10 23:15', 'Boeing', 'B787', 'ECMSZ', 292),
    ('UX051', TRUE, 'UX', 'Madrid', 'La Habana', '2026-11-11 13:00', 'Boeing', 'B787', 'ECNVY', 337);

INSERT INTO international_flights (flight_code, destiny, scale, scale_number) VALUES
    ('IB6621', 'España', FALSE, 0),
    ('IB6620', 'Cuba', FALSE, 0),
    ('CM217', 'Perú', TRUE, 1),
    ('CM218', 'Cuba', FALSE, 0),
    ('UX052', 'Italia', TRUE, 2),
    ('UX051', 'Cuba', FALSE, 0);
