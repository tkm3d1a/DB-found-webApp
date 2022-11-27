-- Use this to create and modify the Analysis table that is needed

------------------------------------------------------------
-- Table structure for table `analysis`
-- If this is updated, must ensure ORM class is also updated
------------------------------------------------------------

DROP TABLE IF EXISTS `analysis`;
SET character_set_client = utf8mb4;
CREATE TABLE `analysis` (
  `analysis_ID` int(11) NOT NULL AUTO_INCREMENT,
  `playerID` varchar(9) DEFAULT NULL,
  `playerName` varchar(255) DEFAULT NULL,
  `yearID` smallint(6) NOT NULL,
  `birthYear` int(11) DEFAULT NULL,
  `birthMonth` int(11) DEFAULT NULL,
  `birthDay` int(11) DEFAULT NULL,
  `ageForYear` smallint(3) DEFAULT NULL,
  `stint` smallint(2) NOT NULL,
  `team` char(3) DEFAULT NULL,
  `lgid` char(2) DEFAULT NULL,
  `G` smallint(6) DEFAULT NULL,
  `AB` smallint(6) DEFAULT NULL,
  `R` smallint(6) DEFAULT NULL,
  `H` smallint(6) DEFAULT NULL,
  `B2` smallint(6) DEFAULT NULL,
  `B3` smallint(6) DEFAULT NULL,
  `HR` smallint(6) DEFAULT NULL,
  `RBI` smallint(6) DEFAULT NULL,
  `SB` smallint(6) DEFAULT NULL,
  `CS` smallint(6) DEFAULT NULL,
  `BB` smallint(6) DEFAULT NULL,
  `SO` smallint(6) DEFAULT NULL,
  `IBB` smallint(6) DEFAULT NULL,
  `HBP` smallint(6) DEFAULT NULL,
  `SH` smallint(6) DEFAULT NULL,
  `SF` smallint(6) DEFAULT NULL,
  `GIDP` smallint(6) DEFAULT NULL,
  `OBP` numeric(5,3) DEFAULT NULL,
  `SLG` numeric(5,3) DEFAULT NULL,
  `TB` smallint(6) DEFAULT NULL,
  `RC` numeric(5,1) DEFAULT NULL,
  `RC27` numeric(5,2) DEFAULT NULL,
  `PARC` numeric(5,1) DEFAULT NULL,
  `PARC27` numeric(5,2) DEFAULT NULL,
  -- NEW VARIABLES - KP
  `W` numeric(5,2) DEFAULT NULL,
  `SSB` numeric(5,2) DEFAULT NULL,
  `TOB` numeric(5,2) DEFAULT NULL,
  `OUTS` smallint(6) DEFAULT NULL,
  `PA` numeric(5,2) DEFAULT NULL,
  `BA` numeric(5,2) DEFAULT NULL,
  PRIMARY KEY (`analysis_ID`),
  UNIQUE KEY `analysisID` (`playerID`,`yearID`, `stint`),
  CONSTRAINT `analysis_peoplefk` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Inserting base values into analysis set
-- These are just the values to use for starting, further calcs needed to populate all values in table
-- Does not set the following:
-- OBP,
-- SLG,
-- TB,
-- RC,
-- RC27,
-- PARC,
-- PARC27

-- NEW VARIABLES - KP
-- TOB (Time on Base) (Not required, but used to calculate RC)
-- OUTS (Not required, but used to calculate PARC27)
-- BA (Bases Advanced) (Not required, but used to calculate RC)
-- PA (Plate Appearances) (Not required, but used to calculate RC)
-- W (Walks) (Not required, but used to calculate BA)
-- SSB (Sacrifices and Stolen Bases) (Not required, but used to calculate BA)

INSERT INTO analysis(
  playerid,
  yearid,
  stint,
  team,
  lgid,
  g,
  ab,
  r,
  h,
  b2,
  b3,
  hr,
  rbi,
  sb,
  cs,
  bb,
  so,
  ibb,
  hbp,
  sh,
  sf,
  gidp) 
SELECT 
  playerid,
  yearid,
  stint,
  teamid,
  lgid,
  g,
  ab,
  r,
  h,
  2b,
  3b,
  hr,
  rbi,
  COALESCE(sb,0),
  COALESCE(cs,0),
  bb,
  so,
  COALESCE(ibb,0),
  COALESCE(hbp,0),
  COALESCE(sh,0),
  COALESCE(sf,0),
  COALESCE(gidp,0)
FROM batting GROUP BY playerid,yearid,stint;

----------------------------------------------------------------
-- Commands to run to verify analysis table has been initialized 
-- correctly
----------------------------------------------------------------
-- SELECT
--   playerid, yearid, stint,team,
--   G,
--   ab,
--   h
-- FROM
--   analysis
-- WHERE
--   playerid = 'chaveje01';


-- SELECT
--   playerid, yearid, stint,
--   G,
--   ab,
--   h
-- FROM
--   batting
-- WHERE
--   playerid = 'chaveje01';
----------------------------------------------------------------
----------------------------------------------------------------

------------------
-- Update TB field
------------------
UPDATE analysis a SET TB = h + b2 + 2*b3 + 3*hr;
-- The formula according to the project description is:
-- UPDATE analysis a SET TB = H + (2 * B2) + (3 * B3) + (4 * HR);

-------------------
-- Update OBP Field
-- Might not be necssary depending on which calculation we use - KP
-------------------
UPDATE analysis a SET OBP = 
  CASE 
    WHEN ab+bb+COALESCE(hbp,0)+COALESCE(sf,0) = 0 THEN 0 
    ELSE (
      SELECT ((h+bb+COALESCE(hbp,0)) / (ab+bb+COALESCE(hbp,0)+COALESCE(sf,0)))
      FROM analysis b 
      WHERE a.playerid = b.playerid AND a.yearid = b.yearid AND a.stint = b.stint) 
  END;
  
-------------------
-- Update SLG field
-- the formula for slugging percentage is: (1B + 2Bx2 + 3Bx3 + HRx4)/AB.
-- ref: https://www.mlb.com/glossary/standard-stats/slugging-percentage
-------------------
UPDATE analysis a SET SLG = (h + b2*2 + b3*3 + hr*4) / AB;

-------------------
-- Update birth values Field(s)
-------------------
UPDATE analysis a SET a.birthYear = 
  (SELECT p.birthYear FROM people p where a.playerID = p.playerID);

UPDATE analysis a SET a.birthMonth = 
  (SELECT p.birthMonth FROM people p where a.playerID = p.playerID);

UPDATE analysis a SET a.birthDay = 
  (SELECT p.birthDay FROM people p where a.playerID = p.playerID);

----------------------
-- Update W Field
----------------------
UPDATE analysis a SET W = (BB + HBP - IBB) * 0.26;

----------------------
-- Update SSB Field
----------------------
UPDATE analysis a SET SSB = (SH + SF + SB) * 0.52;

----------------------
-- Update TOB Field
----------------------
UPDATE analysis a SET TOB = H + W + HBP - CS + GIDP;

----------------------
-- Update OUTS Field
----------------------
UPDATE analysis a SET OUTS = AB + SF + SH + CS + GIDP - H;

----------------------
-- Update PA Field
----------------------
UPDATE analysis a SET PA = AB + BB + HBP + SF + SH;

----------------------
-- Update BA Field
----------------------
UPDATE analysis a SET BA = TB + W + SSB;

------------------
-- Update RC Field
------------------
UPDATE analysis a SET RC = 
  CASE
    WHEN PA = 0 THEN 0
    ELSE TOB * BA / PA
   END;

--------------------
-- Update PARC Field
--------------------
UPDATE analysis a1 SET a1.PARC = 
  (SELECT (a2.RC / ((t.BPF + 100) / 200))
  FROM analysis a2, teams t 
  WHERE a2.playerID = a1.playerID
    AND a2.yearID = a1.yearID
    AND a2.stint = a1.stint
    AND a2.team = t.teamID
    AND a2.yearID = t.yearID
   );

-------------------------------
-- Update PARC27 and RC27 Field
-------------------------------
UPDATE analysis a SET PARC27 = 
  CASE 
    WHEN OUTS = 0 THEN 0
    ELSE PARC * 27 / OUTS
  END;
UPDATE analysis a SET RC27 = RC / 27;

-------------------------------
-- Update Name Field
-------------------------------
UPDATE analysis a SET playerName =
    (SELECT CONCAT(nameFirst, ' ', nameLast) 
    FROM people p
    WHERE p.playerID = a.playerID
    ); 

-- select playerid, playerName, yearid, rc, parc, rc27, parc27 from analysis where playerid='ruthba01';
