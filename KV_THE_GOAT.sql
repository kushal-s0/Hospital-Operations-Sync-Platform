-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: hospital_management
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `admissions`
--

DROP TABLE IF EXISTS `admissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admissions` (
  `admission_id` int NOT NULL,
  `patient_id` int DEFAULT NULL,
  `bed_id` int DEFAULT NULL,
  `doctor_id` int DEFAULT NULL,
  `admission_time` datetime DEFAULT NULL,
  `discharge_time` datetime DEFAULT NULL,
  `condition_level` enum('Critical','High','Medium','Low') DEFAULT NULL,
  `status` enum('Active','Discharged') DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `admin_id` int DEFAULT NULL,
  `updated_timestamp` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`admission_id`),
  KEY `patient_id` (`patient_id`),
  KEY `bed_id` (`bed_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `admissions_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`),
  CONSTRAINT `admissions_ibfk_2` FOREIGN KEY (`bed_id`) REFERENCES `beds` (`bed_id`),
  CONSTRAINT `admissions_ibfk_3` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admissions`
--

LOCK TABLES `admissions` WRITE;
/*!40000 ALTER TABLE `admissions` DISABLE KEYS */;
INSERT INTO `admissions` VALUES (1,1,4,2,'2024-06-15 10:00:00','2026-01-20 13:25:20','High','Discharged','2026-01-19 18:17:53','2026-01-20 13:25:20',NULL,'2026-01-20 13:25:20'),(2,4,2,2,'2024-06-18 17:00:00',NULL,'Critical','Active','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(3,5,7,7,'2024-06-19 09:00:00',NULL,'Critical','Active','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(4,2,3,NULL,'2026-01-19 13:20:37','2026-01-19 17:57:03','High','Discharged','2026-01-19 13:20:37','2026-01-19 17:57:03',NULL,'2026-01-19 17:57:03'),(5,3,5,NULL,'2026-01-19 13:20:37','2026-01-20 13:25:57','High','Discharged','2026-01-19 13:20:37','2026-01-20 13:25:57',NULL,'2026-01-20 13:25:57'),(6,6,9,NULL,'2026-01-19 13:20:37',NULL,'Medium','Active','2026-01-19 13:20:37','2026-01-19 13:20:37',NULL,'2026-01-19 13:20:37'),(7,7,13,NULL,'2026-01-19 13:20:37',NULL,'Medium','Active','2026-01-19 13:20:37','2026-01-19 13:20:37',NULL,'2026-01-19 13:20:37'),(8,8,16,NULL,'2026-01-19 13:20:37',NULL,'Medium','Active','2026-01-19 13:20:37','2026-01-19 13:20:37',NULL,'2026-01-19 13:20:37'),(9,9,19,NULL,'2026-01-19 13:20:37',NULL,'Medium','Active','2026-01-19 13:20:37','2026-01-19 13:20:37',NULL,'2026-01-19 13:20:37'),(10,10,22,NULL,'2026-01-19 13:20:37','2026-01-20 14:11:39','Medium','Discharged','2026-01-19 13:20:37','2026-01-20 14:11:39',NULL,'2026-01-20 14:11:39'),(11,11,NULL,NULL,'2026-01-19 13:20:37','2026-01-20 14:07:48','Medium','Discharged','2026-01-19 13:20:37','2026-01-20 14:07:48',NULL,'2026-01-20 14:07:48'),(12,12,NULL,NULL,'2026-01-19 13:20:37','2026-01-20 14:07:43','Medium','Discharged','2026-01-19 13:20:37','2026-01-20 14:07:43',NULL,'2026-01-20 14:07:43');
/*!40000 ALTER TABLE `admissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admissions_admissionrule`
--

DROP TABLE IF EXISTS `admissions_admissionrule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admissions_admissionrule` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `condition` longtext NOT NULL,
  `recommended_bed_type` varchar(50) NOT NULL,
  `recommended_department` varchar(100) NOT NULL,
  `priority` int NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admissions_admissionrule`
--

LOCK TABLES `admissions_admissionrule` WRITE;
/*!40000 ALTER TABLE `admissions_admissionrule` DISABLE KEYS */;
/*!40000 ALTER TABLE `admissions_admissionrule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `appointment_id` int NOT NULL,
  `patient_id` int DEFAULT NULL,
  `doctor_id` int DEFAULT NULL,
  `visit_id` int DEFAULT NULL,
  `appointment_date` date DEFAULT NULL,
  `appointment_time` time DEFAULT NULL,
  `reason_for_visit` varchar(200) DEFAULT NULL,
  `status` enum('Scheduled','Completed','Cancelled') DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `admin_id` int DEFAULT NULL,
  `updated_timestamp` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`appointment_id`),
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `visit_id` (`visit_id`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`),
  CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`doctor_id`),
  CONSTRAINT `appointments_ibfk_3` FOREIGN KEY (`visit_id`) REFERENCES `visits` (`visit_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES (1,1,2,1,'2024-06-15','09:30:00','Chest pain','Completed','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(2,2,2,2,'2024-06-16','14:20:00','Heart checkup','Completed','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(3,3,6,3,'2024-06-17','11:00:00','Fever and cough','Completed','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(4,4,2,4,'2024-06-18','16:45:00','Vaccination','Completed','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(5,5,7,5,'2024-06-19','08:15:00','Accident injury','Completed','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(6,1,2,NULL,'2024-07-01','10:00:00','Follow-up checkup','Scheduled','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53');
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `audit_log`
--

DROP TABLE IF EXISTS `audit_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_log` (
  `audit_id` int NOT NULL AUTO_INCREMENT,
  `table_name` varchar(100) NOT NULL,
  `record_id` int NOT NULL,
  `operation_type` enum('INSERT','UPDATE','DELETE') NOT NULL,
  `admin_id` int DEFAULT NULL,
  `admin_name` varchar(200) DEFAULT NULL,
  `admin_role` varchar(50) DEFAULT NULL,
  `old_values` json DEFAULT NULL,
  `new_values` json DEFAULT NULL,
  `changed_fields` text,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` varchar(255) DEFAULT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`audit_id`),
  KEY `table_name` (`table_name`),
  KEY `record_id` (`record_id`),
  KEY `admin_id` (`admin_id`),
  KEY `timestamp` (`timestamp`),
  KEY `operation_type` (`operation_type`),
  CONSTRAINT `audit_log_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `staff_users` (`staff_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_log`
--

LOCK TABLES `audit_log` WRITE;
/*!40000 ALTER TABLE `audit_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `audit_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=129 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add Blacklisted Token',7,'add_blacklistedtoken'),(26,'Can change Blacklisted Token',7,'change_blacklistedtoken'),(27,'Can delete Blacklisted Token',7,'delete_blacklistedtoken'),(28,'Can view Blacklisted Token',7,'view_blacklistedtoken'),(29,'Can add Outstanding Token',8,'add_outstandingtoken'),(30,'Can change Outstanding Token',8,'change_outstandingtoken'),(31,'Can delete Outstanding Token',8,'delete_outstandingtoken'),(32,'Can view Outstanding Token',8,'view_outstandingtoken'),(33,'Can add hospital',9,'add_hospital'),(34,'Can change hospital',9,'change_hospital'),(35,'Can delete hospital',9,'delete_hospital'),(36,'Can view hospital',9,'view_hospital'),(37,'Can add department',10,'add_department'),(38,'Can change department',10,'change_department'),(39,'Can delete department',10,'delete_department'),(40,'Can view department',10,'view_department'),(41,'Can add staff user',11,'add_staffuser'),(42,'Can change staff user',11,'change_staffuser'),(43,'Can delete staff user',11,'delete_staffuser'),(44,'Can view staff user',11,'view_staffuser'),(45,'Can add doctor',12,'add_doctor'),(46,'Can change doctor',12,'change_doctor'),(47,'Can delete doctor',12,'delete_doctor'),(48,'Can view doctor',12,'view_doctor'),(49,'Can add patient',13,'add_patient'),(50,'Can change patient',13,'change_patient'),(51,'Can delete patient',13,'delete_patient'),(52,'Can view patient',13,'view_patient'),(53,'Can add bed',14,'add_bed'),(54,'Can change bed',14,'change_bed'),(55,'Can delete bed',14,'delete_bed'),(56,'Can view bed',14,'view_bed'),(57,'Can add admission',15,'add_admission'),(58,'Can change admission',15,'change_admission'),(59,'Can delete admission',15,'delete_admission'),(60,'Can view admission',15,'view_admission'),(61,'Can add visit',16,'add_visit'),(62,'Can change visit',16,'change_visit'),(63,'Can delete visit',16,'delete_visit'),(64,'Can view visit',16,'view_visit'),(65,'Can add appointment',17,'add_appointment'),(66,'Can change appointment',17,'change_appointment'),(67,'Can delete appointment',17,'delete_appointment'),(68,'Can view appointment',17,'view_appointment'),(69,'Can add treatment',18,'add_treatment'),(70,'Can change treatment',18,'change_treatment'),(71,'Can delete treatment',18,'delete_treatment'),(72,'Can view treatment',18,'view_treatment'),(73,'Can add billing',19,'add_billing'),(74,'Can change billing',19,'change_billing'),(75,'Can delete billing',19,'delete_billing'),(76,'Can view billing',19,'view_billing'),(77,'Can add inventory item',20,'add_inventoryitem'),(78,'Can change inventory item',20,'change_inventoryitem'),(79,'Can delete inventory item',20,'delete_inventoryitem'),(80,'Can view inventory item',20,'view_inventoryitem'),(81,'Can add inventory usage',21,'add_inventoryusage'),(82,'Can change inventory usage',21,'change_inventoryusage'),(83,'Can delete inventory usage',21,'delete_inventoryusage'),(84,'Can view inventory usage',21,'view_inventoryusage'),(85,'Can add financial transaction',22,'add_financialtransaction'),(86,'Can change financial transaction',22,'change_financialtransaction'),(87,'Can delete financial transaction',22,'delete_financialtransaction'),(88,'Can view financial transaction',22,'view_financialtransaction'),(89,'Can add audit log',23,'add_auditlog'),(90,'Can change audit log',23,'change_auditlog'),(91,'Can delete audit log',23,'delete_auditlog'),(92,'Can view audit log',23,'view_auditlog'),(93,'Can add opd queue',24,'add_opdqueue'),(94,'Can change opd queue',24,'change_opdqueue'),(95,'Can delete opd queue',24,'delete_opdqueue'),(96,'Can view opd queue',24,'view_opdqueue'),(97,'Can add opd statistics',25,'add_opdstatistics'),(98,'Can change opd statistics',25,'change_opdstatistics'),(99,'Can delete opd statistics',25,'delete_opdstatistics'),(100,'Can view opd statistics',25,'view_opdstatistics'),(101,'Can add inventory category',26,'add_inventorycategory'),(102,'Can change inventory category',26,'change_inventorycategory'),(103,'Can delete inventory category',26,'delete_inventorycategory'),(104,'Can view inventory category',26,'view_inventorycategory'),(105,'Can add inventory transaction',27,'add_inventorytransaction'),(106,'Can change inventory transaction',27,'change_inventorytransaction'),(107,'Can delete inventory transaction',27,'delete_inventorytransaction'),(108,'Can view inventory transaction',27,'view_inventorytransaction'),(109,'Can add admission rule',28,'add_admissionrule'),(110,'Can change admission rule',28,'change_admissionrule'),(111,'Can delete admission rule',28,'delete_admissionrule'),(112,'Can view admission rule',28,'view_admissionrule'),(113,'Can add hospital',29,'add_hospital'),(114,'Can change hospital',29,'change_hospital'),(115,'Can delete hospital',29,'delete_hospital'),(116,'Can view hospital',29,'view_hospital'),(117,'Can add capacity snapshot',30,'add_capacitysnapshot'),(118,'Can change capacity snapshot',30,'change_capacitysnapshot'),(119,'Can delete capacity snapshot',30,'delete_capacitysnapshot'),(120,'Can view capacity snapshot',30,'view_capacitysnapshot'),(121,'Can add opd queue',31,'add_opdqueue'),(122,'Can change opd queue',31,'change_opdqueue'),(123,'Can delete opd queue',31,'delete_opdqueue'),(124,'Can view opd queue',31,'view_opdqueue'),(125,'Can add receptionist dashboard view',32,'add_receptionistdashboardview'),(126,'Can change receptionist dashboard view',32,'change_receptionistdashboardview'),(127,'Can delete receptionist dashboard view',32,'delete_receptionistdashboardview'),(128,'Can view receptionist dashboard view',32,'view_receptionistdashboardview');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `beds`
--

DROP TABLE IF EXISTS `beds`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `beds` (
  `bed_id` int NOT NULL,
  `hospital_id` int DEFAULT NULL,
  `department_id` int DEFAULT NULL,
  `bed_type` enum('Normal','ICU','Ventilator','Emergency') DEFAULT NULL,
  `status` enum('Available','Occupied','Maintenance') DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `admin_id` int DEFAULT NULL,
  `updated_timestamp` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`bed_id`),
  KEY `hospital_id` (`hospital_id`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `beds_ibfk_1` FOREIGN KEY (`hospital_id`) REFERENCES `hospitals` (`hospital_id`),
  CONSTRAINT `beds_ibfk_2` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `beds`
--

LOCK TABLES `beds` WRITE;
/*!40000 ALTER TABLE `beds` DISABLE KEYS */;
INSERT INTO `beds` VALUES (1,3,6,'ICU','Available','2026-01-19 18:17:53','2026-01-20 14:19:03',NULL,'2026-01-20 14:19:03'),(2,3,3,'ICU','Occupied','2026-01-19 18:17:53','2026-01-20 19:10:28',NULL,'2026-01-20 19:10:28'),(3,1,2,'Normal','Available','2026-01-19 18:17:53','2026-01-20 19:40:55',NULL,'2026-01-20 19:40:55'),(4,1,2,'ICU','Available','2026-01-19 18:17:53','2026-01-20 19:40:55',NULL,'2026-01-20 19:40:55'),(5,1,3,'Normal','Available','2026-01-19 18:17:53','2026-01-20 19:40:55',NULL,'2026-01-20 19:40:55'),(6,2,5,'Normal','Available','2026-01-19 18:17:53','2026-01-20 19:40:55',NULL,'2026-01-20 19:40:55'),(7,3,6,'ICU','Occupied','2026-01-19 18:17:53','2026-01-20 19:10:28',NULL,'2026-01-20 19:10:28'),(8,3,6,'Ventilator','Available','2026-01-19 18:17:53','2026-01-20 19:40:55',NULL,'2026-01-20 19:40:55'),(9,1,4,'Normal','Occupied','2026-01-19 18:17:53','2026-01-20 19:10:28',NULL,'2026-01-20 19:10:28'),(10,2,103,'Ventilator','Maintenance','2026-01-19 18:17:53','2026-01-20 14:42:37',NULL,'2026-01-20 14:42:37'),(11,1,5,'Normal','Available','2026-01-19 13:20:37','2026-01-20 19:40:55',NULL,'2026-01-20 19:40:55'),(12,1,5,'Normal','Available','2026-01-19 13:20:37','2026-01-20 19:40:55',NULL,'2026-01-20 19:40:55'),(13,1,5,'Normal','Occupied','2026-01-19 13:20:37','2026-01-20 19:10:28',NULL,'2026-01-20 19:10:28'),(14,1,2,'Normal','Available','2026-01-19 13:20:37','2026-01-20 19:40:55',NULL,'2026-01-20 19:40:55'),(15,1,2,'Normal','Available','2026-01-19 13:20:37','2026-01-20 19:40:55',NULL,'2026-01-20 19:40:55'),(16,1,2,'Normal','Occupied','2026-01-19 13:20:37','2026-01-20 19:10:28',NULL,'2026-01-20 19:10:28'),(17,1,103,'Normal','Available','2026-01-19 13:20:37','2026-01-20 19:40:55',NULL,'2026-01-20 19:40:55'),(18,1,103,'Normal','Available','2026-01-19 13:20:37','2026-01-20 19:40:55',NULL,'2026-01-20 19:40:55'),(19,1,103,'Normal','Occupied','2026-01-19 13:20:37','2026-01-20 14:12:25',NULL,'2026-01-20 14:12:25'),(20,1,1,'Normal','Available','2026-01-19 13:20:37','2026-01-20 19:40:55',NULL,'2026-01-20 19:40:55'),(21,1,1,'Normal','Available','2026-01-19 13:20:37','2026-01-20 19:40:55',NULL,'2026-01-20 19:40:55'),(22,1,1,'Normal','Maintenance','2026-01-19 13:20:37','2026-01-20 14:11:39',NULL,'2026-01-20 14:11:39'),(50,2,7,'Ventilator','Available','2026-01-20 14:42:57','2026-01-20 14:42:57',NULL,'2026-01-20 14:42:57');
/*!40000 ALTER TABLE `beds` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `billing`
--

DROP TABLE IF EXISTS `billing`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `billing` (
  `bill_id` int NOT NULL,
  `patient_id` int DEFAULT NULL,
  `treatment_id` int DEFAULT NULL,
  `bill_date` date DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `payment_method` enum('Cash','Card','Insurance') DEFAULT NULL,
  `payment_status` enum('Paid','Pending','Failed') DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `admin_id` int DEFAULT NULL,
  `updated_timestamp` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`bill_id`),
  KEY `patient_id` (`patient_id`),
  KEY `treatment_id` (`treatment_id`),
  CONSTRAINT `billing_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`),
  CONSTRAINT `billing_ibfk_2` FOREIGN KEY (`treatment_id`) REFERENCES `treatments` (`treatment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `billing`
--

LOCK TABLES `billing` WRITE;
/*!40000 ALTER TABLE `billing` DISABLE KEYS */;
INSERT INTO `billing` VALUES (1,1,1,'2024-06-15',1500.00,'Card','Paid','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(2,2,2,'2024-06-16',800.00,'Insurance','Paid','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(3,3,3,'2024-06-17',500.00,'Cash','Paid','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(4,4,4,'2024-06-18',300.00,'Card','Paid','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(5,5,5,'2024-06-19',1200.00,'Insurance','Pending','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53');
/*!40000 ALTER TABLE `billing` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departments`
--

DROP TABLE IF EXISTS `departments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departments` (
  `department_id` int NOT NULL,
  `hospital_id` int DEFAULT NULL,
  `department_name` varchar(100) DEFAULT NULL,
  `total_beds` int DEFAULT NULL,
  `available_beds` int DEFAULT NULL,
  `emergency_beds` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `admin_id` int DEFAULT NULL,
  `updated_timestamp` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`department_id`),
  KEY `hospital_id` (`hospital_id`),
  CONSTRAINT `departments_ibfk_1` FOREIGN KEY (`hospital_id`) REFERENCES `hospitals` (`hospital_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departments`
--

LOCK TABLES `departments` WRITE;
/*!40000 ALTER TABLE `departments` DISABLE KEYS */;
INSERT INTO `departments` VALUES (1,1,'Emergency',50,10,20,'2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(2,1,'Cardiology',40,15,5,'2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(3,1,'Orthopedics',35,12,3,'2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(4,1,'Pediatrics',45,18,8,'2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(5,2,'General Medicine',60,25,10,'2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(6,3,'ICU',30,5,15,'2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(7,3,'Surgery',40,10,5,'2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(103,1,'Pulmonology',10,5,NULL,'2026-01-19 13:20:36','2026-01-19 13:20:36',NULL,'2026-01-19 13:20:36');
/*!40000 ALTER TABLE `departments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(28,'admissions','admissionrule'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(15,'authentication','admission'),(17,'authentication','appointment'),(23,'authentication','auditlog'),(14,'authentication','bed'),(19,'authentication','billing'),(10,'authentication','department'),(12,'authentication','doctor'),(22,'authentication','financialtransaction'),(9,'authentication','hospital'),(20,'authentication','inventoryitem'),(21,'authentication','inventoryusage'),(31,'authentication','opdqueue'),(13,'authentication','patient'),(11,'authentication','staffuser'),(18,'authentication','treatment'),(16,'authentication','visit'),(5,'contenttypes','contenttype'),(30,'interhospital','capacitysnapshot'),(29,'interhospital','hospital'),(26,'inventory','inventorycategory'),(27,'inventory','inventorytransaction'),(24,'opd','opdqueue'),(25,'opd','opdstatistics'),(32,'receptionist','receptionistdashboardview'),(6,'sessions','session'),(7,'token_blacklist','blacklistedtoken'),(8,'token_blacklist','outstandingtoken');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2026-01-19 13:19:36.845732'),(2,'auth','0001_initial','2026-01-19 13:19:37.447024'),(3,'admin','0001_initial','2026-01-19 13:19:37.574398'),(4,'admin','0002_logentry_remove_auto_add','2026-01-19 13:19:37.580985'),(5,'admin','0003_logentry_add_action_flag_choices','2026-01-19 13:19:37.585996'),(6,'contenttypes','0002_remove_content_type_name','2026-01-19 13:19:37.698806'),(7,'auth','0002_alter_permission_name_max_length','2026-01-19 13:19:37.767491'),(8,'auth','0003_alter_user_email_max_length','2026-01-19 13:19:37.793750'),(9,'auth','0004_alter_user_username_opts','2026-01-19 13:19:37.802895'),(10,'auth','0005_alter_user_last_login_null','2026-01-19 13:19:37.871678'),(11,'auth','0006_require_contenttypes_0002','2026-01-19 13:19:37.875685'),(12,'auth','0007_alter_validators_add_error_messages','2026-01-19 13:19:37.883414'),(13,'auth','0008_alter_user_username_max_length','2026-01-19 13:19:37.951646'),(14,'auth','0009_alter_user_last_name_max_length','2026-01-19 13:19:38.029742'),(15,'auth','0010_alter_group_name_max_length','2026-01-19 13:19:38.051434'),(16,'auth','0011_update_proxy_permissions','2026-01-19 13:19:38.070038'),(17,'auth','0012_alter_user_first_name_max_length','2026-01-19 13:19:38.137302'),(18,'sessions','0001_initial','2026-01-19 13:19:38.167577'),(19,'token_blacklist','0001_initial','2026-01-19 13:19:38.345371'),(20,'token_blacklist','0002_outstandingtoken_jti_hex','2026-01-19 13:19:38.407602'),(21,'token_blacklist','0003_auto_20171017_2007','2026-01-19 13:19:38.435800'),(22,'token_blacklist','0004_auto_20171017_2013','2026-01-19 13:19:38.506895'),(23,'token_blacklist','0005_remove_outstandingtoken_jti','2026-01-19 13:19:38.570741'),(24,'token_blacklist','0006_auto_20171017_2113','2026-01-19 13:19:38.598838'),(25,'token_blacklist','0007_auto_20171017_2214','2026-01-19 13:19:38.797225'),(26,'token_blacklist','0008_migrate_to_bigautofield','2026-01-19 13:19:39.033705'),(27,'token_blacklist','0010_fix_migrate_to_bigautofield','2026-01-19 13:19:39.043304'),(28,'token_blacklist','0011_linearizes_history','2026-01-19 13:19:39.046304'),(29,'token_blacklist','0012_alter_outstandingtoken_user','2026-01-19 13:19:39.052860'),(30,'token_blacklist','0013_alter_blacklistedtoken_options_and_more','2026-01-19 13:19:39.063475'),(31,'admissions','0001_initial','2026-01-19 13:20:22.174829'),(32,'inventory','0001_initial','2026-01-19 13:20:22.258733'),(33,'opd','0001_initial','2026-01-19 13:20:22.348997'),(34,'opd','0002_delete_opdqueue','2026-01-20 10:33:35.000267');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctors`
--

DROP TABLE IF EXISTS `doctors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctors` (
  `doctor_id` int NOT NULL,
  `specialization` varchar(100) DEFAULT NULL,
  `years_experience` int DEFAULT NULL,
  `admin_id` int DEFAULT NULL,
  `updated_timestamp` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`doctor_id`),
  CONSTRAINT `doctors_ibfk_1` FOREIGN KEY (`doctor_id`) REFERENCES `staff_users` (`staff_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctors`
--

LOCK TABLES `doctors` WRITE;
/*!40000 ALTER TABLE `doctors` DISABLE KEYS */;
INSERT INTO `doctors` VALUES (2,'Cardiology',10,NULL,'2026-01-19 18:17:53'),(6,'General Practitioner',5,NULL,'2026-01-19 18:17:53'),(7,'Critical Care',8,NULL,'2026-01-19 18:17:53');
/*!40000 ALTER TABLE `doctors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `financial_transactions`
--

DROP TABLE IF EXISTS `financial_transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `financial_transactions` (
  `transaction_id` int NOT NULL,
  `hospital_id` int DEFAULT NULL,
  `reference_type` enum('Billing','Inventory','Salary','Maintenance','Other') DEFAULT NULL,
  `reference_id` int DEFAULT NULL,
  `transaction_type` enum('INCOME','EXPENSE') DEFAULT NULL,
  `amount` decimal(12,2) DEFAULT NULL,
  `payment_method` enum('Cash','Card','Insurance','UPI','Bank') DEFAULT NULL,
  `description` text,
  `transaction_date` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `admin_id` int DEFAULT NULL,
  `updated_timestamp` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`transaction_id`),
  KEY `hospital_id` (`hospital_id`),
  CONSTRAINT `financial_transactions_ibfk_1` FOREIGN KEY (`hospital_id`) REFERENCES `hospitals` (`hospital_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `financial_transactions`
--

LOCK TABLES `financial_transactions` WRITE;
/*!40000 ALTER TABLE `financial_transactions` DISABLE KEYS */;
INSERT INTO `financial_transactions` VALUES (1,1,'Billing',1,'INCOME',1500.00,'Card','Patient billing payment','2024-06-15 11:00:00','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(2,1,'Billing',2,'INCOME',800.00,'Insurance','Insurance claim settled','2024-06-16 15:00:00','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(3,2,'Inventory',1,'EXPENSE',50000.00,'Bank','Medicine stock purchase','2024-06-17 10:00:00','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(4,1,'Salary',NULL,'EXPENSE',150000.00,'Bank','Monthly staff salary','2024-06-01 09:00:00','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(5,3,'Maintenance',NULL,'EXPENSE',25000.00,'Bank','Equipment maintenance','2024-06-20 14:00:00','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53');
/*!40000 ALTER TABLE `financial_transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `hospitals`
--

DROP TABLE IF EXISTS `hospitals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hospitals` (
  `hospital_id` int NOT NULL,
  `hospital_name` varchar(150) DEFAULT NULL,
  `region` enum('Urban','Rural') DEFAULT NULL,
  `facility_size_beds` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `admin_id` int DEFAULT NULL,
  `updated_timestamp` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`hospital_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hospitals`
--

LOCK TABLES `hospitals` WRITE;
/*!40000 ALTER TABLE `hospitals` DISABLE KEYS */;
INSERT INTO `hospitals` VALUES (1,'City General Hospital','Urban',500,'2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(2,'Rural Health Center','Rural',150,'2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(3,'Metro Medical Center','Urban',350,'2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53');
/*!40000 ALTER TABLE `hospitals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_inventorycategory`
--

DROP TABLE IF EXISTS `inventory_inventorycategory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_inventorycategory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_inventorycategory`
--

LOCK TABLES `inventory_inventorycategory` WRITE;
/*!40000 ALTER TABLE `inventory_inventorycategory` DISABLE KEYS */;
INSERT INTO `inventory_inventorycategory` VALUES (1,'Medicine','Pharmaceutical products','2026-01-19 13:20:42.647914'),(2,'Consumable','Medical consumables','2026-01-19 13:20:42.651952'),(3,'Equipment','Medical equipment','2026-01-19 13:20:42.655273');
/*!40000 ALTER TABLE `inventory_inventorycategory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_inventorytransaction`
--

DROP TABLE IF EXISTS `inventory_inventorytransaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_inventorytransaction` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `transaction_type` varchar(20) NOT NULL,
  `quantity` int NOT NULL,
  `reference` varchar(100) NOT NULL,
  `notes` longtext NOT NULL,
  `performed_by` varchar(200) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `item_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `inventory_inventoryt_item_id_35d8d850_fk_inventory` (`item_id`),
  CONSTRAINT `inventory_inventoryt_item_id_35d8d850_fk_inventory` FOREIGN KEY (`item_id`) REFERENCES `inventory_items` (`item_id`)
) ENGINE=InnoDB AUTO_INCREMENT=373 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_inventorytransaction`
--

LOCK TABLES `inventory_inventorytransaction` WRITE;
/*!40000 ALTER TABLE `inventory_inventorytransaction` DISABLE KEYS */;
INSERT INTO `inventory_inventorytransaction` VALUES (1,'out',17,'AUTO-1-2','Auto-generated usage for testing','System','2026-01-19 13:20:42.701163',1),(2,'out',5,'AUTO-1-3','Auto-generated usage for testing','System','2026-01-19 13:20:42.706175',1),(3,'out',19,'AUTO-1-5','Auto-generated usage for testing','System','2026-01-19 13:20:42.710182',1),(4,'out',20,'AUTO-1-6','Auto-generated usage for testing','System','2026-01-19 13:20:42.712702',1),(5,'out',5,'AUTO-1-7','Auto-generated usage for testing','System','2026-01-19 13:20:42.715709',1),(6,'out',7,'AUTO-1-8','Auto-generated usage for testing','System','2026-01-19 13:20:42.718702',1),(7,'out',5,'AUTO-1-9','Auto-generated usage for testing','System','2026-01-19 13:20:42.721869',1),(8,'out',20,'AUTO-1-12','Auto-generated usage for testing','System','2026-01-19 13:20:42.725867',1),(9,'out',6,'AUTO-1-13','Auto-generated usage for testing','System','2026-01-19 13:20:42.729548',1),(10,'out',6,'AUTO-1-14','Auto-generated usage for testing','System','2026-01-19 13:20:42.734148',1),(11,'out',16,'AUTO-1-15','Auto-generated usage for testing','System','2026-01-19 13:20:42.737147',1),(12,'out',18,'AUTO-1-17','Auto-generated usage for testing','System','2026-01-19 13:20:42.743182',1),(13,'out',8,'AUTO-1-18','Auto-generated usage for testing','System','2026-01-19 13:20:42.746170',1),(14,'out',19,'AUTO-1-20','Auto-generated usage for testing','System','2026-01-19 13:20:42.749910',1),(15,'out',8,'AUTO-1-21','Auto-generated usage for testing','System','2026-01-19 13:20:42.753021',1),(16,'out',9,'AUTO-1-22','Auto-generated usage for testing','System','2026-01-19 13:20:42.756516',1),(17,'out',5,'AUTO-1-24','Auto-generated usage for testing','System','2026-01-19 13:20:42.759022',1),(18,'out',19,'AUTO-1-25','Auto-generated usage for testing','System','2026-01-19 13:20:42.762115',1),(19,'out',15,'AUTO-1-26','Auto-generated usage for testing','System','2026-01-19 13:20:42.766130',1),(20,'out',18,'AUTO-1-29','Auto-generated usage for testing','System','2026-01-19 13:20:42.769644',1),(21,'out',5,'AUTO-2-1','Auto-generated usage for testing','System','2026-01-19 13:20:42.773460',2),(22,'out',14,'AUTO-2-2','Auto-generated usage for testing','System','2026-01-19 13:20:42.778458',2),(23,'out',14,'AUTO-2-3','Auto-generated usage for testing','System','2026-01-19 13:20:42.781495',2),(24,'out',20,'AUTO-2-5','Auto-generated usage for testing','System','2026-01-19 13:20:42.786064',2),(25,'out',5,'AUTO-2-8','Auto-generated usage for testing','System','2026-01-19 13:20:42.791973',2),(26,'out',7,'AUTO-2-11','Auto-generated usage for testing','System','2026-01-19 13:20:42.794961',2),(27,'out',14,'AUTO-2-12','Auto-generated usage for testing','System','2026-01-19 13:20:42.799088',2),(28,'out',16,'AUTO-2-13','Auto-generated usage for testing','System','2026-01-19 13:20:42.802910',2),(29,'out',13,'AUTO-2-14','Auto-generated usage for testing','System','2026-01-19 13:20:42.807909',2),(30,'out',6,'AUTO-2-15','Auto-generated usage for testing','System','2026-01-19 13:20:42.811033',2),(31,'out',11,'AUTO-2-16','Auto-generated usage for testing','System','2026-01-19 13:20:42.815316',2),(32,'out',20,'AUTO-2-17','Auto-generated usage for testing','System','2026-01-19 13:20:42.817597',2),(33,'out',13,'AUTO-2-19','Auto-generated usage for testing','System','2026-01-19 13:20:42.821691',2),(34,'out',8,'AUTO-2-20','Auto-generated usage for testing','System','2026-01-19 13:20:42.824719',2),(35,'out',7,'AUTO-2-21','Auto-generated usage for testing','System','2026-01-19 13:20:42.826719',2),(36,'out',17,'AUTO-2-23','Auto-generated usage for testing','System','2026-01-19 13:20:42.829729',2),(37,'out',5,'AUTO-2-24','Auto-generated usage for testing','System','2026-01-19 13:20:42.834130',2),(38,'out',9,'AUTO-2-25','Auto-generated usage for testing','System','2026-01-19 13:20:42.837142',2),(39,'out',8,'AUTO-2-26','Auto-generated usage for testing','System','2026-01-19 13:20:42.840937',2),(40,'out',13,'AUTO-2-29','Auto-generated usage for testing','System','2026-01-19 13:20:42.845145',2),(41,'out',16,'AUTO-2-30','Auto-generated usage for testing','System','2026-01-19 13:20:42.847424',2),(42,'out',8,'AUTO-3-1','Auto-generated usage for testing','System','2026-01-19 13:20:42.853597',3),(43,'out',12,'AUTO-3-2','Auto-generated usage for testing','System','2026-01-19 13:20:42.864583',3),(44,'out',8,'AUTO-3-4','Auto-generated usage for testing','System','2026-01-19 13:20:42.884386',3),(45,'out',10,'AUTO-3-5','Auto-generated usage for testing','System','2026-01-19 13:20:42.887384',3),(46,'out',11,'AUTO-3-7','Auto-generated usage for testing','System','2026-01-19 13:20:42.892940',3),(47,'out',19,'AUTO-3-8','Auto-generated usage for testing','System','2026-01-19 13:20:42.896444',3),(48,'out',11,'AUTO-3-9','Auto-generated usage for testing','System','2026-01-19 13:20:42.900972',3),(49,'out',11,'AUTO-3-10','Auto-generated usage for testing','System','2026-01-19 13:20:42.904481',3),(50,'out',17,'AUTO-3-12','Auto-generated usage for testing','System','2026-01-19 13:20:42.907492',3),(51,'out',9,'AUTO-3-13','Auto-generated usage for testing','System','2026-01-19 13:20:42.911543',3),(52,'out',12,'AUTO-3-14','Auto-generated usage for testing','System','2026-01-19 13:20:42.915557',3),(53,'out',16,'AUTO-3-15','Auto-generated usage for testing','System','2026-01-19 13:20:42.918673',3),(54,'out',14,'AUTO-3-16','Auto-generated usage for testing','System','2026-01-19 13:20:42.922707',3),(55,'out',18,'AUTO-3-17','Auto-generated usage for testing','System','2026-01-19 13:20:42.925712',3),(56,'out',11,'AUTO-3-21','Auto-generated usage for testing','System','2026-01-19 13:20:42.928717',3),(57,'out',11,'AUTO-3-22','Auto-generated usage for testing','System','2026-01-19 13:20:42.934266',3),(58,'out',11,'AUTO-3-23','Auto-generated usage for testing','System','2026-01-19 13:20:42.937286',3),(59,'out',15,'AUTO-3-24','Auto-generated usage for testing','System','2026-01-19 13:20:42.941318',3),(60,'out',18,'AUTO-3-26','Auto-generated usage for testing','System','2026-01-19 13:20:42.945340',3),(61,'out',18,'AUTO-3-27','Auto-generated usage for testing','System','2026-01-19 13:20:42.948865',3),(62,'out',12,'AUTO-3-28','Auto-generated usage for testing','System','2026-01-19 13:20:42.953918',3),(63,'out',10,'AUTO-3-29','Auto-generated usage for testing','System','2026-01-19 13:20:42.957915',3),(64,'out',7,'AUTO-3-30','Auto-generated usage for testing','System','2026-01-19 13:20:42.961434',3),(65,'out',16,'AUTO-4-1','Auto-generated usage for testing','System','2026-01-19 13:20:42.967194',4),(66,'out',11,'AUTO-4-2','Auto-generated usage for testing','System','2026-01-19 13:20:42.972770',4),(67,'out',6,'AUTO-4-3','Auto-generated usage for testing','System','2026-01-19 13:20:42.977778',4),(68,'out',19,'AUTO-4-4','Auto-generated usage for testing','System','2026-01-19 13:20:42.982344',4),(69,'out',15,'AUTO-4-5','Auto-generated usage for testing','System','2026-01-19 13:20:42.986351',4),(70,'out',20,'AUTO-4-6','Auto-generated usage for testing','System','2026-01-19 13:20:42.990373',4),(71,'out',19,'AUTO-4-9','Auto-generated usage for testing','System','2026-01-19 13:20:42.993920',4),(72,'out',15,'AUTO-4-10','Auto-generated usage for testing','System','2026-01-19 13:20:42.998944',4),(73,'out',19,'AUTO-4-11','Auto-generated usage for testing','System','2026-01-19 13:20:43.002983',4),(74,'out',14,'AUTO-4-13','Auto-generated usage for testing','System','2026-01-19 13:20:43.007984',4),(75,'out',17,'AUTO-4-15','Auto-generated usage for testing','System','2026-01-19 13:20:43.012873',4),(76,'out',18,'AUTO-4-16','Auto-generated usage for testing','System','2026-01-19 13:20:43.015878',4),(77,'out',20,'AUTO-4-17','Auto-generated usage for testing','System','2026-01-19 13:20:43.019526',4),(78,'out',15,'AUTO-4-18','Auto-generated usage for testing','System','2026-01-19 13:20:43.024572',4),(79,'out',14,'AUTO-4-20','Auto-generated usage for testing','System','2026-01-19 13:20:43.027574',4),(80,'out',11,'AUTO-4-21','Auto-generated usage for testing','System','2026-01-19 13:20:43.031648',4),(81,'out',16,'AUTO-4-25','Auto-generated usage for testing','System','2026-01-19 13:20:43.035656',4),(82,'out',7,'AUTO-4-26','Auto-generated usage for testing','System','2026-01-19 13:20:43.039657',4),(83,'out',9,'AUTO-4-28','Auto-generated usage for testing','System','2026-01-19 13:20:43.043701',4),(84,'out',5,'AUTO-4-29','Auto-generated usage for testing','System','2026-01-19 13:20:43.047690',4),(85,'out',16,'AUTO-4-30','Auto-generated usage for testing','System','2026-01-19 13:20:43.051254',4),(86,'out',16,'AUTO-5-6','Auto-generated usage for testing','System','2026-01-19 13:20:43.055258',5),(87,'out',17,'AUTO-5-7','Auto-generated usage for testing','System','2026-01-19 13:20:43.059780',5),(88,'out',15,'AUTO-5-9','Auto-generated usage for testing','System','2026-01-19 13:20:43.064150',5),(89,'out',19,'AUTO-5-11','Auto-generated usage for testing','System','2026-01-19 13:20:43.068664',5),(90,'out',10,'AUTO-5-13','Auto-generated usage for testing','System','2026-01-19 13:20:43.073707',5),(91,'out',11,'AUTO-5-15','Auto-generated usage for testing','System','2026-01-19 13:20:43.077706',5),(92,'out',13,'AUTO-5-16','Auto-generated usage for testing','System','2026-01-19 13:20:43.080743',5),(93,'out',8,'AUTO-5-18','Auto-generated usage for testing','System','2026-01-19 13:20:43.083767',5),(94,'out',7,'AUTO-5-19','Auto-generated usage for testing','System','2026-01-19 13:20:43.086758',5),(95,'out',20,'AUTO-5-20','Auto-generated usage for testing','System','2026-01-19 13:20:43.090261',5),(96,'out',11,'AUTO-5-21','Auto-generated usage for testing','System','2026-01-19 13:20:43.092796',5),(97,'out',10,'AUTO-5-22','Auto-generated usage for testing','System','2026-01-19 13:20:43.094794',5),(98,'out',20,'AUTO-5-23','Auto-generated usage for testing','System','2026-01-19 13:20:43.099854',5),(99,'out',9,'AUTO-5-24','Auto-generated usage for testing','System','2026-01-19 13:20:43.103374',5),(100,'out',7,'AUTO-5-25','Auto-generated usage for testing','System','2026-01-19 13:20:43.106377',5),(101,'out',15,'AUTO-5-26','Auto-generated usage for testing','System','2026-01-19 13:20:43.108884',5),(102,'out',7,'AUTO-5-27','Auto-generated usage for testing','System','2026-01-19 13:20:43.112047',5),(103,'out',7,'AUTO-5-28','Auto-generated usage for testing','System','2026-01-19 13:20:43.115033',5),(104,'out',9,'AUTO-5-29','Auto-generated usage for testing','System','2026-01-19 13:20:43.118046',5),(105,'out',18,'AUTO-6-1','Auto-generated usage for testing','System','2026-01-19 13:20:43.121048',6),(106,'out',10,'AUTO-6-2','Auto-generated usage for testing','System','2026-01-19 13:20:43.124243',6),(107,'out',14,'AUTO-6-3','Auto-generated usage for testing','System','2026-01-19 13:20:43.127245',6),(108,'out',16,'AUTO-6-5','Auto-generated usage for testing','System','2026-01-19 13:20:43.130841',6),(109,'out',16,'AUTO-6-6','Auto-generated usage for testing','System','2026-01-19 13:20:43.134848',6),(110,'out',7,'AUTO-6-8','Auto-generated usage for testing','System','2026-01-19 13:20:43.136850',6),(111,'out',20,'AUTO-6-9','Auto-generated usage for testing','System','2026-01-19 13:20:43.139357',6),(112,'out',19,'AUTO-6-10','Auto-generated usage for testing','System','2026-01-19 13:20:43.143375',6),(113,'out',13,'AUTO-6-11','Auto-generated usage for testing','System','2026-01-19 13:20:43.146393',6),(114,'out',5,'AUTO-6-12','Auto-generated usage for testing','System','2026-01-19 13:20:43.149908',6),(115,'out',8,'AUTO-6-13','Auto-generated usage for testing','System','2026-01-19 13:20:43.152919',6),(116,'out',15,'AUTO-6-14','Auto-generated usage for testing','System','2026-01-19 13:20:43.155924',6),(117,'out',20,'AUTO-6-15','Auto-generated usage for testing','System','2026-01-19 13:20:43.158936',6),(118,'out',8,'AUTO-6-18','Auto-generated usage for testing','System','2026-01-19 13:20:43.162128',6),(119,'out',17,'AUTO-6-19','Auto-generated usage for testing','System','2026-01-19 13:20:43.166472',6),(120,'out',13,'AUTO-6-21','Auto-generated usage for testing','System','2026-01-19 13:20:43.171487',6),(121,'out',19,'AUTO-6-23','Auto-generated usage for testing','System','2026-01-19 13:20:43.175646',6),(122,'out',19,'AUTO-6-24','Auto-generated usage for testing','System','2026-01-19 13:20:43.178666',6),(123,'out',12,'AUTO-6-26','Auto-generated usage for testing','System','2026-01-19 13:20:43.182766',6),(124,'out',17,'AUTO-6-27','Auto-generated usage for testing','System','2026-01-19 13:20:43.185232',6),(125,'out',15,'AUTO-6-28','Auto-generated usage for testing','System','2026-01-19 13:20:43.188750',6),(126,'out',19,'AUTO-7-2','Auto-generated usage for testing','System','2026-01-19 13:20:43.191804',7),(127,'out',16,'AUTO-7-3','Auto-generated usage for testing','System','2026-01-19 13:20:43.194799',7),(128,'out',11,'AUTO-7-5','Auto-generated usage for testing','System','2026-01-19 13:20:43.198820',7),(129,'out',16,'AUTO-7-6','Auto-generated usage for testing','System','2026-01-19 13:20:43.203105',7),(130,'out',9,'AUTO-7-8','Auto-generated usage for testing','System','2026-01-19 13:20:43.207102',7),(131,'out',17,'AUTO-7-9','Auto-generated usage for testing','System','2026-01-19 13:20:43.210639',7),(132,'out',11,'AUTO-7-11','Auto-generated usage for testing','System','2026-01-19 13:20:43.214665',7),(133,'out',19,'AUTO-7-13','Auto-generated usage for testing','System','2026-01-19 13:20:43.217654',7),(134,'out',19,'AUTO-7-14','Auto-generated usage for testing','System','2026-01-19 13:20:43.220626',7),(135,'out',20,'AUTO-7-15','Auto-generated usage for testing','System','2026-01-19 13:20:43.223643',7),(136,'out',14,'AUTO-7-16','Auto-generated usage for testing','System','2026-01-19 13:20:43.226641',7),(137,'out',12,'AUTO-7-17','Auto-generated usage for testing','System','2026-01-19 13:20:43.229661',7),(138,'out',19,'AUTO-7-19','Auto-generated usage for testing','System','2026-01-19 13:20:43.234103',7),(139,'out',10,'AUTO-7-20','Auto-generated usage for testing','System','2026-01-19 13:20:43.237123',7),(140,'out',13,'AUTO-7-24','Auto-generated usage for testing','System','2026-01-19 13:20:43.241722',7),(141,'out',15,'AUTO-7-25','Auto-generated usage for testing','System','2026-01-19 13:20:43.244711',7),(142,'out',12,'AUTO-7-27','Auto-generated usage for testing','System','2026-01-19 13:20:43.247724',7),(143,'out',15,'AUTO-7-29','Auto-generated usage for testing','System','2026-01-19 13:20:43.250780',7),(144,'out',20,'AUTO-7-30','Auto-generated usage for testing','System','2026-01-19 13:20:43.253309',7),(145,'out',5,'AUTO-8-1','Auto-generated usage for testing','System','2026-01-19 13:20:43.257297',8),(146,'out',10,'AUTO-8-2','Auto-generated usage for testing','System','2026-01-19 13:20:43.260832',8),(147,'out',16,'AUTO-8-3','Auto-generated usage for testing','System','2026-01-19 13:20:43.264540',8),(148,'out',10,'AUTO-8-4','Auto-generated usage for testing','System','2026-01-19 13:20:43.268679',8),(149,'out',9,'AUTO-8-5','Auto-generated usage for testing','System','2026-01-19 13:20:43.272675',8),(150,'out',14,'AUTO-8-6','Auto-generated usage for testing','System','2026-01-19 13:20:43.275675',8),(151,'out',20,'AUTO-8-7','Auto-generated usage for testing','System','2026-01-19 13:20:43.278140',8),(152,'out',14,'AUTO-8-9','Auto-generated usage for testing','System','2026-01-19 13:20:43.280639',8),(153,'out',6,'AUTO-8-10','Auto-generated usage for testing','System','2026-01-19 13:20:43.284003',8),(154,'out',19,'AUTO-8-11','Auto-generated usage for testing','System','2026-01-19 13:20:43.287010',8),(155,'out',9,'AUTO-8-13','Auto-generated usage for testing','System','2026-01-19 13:20:43.289520',8),(156,'out',6,'AUTO-8-15','Auto-generated usage for testing','System','2026-01-19 13:20:43.292032',8),(157,'out',12,'AUTO-8-16','Auto-generated usage for testing','System','2026-01-19 13:20:43.294847',8),(158,'out',6,'AUTO-8-18','Auto-generated usage for testing','System','2026-01-19 13:20:43.298878',8),(159,'out',13,'AUTO-8-21','Auto-generated usage for testing','System','2026-01-19 13:20:43.302034',8),(160,'out',20,'AUTO-8-22','Auto-generated usage for testing','System','2026-01-19 13:20:43.306328',8),(161,'out',8,'AUTO-8-25','Auto-generated usage for testing','System','2026-01-19 13:20:43.309858',8),(162,'out',17,'AUTO-8-26','Auto-generated usage for testing','System','2026-01-19 13:20:43.311819',8),(163,'out',7,'AUTO-8-27','Auto-generated usage for testing','System','2026-01-19 13:20:43.315836',8),(164,'out',16,'AUTO-8-28','Auto-generated usage for testing','System','2026-01-19 13:20:43.318593',8),(165,'out',18,'AUTO-8-30','Auto-generated usage for testing','System','2026-01-19 13:20:43.320607',8),(166,'out',8,'AUTO-9-2','Auto-generated usage for testing','System','2026-01-19 13:20:43.323622',9),(167,'out',10,'AUTO-9-3','Auto-generated usage for testing','System','2026-01-19 13:20:43.326618',9),(168,'out',12,'AUTO-9-4','Auto-generated usage for testing','System','2026-01-19 13:20:43.328613',9),(169,'out',10,'AUTO-9-5','Auto-generated usage for testing','System','2026-01-19 13:20:43.331784',9),(170,'out',10,'AUTO-9-6','Auto-generated usage for testing','System','2026-01-19 13:20:43.334791',9),(171,'out',15,'AUTO-9-7','Auto-generated usage for testing','System','2026-01-19 13:20:43.337856',9),(172,'out',18,'AUTO-9-10','Auto-generated usage for testing','System','2026-01-19 13:20:43.340912',9),(173,'out',8,'AUTO-9-11','Auto-generated usage for testing','System','2026-01-19 13:20:43.342917',9),(174,'out',13,'AUTO-9-15','Auto-generated usage for testing','System','2026-01-19 13:20:43.345916',9),(175,'out',14,'AUTO-9-16','Auto-generated usage for testing','System','2026-01-19 13:20:43.348921',9),(176,'out',14,'AUTO-9-18','Auto-generated usage for testing','System','2026-01-19 13:20:43.352012',9),(177,'out',20,'AUTO-9-19','Auto-generated usage for testing','System','2026-01-19 13:20:43.354012',9),(178,'out',11,'AUTO-9-20','Auto-generated usage for testing','System','2026-01-19 13:20:43.357011',9),(179,'out',15,'AUTO-9-22','Auto-generated usage for testing','System','2026-01-19 13:20:43.359012',9),(180,'out',6,'AUTO-9-23','Auto-generated usage for testing','System','2026-01-19 13:20:43.361386',9),(181,'out',16,'AUTO-9-25','Auto-generated usage for testing','System','2026-01-19 13:20:43.364411',9),(182,'out',8,'AUTO-9-27','Auto-generated usage for testing','System','2026-01-19 13:20:43.367416',9),(183,'out',10,'AUTO-9-28','Auto-generated usage for testing','System','2026-01-19 13:20:43.370437',9),(184,'out',19,'AUTO-9-29','Auto-generated usage for testing','System','2026-01-19 13:20:43.372981',9),(185,'out',8,'AUTO-10-1','Auto-generated usage for testing','System','2026-01-19 13:20:43.375987',10),(186,'out',5,'AUTO-10-3','Auto-generated usage for testing','System','2026-01-19 13:20:43.377987',10),(187,'out',11,'AUTO-10-4','Auto-generated usage for testing','System','2026-01-19 13:20:43.380736',10),(188,'out',18,'AUTO-10-6','Auto-generated usage for testing','System','2026-01-19 13:20:43.383742',10),(189,'out',10,'AUTO-10-8','Auto-generated usage for testing','System','2026-01-19 13:20:43.385702',10),(190,'out',12,'AUTO-10-9','Auto-generated usage for testing','System','2026-01-19 13:20:43.388691',10),(191,'out',12,'AUTO-10-10','Auto-generated usage for testing','System','2026-01-19 13:20:43.391039',10),(192,'out',15,'AUTO-10-11','Auto-generated usage for testing','System','2026-01-19 13:20:43.394275',10),(193,'out',11,'AUTO-10-13','Auto-generated usage for testing','System','2026-01-19 13:20:43.397785',10),(194,'out',9,'AUTO-10-14','Auto-generated usage for testing','System','2026-01-19 13:20:43.401810',10),(195,'out',8,'AUTO-10-15','Auto-generated usage for testing','System','2026-01-19 13:20:43.403810',10),(196,'out',17,'AUTO-10-16','Auto-generated usage for testing','System','2026-01-19 13:20:43.407810',10),(197,'out',16,'AUTO-10-17','Auto-generated usage for testing','System','2026-01-19 13:20:43.409972',10),(198,'out',12,'AUTO-10-18','Auto-generated usage for testing','System','2026-01-19 13:20:43.412060',10),(199,'out',10,'AUTO-10-19','Auto-generated usage for testing','System','2026-01-19 13:20:43.414774',10),(200,'out',16,'AUTO-10-20','Auto-generated usage for testing','System','2026-01-19 13:20:43.417763',10),(201,'out',11,'AUTO-10-21','Auto-generated usage for testing','System','2026-01-19 13:20:43.419299',10),(202,'out',12,'AUTO-10-22','Auto-generated usage for testing','System','2026-01-19 13:20:43.422821',10),(203,'out',6,'AUTO-10-23','Auto-generated usage for testing','System','2026-01-19 13:20:43.424808',10),(204,'out',20,'AUTO-10-24','Auto-generated usage for testing','System','2026-01-19 13:20:43.427808',10),(205,'out',8,'AUTO-10-25','Auto-generated usage for testing','System','2026-01-19 13:20:43.430316',10),(206,'out',7,'AUTO-10-26','Auto-generated usage for testing','System','2026-01-19 13:20:43.432834',10),(207,'out',20,'AUTO-10-27','Auto-generated usage for testing','System','2026-01-19 13:20:43.435833',10),(208,'out',19,'AUTO-10-28','Auto-generated usage for testing','System','2026-01-19 13:20:43.437833',10),(209,'out',12,'AUTO-10-30','Auto-generated usage for testing','System','2026-01-19 13:20:43.441757',10),(210,'out',11,'AUTO-11-3','Auto-generated usage for testing','System','2026-01-19 13:20:43.443997',11),(211,'out',5,'AUTO-11-5','Auto-generated usage for testing','System','2026-01-19 13:20:43.445924',11),(212,'out',10,'AUTO-11-7','Auto-generated usage for testing','System','2026-01-19 13:20:43.448914',11),(213,'out',19,'AUTO-11-8','Auto-generated usage for testing','System','2026-01-19 13:20:43.451532',11),(214,'out',12,'AUTO-11-9','Auto-generated usage for testing','System','2026-01-19 13:20:43.453532',11),(215,'out',9,'AUTO-11-10','Auto-generated usage for testing','System','2026-01-19 13:20:43.456530',11),(216,'out',7,'AUTO-11-11','Auto-generated usage for testing','System','2026-01-19 13:20:43.459035',11),(217,'out',12,'AUTO-11-12','Auto-generated usage for testing','System','2026-01-19 13:20:43.461560',11),(218,'out',11,'AUTO-11-13','Auto-generated usage for testing','System','2026-01-19 13:20:43.463094',11),(219,'out',19,'AUTO-11-14','Auto-generated usage for testing','System','2026-01-19 13:20:43.467623',11),(220,'out',14,'AUTO-11-15','Auto-generated usage for testing','System','2026-01-19 13:20:43.470650',11),(221,'out',14,'AUTO-11-16','Auto-generated usage for testing','System','2026-01-19 13:20:43.473665',11),(222,'out',14,'AUTO-11-17','Auto-generated usage for testing','System','2026-01-19 13:20:43.476644',11),(223,'out',6,'AUTO-11-19','Auto-generated usage for testing','System','2026-01-19 13:20:43.478652',11),(224,'out',16,'AUTO-11-21','Auto-generated usage for testing','System','2026-01-19 13:20:43.481699',11),(225,'out',16,'AUTO-11-23','Auto-generated usage for testing','System','2026-01-19 13:20:43.484707',11),(226,'out',17,'AUTO-11-24','Auto-generated usage for testing','System','2026-01-19 13:20:43.486709',11),(227,'out',10,'AUTO-11-25','Auto-generated usage for testing','System','2026-01-19 13:20:43.490761',11),(228,'out',11,'AUTO-11-28','Auto-generated usage for testing','System','2026-01-19 13:20:43.493777',11),(229,'out',18,'AUTO-12-1','Auto-generated usage for testing','System','2026-01-19 13:20:43.496273',12),(230,'out',14,'AUTO-12-2','Auto-generated usage for testing','System','2026-01-19 13:20:43.499795',12),(231,'out',14,'AUTO-12-6','Auto-generated usage for testing','System','2026-01-19 13:20:43.502884',12),(232,'out',14,'AUTO-12-7','Auto-generated usage for testing','System','2026-01-19 13:20:43.504875',12),(233,'out',9,'AUTO-12-8','Auto-generated usage for testing','System','2026-01-19 13:20:43.507874',12),(234,'out',19,'AUTO-12-9','Auto-generated usage for testing','System','2026-01-19 13:20:43.510925',12),(235,'out',15,'AUTO-12-10','Auto-generated usage for testing','System','2026-01-19 13:20:43.512936',12),(236,'out',11,'AUTO-12-11','Auto-generated usage for testing','System','2026-01-19 13:20:43.515829',12),(237,'out',8,'AUTO-12-12','Auto-generated usage for testing','System','2026-01-19 13:20:43.517829',12),(238,'out',14,'AUTO-12-13','Auto-generated usage for testing','System','2026-01-19 13:20:43.522013',12),(239,'out',10,'AUTO-12-14','Auto-generated usage for testing','System','2026-01-19 13:20:43.525023',12),(240,'out',16,'AUTO-12-16','Auto-generated usage for testing','System','2026-01-19 13:20:43.528018',12),(241,'out',6,'AUTO-12-17','Auto-generated usage for testing','System','2026-01-19 13:20:43.535607',12),(242,'out',7,'AUTO-12-18','Auto-generated usage for testing','System','2026-01-19 13:20:43.540603',12),(243,'out',16,'AUTO-12-20','Auto-generated usage for testing','System','2026-01-19 13:20:43.542757',12),(244,'out',6,'AUTO-12-21','Auto-generated usage for testing','System','2026-01-19 13:20:43.545782',12),(245,'out',10,'AUTO-12-22','Auto-generated usage for testing','System','2026-01-19 13:20:43.548782',12),(246,'out',17,'AUTO-12-26','Auto-generated usage for testing','System','2026-01-19 13:20:43.550644',12),(247,'out',14,'AUTO-12-27','Auto-generated usage for testing','System','2026-01-19 13:20:43.553649',12),(248,'out',11,'AUTO-12-28','Auto-generated usage for testing','System','2026-01-19 13:20:43.556649',12),(249,'out',10,'AUTO-12-30','Auto-generated usage for testing','System','2026-01-19 13:20:43.558653',12),(250,'out',12,'AUTO-13-2','Auto-generated usage for testing','System','2026-01-19 13:20:43.561747',13),(251,'out',12,'AUTO-13-6','Auto-generated usage for testing','System','2026-01-19 13:20:43.564758',13),(252,'out',5,'AUTO-13-8','Auto-generated usage for testing','System','2026-01-19 13:20:43.567772',13),(253,'out',16,'AUTO-13-9','Auto-generated usage for testing','System','2026-01-19 13:20:43.570807',13),(254,'out',11,'AUTO-13-10','Auto-generated usage for testing','System','2026-01-19 13:20:43.573825',13),(255,'out',18,'AUTO-13-11','Auto-generated usage for testing','System','2026-01-19 13:20:43.575828',13),(256,'out',19,'AUTO-13-12','Auto-generated usage for testing','System','2026-01-19 13:20:43.578826',13),(257,'out',20,'AUTO-13-13','Auto-generated usage for testing','System','2026-01-19 13:20:43.581387',13),(258,'out',18,'AUTO-13-14','Auto-generated usage for testing','System','2026-01-19 13:20:43.583396',13),(259,'out',19,'AUTO-13-15','Auto-generated usage for testing','System','2026-01-19 13:20:43.585402',13),(260,'out',15,'AUTO-13-16','Auto-generated usage for testing','System','2026-01-19 13:20:43.588906',13),(261,'out',7,'AUTO-13-17','Auto-generated usage for testing','System','2026-01-19 13:20:43.591948',13),(262,'out',17,'AUTO-13-18','Auto-generated usage for testing','System','2026-01-19 13:20:43.593948',13),(263,'out',20,'AUTO-13-20','Auto-generated usage for testing','System','2026-01-19 13:20:43.596444',13),(264,'out',17,'AUTO-13-21','Auto-generated usage for testing','System','2026-01-19 13:20:43.599959',13),(265,'out',10,'AUTO-13-23','Auto-generated usage for testing','System','2026-01-19 13:20:43.602486',13),(266,'out',11,'AUTO-13-24','Auto-generated usage for testing','System','2026-01-19 13:20:43.604477',13),(267,'out',20,'AUTO-13-25','Auto-generated usage for testing','System','2026-01-19 13:20:43.606487',13),(268,'out',15,'AUTO-13-26','Auto-generated usage for testing','System','2026-01-19 13:20:43.610000',13),(269,'out',8,'AUTO-13-27','Auto-generated usage for testing','System','2026-01-19 13:20:43.612515',13),(270,'out',15,'AUTO-13-28','Auto-generated usage for testing','System','2026-01-19 13:20:43.616012',13),(271,'out',12,'AUTO-14-1','Auto-generated usage for testing','System','2026-01-19 13:20:43.617491',14),(272,'out',5,'AUTO-14-4','Auto-generated usage for testing','System','2026-01-19 13:20:43.621011',14),(273,'out',5,'AUTO-14-5','Auto-generated usage for testing','System','2026-01-19 13:20:43.623522',14),(274,'out',11,'AUTO-14-6','Auto-generated usage for testing','System','2026-01-19 13:20:43.625521',14),(275,'out',20,'AUTO-14-8','Auto-generated usage for testing','System','2026-01-19 13:20:43.627521',14),(276,'out',18,'AUTO-14-9','Auto-generated usage for testing','System','2026-01-19 13:20:43.630558',14),(277,'out',9,'AUTO-14-10','Auto-generated usage for testing','System','2026-01-19 13:20:43.634583',14),(278,'out',16,'AUTO-14-11','Auto-generated usage for testing','System','2026-01-19 13:20:43.637308',14),(279,'out',20,'AUTO-14-12','Auto-generated usage for testing','System','2026-01-19 13:20:43.640828',14),(280,'out',9,'AUTO-14-14','Auto-generated usage for testing','System','2026-01-19 13:20:43.642984',14),(281,'out',11,'AUTO-14-15','Auto-generated usage for testing','System','2026-01-19 13:20:43.645980',14),(282,'out',19,'AUTO-14-16','Auto-generated usage for testing','System','2026-01-19 13:20:43.647976',14),(283,'out',18,'AUTO-14-17','Auto-generated usage for testing','System','2026-01-19 13:20:43.649977',14),(284,'out',18,'AUTO-14-18','Auto-generated usage for testing','System','2026-01-19 13:20:43.653088',14),(285,'out',10,'AUTO-14-19','Auto-generated usage for testing','System','2026-01-19 13:20:43.655086',14),(286,'out',10,'AUTO-14-23','Auto-generated usage for testing','System','2026-01-19 13:20:43.657085',14),(287,'out',13,'AUTO-14-24','Auto-generated usage for testing','System','2026-01-19 13:20:43.659602',14),(288,'out',12,'AUTO-14-25','Auto-generated usage for testing','System','2026-01-19 13:20:43.662668',14),(289,'out',18,'AUTO-14-26','Auto-generated usage for testing','System','2026-01-19 13:20:43.666074',14),(290,'out',7,'AUTO-14-27','Auto-generated usage for testing','System','2026-01-19 13:20:43.668074',14),(291,'out',10,'AUTO-14-30','Auto-generated usage for testing','System','2026-01-19 13:20:43.670587',14),(292,'out',6,'AUTO-15-1','Auto-generated usage for testing','System','2026-01-19 13:20:43.673597',15),(293,'out',6,'AUTO-15-2','Auto-generated usage for testing','System','2026-01-19 13:20:43.675353',15),(294,'out',20,'AUTO-15-4','Auto-generated usage for testing','System','2026-01-19 13:20:43.677352',15),(295,'out',18,'AUTO-15-6','Auto-generated usage for testing','System','2026-01-19 13:20:43.679861',15),(296,'out',16,'AUTO-15-7','Auto-generated usage for testing','System','2026-01-19 13:20:43.682906',15),(297,'out',5,'AUTO-15-8','Auto-generated usage for testing','System','2026-01-19 13:20:43.684905',15),(298,'out',19,'AUTO-15-9','Auto-generated usage for testing','System','2026-01-19 13:20:43.686905',15),(299,'out',8,'AUTO-15-10','Auto-generated usage for testing','System','2026-01-19 13:20:43.689958',15),(300,'out',14,'AUTO-15-11','Auto-generated usage for testing','System','2026-01-19 13:20:43.692357',15),(301,'out',9,'AUTO-15-12','Auto-generated usage for testing','System','2026-01-19 13:20:43.694344',15),(302,'out',7,'AUTO-15-13','Auto-generated usage for testing','System','2026-01-19 13:20:43.696851',15),(303,'out',19,'AUTO-15-14','Auto-generated usage for testing','System','2026-01-19 13:20:43.699972',15),(304,'out',17,'AUTO-15-16','Auto-generated usage for testing','System','2026-01-19 13:20:43.702076',15),(305,'out',7,'AUTO-15-17','Auto-generated usage for testing','System','2026-01-19 13:20:43.704661',15),(306,'out',15,'AUTO-15-19','Auto-generated usage for testing','System','2026-01-19 13:20:43.707667',15),(307,'out',6,'AUTO-15-20','Auto-generated usage for testing','System','2026-01-19 13:20:43.710164',15),(308,'out',7,'AUTO-15-21','Auto-generated usage for testing','System','2026-01-19 13:20:43.711683',15),(309,'out',7,'AUTO-15-22','Auto-generated usage for testing','System','2026-01-19 13:20:43.714690',15),(310,'out',7,'AUTO-15-25','Auto-generated usage for testing','System','2026-01-19 13:20:43.716684',15),(311,'out',9,'AUTO-15-26','Auto-generated usage for testing','System','2026-01-19 13:20:43.718683',15),(312,'out',17,'AUTO-16-1','Auto-generated usage for testing','System','2026-01-19 13:20:43.720984',16),(313,'out',18,'AUTO-16-2','Auto-generated usage for testing','System','2026-01-19 13:20:43.723995',16),(314,'out',9,'AUTO-16-3','Auto-generated usage for testing','System','2026-01-19 13:20:43.725995',16),(315,'out',17,'AUTO-16-4','Auto-generated usage for testing','System','2026-01-19 13:20:43.727991',16),(316,'out',8,'AUTO-16-5','Auto-generated usage for testing','System','2026-01-19 13:20:43.731570',16),(317,'out',6,'AUTO-16-8','Auto-generated usage for testing','System','2026-01-19 13:20:43.734579',16),(318,'out',10,'AUTO-16-9','Auto-generated usage for testing','System','2026-01-19 13:20:43.736581',16),(319,'out',6,'AUTO-16-10','Auto-generated usage for testing','System','2026-01-19 13:20:43.738580',16),(320,'out',15,'AUTO-16-12','Auto-generated usage for testing','System','2026-01-19 13:20:43.741881',16),(321,'out',18,'AUTO-16-13','Auto-generated usage for testing','System','2026-01-19 13:20:43.743902',16),(322,'out',11,'AUTO-16-15','Auto-generated usage for testing','System','2026-01-19 13:20:43.746714',16),(323,'out',16,'AUTO-16-16','Auto-generated usage for testing','System','2026-01-19 13:20:43.748776',16),(324,'out',19,'AUTO-16-17','Auto-generated usage for testing','System','2026-01-19 13:20:43.750878',16),(325,'out',5,'AUTO-16-19','Auto-generated usage for testing','System','2026-01-19 13:20:43.752891',16),(326,'out',18,'AUTO-16-20','Auto-generated usage for testing','System','2026-01-19 13:20:43.755889',16),(327,'out',12,'AUTO-16-21','Auto-generated usage for testing','System','2026-01-19 13:20:43.757890',16),(328,'out',8,'AUTO-16-24','Auto-generated usage for testing','System','2026-01-19 13:20:43.759413',16),(329,'out',7,'AUTO-16-25','Auto-generated usage for testing','System','2026-01-19 13:20:43.761480',16),(330,'out',16,'AUTO-16-26','Auto-generated usage for testing','System','2026-01-19 13:20:43.765008',16),(331,'out',18,'AUTO-16-27','Auto-generated usage for testing','System','2026-01-19 13:20:43.767630',16),(332,'out',20,'AUTO-16-28','Auto-generated usage for testing','System','2026-01-19 13:20:43.770643',16),(333,'out',20,'AUTO-16-29','Auto-generated usage for testing','System','2026-01-19 13:20:43.772648',16),(334,'out',6,'AUTO-16-30','Auto-generated usage for testing','System','2026-01-19 13:20:43.775649',16),(335,'out',20,'AUTO-17-4','Auto-generated usage for testing','System','2026-01-19 13:20:43.777649',17),(336,'out',11,'AUTO-17-5','Auto-generated usage for testing','System','2026-01-19 13:20:43.780649',17),(337,'out',5,'AUTO-17-7','Auto-generated usage for testing','System','2026-01-19 13:20:43.782861',17),(338,'out',12,'AUTO-17-11','Auto-generated usage for testing','System','2026-01-19 13:20:43.784862',17),(339,'out',15,'AUTO-17-12','Auto-generated usage for testing','System','2026-01-19 13:20:43.786861',17),(340,'out',11,'AUTO-17-13','Auto-generated usage for testing','System','2026-01-19 13:20:43.789927',17),(341,'out',13,'AUTO-17-15','Auto-generated usage for testing','System','2026-01-19 13:20:43.796448',17),(342,'out',20,'AUTO-17-16','Auto-generated usage for testing','System','2026-01-19 13:20:43.800551',17),(343,'out',12,'AUTO-17-17','Auto-generated usage for testing','System','2026-01-19 13:20:43.802556',17),(344,'out',14,'AUTO-17-18','Auto-generated usage for testing','System','2026-01-19 13:20:43.805556',17),(345,'out',13,'AUTO-17-19','Auto-generated usage for testing','System','2026-01-19 13:20:43.807556',17),(346,'out',5,'AUTO-17-21','Auto-generated usage for testing','System','2026-01-19 13:20:43.810611',17),(347,'out',10,'AUTO-17-24','Auto-generated usage for testing','System','2026-01-19 13:20:43.812617',17),(348,'out',9,'AUTO-17-26','Auto-generated usage for testing','System','2026-01-19 13:20:43.815616',17),(349,'out',14,'AUTO-17-27','Auto-generated usage for testing','System','2026-01-19 13:20:43.818616',17),(350,'out',11,'AUTO-17-29','Auto-generated usage for testing','System','2026-01-19 13:20:43.821415',17),(351,'out',11,'AUTO-18-1','Auto-generated usage for testing','System','2026-01-19 13:20:43.824427',18),(352,'out',7,'AUTO-18-2','Auto-generated usage for testing','System','2026-01-19 13:20:43.826420',18),(353,'out',19,'AUTO-18-4','Auto-generated usage for testing','System','2026-01-19 13:20:43.828940',18),(354,'out',6,'AUTO-18-6','Auto-generated usage for testing','System','2026-01-19 13:20:43.833410',18),(355,'out',7,'AUTO-18-7','Auto-generated usage for testing','System','2026-01-19 13:20:43.835409',18),(356,'out',20,'AUTO-18-9','Auto-generated usage for testing','System','2026-01-19 13:20:43.840939',18),(357,'out',20,'AUTO-18-12','Auto-generated usage for testing','System','2026-01-19 13:20:43.844010',18),(358,'out',11,'AUTO-18-13','Auto-generated usage for testing','System','2026-01-19 13:20:43.849012',18),(359,'out',19,'AUTO-18-14','Auto-generated usage for testing','System','2026-01-19 13:20:43.854914',18),(360,'out',20,'AUTO-18-15','Auto-generated usage for testing','System','2026-01-19 13:20:43.858923',18),(361,'out',6,'AUTO-18-16','Auto-generated usage for testing','System','2026-01-19 13:20:43.865022',18),(362,'out',14,'AUTO-18-17','Auto-generated usage for testing','System','2026-01-19 13:20:43.869034',18),(363,'out',19,'AUTO-18-18','Auto-generated usage for testing','System','2026-01-19 13:20:43.874065',18),(364,'out',8,'AUTO-18-19','Auto-generated usage for testing','System','2026-01-19 13:20:43.877073',18),(365,'out',7,'AUTO-18-20','Auto-generated usage for testing','System','2026-01-19 13:20:43.881605',18),(366,'out',20,'AUTO-18-22','Auto-generated usage for testing','System','2026-01-19 13:20:43.885598',18),(367,'out',17,'AUTO-18-25','Auto-generated usage for testing','System','2026-01-19 13:20:43.890113',18),(368,'out',17,'AUTO-18-26','Auto-generated usage for testing','System','2026-01-19 13:20:43.893638',18),(369,'out',19,'AUTO-18-27','Auto-generated usage for testing','System','2026-01-19 13:20:43.898653',18),(370,'out',5,'AUTO-18-28','Auto-generated usage for testing','System','2026-01-19 13:20:43.902712',18),(371,'out',11,'AUTO-18-29','Auto-generated usage for testing','System','2026-01-19 13:20:43.907711',18),(372,'out',10,'AUTO-18-30','Auto-generated usage for testing','System','2026-01-19 13:20:43.911758',18);
/*!40000 ALTER TABLE `inventory_inventorytransaction` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_items`
--

DROP TABLE IF EXISTS `inventory_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_items` (
  `item_id` int NOT NULL,
  `item_name` varchar(150) DEFAULT NULL,
  `category` enum('Medicine','Consumable','Equipment') DEFAULT NULL,
  `quantity_available` int DEFAULT NULL,
  `reorder_level` int DEFAULT NULL,
  `supplier` varchar(150) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `admin_id` int DEFAULT NULL,
  `updated_timestamp` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `unit_price` decimal(10,2) DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_items`
--

LOCK TABLES `inventory_items` WRITE;
/*!40000 ALTER TABLE `inventory_items` DISABLE KEYS */;
INSERT INTO `inventory_items` VALUES (1,'Paracetamol 500mg','Medicine',5000,1000,'PharmaCorp Ltd','2026-01-19 18:17:53','2026-01-20 16:16:24',NULL,'2026-01-20 16:16:24',5.50,'2026-12-31'),(2,'Surgical Gloves','Consumable',2010,500,'MedSupply Inc','2026-01-19 18:17:53','2026-01-20 10:59:51',NULL,'2026-01-20 10:59:51',15.00,'2027-06-30'),(3,'Syringes 5ml','Consumable',3000,800,'MedSupply Inc','2026-01-19 18:17:53','2026-01-20 16:16:24',NULL,'2026-01-20 16:16:24',15.00,'2027-06-30'),(4,'Blood Pressure Monitor','Equipment',50,10,'MedEquip Solutions','2026-01-19 18:17:53','2026-01-20 16:55:38',NULL,'2026-01-20 16:55:38',250.00,'2027-06-30'),(5,'Amoxicillin 250mg','Medicine',3000,600,'PharmaCorp Ltd','2026-01-19 18:17:53','2026-01-20 16:16:24',NULL,'2026-01-20 16:16:24',5.50,'2026-12-31'),(6,'Bandages','Consumable',1500,300,'MedSupply Inc','2026-01-19 18:17:53','2026-01-20 16:16:24',NULL,'2026-01-20 16:16:24',15.00,'2027-06-30'),(7,'Oxygen Cylinder','Equipment',100,20,'OxyMed Systems','2026-01-19 18:17:53','2026-01-20 16:55:38',NULL,'2026-01-20 16:55:38',250.00,'2027-06-15'),(8,'Insulin Injection','Medicine',810,200,'PharmaCorp Ltd','2026-01-19 18:17:53','2026-01-20 10:49:03',NULL,'2026-01-20 10:49:03',5.50,'2026-12-31'),(9,'Paracetamol 500mg','Medicine',500,100,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-01-20 16:55:38',NULL,'2026-01-20 16:55:38',5.00,'2027-02-12'),(10,'Surgical Gloves (L)','Consumable',50,100,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-01-20 16:55:38',NULL,'2026-01-20 16:55:38',10.00,'2027-01-30'),(11,'IV Cannula 20G','Consumable',200,150,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-01-20 16:55:38',NULL,'2026-01-20 16:55:38',50.00,'2027-01-12'),(12,'Amoxicillin 250mg','Medicine',60,50,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-01-20 16:55:38',NULL,'2026-01-20 16:55:38',12.00,'2027-02-10'),(13,'Oxygen Mask','Equipment',75,30,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-01-20 16:55:38',NULL,'2026-01-20 16:55:38',132.00,'2026-12-11'),(14,'Surgical Sutures','Equipment',15,25,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-01-20 16:55:38',NULL,'2026-01-20 16:55:38',122.00,'2026-09-23'),(15,'Metformin 500mg','Medicine',80,100,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-01-20 16:55:38',NULL,'2026-01-20 16:55:38',11.00,'2026-12-04'),(16,'Azithromycin 250mg','Medicine',25,40,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-01-20 16:55:38',NULL,'2026-01-20 16:55:38',111.00,'2026-10-11'),(17,'Bandages','Consumable',300,100,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-01-20 16:55:38',NULL,'2026-01-20 16:55:38',23.00,'2026-07-15'),(18,'Syringes 5ml','Consumable',200,200,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-01-20 13:19:49',NULL,'2026-01-20 13:19:49',23.00,'2026-02-12'),(19,'Insulin Injection','Medicine',10,10,'Medical Supplies Inc.','2026-01-20 10:58:11','2026-01-20 10:58:11',NULL,'2026-01-20 10:58:11',4.97,'2026-02-20'),(20,'dolo655','Medicine',10,10,'PharmaCorp Ltd','2026-01-20 11:37:46','2026-01-20 11:37:46',NULL,'2026-01-20 11:37:46',10.00,'2026-01-31');
/*!40000 ALTER TABLE `inventory_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory_usage`
--

DROP TABLE IF EXISTS `inventory_usage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory_usage` (
  `usage_id` int NOT NULL,
  `item_id` int DEFAULT NULL,
  `patient_id` int DEFAULT NULL,
  `quantity_used` int DEFAULT NULL,
  `usage_date` datetime DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `admin_id` int DEFAULT NULL,
  `updated_timestamp` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`usage_id`),
  KEY `item_id` (`item_id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `inventory_usage_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `inventory_items` (`item_id`),
  CONSTRAINT `inventory_usage_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory_usage`
--

LOCK TABLES `inventory_usage` WRITE;
/*!40000 ALTER TABLE `inventory_usage` DISABLE KEYS */;
INSERT INTO `inventory_usage` VALUES (1,1,1,10,'2024-06-15 10:30:00','Cardiology','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(2,2,2,5,'2024-06-16 14:30:00','Emergency','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(3,3,3,2,'2024-06-17 11:30:00','General Medicine','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(4,5,4,7,'2024-06-18 17:00:00','Pediatrics','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(5,7,5,1,'2024-06-19 09:15:00','ICU','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53');
/*!40000 ALTER TABLE `inventory_usage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opd_opdstatistics`
--

DROP TABLE IF EXISTS `opd_opdstatistics`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `opd_opdstatistics` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `department` varchar(100) NOT NULL,
  `total_patients` int NOT NULL,
  `average_wait_time` double NOT NULL,
  `average_consultation_time` double NOT NULL,
  `peak_hour` int DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opd_opdstatistics_date_department_cf0509c2_uniq` (`date`,`department`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opd_opdstatistics`
--

LOCK TABLES `opd_opdstatistics` WRITE;
/*!40000 ALTER TABLE `opd_opdstatistics` DISABLE KEYS */;
/*!40000 ALTER TABLE `opd_opdstatistics` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `opd_queue`
--

DROP TABLE IF EXISTS `opd_queue`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `opd_queue` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `doctor_id` int NOT NULL COMMENT 'References staff_users.staff_id where role=Doctor',
  `department_id` int NOT NULL,
  `token_number` int NOT NULL,
  `status` enum('waiting','in_consultation','completed','cancelled') DEFAULT 'waiting',
  `priority` enum('normal','urgent','emergency') DEFAULT 'normal',
  `check_in_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `consultation_start_time` datetime DEFAULT NULL,
  `consultation_end_time` datetime DEFAULT NULL,
  `estimated_wait_time` int DEFAULT '0' COMMENT 'Estimated wait time in minutes',
  `notes` text,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `admin_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  KEY `department_id` (`department_id`),
  KEY `status_idx` (`status`),
  KEY `check_in_time_idx` (`check_in_time`),
  CONSTRAINT `opd_queue_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`) ON DELETE CASCADE,
  CONSTRAINT `opd_queue_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `staff_users` (`staff_id`),
  CONSTRAINT `opd_queue_ibfk_3` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opd_queue`
--

LOCK TABLES `opd_queue` WRITE;
/*!40000 ALTER TABLE `opd_queue` DISABLE KEYS */;
INSERT INTO `opd_queue` VALUES (1,1,2,2,1,'completed','normal','2026-01-19 08:00:00','2026-01-19 08:15:00','2026-01-19 08:30:00',15,'Regular cardiac checkup - James Miller','2026-01-19 22:58:12','2026-01-19 22:58:12',1),(2,2,6,5,2,'completed','normal','2026-01-19 08:30:00','2026-01-19 08:45:00','2026-01-19 09:00:00',15,'General consultation - Maria Garcia','2026-01-19 22:58:12','2026-01-19 22:58:12',1),(3,3,2,2,3,'in_consultation','urgent','2026-01-19 09:00:00','2026-01-19 09:05:00',NULL,5,'Urgent cardiac assessment - William Martinez','2026-01-19 22:58:12','2026-01-19 22:58:12',1),(4,4,6,5,4,'completed','normal','2026-01-19 09:15:00','2026-01-19 17:41:12','2026-01-19 17:41:14',20,'Follow-up consultation - Emma Rodriguez','2026-01-19 22:58:12','2026-01-19 22:58:12',1),(5,5,7,6,5,'waiting','emergency','2026-01-19 09:30:00',NULL,NULL,5,'Emergency ICU admission - Oliver Hernandez','2026-01-19 22:58:12','2026-01-19 22:58:12',1),(6,1,6,5,6,'waiting','normal','2026-01-19 09:45:00',NULL,NULL,5,'General medicine checkup - James Miller','2026-01-19 22:58:12','2026-01-19 23:41:48',1),(7,2,2,2,7,'waiting','normal','2026-01-19 10:00:00',NULL,NULL,17,'Routine cardiac monitoring - Maria Garcia','2026-01-19 22:58:12','2026-01-20 19:54:06',1),(10,3,7,6,3,'completed','urgent','2026-01-18 09:00:00','2026-01-18 09:10:00','2026-01-18 09:40:00',10,'ICU assessment - urgent case','2026-01-19 22:58:12','2026-01-19 22:58:12',1),(11,4,2,2,4,'completed','normal','2026-01-18 09:30:00','2026-01-18 09:50:00','2026-01-18 10:20:00',20,'Cardiac follow-up','2026-01-19 22:58:12','2026-01-19 22:58:12',1),(12,5,6,5,5,'completed','normal','2026-01-18 10:00:00','2026-01-18 10:20:00','2026-01-18 10:45:00',20,'General consultation','2026-01-19 22:58:12','2026-01-19 22:58:12',1),(18,1,6,5,1,'completed','normal','2026-01-16 08:00:00','2026-01-16 08:20:00','2026-01-16 08:45:00',20,'General medicine visit','2026-01-19 22:58:12','2026-01-19 22:58:12',1),(19,2,2,2,2,'completed','urgent','2026-01-16 08:30:00','2026-01-16 08:35:00','2026-01-16 09:15:00',5,'Urgent cardiology case','2026-01-19 22:58:12','2026-01-19 22:58:12',1),(20,3,6,5,3,'completed','normal','2026-01-16 09:00:00','2026-01-16 09:20:00','2026-01-16 09:50:00',20,'Regular checkup','2026-01-19 22:58:12','2026-01-19 22:58:12',1),(21,4,7,6,4,'completed','normal','2026-01-16 09:30:00','2026-01-16 09:55:00','2026-01-16 10:25:00',25,'ICU consultation','2026-01-19 22:58:12','2026-01-19 22:58:12',1),(22,20,2,1,8,'completed','normal','2026-01-19 17:38:04','2026-01-19 17:38:04','2026-01-19 17:38:04',15,'Test queue entry from integration test','2026-01-19 17:38:04',NULL,NULL),(23,21,6,5,9,'waiting','normal','2026-01-19 18:00:42',NULL,NULL,17,'','2026-01-19 18:00:42','2026-01-20 19:54:06',NULL),(24,22,6,5,10,'waiting','normal','2026-01-19 18:02:36',NULL,NULL,34,'','2026-01-19 18:02:36','2026-01-20 19:54:06',NULL);
/*!40000 ALTER TABLE `opd_queue` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients`
--

DROP TABLE IF EXISTS `patients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients` (
  `patient_id` int NOT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `gender` char(1) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `contact_number` varchar(20) DEFAULT NULL,
  `address` text,
  `registration_date` date DEFAULT NULL,
  `insurance_provider` varchar(100) DEFAULT NULL,
  `insurance_number` varchar(50) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `admin_id` int DEFAULT NULL,
  `updated_timestamp` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`patient_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients`
--

LOCK TABLES `patients` WRITE;
/*!40000 ALTER TABLE `patients` DISABLE KEYS */;
INSERT INTO `patients` VALUES (1,'James','Miller','M','1985-03-15','8765432101','123 Main St, City','2024-01-10','Health Plus','HP12345','james.m@email.com','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(2,'Maria','Garcia','F','1990-07-22','8765432102','456 Oak Ave, Town','2024-02-05','Care First','CF67890','maria.g@email.com','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(3,'William','Martinez','M','1978-11-30','8765432103','789 Pine Rd, Village','2024-03-12','Med Insurance','MI54321','william.m@email.com','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(4,'Emma','Rodriguez','F','2010-05-18','8765432104','321 Elm St, City','2024-04-20','Health Plus','HP98765','emma.r@email.com','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(5,'Oliver','Hernandez','M','1995-09-08','8765432105','654 Maple Dr, Town','2024-05-15',NULL,NULL,'oliver.h@email.com','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(6,'Test1','Patient1','M','1990-01-01','1234567891','Test Address','2026-01-19',NULL,NULL,'test1@patient.com','2026-01-19 13:19:28','2026-01-19 13:19:28',NULL,'2026-01-19 13:19:28'),(7,'Test2','Patient2','M','1990-01-01','1234567892','Test Address','2026-01-19',NULL,NULL,'test2@patient.com','2026-01-19 13:19:28','2026-01-19 13:19:28',NULL,'2026-01-19 13:19:28'),(8,'Test3','Patient3','M','1990-01-01','1234567893','Test Address','2026-01-19',NULL,NULL,'test3@patient.com','2026-01-19 13:19:28','2026-01-19 13:19:28',NULL,'2026-01-19 13:19:28'),(9,'Test4','Patient4','M','1990-01-01','1234567894','Test Address','2026-01-19',NULL,NULL,'test4@patient.com','2026-01-19 13:19:28','2026-01-19 13:19:28',NULL,'2026-01-19 13:19:28'),(10,'Test5','Patient5','M','1990-01-01','1234567895','Test Address','2026-01-19',NULL,NULL,'test5@patient.com','2026-01-19 13:19:28','2026-01-19 13:19:28',NULL,'2026-01-19 13:19:28'),(11,'Test6','Patient6','M','1990-01-01','1234567896','Test Address','2026-01-19',NULL,NULL,'test6@patient.com','2026-01-19 13:19:28','2026-01-19 13:19:28',NULL,'2026-01-19 13:19:28'),(12,'Test7','Patient7','M','1990-01-01','1234567897','Test Address','2026-01-19',NULL,NULL,'test7@patient.com','2026-01-19 13:19:28','2026-01-19 13:19:28',NULL,'2026-01-19 13:19:28'),(13,'Test1','Patient1','M','1990-01-01','1234567891','Test Address','2026-01-19',NULL,NULL,'test1@patient.com','2026-01-19 13:20:29','2026-01-19 13:20:29',NULL,'2026-01-19 13:20:29'),(14,'Test2','Patient2','M','1990-01-01','1234567892','Test Address','2026-01-19',NULL,NULL,'test2@patient.com','2026-01-19 13:20:29','2026-01-19 13:20:29',NULL,'2026-01-19 13:20:29'),(15,'Test3','Patient3','M','1990-01-01','1234567893','Test Address','2026-01-19',NULL,NULL,'test3@patient.com','2026-01-19 13:20:29','2026-01-19 13:20:29',NULL,'2026-01-19 13:20:29'),(16,'Test4','Patient4','M','1990-01-01','1234567894','Test Address','2026-01-19',NULL,NULL,'test4@patient.com','2026-01-19 13:20:29','2026-01-19 13:20:29',NULL,'2026-01-19 13:20:29'),(17,'Test5','Patient5','M','1990-01-01','1234567895','Test Address','2026-01-19',NULL,NULL,'test5@patient.com','2026-01-19 13:20:29','2026-01-19 13:20:29',NULL,'2026-01-19 13:20:29'),(18,'Test6','Patient6','M','1990-01-01','1234567896','Test Address','2026-01-19',NULL,NULL,'test6@patient.com','2026-01-19 13:20:29','2026-01-19 13:20:29',NULL,'2026-01-19 13:20:29'),(19,'Test7','Patient7','M','1990-01-01','1234567897','Test Address','2026-01-19',NULL,NULL,'test7@patient.com','2026-01-19 13:20:29','2026-01-19 13:20:29',NULL,'2026-01-19 13:20:29'),(20,'Test','Patient',NULL,NULL,'9999999999',NULL,'2026-01-19',NULL,NULL,NULL,'2026-01-19 17:38:04','2026-01-19 17:38:04',NULL,'2026-01-19 17:38:04'),(21,'textq','teststs',NULL,NULL,'7894512315',NULL,'2026-01-19',NULL,NULL,NULL,'2026-01-19 18:00:42','2026-01-19 18:00:42',NULL,'2026-01-19 18:00:42'),(22,'new','nw',NULL,NULL,'7894512333',NULL,'2026-01-19',NULL,NULL,NULL,'2026-01-19 18:02:36','2026-01-19 18:02:36',NULL,'2026-01-19 18:02:36');
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff_users`
--

DROP TABLE IF EXISTS `staff_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff_users` (
  `staff_id` int NOT NULL,
  `hospital_id` int DEFAULT NULL,
  `department_id` int DEFAULT NULL,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `role` enum('Doctor','Nurse','Admin','Receptionist','Pharmacist') DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `email` varchar(120) DEFAULT NULL,
  `password_hash` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `last_login` datetime DEFAULT NULL,
  `admin_id` int DEFAULT NULL,
  `updated_timestamp` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`staff_id`),
  UNIQUE KEY `email` (`email`),
  KEY `hospital_id` (`hospital_id`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `staff_users_ibfk_1` FOREIGN KEY (`hospital_id`) REFERENCES `hospitals` (`hospital_id`),
  CONSTRAINT `staff_users_ibfk_2` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff_users`
--

LOCK TABLES `staff_users` WRITE;
/*!40000 ALTER TABLE `staff_users` DISABLE KEYS */;
INSERT INTO `staff_users` VALUES (1,1,1,'Admin','User','Admin','9876543210','admin@hospital.com','pbkdf2_sha256$600000$DTjJTiaHj5EKehTFcOhn2R$XNewV6dsDfLOfohYviZVDyXVUZBgJ1uXi6oSQyX72mA=',1,'2026-01-19 18:17:53','2026-01-20 14:42:11',NULL,'2026-01-20 20:12:11'),(2,1,2,'John','Smith','Doctor','9876543211','john.smith@hospital.com','pbkdf2_sha256$600000$zYquOVSuIo64REx8fn2m0I$JBs0u/excyV2IYKO+xr7WLvpInwnvLoSwfDVG+n4dwM=',1,'2026-01-19 18:17:53','2026-01-20 13:22:38',NULL,'2026-01-20 18:52:37'),(3,1,2,'Sarah','Johnson','Nurse','9876543212','sarah.j@hospital.com','pbkdf2_sha256$600000$HnP9LPMUu0ZUtv3vjT5eLd$jTcRNEz/3SfgfeIoGkx4TIoZfxlzgTacEUEuN1JWajY=',1,'2026-01-19 18:17:53','2026-01-20 13:25:10',NULL,'2026-01-20 18:55:10'),(4,1,1,'Emily','Davis','Receptionist','9876543213','emily.d@hospital.com','pbkdf2_sha256$600000$DpJYNCirNGmhAVobUl5A4a$CgMfm2hTs5mHUtEmDeek0s21/Q/oYEk53B8FW2jlvak=',1,'2026-01-19 18:17:53','2026-01-20 14:41:13',NULL,'2026-01-20 20:11:12'),(5,1,3,'Michael','Brown','Pharmacist','9876543214','michael.b@hospital.com','pbkdf2_sha256$600000$AsQnxkeQrUjq6nlQpmAUft$BkTPl0/cQnJI4PXNUDLoJAuR6lblvRiJdCBp6wdyKaA=',1,'2026-01-19 18:17:53','2026-01-20 13:09:15',NULL,'2026-01-20 18:39:15'),(6,2,5,'David','Wilson','Doctor','9876543215','david.w@hospital.com','pbkdf2_sha256$600000$ysPNkTprI12DeZGOdSczLr$zgPPuYFCvW3oN0RhE7fIPoUviDkHKDu7kUYisxhjzXQ=',1,'2026-01-19 18:17:53',NULL,NULL,'2026-01-19 13:08:40'),(7,3,6,'Lisa','Anderson','Doctor','9876543216','lisa.a@hospital.com','pbkdf2_sha256$600000$gzYkLlXARznmwJ3tSHzCuN$M48ONFKKLhsVrBzLn5J06xEsde0o/v8UJFe24CXZENQ=',1,'2026-01-19 18:17:53',NULL,NULL,'2026-01-19 13:08:40'),(8,3,6,'Robert','Taylor','Nurse','9876543217','robert.t@hospital.com','pbkdf2_sha256$600000$q5o5rK0dToDQJGgt8KvcQT$2GW0Hk7B3YPo4wByBNsW/TWoSoRlH8O7fDnM9aUoQ7o=',1,'2026-01-19 18:17:53',NULL,NULL,'2026-01-19 13:08:40');
/*!40000 ALTER TABLE `staff_users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token_blacklist_blacklistedtoken`
--

DROP TABLE IF EXISTS `token_blacklist_blacklistedtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_blacklistedtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `blacklisted_at` datetime(6) NOT NULL,
  `token_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_id` (`token_id`),
  CONSTRAINT `token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk` FOREIGN KEY (`token_id`) REFERENCES `token_blacklist_outstandingtoken` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_blacklistedtoken`
--

LOCK TABLES `token_blacklist_blacklistedtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token_blacklist_outstandingtoken`
--

DROP TABLE IF EXISTS `token_blacklist_outstandingtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_outstandingtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` int DEFAULT NULL,
  `jti` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq` (`jti`),
  KEY `token_blacklist_outs_user_id_83bc629a_fk_auth_user` (`user_id`),
  CONSTRAINT `token_blacklist_outs_user_id_83bc629a_fk_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_outstandingtoken`
--

LOCK TABLES `token_blacklist_outstandingtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `treatments`
--

DROP TABLE IF EXISTS `treatments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `treatments` (
  `treatment_id` int NOT NULL,
  `appointment_id` int DEFAULT NULL,
  `treatment_type` varchar(100) DEFAULT NULL,
  `description` text,
  `cost` decimal(10,2) DEFAULT NULL,
  `treatment_date` date DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `admin_id` int DEFAULT NULL,
  `updated_timestamp` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`treatment_id`),
  KEY `appointment_id` (`appointment_id`),
  CONSTRAINT `treatments_ibfk_1` FOREIGN KEY (`appointment_id`) REFERENCES `appointments` (`appointment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `treatments`
--

LOCK TABLES `treatments` WRITE;
/*!40000 ALTER TABLE `treatments` DISABLE KEYS */;
INSERT INTO `treatments` VALUES (1,1,'ECG Test','Electrocardiogram to check heart rhythm',1500.00,'2024-06-15','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(2,2,'Blood Test','Complete blood count and lipid profile',800.00,'2024-06-16','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(3,3,'Consultation','General physician consultation',500.00,'2024-06-17','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(4,4,'Vaccination','DTaP booster shot',300.00,'2024-06-18','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(5,5,'X-Ray','Chest X-ray for injury assessment',1200.00,'2024-06-19','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53');
/*!40000 ALTER TABLE `treatments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visits`
--

DROP TABLE IF EXISTS `visits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `visits` (
  `visit_id` int NOT NULL,
  `patient_id` int DEFAULT NULL,
  `hospital_id` int DEFAULT NULL,
  `department_id` int DEFAULT NULL,
  `visit_datetime` datetime DEFAULT NULL,
  `day_of_week` varchar(20) DEFAULT NULL,
  `season` varchar(20) DEFAULT NULL,
  `time_of_day` varchar(20) DEFAULT NULL,
  `urgency_level` enum('Critical','High','Medium','Low') DEFAULT NULL,
  `nurse_patient_ratio` decimal(4,2) DEFAULT NULL,
  `specialist_availability` int DEFAULT NULL,
  `time_to_registration_min` int DEFAULT NULL,
  `time_to_triage_min` int DEFAULT NULL,
  `time_to_medical_professional_min` int DEFAULT NULL,
  `total_wait_time_min` int DEFAULT NULL,
  `patient_outcome` enum('Admitted','Discharged','Left Without Being Seen') DEFAULT NULL,
  `patient_satisfaction` int DEFAULT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `admin_id` int DEFAULT NULL,
  `updated_timestamp` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`visit_id`),
  KEY `patient_id` (`patient_id`),
  KEY `hospital_id` (`hospital_id`),
  KEY `department_id` (`department_id`),
  CONSTRAINT `visits_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`),
  CONSTRAINT `visits_ibfk_2` FOREIGN KEY (`hospital_id`) REFERENCES `hospitals` (`hospital_id`),
  CONSTRAINT `visits_ibfk_3` FOREIGN KEY (`department_id`) REFERENCES `departments` (`department_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visits`
--

LOCK TABLES `visits` WRITE;
/*!40000 ALTER TABLE `visits` DISABLE KEYS */;
INSERT INTO `visits` VALUES (1,1,1,2,'2024-06-15 09:30:00','Saturday','Summer','Morning','Medium',0.25,3,10,15,25,50,'Admitted',8,'2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(2,2,1,1,'2024-06-16 14:20:00','Sunday','Summer','Afternoon','High',0.30,5,5,10,15,30,'Discharged',9,'2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(3,3,2,5,'2024-06-17 11:00:00','Monday','Summer','Morning','Low',0.20,2,20,30,40,90,'Discharged',6,'2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(4,4,1,4,'2024-06-18 16:45:00','Tuesday','Summer','Evening','Critical',0.35,4,3,5,8,16,'Admitted',10,'2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(5,5,3,6,'2024-06-19 08:15:00','Wednesday','Summer','Morning','Critical',0.40,6,2,3,5,10,'Admitted',9,'2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53');
/*!40000 ALTER TABLE `visits` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-20 20:55:11
