CREATE TABLE IF NOT EXISTS role (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    permissions JSON
);

CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL,
    username VARCHAR NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    role_id INTEGER REFERENCES role(id),
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN DEFAULT TRUE NOT NULL,
    is_superuser BOOLEAN DEFAULT FALSE NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE NOT NULL
);

CREATE TABLE IF NOT EXISTS operation (
    id SERIAL PRIMARY KEY,
    quantity VARCHAR,
    figi VARCHAR,
    type VARCHAR,
    date TIMESTAMP
);
