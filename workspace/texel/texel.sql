-- MySQL dump 10.13  Distrib 5.5.38, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: texel
-- ------------------------------------------------------
-- Server version	5.5.38-0ubuntu0.12.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=70 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add project',7,'add_project'),(20,'Can change project',7,'change_project'),(21,'Can delete project',7,'delete_project'),(22,'Can add webcam',8,'add_webcam'),(23,'Can change webcam',8,'change_webcam'),(24,'Can delete webcam',8,'delete_webcam'),(25,'Can add project locatie',9,'add_projectlocatie'),(26,'Can change project locatie',9,'change_projectlocatie'),(27,'Can delete project locatie',9,'delete_projectlocatie'),(28,'Can add meet locatie',10,'add_meetlocatie'),(29,'Can change meet locatie',10,'change_meetlocatie'),(30,'Can delete meet locatie',10,'delete_meetlocatie'),(31,'Can add generator',11,'add_generator'),(32,'Can change generator',11,'change_generator'),(33,'Can delete generator',11,'delete_generator'),(34,'Can add gegevensbron',12,'add_datasource'),(35,'Can change gegevensbron',12,'change_datasource'),(36,'Can delete gegevensbron',12,'delete_datasource'),(37,'Can add bronbestand',13,'add_sourcefile'),(38,'Can change bronbestand',13,'change_sourcefile'),(39,'Can delete bronbestand',13,'delete_sourcefile'),(40,'Can add parameter',14,'add_parameter'),(41,'Can change parameter',14,'change_parameter'),(42,'Can delete parameter',14,'delete_parameter'),(43,'Can add Reeks',15,'add_series'),(44,'Can change Reeks',15,'change_series'),(45,'Can delete Reeks',15,'delete_series'),(46,'Can add variabele',16,'add_variable'),(47,'Can change variabele',16,'change_variable'),(48,'Can delete variabele',16,'delete_variable'),(49,'Can add Berekende reeks',17,'add_formula'),(50,'Can change Berekende reeks',17,'change_formula'),(51,'Can delete Berekende reeks',17,'delete_formula'),(52,'Can add data point',18,'add_datapoint'),(53,'Can change data point',18,'change_datapoint'),(54,'Can delete data point',18,'delete_datapoint'),(55,'Can add Grafiek',19,'add_chart'),(56,'Can change Grafiek',19,'change_chart'),(57,'Can delete Grafiek',19,'delete_chart'),(58,'Can add tijdreeks',20,'add_chartseries'),(59,'Can change tijdreeks',20,'change_chartseries'),(60,'Can delete tijdreeks',20,'delete_chartseries'),(61,'Can add dashboard',21,'add_dashboard'),(62,'Can change dashboard',21,'change_dashboard'),(63,'Can delete dashboard',21,'delete_dashboard'),(64,'Can add tab group',22,'add_tabgroup'),(65,'Can change tab group',22,'change_tabgroup'),(66,'Can delete tab group',22,'delete_tabgroup'),(67,'Can add tab page',23,'add_tabpage'),(68,'Can change tab page',23,'change_tabpage'),(69,'Can delete tab page',23,'delete_tabpage');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$12000$HcwU5vBBjZ4a$HejGgOOmVuurAjERSDx2SucBa4mPKN6YwvQPzJhTm0k=','2014-10-07 15:15:34',1,'theo','','','tkleinen@gmail.com',1,1,'2014-10-04 19:00:12');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_6340c63c` (`user_id`),
  KEY `auth_user_groups_5f412f9a` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
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
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_6340c63c` (`user_id`),
  KEY `auth_user_user_permissions_83d7f98b` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_chart`
--

DROP TABLE IF EXISTS `data_chart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_chart` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` longtext,
  `title` varchar(50) NOT NULL,
  `user_id` int(11) NOT NULL,
  `start` datetime DEFAULT NULL,
  `stop` datetime DEFAULT NULL,
  `percount` int(11) NOT NULL,
  `perunit` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `data_chart_6340c63c` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_chart`
--

LOCK TABLES `data_chart` WRITE;
/*!40000 ALTER TABLE `data_chart` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_chart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_chartseries`
--

