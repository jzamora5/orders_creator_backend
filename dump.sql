-- MySQL dump 10.13  Distrib 8.0.20, for Linux (x86_64)
--
-- Host: localhost    Database: orders_creator
-- ------------------------------------------------------
-- Server version	8.0.20-0ubuntu0.20.04.1
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
--
-- Table structure for table `orders`
--
DROP DATABASE IF EXISTS orders_creator;
CREATE DATABASE IF NOT EXISTS orders_creator;
USE orders_creator;
DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` varchar(60) NOT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `total` float NOT NULL,
  `sub_total` float NOT NULL,
  `taxes` float NOT NULL,
  `paid` tinyint(1) NOT NULL,
  `status` varchar(60) NOT NULL,
  `user_id` varchar(60) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- Dumping data for table `orders`
--
LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO
  `orders`
VALUES
  (
    '20f281b1-2cd1-4e36-a7c7-d1062ff16bcd',
    '2020-03-26 02:17:06',
    '2020-03-26 02:17:06',
    297500,
    250000,
    47500,
    1,
    'accepted',
    '017ec502-e84a-4a0f-92d6-d97e27bb6bdf'
  ),
  (
    '2c620702-d41c-4732-a1cf-6e40f7877dc3',
    '2021-03-26 02:17:06',
    '2021-03-26 02:17:06',
    119000,
    100000,
    19000,
    0,
    'processing',
    '017ec502-e84a-4a0f-92d6-d97e27bb6bdf'
  ),
  (
    '2f055228-5fd3-4b1d-a021-7e4b9b7d70a6',
    '2021-03-26 02:17:06',
    '2021-03-26 02:17:06',
    571200,
    480000,
    91200,
    0,
    'rejected',
    '017ec502-e84a-4a0f-92d6-d97e27bb6bdf'
  ),
  (
    '3e73edf2-c3d6-409f-9202-213df4a7a25a',
    '2019-03-26 02:17:06',
    '2019-03-26 02:17:06',
    428400,
    360000,
    68400,
    1,
    'accepted',
    '0d375b05-5ef9-4d43-aaca-436762bb25bf'
  ),
  (
    '3fccec93-2842-49a0-8fdb-4008af2ef041',
    '2019-03-26 02:17:06',
    '2019-03-26 02:17:06',
    140800,
    120000,
    22800,
    1,
    'accepted',
    '0d375b05-5ef9-4d43-aaca-436762bb25bf'
  );
  /*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;
--
  -- Table structure for table `payments`
  --
  DROP TABLE IF EXISTS `payments`;
  /*!40101 SET @saved_cs_client     = @@character_set_client */;
  /*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
    `id` varchar(60) NOT NULL,
    `created_at` datetime DEFAULT NULL,
    `updated_at` datetime DEFAULT NULL,
    `payment_type` varchar(60) DEFAULT NULL,
    `total` float NOT NULL,
    `status` varchar(60) NOT NULL,
    `order_id` varchar(60) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `order_id` (`order_id`),
    CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`)
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
  /*!40101 SET character_set_client = @saved_cs_client */;
--
  -- Dumping data for table `payments`
  --
  LOCK TABLES `payments` WRITE;
INSERT INTO
  `payments`
VALUES
  (
    '416cddd7-746e-4715-821c-3ad30b9bc3c3',
    '2020-03-26 02:17:06',
    '2020-03-26 02:17:06',
    'credit',
    148750,
    'accepted',
    '20f281b1-2cd1-4e36-a7c7-d1062ff16bcd'
  ),
  (
    'd3cb5b63-2f99-4c55-86a7-3127eb4a8128',
    '2020-05-20 02:17:06',
    '2020-05-20 02:17:06',
    'debit',
    148750,
    'accepted',
    '20f281b1-2cd1-4e36-a7c7-d1062ff16bcd'
  ),
  (
    'd7275f8c-70e5-4c27-bcd6-aafd5256fccd',
    '2020-05-20 02:17:06',
    '2020-05-20 02:17:06',
    'credit',
    100000,
    'rejected',
    '2c620702-d41c-4732-a1cf-6e40f7877dc3'
  ),
  (
    'dcfb45cc-b170-4ace-97af-9957b564606a',
    '2020-05-20 02:17:06',
    '2020-05-20 02:17:06',
    'credit',
    50000,
    'rejected',
    '2c620702-d41c-4732-a1cf-6e40f7877dc3'
  ),
  (
    'e7680872-7b76-4565-aa8b-6c3d182caa1c',
    '2020-05-20 02:17:06',
    '2020-05-20 02:17:06',
    'credit',
    50000,
    'ok',
    '2c620702-d41c-4732-a1cf-6e40f7877dc3'
  ),
  (
    'ea518e20-3370-4cb3-b38f-df1cccbdd8a9',
    '2020-05-20 02:17:06',
    '2020-05-20 02:17:06',
    'debit',
    80000,
    'ok',
    '2c620702-d41c-4732-a1cf-6e40f7877dc3'
  ),
  (
    'efafcf4e-59cf-45e2-b8c5-e14ae252ca01',
    '2020-05-20 02:17:06',
    '2020-05-20 02:17:06',
    'cash',
    50000,
    'ok',
    '2f055228-5fd3-4b1d-a021-7e4b9b7d70a6'
  );
  /*!40000 ALTER TABLE `payments` DISABLE KEYS */;
  /*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;
--
  -- Table structure for table `shippings`
  --
  DROP TABLE IF EXISTS `shippings`;
  /*!40101 SET @saved_cs_client     = @@character_set_client */;
  /*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `shippings` (
    `id` varchar(60) NOT NULL,
    `created_at` datetime DEFAULT NULL,
    `updated_at` datetime DEFAULT NULL,
    `address` varchar(128) DEFAULT NULL,
    `city` varchar(128) DEFAULT NULL,
    `state` varchar(128) NOT NULL,
    `country` varchar(128) NOT NULL,
    `cost` float NOT NULL,
    `order_id` varchar(60) NOT NULL,
    PRIMARY KEY (`id`),
    KEY `order_id` (`order_id`),
    CONSTRAINT `shippings_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`)
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
  /*!40101 SET character_set_client = @saved_cs_client */;
