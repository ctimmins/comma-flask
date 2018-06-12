CREATE TABLE trips_overview (
  trip_id     VARCHAR(32),
  pt_count    INT,
  avg_speed   FLOAT,
  route       GEOMETRY,
  PRIMARY KEY (trip_id)
);

INSERT INTO trips_overview (trip_id, pt_count, avg_speed, route)
  SELECT
    trip_id,
    count(*),
    avg(speed),
    st_setsrid(st_simplify(st_makeline(array_agg(geom)), 0.001),4326)
  FROM trips GROUP BY trip_id;

CREATE INDEX ON trips_overview USING gist(route);