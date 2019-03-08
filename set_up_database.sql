-- Creates database hbnb_dev_db
DROP DATABASE IF EXISTS career_path_db;
CREATE DATABASE IF NOT EXISTS career_path_db;
USE career_path_db;
CREATE USER IF NOT EXISTS 'career_path'@'localhost';
SET PASSWORD FOR 'career_path'@'localhost' = 'career_path_pwd';
GRANT ALL PRIVILEGES ON career_path_db.* TO 'career_path'@'localhost';
GRANT SELECT ON performance_schema.* TO 'career_path'@'localhost';
