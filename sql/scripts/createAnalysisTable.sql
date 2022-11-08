-- Use this to create and modify the Analysis table that is needed

------------------------------------------------------------
-- Table structure for table `analysis`
-- If this is updated, must ensure ORM class is also updated
------------------------------------------------------------

DROP TABLE IF EXISTS `analysis`;
SET character_set_client = utf8mb4;
CREATE TABLE `analysis` (
  `analysis_ID` int(11) NOT NULL AUTO_INCREMENT,
  `playerID` varchar(9) NOT NULL,
  `yearID` smallint(6) NOT NULL,
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
  PRIMARY KEY (`analysis_ID`),
  UNIQUE KEY `analysisID` (`playerID`,`yearID`, `stint`),
  CONSTRAINT `analysis_peoplefk` FOREIGN KEY (`playerID`) REFERENCES `people` (`playerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

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
  sb,
  cs,
  bb,
  so,
  ibb,
  hbp,
  sh,
  sf,
  gidp 
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

-------------------
-- Update OBP Field
-- FIXME:returning multiple results, need to investigate
-------------------
UPDATE analysis a SET OBP = 
        CASE 
          WHEN ab+bb+COALESCE(hbp,0)+COALESCE(sf,0) = 0 THEN 0 
          ELSE (
            SELECT ((h+bb+COALESCE(hbp,0)) / (ab+bb+COALESCE(hbp,0)+COALESCE(sf,0)))
            FROM analysis b 
            WHERE a.playerid = b.playerid AND a.yearid = b.yearid) 
        END;

------------------
-- Update RC Field
------------------
UPDATE analysis a SET RC = OBP * TB;

-------------------
-- Update SLG field
-- the formula for slugging percentage is: (1B + 2Bx2 + 3Bx3 + HRx4)/AB.
-- ref: https://www.mlb.com/glossary/standard-stats/slugging-percentage
-------------------
UPDATE analysis a SET SLG = (h + b2*2 + b3*3 + hr*4) / AB;

--------------------
-- Update RC27 Field
-- no concensus on formula past RC / 27
--------------------
UPDATE analysis a SET RC27 = RC / 27;

--------------------
-- Update PARC Field
--------------------
--TODO:

----------------------
-- Update PARC27 Field
----------------------
--TODO:


-- TODO: Decide if a trigger is needed to keep the table up to date?