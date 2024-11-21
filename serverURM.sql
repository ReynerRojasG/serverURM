-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: avi
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `ai_answer`
--

DROP TABLE IF EXISTS `ai_answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ai_answer` (
  `answer_id` int NOT NULL AUTO_INCREMENT,
  `answer` varchar(1000) NOT NULL,
  PRIMARY KEY (`answer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ai_answer`
--

LOCK TABLES `ai_answer` WRITE;
/*!40000 ALTER TABLE `ai_answer` DISABLE KEYS */;
INSERT INTO `ai_answer` VALUES (2,'Bien hecho, eres un excelente estudiante.'),(4,'necesita mejorar, sigue progresando'),(5,'regular, pero aceptable');
/*!40000 ALTER TABLE `ai_answer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `assignment`
--

DROP TABLE IF EXISTS `assignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `assignment` (
  `assignment_id` int NOT NULL AUTO_INCREMENT,
  `course_id` int NOT NULL,
  `professor_id` int NOT NULL,
  `course_statement` varchar(300) NOT NULL,
  `assignment_type` enum('Tarea','Proyecto','Laboratorio','Foro','Examen') NOT NULL,
  `initial_date` varchar(10) NOT NULL,
  `final_date` varchar(10) NOT NULL,
  PRIMARY KEY (`assignment_id`),
  KEY `fk_id_course_idx` (`course_id`),
  KEY `fk_id_professor_idx` (`professor_id`),
  CONSTRAINT `fk_id_course` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_id_professor` FOREIGN KEY (`professor_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `assignment`
--

LOCK TABLES `assignment` WRITE;
/*!40000 ALTER TABLE `assignment` DISABLE KEYS */;
INSERT INTO `assignment` VALUES (1,1,10,'Hacer un insert de listas','Tarea','2024-10-16','2024-10-20'),(3,1,7,'Crear una funcion de python','Tarea','2024-10-12','2024-10-15'),(5,1,7,'Crear una aplicacion Flask','Tarea','2024-12-01','2024-12-31'),(6,4,7,'Este es un examen de Algebra','Examen','20/05/2024','20/05/2024');
/*!40000 ALTER TABLE `assignment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `course_id` int NOT NULL AUTO_INCREMENT,
  `professor_id` int NOT NULL,
  `department_id` int NOT NULL,
  `course_name` varchar(45) NOT NULL,
  `course_information` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`course_id`),
  KEY `fk_professor_id_idx` (`professor_id`),
  KEY `fk_department_id_idx` (`department_id`),
  CONSTRAINT `fk_department_id` FOREIGN KEY (`department_id`) REFERENCES `department` (`department_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_professor_id` FOREIGN KEY (`professor_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,7,1,'Estructuras Discretas','Curso enfocado en matematicas discretas'),(3,10,1,'Estructuras de datos','Esto es un curso nuevo'),(4,7,1,'Algebra Lineal','Curso enfocado en algebra lineal'),(6,12,4,'Cálculo I','Contempla límites, derivadas e integrales');
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `department` (
  `department_id` int NOT NULL AUTO_INCREMENT,
  `department_name` varchar(45) NOT NULL,
  `department_information` varchar(45) DEFAULT NULL,
  `faculty_id` int NOT NULL,
  PRIMARY KEY (`department_id`),
  KEY `fk_faculty_id_idx` (`faculty_id`),
  CONSTRAINT `fk_faculty_id` FOREIGN KEY (`faculty_id`) REFERENCES `faculty` (`faculty_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES (1,'Departamento de Informatica','Departamento enfocado en informatica',1),(4,'Departamento de Matemáticas','Esto es un departamento de mate',4);
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `faculty`
--

DROP TABLE IF EXISTS `faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty` (
  `faculty_id` int NOT NULL AUTO_INCREMENT,
  `faculty_name` varchar(45) NOT NULL,
  `faculty_information` varchar(45) DEFAULT NULL,
  `university_id` int NOT NULL,
  PRIMARY KEY (`faculty_id`),
  KEY `fk_university_id_idx` (`university_id`),
  CONSTRAINT `fk_university_id` FOREIGN KEY (`university_id`) REFERENCES `university` (`university_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty`
--

LOCK TABLES `faculty` WRITE;
/*!40000 ALTER TABLE `faculty` DISABLE KEYS */;
INSERT INTO `faculty` VALUES (1,'Facultad de Ingeniería','Somos la facultad de ingeniería',2),(4,'Facultad de Matemáticas','Facultad de matematicos',2),(5,'Facultad de Filosofía','Somos la facultad de filosofía',2),(6,'Facultad de Ciencias Sociales','Somos expertos en ciencias sociales',5),(7,'Facultad de Ciencias de la Salud','Somos número 1 en Salud',5),(8,'Facultad de Letras','Somos facultad de letras',4);
/*!40000 ALTER TABLE `faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration`
--

DROP TABLE IF EXISTS `registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registration` (
  `registration_id` int NOT NULL AUTO_INCREMENT,
  `student_id` int NOT NULL,
  `course_id` int NOT NULL,
  PRIMARY KEY (`registration_id`),
  KEY `fk_user_id_idx` (`student_id`),
  KEY `fk_course_id_idx` (`course_id`),
  CONSTRAINT `fk_course_id` FOREIGN KEY (`course_id`) REFERENCES `course` (`course_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_user_id` FOREIGN KEY (`student_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration`
--

LOCK TABLES `registration` WRITE;
/*!40000 ALTER TABLE `registration` DISABLE KEYS */;
INSERT INTO `registration` VALUES (5,4,3),(6,6,1),(8,3,1),(11,4,4);
/*!40000 ALTER TABLE `registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `submission`
--

DROP TABLE IF EXISTS `submission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `submission` (
  `submission_id` int NOT NULL AUTO_INCREMENT,
  `submission_score` float DEFAULT NULL,
  `assignment_id` int NOT NULL,
  `student_id` int NOT NULL,
  `submission_date` varchar(10) NOT NULL,
  `submission_file` varchar(300) NOT NULL,
  `submission_status` enum('Revisado','No revisado') NOT NULL,
  `comment_ai` varchar(1000) DEFAULT NULL,
  `comment_professor` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`submission_id`),
  KEY `fk_assignment_id_idx` (`assignment_id`),
  KEY `fk_id_student_idx` (`student_id`),
  CONSTRAINT `fk_assignmet_id` FOREIGN KEY (`assignment_id`) REFERENCES `assignment` (`assignment_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_id_student` FOREIGN KEY (`student_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `submission`
--

LOCK TABLES `submission` WRITE;
/*!40000 ALTER TABLE `submission` DISABLE KEYS */;
INSERT INTO `submission` VALUES (3,70,1,3,'2024-10-16','avanceMakinReyner.py','Revisado','','Debes continuar profundizando'),(4,80,3,4,'2024-10-12','avance.pdf','Revisado','Bien hecho, eres un excelente estudiante.','Null'),(5,52,3,4,'2024-10-15','avance2.cpp','Revisado','necesita mejorar, sigue progresando','Null'),(6,74,3,4,'2024-10-24','avanceFinal.cpp','Revisado','regular, pero aceptable','Null'),(8,0,1,3,'2024-11-30','archivo.txt','No revisado','',''),(15,74,5,6,'2024-12-02','proyectoListas.pdf','Revisado','regular, pero aceptable','Null'),(16,NULL,3,6,'12/10/2024','run.py','No revisado',NULL,NULL);
/*!40000 ALTER TABLE `submission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `university`
--

DROP TABLE IF EXISTS `university`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `university` (
  `university_id` int NOT NULL AUTO_INCREMENT,
  `university_name` varchar(45) NOT NULL,
  PRIMARY KEY (`university_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `university`
--

LOCK TABLES `university` WRITE;
/*!40000 ALTER TABLE `university` DISABLE KEYS */;
INSERT INTO `university` VALUES (1,'Universidad Latinoamericana'),(2,'Universidad Nacional'),(4,'Universidad Fidelitas'),(5,'Universidad de Costa Rica'),(6,'Universidad Castro Carazo'),(9,'UNED');
/*!40000 ALTER TABLE `university` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `university_id` int NOT NULL,
  `user_name` varchar(45) NOT NULL,
  `user_type` enum('Profesor','Estudiante','Administrador') NOT NULL,
  `user_password` varchar(10) NOT NULL,
  `user_identification` varchar(10) NOT NULL,
  PRIMARY KEY (`user_id`),
  KEY `fk_university_id_idx` (`university_id`),
  KEY `fk_id_university_idx` (`university_id`),
  CONSTRAINT `fk_id_university` FOREIGN KEY (`university_id`) REFERENCES `university` (`university_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (3,1,'Maki','Estudiante','pass456','ID654321'),(4,1,'Esdras','Estudiante','1708','ID1415'),(5,1,'Harry','Estudiante','934','ID554466'),(6,1,'Anne','Estudiante','Anne','604880490'),(7,2,'Douglas','Profesor','limite123','12441122'),(9,5,'Luisca','Estudiante','1234','604550322'),(10,2,'Juanito','Profesor','1234','604110335'),(12,1,'Elizabeth','Profesor','mate123','6060606'),(13,2,'Reyner','Administrador','RG2004','604890632'),(14,5,'Josepe','Administrador','jerry123','605210321');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-20 23:57:06
