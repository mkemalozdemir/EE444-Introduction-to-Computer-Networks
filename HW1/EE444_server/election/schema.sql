-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS parties;
DROP TABLE IF EXISTS region;

CREATE TABLE parties (
  party_name TEXT UNIQUE PRIMARY KEY NOT NULL
);

CREATE TABLE region (
  region_name TEXT UNIQUE PRIMARY KEY NOT NULL,
  seats INTEGER NOT NULL
);


