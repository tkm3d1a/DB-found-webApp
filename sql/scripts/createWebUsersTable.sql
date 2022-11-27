------------------------------------------------------------
-- Table structure for table `webUsers`
-- If this is updated, must ensure ORM class is also updated
------------------------------------------------------------

-- FIXME: Need to compare against how user saving is going to be made
-- Need to hash the password somehow?

DROP TABLE IF EXISTS `webUsers`;
SET character_set_client = utf8mb4;
CREATE TABLE `webUsers` (
  `webuser_ID` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_pt` varchar(255) NOT NULL,
  PRIMARY KEY (`webuser_ID`),
  UNIQUE KEY `webuserID` (`username`,`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO webUsers(
  username,
  email,
  password_pt
) VALUES (
  'test_login',
  'test@test.com',
  'nohash'
);