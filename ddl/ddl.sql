-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: payhere
-- ------------------------------------------------------
-- Server version	5.7.41

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
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `category` varchar(100) NOT NULL COMMENT '상품 카테코리',
  `price` int(7) NOT NULL COMMENT '판매 가격',
  `cost` int(7) NOT NULL COMMENT '원가',
  `product_name` varchar(100) NOT NULL COMMENT '상품 이름',
  `product_detail` varchar(500) NOT NULL COMMENT '상품 설명',
  `barcode` int(13) NOT NULL COMMENT '바코드',
  `expiration_date` datetime NOT NULL COMMENT '유통 기한',
  `size` varchar(10) NOT NULL COMMENT '사이즈 small or large',
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `items_ibfk_1` (`user_id`),
  CONSTRAINT `items_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `phone` varchar(20) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-07  4:53:37

------------ 사용자정의 펑션 -------------------
DELIMITER //
CREATE FUNCTION `chosung`(STR VARCHAR(255)) RETURNS varchar(255) CHARSET utf8mb4
    DETERMINISTIC
BEGIN
 DECLARE I INT(10);
 DECLARE J INT;
 DECLARE TMPSTR VARCHAR(255);
 DECLARE COL1 VARCHAR(2);

 SET I = char_length(STR);
 SET J = 1;
 SET TMPSTR = '';
  WHILE J <=I  DO
    SET COL1 = SUBSTRING(STR, J, 1);
  SET TMPSTR = CONCAT(TMPSTR,(
                       CASE WHEN COL1 < 'ㄱ' THEN COL1 
                       WHEN ascii('ㄱ') <= ascii(COL1) and 
                              ascii(COL1)<= ascii('ㅎ') THEN COL1 
                       WHEN COL1 < '까' THEN 'ㄱ'
                       WHEN COL1 < '나' THEN 'ㄲ'
                       WHEN COL1 < '다' THEN 'ㄴ'
                       WHEN COL1 < '따' THEN 'ㄷ'
                       WHEN COL1 < '라' THEN 'ㄸ'
                       WHEN COL1 < '마' THEN 'ㄹ'
                       WHEN COL1 < '바' THEN 'ㅁ'
                       WHEN COL1 < '빠' THEN 'ㅂ'
                       WHEN COL1 < '사' THEN 'ㅃ'
                       WHEN COL1 < '싸' THEN 'ㅅ'
                       WHEN COL1 < '아' THEN 'ㅆ'
                       WHEN COL1 < '자' THEN 'ㅇ'
                       WHEN COL1 < '짜' THEN 'ㅈ'
                       WHEN COL1 < '차' THEN 'ㅉ'
                       WHEN COL1 < '카' THEN 'ㅊ'
                       WHEN COL1 < '타' THEN 'ㅋ'
                       WHEN COL1 < '파' THEN 'ㅌ'
                       WHEN COL1 < '하' THEN 'ㅍ'
                       WHEN COL1 <= '힣' THEN 'ㅎ'
                       ELSE COL1
                       END
         ));
      SET J = J + 1 ;
  END WHILE;
  RETURN TMPSTR;
END//
DELIMITER ;

------------ 테스트 계정 ---------
