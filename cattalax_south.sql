-- MySQL dump 10.13  Distrib 5.5.34, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: cat_dashboard
-- ------------------------------------------------------
-- Server version	5.5.34-0ubuntu0.12.04.1

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
-- Table structure for table `south_migrationhistory`
--

DROP TABLE IF EXISTS `south_migrationhistory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `south_migrationhistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_name` varchar(255) NOT NULL,
  `migration` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `south_migrationhistory`
--

LOCK TABLES `south_migrationhistory` WRITE;
/*!40000 ALTER TABLE `south_migrationhistory` DISABLE KEYS */;
INSERT INTO `south_migrationhistory` VALUES (1,'dashboard','0001_initial','2014-02-04 11:11:53'),(2,'dashboard','0002_auto__add_field_visit_time','2014-02-05 12:46:40'),(3,'dashboard','0003_time_create','2014-02-05 13:01:49'),(4,'dashboard','0004_auto__del_field_visit_arrival_time','2014-02-05 13:04:24'),(5,'dashboard','0005_auto__add_field_visit_time2','2014-02-05 13:30:21'),(6,'dashboard','0006_create_time','2014-02-05 13:43:50'),(7,'dashboard','0007_auto__chg_field_visit_time','2014-02-05 13:44:50'),(8,'dashboard','0008_auto__del_field_visit_time2','2014-02-05 13:46:23'),(9,'dashboard','0009_auto__add_field_visit_datetime__add_field_walkby_datetime','2014-02-05 14:01:10'),(10,'dashboard','0010_create_date','2014-02-05 14:11:54'),(11,'dashboard','0011_create_date','2014-02-05 14:22:18'),(12,'dashboard','0012_auto__add_field_day_datetime__add_field_hour_datetime','2014-02-05 15:33:02'),(13,'dashboard','0013_create_datetime_for_times','2014-02-05 15:46:57'),(14,'dashboard','0014_auto__add_week','2014-02-05 16:13:56'),(15,'dashboard','0015_auto__add_month__add_field_week_year','2014-02-05 16:52:34'),(16,'dashboard','0016_create_day_month','2014-02-06 15:00:51'),(17,'dashboard','0017_auto__add_field_day_over_month__add_field_day_over_week','2014-02-06 15:00:53');
/*!40000 ALTER TABLE `south_migrationhistory` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-02-06 17:45:00
