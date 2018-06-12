CREATE TABLE trips (
  trip_id     VARCHAR(32),
  start_time  VARCHAR(20),
  end_time    VARCHAR(20),
  coord_index INT,
  speed       FLOAT,
  dist        FLOAT,
  lat         FLOAT,
  lng         FLOAT,
  geom        GEOMETRY,
  PRIMARY KEY (trip_id, coord_index)
);

CREATE INDEX ON trips USING gist(geom);