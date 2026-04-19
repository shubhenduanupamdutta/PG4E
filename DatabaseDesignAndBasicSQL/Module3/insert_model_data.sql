-- pg4e_135aca6452=> SELECT * FROM make;
--  id | name  
-- ----+-------
--   1 | Ford
--   2 | Mazda
-- (2 rows)

INSERT INTO model (name, make_id) VALUES ('Fiesta ST FWD', 1), ('Five Hundred AWD', 1), ('Five Hundred FWD', 1), ('CX-3 4WD', 2), ('CX-5 2WD', 2);