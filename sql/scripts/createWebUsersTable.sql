------------------------------------------------------------
-- Table structure for table `webUsers`
-- If this is updated, must ensure ORM class is also updated
------------------------------------------------------------

-- Password hash complete using sha256
-- can be improved, but works for now

DROP TABLE IF EXISTS `webUsers`;
SET character_set_client = utf8mb4;
CREATE TABLE `webUsers` (
  `webuser_ID` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  -- `password_pt` varchar(255) NOT NULL,
  `salt` varchar(8) NOT NULL,
  `pw_hash` varchar(255) NOT NULL,
  PRIMARY KEY (`webuser_ID`),
  UNIQUE KEY `webuserID` (`username`,`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO webUsers(
  username,
  email,
  -- password_pt,
  salt,
  pw_hash
) VALUES (
  'test_login',
  'test@test.com',
  -- 'nohash',
  '12345678',
  '7683088240e0fb46b346452980a86ed67870be71019a71f9893b324865d5f87a'
);