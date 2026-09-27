# Esquema PostGIS

Las migraciones se aplican por orden numérico. `dataset_version` centraliza la
procedencia inmutable y las tablas derivadas conservan su clave foránea.

```sh
docker compose -p pedsdata_phase1 up -d db
./scripts/test_postgis.sh pedsdata_phase1-db-1
```

`island_facility_coverage` parte de `island` y usa `LEFT JOIN`, por lo que
conserva las siete islas aunque alguna no tenga observaciones.
