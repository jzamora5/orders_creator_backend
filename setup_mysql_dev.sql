-- prepares a MySQL server for the project
CREATE DATABASE IF NOT EXISTS orders_creator;
CREATE USER IF NOT EXISTS 'test_user' @'localhost' IDENTIFIED BY 'test_pwd';
GRANT ALL PRIVILEGES ON `orders_creator`.* TO 'test_user' @'localhost';
GRANT
SELECT
  ON `performance_schema`.* TO 'test_user' @'localhost';
FLUSH PRIVILEGES;