--
  -- Dumping data for table `shippings`
  --
  LOCK TABLES `shippings` WRITE;
  /*!40000 ALTER TABLE `shippings` DISABLE KEYS */;
INSERT INTO
  `shippings`
VALUES
  (
    'f4dfd576-7c29-4bdf-9fbd-5c95a170ebce',
    '2020-03-26 02:17:06',
    '2020-03-26 02:17:06',
    'Vona Vibra Street',
    'Denver',
    'Colorado',
    'USA',
    10000,
    '20f281b1-2cd1-4e36-a7c7-d1062ff16bcd'
  ),
  (
    'f4e98f0a-053a-42e2-9633-0cca2a587410',
    '2020-03-26 02:17:06',
    '2020-03-26 02:17:06',
    'Chandelier 2030 Street',
    'Denver',
    'Colorado',
    'USA',
    10000,
    '2c620702-d41c-4732-a1cf-6e40f7877dc3'
  ),
  (
    'f7a087bb-13e2-463d-a951-b8feb7da899f',
    '2020-03-26 02:17:06',
    '2020-03-26 02:17:06',
    'Empire Doughnut',
    'New York',
    'New York',
    'USA',
    10000,
    '2f055228-5fd3-4b1d-a021-7e4b9b7d70a6'
  ),
  (
    'f7c854a4-f565-4aa5-8542-c4e17c498ef1',
    '2020-03-26 02:17:06',
    '2020-03-26 02:17:06',
    'Conjunto Tronquitos',
    'Chia',
    'Cundinamarca',
    'COL',
    10000,
    '3e73edf2-c3d6-409f-9202-213df4a7a25a'
  ),
  (
    'c29b5191-ac68-4e9b-a68f-aa42ea1dcb01',
    '2020-03-26 02:17:06',
    '2020-03-26 02:17:06',
    'Centro Historico',
    'Bogota',
    'Cundinamarca',
    'COL',
    10000,
    '3fccec93-2842-49a0-8fdb-4008af2ef041'
  );
  /*!40000 ALTER TABLE `shippings` ENABLE KEYS */;
UNLOCK TABLES;
--
  -- Table structure for table `users`
  --
  DROP TABLE IF EXISTS `users`;
  /*!40101 SET @saved_cs_client     = @@character_set_client */;
  /*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
    `id` varchar(60) NOT NULL,
    `created_at` datetime DEFAULT NULL,
    `updated_at` datetime DEFAULT NULL,
    `name` varchar(128) DEFAULT NULL,
    `last_name` varchar(128) DEFAULT NULL,
    `email` varchar(128) NOT NULL,
    `password` varchar(128) NOT NULL,
    `company` varchar(128) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE KEY `email` (`email`)
  ) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;
  /*!40101 SET character_set_client = @saved_cs_client */;
--
  -- Dumping data for table `users`
  --
  LOCK TABLES `users` WRITE;
  /*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO
  `users`
VALUES
  (
    '017ec502-e84a-4a0f-92d6-d97e27bb6bdf',
    '2017-03-25 02:17:06',
    '2017-03-25 02:17:06',
    'Larry',
    'Hudson',
    'larry@test.com',
    '123456789',
    'personal'
  ),(
    '0d375b05-5ef9-4d43-aaca-436762bb25bf',
    '2018-03-25 02:17:06',
    '2018-03-25 02:17:06',
    'Erika',
    'Merlon',
    'erika@test.com',
    '123456789',
    'erikagame'
  ),(
    '12e9ccb4-03e4-4f82-ac3d-4fc7e3ebfbfe',
    '2019-03-25 02:17:06',
    '2019-03-25 02:17:06',
    'Marco',
    'Polo',
    'marco@test.com',
    '123456789',
    'marcowood'
  ),(
    '1e0f976d-beef-497b-b29c-b4a25d1c071a',
    '2020-03-25 02:17:06',
    '2020-03-25 02:17:06',
    'Ramon',
    'Perez',
    'ramon@test.com',
    '123456789',
    'ramonfood'
  );
  /*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
  /*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
  /*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
  /*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
  /*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
  /*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
  /*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
  /*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
  /*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
-- Dump completed on 2021-03-23 12:24:46