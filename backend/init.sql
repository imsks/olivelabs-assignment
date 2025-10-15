# PostgreSQL initialization script
CREATE DATABASE nlq_app;
CREATE USER nlq_user WITH PASSWORD 'nlq_password';
GRANT ALL PRIVILEGES ON DATABASE nlq_app TO nlq_user;
