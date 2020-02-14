CREATE TABLE user_account(
  id SERIAL PRIMARY KEY,
  first_name VARCHAR NOT NULL,
  middle_name VARCHAR,
  father_surname VARCHAR not null,
  mother_surname VARCHAR NOT NULL,
  email VARCHAR NOT NULL UNIQUE,
  cellphone VARCHAR NOT NULL,
  birth_date DATE NOT NULL,
  joined_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE credentials(
  email VARCHAR NOT NULL REFERENCES user_account(email),
  salt VARCHAR NOT NULL,
  hashed_password VARCHAR NOT NULL
)
