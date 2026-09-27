BEGIN;

INSERT INTO island (island_id, official_code, name, sort_order) VALUES
  ('el-hierro', '7', 'El Hierro', 1),
  ('la-gomera', '6', 'La Gomera', 2),
  ('la-palma', '5', 'La Palma', 3),
  ('tenerife', '4', 'Tenerife', 4),
  ('gran-canaria', '3', 'Gran Canaria', 5),
  ('fuerteventura', '2', 'Fuerteventura', 6),
  ('lanzarote', '1', 'Lanzarote', 7)
ON CONFLICT (island_id) DO UPDATE SET
  official_code = EXCLUDED.official_code,
  name = EXCLUDED.name,
  sort_order = EXCLUDED.sort_order;

COMMIT;
