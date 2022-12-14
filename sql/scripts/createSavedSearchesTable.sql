------------------------------------------------------------
-- Table structure for table `SavedSearches`
-- If this is updated, must ensure ORM class is also updated
------------------------------------------------------------

-- FIXME: Not complete, maybe need to work on ER a bit more to flesh out
-- Will need to link user to a specific first name/last name wildcard search
-- OR
-- Fix a specific playerid to a webuserid

DROP TABLE IF EXISTS `savedSearches`;
SET character_set_client = utf8mb4;
CREATE TABLE `savedSearches` (
  `search_ID` int(11) NOT NULL AUTO_INCREMENT,
  `webuserID` varchar(255) NOT NULL,
  `playerName` varchar(255) DEFAULT NULL,
  `playerID` varchar(9) DEFAULT NULL,
  PRIMARY KEY (`search_ID`),
  UNIQUE KEY `searchID` (`webuserID`,`playerid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;