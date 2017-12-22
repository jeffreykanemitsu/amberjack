-- script that prepares a MySQL server for the project
CREATE DATABASE IF NOT EXISTS url_dev_db;
CREATE USER IF NOT EXISTS 'url_dev'@'localhost' IDENTIFIED BY 'url_dev_pwd';
GRANT ALL ON url_dev_db.* TO 'url_dev'@'localhost';
GRANT SELECT ON performance_schema.* TO 'url_dev'@'localhost';
