-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: hospital_management
-- ------------------------------------------------------
-- Server version	8.0.43

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
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
INSERT INTO `admissions` VALUES (1,1,4,2,'2026-02-05 10:00:00','2026-02-12 13:25:20','High','Discharged','2026-02-05 09:17:53','2026-02-12 13:25:20',NULL,'2026-02-12 13:25:20'),(2,4,2,2,'2026-02-08 17:00:00','2026-02-20 11:30:00','Critical','Discharged','2026-02-08 16:17:53','2026-02-20 11:30:00',NULL,'2026-02-20 11:30:00'),(3,5,7,7,'2026-02-09 09:00:00','2026-02-15 14:45:00','Critical','Discharged','2026-02-09 08:17:53','2026-02-15 14:45:00',NULL,'2026-02-15 14:45:00'),(4,2,3,NULL,'2026-02-06 13:20:37','2026-02-06 17:57:03','High','Discharged','2026-02-06 13:20:37','2026-02-06 17:57:03',NULL,'2026-02-06 17:57:03'),(5,3,5,NULL,'2026-02-07 13:20:37','2026-02-14 13:25:57','High','Discharged','2026-02-07 13:20:37','2026-02-14 13:25:57',NULL,'2026-02-14 13:25:57'),(13,3,1,2,'2026-03-05 18:27:23',NULL,'High','Active','2026-03-05 18:27:23','2026-03-05 18:27:23',1,'2026-03-05 18:27:23'),(14,24,6,6,'2026-03-03 18:28:33','2026-03-04 11:29:31','Medium','Discharged','2026-03-03 18:28:33','2026-03-04 11:29:31',1,'2026-03-04 11:29:31'),(15,23,8,7,'2026-03-06 09:07:49',NULL,'Critical','Active','2026-03-06 09:07:48','2026-03-06 09:07:48',NULL,'2026-03-06 09:07:48');
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
INSERT INTO `appointments` VALUES (1,1,2,1,'2026-02-05','09:30:00','Chest pain','Completed','2026-02-05 09:15:00','2026-02-05 10:05:00',NULL,'2026-02-05 10:05:00'),(2,2,2,2,'2026-02-06','14:20:00','Heart checkup','Completed','2026-02-06 14:00:00','2026-02-06 15:10:00',NULL,'2026-02-06 15:10:00'),(3,3,6,3,'2026-02-07','11:00:00','Fever and cough','Completed','2026-02-07 10:45:00','2026-02-07 11:45:00',NULL,'2026-02-07 11:45:00'),(4,4,2,4,'2026-02-08','16:45:00','Vaccination','Completed','2026-02-08 16:30:00','2026-02-08 17:20:00',NULL,'2026-02-08 17:20:00'),(5,5,7,5,'2026-02-09','08:15:00','Accident injury','Completed','2026-02-09 08:00:00','2026-02-09 09:10:00',NULL,'2026-02-09 09:10:00'),(6,1,2,NULL,'2026-03-20','10:00:00','Follow-up checkup','Scheduled','2026-03-07 11:00:00','2026-03-07 11:00:00',NULL,'2026-03-07 11:00:00'),(7,23,7,NULL,'2026-02-20','10:55:00','Heart pain','Cancelled','2026-02-20 10:21:16','2026-02-20 10:46:10',NULL,'2026-02-20 10:46:10'),(8,24,6,NULL,'2026-02-22','11:30:00','Fever','Cancelled','2026-02-22 11:48:31','2026-02-22 11:49:59',NULL,'2026-02-22 11:49:59'),(9,25,7,NULL,'2026-02-24','09:39:00','Fever','Completed','2026-02-24 09:54:55','2026-02-24 10:30:20',NULL,'2026-02-24 10:30:20'),(10,26,6,NULL,'2026-03-01','10:12:00','Abdominal pain','Completed','2026-03-01 10:38:39','2026-03-01 11:39:18',NULL,'2026-03-01 11:39:18'),(11,27,7,NULL,'2026-03-01','10:15:00','Headache','Completed','2026-03-01 10:41:42','2026-03-01 11:42:01',NULL,'2026-03-01 11:42:01'),(12,28,2,NULL,'2026-03-02','09:35:00','Heart pain','Completed','2026-03-02 09:01:48','2026-03-02 10:02:17',NULL,'2026-03-02 10:02:17'),(13,29,2,NULL,'2026-03-03','09:40:00','Chest tightness','Completed','2026-03-03 09:08:48','2026-03-03 10:39:07',NULL,'2026-03-03 10:39:07'),(14,30,6,NULL,'2026-03-04','10:45:00','Joint pain','Completed','2026-03-04 10:15:06','2026-03-04 11:45:32',NULL,'2026-03-04 11:45:32'),(15,31,7,NULL,'2026-03-04','09:52:00','Back pain','Completed','2026-03-04 09:22:48','2026-03-04 10:53:15',NULL,'2026-03-04 10:53:15'),(16,32,7,NULL,'2026-03-05','10:04:00','Shoulder pain','Completed','2026-03-05 09:31:38','2026-03-05 11:02:15',NULL,'2026-03-05 11:02:15'),(17,23,6,NULL,'2026-03-05','09:05:00','General checkup','Completed','2026-03-05 09:35:10','2026-03-05 10:05:19',NULL,'2026-03-05 10:05:19'),(18,33,2,NULL,'2026-03-05','10:08:00','Chest pain','Completed','2026-03-05 09:38:26','2026-03-05 11:10:32',NULL,'2026-03-05 11:10:32'),(19,34,2,NULL,'2026-03-06','09:14:00','Palpitations','Completed','2026-03-06 08:44:48','2026-03-06 10:15:04',NULL,'2026-03-06 10:15:04'),(22,35,7,NULL,'2026-03-06','10:44:00','Dizziness','Completed','2026-03-06 10:14:49','2026-03-06 11:45:53',NULL,'2026-03-06 11:45:53'),(24,36,6,NULL,'2026-03-07','10:58:00','Vomiting and nausea','Completed','2026-03-07 10:30:20','2026-03-07 11:01:08',NULL,'2026-03-07 11:01:08');
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
INSERT INTO `beds` VALUES (1,3,6,'ICU','Occupied','2026-01-19 18:17:53','2026-03-05 18:27:23',NULL,'2026-03-05 18:27:23'),(2,3,3,'ICU','Available','2026-01-19 18:17:53','2026-02-20 11:30:00',NULL,'2026-02-20 11:30:00'),(3,1,2,'Normal','Available','2026-01-19 18:17:53','2026-02-06 17:57:03',NULL,'2026-02-06 17:57:03'),(4,1,2,'ICU','Available','2026-01-19 18:17:53','2026-02-12 13:25:20',NULL,'2026-02-12 13:25:20'),(5,1,3,'Normal','Available','2026-01-19 18:17:53','2026-02-14 13:25:57',NULL,'2026-02-14 13:25:57'),(6,2,5,'Normal','Maintenance','2026-01-19 18:17:53','2026-03-04 11:29:31',NULL,'2026-03-04 11:29:31'),(7,3,6,'ICU','Available','2026-01-19 18:17:53','2026-02-15 14:45:00',NULL,'2026-02-15 14:45:00'),(8,3,6,'Ventilator','Occupied','2026-01-19 18:17:53','2026-03-06 09:07:49',NULL,'2026-03-06 09:07:49'),(9,1,4,'Normal','Available','2026-01-19 18:17:53','2026-03-08 08:00:00',NULL,'2026-03-08 08:00:00'),(10,2,103,'Ventilator','Maintenance','2026-01-19 18:17:53','2026-02-20 14:42:37',NULL,'2026-02-20 14:42:37'),(11,1,5,'Normal','Available','2026-01-19 13:20:37','2026-03-08 08:00:00',NULL,'2026-03-08 08:00:00'),(12,1,5,'Normal','Available','2026-01-19 13:20:37','2026-03-08 08:00:00',NULL,'2026-03-08 08:00:00'),(13,1,5,'Normal','Available','2026-01-19 13:20:37','2026-03-08 08:00:00',NULL,'2026-03-08 08:00:00'),(14,1,2,'Normal','Available','2026-01-19 13:20:37','2026-03-08 08:00:00',NULL,'2026-03-08 08:00:00'),(15,1,2,'Normal','Available','2026-01-19 13:20:37','2026-03-08 08:00:00',NULL,'2026-03-08 08:00:00'),(16,1,2,'Normal','Maintenance','2026-01-19 13:20:37','2026-03-01 08:00:00',NULL,'2026-03-01 08:00:00'),(17,1,103,'Normal','Available','2026-01-19 13:20:37','2026-03-08 08:00:00',NULL,'2026-03-08 08:00:00'),(18,1,103,'Normal','Available','2026-01-19 13:20:37','2026-03-08 08:00:00',NULL,'2026-03-08 08:00:00'),(19,1,103,'Normal','Available','2026-01-19 13:20:37','2026-03-08 08:00:00',NULL,'2026-03-08 08:00:00'),(20,1,1,'Normal','Available','2026-01-19 13:20:37','2026-03-08 08:00:00',NULL,'2026-03-08 08:00:00'),(21,1,1,'Normal','Available','2026-01-19 13:20:37','2026-03-08 08:00:00',NULL,'2026-03-08 08:00:00'),(22,1,1,'Normal','Maintenance','2026-01-19 13:20:37','2026-03-01 08:00:00',NULL,'2026-03-01 08:00:00'),(50,2,7,'Ventilator','Available','2026-02-20 14:42:57','2026-02-20 14:42:57',NULL,'2026-02-20 14:42:57');
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
INSERT INTO `billing` VALUES (1,1,1,'2026-02-05',1500.00,'Card','Pending','2026-02-05 09:17:53','2026-02-05 09:17:53',NULL,'2026-02-05 09:17:53'),(2,2,2,'2026-02-06',800.00,'Insurance','Paid','2026-02-06 14:00:00','2026-02-06 14:00:00',NULL,'2026-02-06 14:00:00'),(3,3,3,'2026-02-07',500.00,'Cash','Pending','2026-02-07 10:45:00','2026-02-07 10:45:00',NULL,'2026-02-07 10:45:00'),(4,4,4,'2026-02-08',300.00,'Card','Paid','2026-02-08 16:30:00','2026-02-08 16:30:00',NULL,'2026-02-08 16:30:00'),(5,5,5,'2026-02-09',1200.00,'Card','Pending','2026-02-09 08:00:00','2026-03-07 09:29:07',NULL,'2026-03-07 09:29:07');
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
INSERT INTO `inventory_items` VALUES (1,'Paracetamol 500mg','Medicine',5000,1000,'PharmaCorp Ltd','2026-01-19 18:17:53','2026-02-20 16:16:24',NULL,'2026-02-20 16:16:24',5.50,'2027-12-31'),(2,'Surgical Gloves','Consumable',2010,500,'MedSupply Inc','2026-01-19 18:17:53','2026-02-20 10:59:51',NULL,'2026-02-20 10:59:51',15.00,'2027-06-30'),(3,'Syringes 5ml','Consumable',3000,800,'MedSupply Inc','2026-01-19 18:17:53','2026-02-20 16:16:24',NULL,'2026-02-20 16:16:24',15.00,'2027-06-30'),(4,'Blood Pressure Monitor','Equipment',50,10,'MedEquip Solutions','2026-01-19 18:17:53','2026-02-20 16:55:38',NULL,'2026-02-20 16:55:38',250.00,'2028-06-30'),(5,'Amoxicillin 250mg','Medicine',3000,600,'PharmaCorp Ltd','2026-01-19 18:17:53','2026-02-20 16:16:24',NULL,'2026-02-20 16:16:24',5.50,'2027-12-31'),(6,'Bandages','Consumable',1500,300,'MedSupply Inc','2026-01-19 18:17:53','2026-02-20 16:16:24',NULL,'2026-02-20 16:16:24',15.00,'2027-06-30'),(7,'Oxygen Cylinder','Equipment',100,20,'OxyMed Systems','2026-01-19 18:17:53','2026-02-20 16:55:38',NULL,'2026-02-20 16:55:38',250.00,'2028-06-15'),(8,'Insulin Injection','Medicine',810,200,'PharmaCorp Ltd','2026-01-19 18:17:53','2026-02-20 10:49:03',NULL,'2026-02-20 10:49:03',5.50,'2027-12-31'),(9,'Paracetamol 500mg','Medicine',500,100,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-02-20 16:55:38',NULL,'2026-02-20 16:55:38',5.00,'2027-12-12'),(10,'Surgical Gloves (L)','Consumable',200,100,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-02-20 16:55:38',NULL,'2026-02-20 16:55:38',10.00,'2028-01-30'),(11,'IV Cannula 20G','Consumable',200,150,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-02-20 16:55:38',NULL,'2026-02-20 16:55:38',50.00,'2028-01-12'),(12,'Amoxicillin 250mg','Medicine',60,50,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-02-20 16:55:38',NULL,'2026-02-20 16:55:38',12.00,'2027-12-10'),(13,'Oxygen Mask','Equipment',75,30,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-02-20 16:55:38',NULL,'2026-02-20 16:55:38',132.00,'2027-12-11'),(14,'Surgical Sutures','Equipment',15,25,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-02-20 16:55:38',NULL,'2026-02-20 16:55:38',122.00,'2027-09-23'),(15,'Metformin 500mg','Medicine',80,100,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-02-20 16:55:38',NULL,'2026-02-20 16:55:38',11.00,'2027-12-04'),(16,'Azithromycin 250mg','Medicine',25,40,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-02-20 16:55:38',NULL,'2026-02-20 16:55:38',111.00,'2027-10-11'),(17,'Bandages','Consumable',300,100,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-02-20 16:55:38',NULL,'2026-02-20 16:55:38',23.00,'2027-07-15'),(18,'Syringes 5ml','Consumable',200,200,'Medical Supplies Inc.','2026-01-19 13:20:43','2026-03-01 13:19:49',NULL,'2026-03-01 13:19:49',23.00,'2027-06-30'),(19,'Insulin Injection','Medicine',10,10,'Medical Supplies Inc.','2026-02-20 10:58:11','2026-03-01 10:58:11',NULL,'2026-03-01 10:58:11',4.97,'2027-06-30'),(20,'Dolo 650mg','Medicine',10,10,'PharmaCorp Ltd','2026-02-20 11:37:46','2026-03-01 11:37:46',NULL,'2026-03-01 11:37:46',10.00,'2027-12-31');
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
INSERT INTO `inventory_usage` VALUES (1,1,1,10,'2026-02-05 10:30:00','Cardiology','2026-02-05 09:17:53',NULL,'2026-02-05 09:17:53'),(2,2,2,5,'2026-02-06 14:30:00','Emergency','2026-02-06 14:00:00',NULL,'2026-02-06 14:00:00'),(3,3,3,2,'2026-02-07 11:30:00','General Medicine','2026-02-07 10:45:00',NULL,'2026-02-07 10:45:00'),(4,5,4,7,'2026-02-08 17:00:00','Pediatrics','2026-02-08 16:30:00',NULL,'2026-02-08 16:30:00'),(5,7,5,1,'2026-02-09 09:15:00','ICU','2026-02-09 08:00:00',NULL,'2026-02-09 08:00:00');
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
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `opd_queue`
--

LOCK TABLES `opd_queue` WRITE;
/*!40000 ALTER TABLE `opd_queue` DISABLE KEYS */;
INSERT INTO `opd_queue` VALUES (1,1,2,2,1,'completed','normal','2026-02-10 08:00:00','2026-02-10 08:15:00','2026-02-10 08:30:00',15,'Regular cardiac checkup - James Miller','2026-02-10 08:00:00','2026-02-10 08:30:00',1),(2,2,6,5,2,'completed','normal','2026-02-10 08:30:00','2026-02-10 08:45:00','2026-02-10 09:00:00',15,'General consultation - Maria Garcia','2026-02-10 08:30:00','2026-02-10 09:00:00',1),(3,3,2,2,3,'completed','urgent','2026-02-10 09:00:00','2026-02-10 09:05:00','2026-03-05 18:27:23',5,'Urgent cardiac assessment - William Martinez

Patient admitted to bed 1.','2026-02-10 09:00:00','2026-03-05 18:27:23',1),(4,4,6,5,4,'completed','normal','2026-02-10 09:15:00','2026-02-10 09:41:12','2026-02-10 09:41:14',20,'Follow-up consultation - Emma Rodriguez','2026-02-10 09:15:00','2026-02-10 09:41:14',1),(5,5,7,6,5,'completed','emergency','2026-02-10 09:30:00','2026-02-10 09:35:00','2026-02-10 10:00:00',5,'Emergency ICU admission - Oliver Hernandez','2026-02-10 09:30:00','2026-02-10 10:00:00',1),(6,1,6,5,6,'completed','normal','2026-02-10 09:45:00','2026-02-10 09:55:00','2026-02-10 10:25:00',5,'General medicine checkup - James Miller','2026-02-10 09:45:00','2026-02-10 10:25:00',1),(7,2,2,2,7,'completed','normal','2026-02-10 10:00:00','2026-02-10 10:10:00','2026-02-10 10:45:00',5,'Routine cardiac monitoring - Maria Garcia','2026-02-10 10:00:00','2026-02-10 10:45:00',1),(10,3,7,6,3,'completed','urgent','2026-02-08 09:00:00','2026-02-08 09:10:00','2026-02-08 09:40:00',10,'ICU assessment - urgent case','2026-02-08 09:00:00','2026-02-08 09:40:00',1),(11,4,2,2,4,'completed','normal','2026-02-08 09:30:00','2026-02-08 09:50:00','2026-02-08 10:20:00',20,'Cardiac follow-up','2026-02-08 09:30:00','2026-02-08 10:20:00',1),(12,5,6,5,5,'completed','normal','2026-02-08 10:00:00','2026-02-08 10:20:00','2026-02-08 10:45:00',20,'General consultation','2026-02-08 10:00:00','2026-02-08 10:45:00',1),(18,1,6,5,1,'completed','normal','2026-02-03 08:00:00','2026-02-03 08:20:00','2026-02-03 08:45:00',20,'General medicine visit','2026-02-03 08:00:00','2026-02-03 08:45:00',1),(19,2,2,2,2,'completed','urgent','2026-02-03 08:30:00','2026-02-03 08:35:00','2026-02-03 09:15:00',5,'Urgent cardiology case','2026-02-03 08:30:00','2026-02-03 09:15:00',1),(20,3,6,5,3,'completed','normal','2026-02-03 09:00:00','2026-02-03 09:20:00','2026-02-03 09:50:00',20,'Regular checkup','2026-02-03 09:00:00','2026-02-03 09:50:00',1),(21,4,7,6,4,'completed','normal','2026-02-03 09:30:00','2026-02-03 09:55:00','2026-02-03 10:25:00',25,'ICU consultation','2026-02-03 09:30:00','2026-02-03 10:25:00',1),(25,23,7,6,1,'completed','normal','2026-03-05 09:41:17','2026-03-05 09:56:25','2026-03-05 09:56:29',NULL,'Appointment approved: Heart pain',NULL,'2026-03-05 09:56:29',NULL),(26,23,7,6,1,'completed','normal','2026-03-05 10:45:59','2026-03-05 11:05:00',NULL,19,'Appointment approved: General checkup',NULL,'2026-03-05 11:05:00',NULL),(27,24,6,5,1,'completed','normal','2026-03-03 11:49:04','2026-03-03 12:28:16','2026-03-03 12:28:33',NULL,'Appointment approved: Fever

Patient admitted to bed 6.',NULL,'2026-03-03 12:28:33',NULL),(28,25,7,6,1,'completed','normal','2026-02-24 09:55:20','2026-02-24 10:05:00','2026-02-24 10:30:00',39,'Appointment approved: Fever','2026-02-24 09:55:20','2026-02-24 10:30:00',NULL),(29,23,7,6,1,'completed','normal','2026-03-06 07:55:03','2026-03-06 08:31:45','2026-03-06 09:07:49',NULL,'Appointment approved: Chest pain

Patient admitted to bed 8.','2026-03-06 07:55:03','2026-03-06 09:07:49',NULL),(30,35,7,6,1,'waiting','normal','2026-03-08 08:45:53',NULL,NULL,5,'Appointment approved: Dizziness','2026-03-08 08:45:53','2026-03-08 08:45:53',NULL),(31,33,7,6,1,'waiting','normal','2026-03-08 09:00:00',NULL,NULL,18,'Appointment approved: Chest pain','2026-03-08 09:00:00','2026-03-08 09:00:00',NULL),(32,36,6,5,1,'waiting','normal','2026-03-08 09:01:08',NULL,NULL,5,'Appointment approved: Vomiting and nausea','2026-03-08 09:01:08','2026-03-08 09:01:23',NULL);
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
INSERT INTO `patients` VALUES (1,'James','Miller','M','1985-03-15','8765432101','123 Main St, City','2024-01-10','Health Plus','HP12345','james.m@email.com','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(2,'Maria','Garcia','F','1990-07-22','8765432102','456 Oak Ave, Town','2024-02-05','Care First','CF67890','maria.g@email.com','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(3,'William','Martinez','M','1978-11-30','8765432103','789 Pine Rd, Village','2024-03-12','Med Insurance','MI54321','william.m@email.com','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(4,'Emma','Rodriguez','F','2010-05-18','8765432104','321 Elm St, City','2024-04-20','Health Plus','HP98765','emma.r@email.com','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(5,'Oliver','Hernandez','M','1995-09-08','8765432105','654 Maple Dr, Town','2024-05-15',NULL,NULL,'oliver.h@email.com','2026-01-19 18:17:53','2026-01-19 18:17:53',NULL,'2026-01-19 18:17:53'),(23,'Tushar','Verma','M','1998-07-06','7418529635','Sector 12, Mumbai','2026-02-01',NULL,NULL,'tushar.v@gmail.com','2026-02-01 09:21:16','2026-03-06 19:54:33',NULL,'2026-03-06 19:54:33'),(24,'Neha','Verma','F','2005-10-06','7418529634','42 Park Street, Delhi','2026-02-03',NULL,NULL,'neha.v@gmail.com','2026-02-03 10:48:31','2026-02-03 10:48:31',NULL,'2026-02-03 10:48:31'),(25,'Anjali','Shah','F','1999-06-20','9638527415','15 Rose Garden, Pune','2026-02-05',NULL,NULL,'anjali.s@gmail.com','2026-02-05 11:54:55','2026-02-05 11:54:55',NULL,'2026-02-05 11:54:55'),(26,'Rahul','Mehta','M','1988-10-20','9123964785','8 LB Nagar, Hyderabad','2026-02-07',NULL,NULL,'rahul.m@gmail.com','2026-02-07 14:38:39','2026-02-07 14:38:39',NULL,'2026-02-07 14:38:39'),(27,'Priya','Singh','F','2004-01-15','8529637415','23 MG Road, Bengaluru','2026-02-08',NULL,NULL,'priya.s@gmail.com','2026-02-08 12:41:42','2026-02-08 12:41:42',NULL,'2026-02-08 12:41:42'),(28,'Harsh','Singh','M','1993-01-21','9234567899','101 Lake View, Kolkata','2026-02-10',NULL,NULL,'harsh.s@gmail.com','2026-02-10 13:01:48','2026-02-10 13:01:48',NULL,'2026-02-10 13:01:48'),(29,'Suresh','Kumar','M','2002-02-23','7465896215','55 Gandhi Road, Chennai','2026-02-11',NULL,NULL,'suresh.k@gmail.com','2026-02-11 13:08:48','2026-02-11 13:08:48',NULL,'2026-02-11 13:08:48'),(30,'Sagar','Desai','M','1995-02-21','9234567890','7 Shivaji Nagar, Nagpur','2026-02-12',NULL,NULL,'sagar.d@gmail.com','2026-02-12 14:15:06','2026-02-12 14:15:06',NULL,'2026-02-12 14:15:06'),(31,'Divya','Patel','F','2000-02-22','7418529636','34 Civil Lines, Ahmedabad','2026-02-13',NULL,NULL,'divya.p@gmail.com','2026-02-13 10:22:48','2026-02-13 10:22:48',NULL,'2026-02-13 10:22:48'),(32,'Arjun','Nair','M','1999-11-22','7418529637','67 Residency Road, Kochi','2026-02-14',NULL,NULL,'arjun.n@gmail.com','2026-02-14 11:31:38','2026-02-14 11:31:38',NULL,'2026-02-14 11:31:38'),(33,'Tushar','Pandey','M','2001-02-22','8529637233','12 Vasant Vihar, Lucknow','2026-02-15',NULL,NULL,'tushar.p@gmail.com','2026-02-15 14:38:26','2026-02-15 15:15:26',NULL,'2026-02-15 15:15:26'),(34,'Jai','Sharma','M','2001-09-11','8529637415','90 Civil Hospital Road, Jaipur','2026-02-16',NULL,NULL,'jai.s@gmail.com','2026-02-16 10:44:48','2026-02-16 10:44:48',NULL,'2026-02-16 10:44:48'),(35,'Ajay','Reddy','M','2000-05-05','7465896212','45 SR Nagar, Hyderabad','2026-02-20',NULL,NULL,'ajay.r@gmail.com','2026-02-20 12:14:49','2026-02-20 12:14:49',NULL,'2026-02-20 12:14:49'),(36,'Kushal','Soni','M','2001-02-12','7467496215','78 Shastri Nagar, Indore','2026-03-01',NULL,NULL,'kushal.s@gmail.com','2026-03-01 08:30:20','2026-03-01 08:30:20',NULL,'2026-03-01 08:30:20');
/*!40000 ALTER TABLE `patients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_transactions`
--

DROP TABLE IF EXISTS `payment_transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_transactions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bill_id` int NOT NULL,
  `razorpay_order_id` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `razorpay_payment_id` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `razorpay_signature` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `currency` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT 'INR',
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'created',
  `payment_method` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `error_code` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `error_description` text COLLATE utf8mb4_unicode_ci,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `razorpay_order_id` (`razorpay_order_id`),
  KEY `idx_bill_id` (`bill_id`),
  KEY `idx_razorpay_order_id` (`razorpay_order_id`),
  KEY `idx_status` (`status`),
  KEY `idx_created_at` (`created_at`),
  CONSTRAINT `payment_transactions_ibfk_1` FOREIGN KEY (`bill_id`) REFERENCES `billing` (`bill_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='Stores Razorpay payment transaction details for billing';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_transactions`
--

LOCK TABLES `payment_transactions` WRITE;
/*!40000 ALTER TABLE `payment_transactions` DISABLE KEYS */;
INSERT INTO `payment_transactions` VALUES (1,5,'order_S6O6fW7KrCS67d','pay_S6O7biZVJxbMYQ','91f34de0a20e66ce8fbff34c613dfd36effee10756aea86b7c01c384885ba23f',1200.00,'INR','captured','card',NULL,NULL,'2026-01-20 22:25:58','2026-01-20 22:27:14');
/*!40000 ALTER TABLE `payment_transactions` ENABLE KEYS */;
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
INSERT INTO `staff_users` VALUES (1,1,1,'Admin','User','Admin','9876543210','admin@hospital.com','pbkdf2_sha256$600000$DTjJTiaHj5EKehTFcOhn2R$XNewV6dsDfLOfohYviZVDyXVUZBgJ1uXi6oSQyX72mA=',1,'2026-01-19 18:17:53','2026-01-21 03:30:32',NULL,'2026-01-21 09:00:31'),(2,1,2,'John','Smith','Doctor','9876543211','john.smith@hospital.com','pbkdf2_sha256$600000$zYquOVSuIo64REx8fn2m0I$JBs0u/excyV2IYKO+xr7WLvpInwnvLoSwfDVG+n4dwM=',1,'2026-01-19 18:17:53','2026-01-20 13:22:38',NULL,'2026-01-20 18:52:37'),(3,1,2,'Sarah','Johnson','Nurse','9876543212','sarah.j@hospital.com','pbkdf2_sha256$600000$HnP9LPMUu0ZUtv3vjT5eLd$jTcRNEz/3SfgfeIoGkx4TIoZfxlzgTacEUEuN1JWajY=',1,'2026-01-19 18:17:53','2026-01-20 17:27:39',NULL,'2026-01-20 22:57:38'),(4,1,1,'Emily','Davis','Receptionist','9876543213','emily.d@hospital.com','pbkdf2_sha256$600000$DpJYNCirNGmhAVobUl5A4a$CgMfm2hTs5mHUtEmDeek0s21/Q/oYEk53B8FW2jlvak=',1,'2026-01-19 18:17:53','2026-01-20 16:24:07',NULL,'2026-01-20 21:54:07'),(5,1,3,'Michael','Brown','Pharmacist','9876543214','michael.b@hospital.com','pbkdf2_sha256$600000$AsQnxkeQrUjq6nlQpmAUft$BkTPl0/cQnJI4PXNUDLoJAuR6lblvRiJdCBp6wdyKaA=',1,'2026-01-19 18:17:53','2026-01-20 13:09:15',NULL,'2026-01-20 18:39:15'),(6,2,5,'David','Wilson','Doctor','9876543215','david.w@hospital.com','pbkdf2_sha256$600000$ysPNkTprI12DeZGOdSczLr$zgPPuYFCvW3oN0RhE7fIPoUviDkHKDu7kUYisxhjzXQ=',1,'2026-01-19 18:17:53',NULL,NULL,'2026-01-19 13:08:40'),(7,3,6,'Lisa','Anderson','Doctor','9876543216','lisa.a@hospital.com','pbkdf2_sha256$600000$gzYkLlXARznmwJ3tSHzCuN$M48ONFKKLhsVrBzLn5J06xEsde0o/v8UJFe24CXZENQ=',1,'2026-01-19 18:17:53',NULL,NULL,'2026-01-19 13:08:40'),(8,3,6,'Robert','Taylor','Nurse','9876543217','robert.t@hospital.com','pbkdf2_sha256$600000$q5o5rK0dToDQJGgt8KvcQT$2GW0Hk7B3YPo4wByBNsW/TWoSoRlH8O7fDnM9aUoQ7o=',1,'2026-01-19 18:17:53',NULL,NULL,'2026-01-19 13:08:40');
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
INSERT INTO `treatments` VALUES (1,1,'ECG Test','Electrocardiogram to check heart rhythm',1500.00,'2026-02-05','2026-02-05 09:17:53','2026-02-05 09:17:53',NULL,'2026-02-05 09:17:53'),(2,2,'Blood Test','Complete blood count and lipid profile',800.00,'2026-02-06','2026-02-06 14:00:00','2026-02-06 14:00:00',NULL,'2026-02-06 14:00:00'),(3,3,'Consultation','General physician consultation',500.00,'2026-02-07','2026-02-07 10:45:00','2026-02-07 10:45:00',NULL,'2026-02-07 10:45:00'),(4,4,'Vaccination','DTaP booster shot',300.00,'2026-02-08','2026-02-08 16:30:00','2026-02-08 16:30:00',NULL,'2026-02-08 16:30:00'),(5,5,'X-Ray','Chest X-ray for injury assessment',1200.00,'2026-02-09','2026-02-09 08:00:00','2026-02-09 08:00:00',NULL,'2026-02-09 08:00:00');
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
INSERT INTO `visits` VALUES (1,1,1,2,'2026-02-05 09:30:00','Thursday','Winter','Morning','Medium',0.25,3,10,15,25,50,'Admitted',8,'2026-02-05 09:17:53','2026-02-05 09:17:53',NULL,'2026-02-05 09:17:53'),(2,2,1,1,'2026-02-06 14:20:00','Friday','Winter','Afternoon','High',0.30,5,5,10,15,30,'Discharged',9,'2026-02-06 14:00:00','2026-02-06 14:00:00',NULL,'2026-02-06 14:00:00'),(3,3,2,5,'2026-02-07 11:00:00','Saturday','Winter','Morning','Low',0.20,2,20,30,40,90,'Discharged',6,'2026-02-07 10:45:00','2026-02-07 10:45:00',NULL,'2026-02-07 10:45:00'),(4,4,1,4,'2026-02-08 16:45:00','Sunday','Winter','Evening','Critical',0.35,4,3,5,8,16,'Admitted',10,'2026-02-08 16:30:00','2026-02-08 16:30:00',NULL,'2026-02-08 16:30:00'),(5,5,3,6,'2026-02-09 08:15:00','Monday','Winter','Morning','Critical',0.40,6,2,3,5,10,'Admitted',9,'2026-02-09 08:00:00','2026-02-09 08:00:00',NULL,'2026-02-09 08:00:00');
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

-- Dump completed on 2026-01-21  9:39:02