DROP TABLE IF EXISTS `data_chartseries`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_chartseries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `chart_id` int(11) NOT NULL,
  `series_id` int(11) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `axis` int(11) NOT NULL,
  `axislr` varchar(2) NOT NULL,
  `color` varchar(20) DEFAULT NULL,
  `type` varchar(10) NOT NULL,
  `stack` varchar(20) DEFAULT NULL,
  `label` varchar(20) DEFAULT NULL,
  `y0` double DEFAULT NULL,
  `y1` double DEFAULT NULL,
  `t0` datetime DEFAULT NULL,
  `t1` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `data_chartseries_48683575` (`chart_id`),
  KEY `data_chartseries_489757ad` (`series_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_chartseries`
--

LOCK TABLES `data_chartseries` WRITE;
/*!40000 ALTER TABLE `data_chartseries` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_chartseries` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_dashboard`
--

DROP TABLE IF EXISTS `data_dashboard`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_dashboard` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` longtext,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `data_dashboard_6340c63c` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_dashboard`
--

LOCK TABLES `data_dashboard` WRITE;
/*!40000 ALTER TABLE `data_dashboard` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_dashboard` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_dashboard_charts`
--

DROP TABLE IF EXISTS `data_dashboard_charts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_dashboard_charts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dashboard_id` int(11) NOT NULL,
  `chart_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dashboard_id` (`dashboard_id`,`chart_id`),
  KEY `data_dashboard_charts_0b1d675a` (`dashboard_id`),
  KEY `data_dashboard_charts_48683575` (`chart_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_dashboard_charts`
--

LOCK TABLES `data_dashboard_charts` WRITE;
/*!40000 ALTER TABLE `data_dashboard_charts` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_dashboard_charts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_datapoint`
--

DROP TABLE IF EXISTS `data_datapoint`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_datapoint` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `series_id` int(11) NOT NULL,
  `date` datetime NOT NULL,
  `value` double NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `series_id` (`series_id`,`date`),
  KEY `data_datapoint_489757ad` (`series_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_datapoint`
--

LOCK TABLES `data_datapoint` WRITE;
/*!40000 ALTER TABLE `data_datapoint` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_datapoint` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_datasource`
--

DROP TABLE IF EXISTS `data_datasource`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_datasource` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` longtext,
  `meetlocatie_id` int(11) NOT NULL,
  `url` varchar(200) DEFAULT NULL,
  `generator_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `last_download` datetime DEFAULT NULL,
  `autoupdate` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  `config` longtext,
  `username` varchar(50) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`,`meetlocatie_id`),
  KEY `data_datasource_2de7b3df` (`meetlocatie_id`),
  KEY `data_datasource_fce70a46` (`generator_id`),
  KEY `data_datasource_6340c63c` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_datasource`
--

LOCK TABLES `data_datasource` WRITE;
/*!40000 ALTER TABLE `data_datasource` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_datasource` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_formula`
--

DROP TABLE IF EXISTS `data_formula`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_formula` (
  `series_ptr_id` int(11) NOT NULL,
  `locatie_id` int(11) NOT NULL,
  `formula_text` longtext,
  PRIMARY KEY (`series_ptr_id`),
  KEY `data_formula_0de3a7c8` (`locatie_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_formula`
--

LOCK TABLES `data_formula` WRITE;
/*!40000 ALTER TABLE `data_formula` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_formula` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_formula_formula_variables`
--

DROP TABLE IF EXISTS `data_formula_formula_variables`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_formula_formula_variables` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `formula_id` int(11) NOT NULL,
  `variable_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `formula_id` (`formula_id`,`variable_id`),
  KEY `data_formula_formula_variables_a8c33650` (`formula_id`),
  KEY `data_formula_formula_variables_5a46c4bf` (`variable_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_formula_formula_variables`
--

LOCK TABLES `data_formula_formula_variables` WRITE;
/*!40000 ALTER TABLE `data_formula_formula_variables` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_formula_formula_variables` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_generator`
--

DROP TABLE IF EXISTS `data_generator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_generator` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `classname` varchar(50) NOT NULL,
  `description` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_generator`
--

LOCK TABLES `data_generator` WRITE;
/*!40000 ALTER TABLE `data_generator` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_generator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_meetlocatie`
--

DROP TABLE IF EXISTS `data_meetlocatie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_meetlocatie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `projectlocatie_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` longtext,
  `image` varchar(100) DEFAULT NULL,
  `location` point NOT NULL,
  `webcam_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `projectlocatie_id` (`projectlocatie_id`,`name`),
  KEY `data_meetlocatie_f6d04a95` (`projectlocatie_id`),
  SPATIAL KEY `data_meetlocatie_location_id` (`location`),
  KEY `data_meetlocatie_27d45d3c` (`webcam_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_meetlocatie`
--

LOCK TABLES `data_meetlocatie` WRITE;
/*!40000 ALTER TABLE `data_meetlocatie` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_meetlocatie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_parameter`
--

DROP TABLE IF EXISTS `data_parameter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_parameter` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `datasource_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` longtext,
  `unit` varchar(10) NOT NULL,
  `type` varchar(20) NOT NULL,
  `thumbnail` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`,`datasource_id`),
  KEY `data_parameter_3f41717a` (`datasource_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_parameter`
--

LOCK TABLES `data_parameter` WRITE;
/*!40000 ALTER TABLE `data_parameter` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_parameter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_project`
--

DROP TABLE IF EXISTS `data_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_project` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` longtext,
  `image` varchar(100) DEFAULT NULL,
  `logo` varchar(100) DEFAULT NULL,
  `theme` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_project`
--

LOCK TABLES `data_project` WRITE;
/*!40000 ALTER TABLE `data_project` DISABLE KEYS */;
INSERT INTO `data_project` VALUES (1,'Texel','Dit is de tekst voor het Texel project','','','dark-blue');
/*!40000 ALTER TABLE `data_project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_projectlocatie`
--

DROP TABLE IF EXISTS `data_projectlocatie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_projectlocatie` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `project_id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` longtext,
  `image` varchar(100) DEFAULT NULL,
  `location` point NOT NULL,
  `webcam_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `project_id` (`project_id`,`name`),
  KEY `data_projectlocatie_37952554` (`project_id`),
  SPATIAL KEY `data_projectlocatie_location_id` (`location`),
  KEY `data_projectlocatie_27d45d3c` (`webcam_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_projectlocatie`
--

LOCK TABLES `data_projectlocatie` WRITE;
/*!40000 ALTER TABLE `data_projectlocatie` DISABLE KEYS */;
INSERT INTO `data_projectlocatie` VALUES (1,1,'Locatie1','','','\0\0\0\0\0\0\0˚Æ¸Õ:\n˚@Ÿ∂ØÃ∫¸ A',NULL),(2,1,'Locatie2','','','\0\0\0\0\0\0\0\nÛ∂Ä1{˝@\'“E˙è!A',NULL);
/*!40000 ALTER TABLE `data_projectlocatie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_series`
--

DROP TABLE IF EXISTS `data_series`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_series` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` longtext,
  `unit` varchar(10) DEFAULT NULL,
  `type` varchar(20) NOT NULL,
  `parameter_id` int(11) DEFAULT NULL,
  `thumbnail` varchar(200) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `resample` varchar(10) DEFAULT NULL,
  `aggregate` varchar(10) DEFAULT NULL,
  `scale` double NOT NULL,
  `offset` double NOT NULL,
  `cumsum` tinyint(1) NOT NULL,
  `cumstart` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `parameter_id` (`parameter_id`,`name`),
  KEY `data_series_1d1f7f60` (`parameter_id`),
  KEY `data_series_6340c63c` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_series`
--

LOCK TABLES `data_series` WRITE;
/*!40000 ALTER TABLE `data_series` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_series` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_sourcefile`
--

DROP TABLE IF EXISTS `data_sourcefile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_sourcefile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `datasource_id` int(11) NOT NULL,
  `file` varchar(200) DEFAULT NULL,
  `rows` int(11) NOT NULL,
  `cols` int(11) NOT NULL,
  `start` datetime DEFAULT NULL,
  `stop` datetime DEFAULT NULL,
  `crc` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `created` datetime NOT NULL,
  `uploaded` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`,`datasource_id`),
  KEY `data_sourcefile_3f41717a` (`datasource_id`),
  KEY `data_sourcefile_6340c63c` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_sourcefile`
--

LOCK TABLES `data_sourcefile` WRITE;
/*!40000 ALTER TABLE `data_sourcefile` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_sourcefile` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_tabgroup`
--

DROP TABLE IF EXISTS `data_tabgroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_tabgroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `location_id` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `data_tabgroup_afbb987d` (`location_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_tabgroup`
--

LOCK TABLES `data_tabgroup` WRITE;
/*!40000 ALTER TABLE `data_tabgroup` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_tabgroup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_tabpage`
--

DROP TABLE IF EXISTS `data_tabpage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_tabpage` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tabgroup_id` int(11) NOT NULL,
  `name` varchar(40) NOT NULL,
  `order` int(11) NOT NULL,
  `dashboard_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `data_tabpage_9f91ee8c` (`tabgroup_id`),
  KEY `data_tabpage_0b1d675a` (`dashboard_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_tabpage`
--

LOCK TABLES `data_tabpage` WRITE;
/*!40000 ALTER TABLE `data_tabpage` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_tabpage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_variable`
--

DROP TABLE IF EXISTS `data_variable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_variable` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `locatie_id` int(11) NOT NULL,
  `name` varchar(10) NOT NULL,
  `series_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `locatie_id` (`locatie_id`,`name`),
  KEY `data_variable_0de3a7c8` (`locatie_id`),
  KEY `data_variable_489757ad` (`series_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_variable`
--

LOCK TABLES `data_variable` WRITE;
/*!40000 ALTER TABLE `data_variable` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_variable` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `data_webcam`
--

DROP TABLE IF EXISTS `data_webcam`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `data_webcam` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` longtext,
  `image` longtext NOT NULL,
  `video` longtext NOT NULL,
  `admin` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_webcam`
--

LOCK TABLES `data_webcam` WRITE;
/*!40000 ALTER TABLE `data_webcam` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_webcam` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `user_id` int(11) NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_6340c63c` (`user_id`),
  KEY `django_admin_log_37ef4eb4` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2014-10-04 19:03:22',1,7,'1','Texel',1,''),(2,'2014-10-07 14:49:58',1,7,'1','Texel',2,'Changed description.'),(3,'2014-10-07 15:21:05',1,9,'1','Locatie1',1,''),(4,'2014-10-07 15:24:13',1,9,'1','Locatie1',2,'Changed location.'),(5,'2014-10-07 15:24:57',1,9,'2','Locatie2',1,''),(6,'2014-10-07 15:25:08',1,9,'2','Locatie2',2,'Changed location.');
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'project','data','project'),(8,'webcam','data','webcam'),(9,'project locatie','data','projectlocatie'),(10,'meet locatie','data','meetlocatie'),(11,'generator','data','generator'),(12,'gegevensbron','data','datasource'),(13,'bronbestand','data','sourcefile'),(14,'parameter','data','parameter'),(15,'Reeks','data','series'),(16,'variabele','data','variable'),(17,'Berekende reeks','data','formula'),(18,'data point','data','datapoint'),(19,'Grafiek','data','chart'),(20,'tijdreeks','data','chartseries'),(21,'dashboard','data','dashboard'),(22,'tab group','data','tabgroup'),(23,'tab page','data','tabpage');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('mehykkxkz3j63t5tyom7x3ij0wenpgou','N2Y3NmFjNzUwMWYyNDA0MzQ0ODhkZDNkMTQ5ZWE1MDBkZDFjYmIyZjp7fQ==','2014-10-21 11:52:26'),('r4cogs8mgk6s08jmruqj2haxhwqy8cw4','MTFhMTE2NWE1ZTY3ZmFkYjcyNTU4MjYzOWM4MTJjMjU0NTlmODgxOTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2014-10-18 19:00:42'),('omnxuhgjh2lvrjszd5syvjazpw6vgf45','N2Y3NmFjNzUwMWYyNDA0MzQ0ODhkZDNkMTQ5ZWE1MDBkZDFjYmIyZjp7fQ==','2014-10-21 12:04:21'),('vp4e2s9p5fnj1s10mqvv3mjpyazusg5j','N2Y3NmFjNzUwMWYyNDA0MzQ0ODhkZDNkMTQ5ZWE1MDBkZDFjYmIyZjp7fQ==','2014-10-21 12:04:58'),('2elohmqe9wcvhlt2wciczl9rtjsvhvsn','N2Y3NmFjNzUwMWYyNDA0MzQ0ODhkZDNkMTQ5ZWE1MDBkZDFjYmIyZjp7fQ==','2014-10-21 12:05:10'),('ln4j0c3l88gpvihi6kvxdk9f2wmjx0az','N2Y3NmFjNzUwMWYyNDA0MzQ0ODhkZDNkMTQ5ZWE1MDBkZDFjYmIyZjp7fQ==','2014-10-21 12:05:41'),('gi3sbsqo6trml8uzlwsrnlhmzyx1lj5j','N2Y3NmFjNzUwMWYyNDA0MzQ0ODhkZDNkMTQ5ZWE1MDBkZDFjYmIyZjp7fQ==','2014-10-21 14:44:31'),('m7pefqaotghlaru83qcoxojs247a62pr','MTFhMTE2NWE1ZTY3ZmFkYjcyNTU4MjYzOWM4MTJjMjU0NTlmODgxOTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2014-10-21 12:05:58'),('yn2d1rmgkz0en8xedx52da6xecal6slo','N2Y3NmFjNzUwMWYyNDA0MzQ0ODhkZDNkMTQ5ZWE1MDBkZDFjYmIyZjp7fQ==','2014-10-21 14:45:26'),('tmo2vfmnaa3g9kbao754183nitm1qnaw','N2Y3NmFjNzUwMWYyNDA0MzQ0ODhkZDNkMTQ5ZWE1MDBkZDFjYmIyZjp7fQ==','2014-10-21 14:46:24'),('k17szxwd8adrp6fdx8mxdmg3t57yms7n','N2Y3NmFjNzUwMWYyNDA0MzQ0ODhkZDNkMTQ5ZWE1MDBkZDFjYmIyZjp7fQ==','2014-10-23 14:49:14'),('3i5bxz8a6daakot4n4n53pvubvt7vqu6','MTFhMTE2NWE1ZTY3ZmFkYjcyNTU4MjYzOWM4MTJjMjU0NTlmODgxOTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2014-10-21 14:49:01'),('2e4128159ps3mvaeij5n0gmqgeexrf38','MTFhMTE2NWE1ZTY3ZmFkYjcyNTU4MjYzOWM4MTJjMjU0NTlmODgxOTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=','2014-10-21 15:15:34'),('gup2bmm50sqxmta04gj7rxmmhbgzl4kc','N2Y3NmFjNzUwMWYyNDA0MzQ0ODhkZDNkMTQ5ZWE1MDBkZDFjYmIyZjp7fQ==','2014-10-26 09:35:49'),('r6k1ntac388sd8698mt2ziqd4w65kpyi','N2Y3NmFjNzUwMWYyNDA0MzQ0ODhkZDNkMTQ5ZWE1MDBkZDFjYmIyZjp7fQ==','2014-10-26 09:46:11');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-10-12 23:58:38
