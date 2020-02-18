CREATE TYPE gender AS ENUM ('M', 'F', 'O', 'U');

CREATE TABLE user_account(
  id SERIAL PRIMARY KEY,
  first_name VARCHAR NOT NULL,
  middle_name VARCHAR,
  father_surname VARCHAR NOT null,
  mother_surname VARCHAR NOT NULL,
  gender gender NOT NULL,
  email VARCHAR NOT NULL UNIQUE,
  salt VARCHAR NOT NULL,
  hashed_password VARCHAR NOT NULL,
  cellphone VARCHAR NOT NULL,
  birth_date DATE NOT NULL,
  joined_at TIMESTAMP NOT NULL DEFAULT NOW()
);
