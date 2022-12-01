-- This script is for generating a non-root user for testing access
-- This user should be able to update, insert and select on all DB tables
-- This user should not be able to delete or remove information
-- The wsl user is created for Tim Klimpel's personal scripts, the normal localhost should work on non-wsl machine setups

CREATE USER web@localhost IDENTIFIED BY 'dbrules';

-- Adding for dev on TK desktop
CREATE USER webwsl@172.21.7.167 IDENTIFIED BY 'dbrules';


GRANT SELECT, INSERT, UPDATE
ON *.* TO web@localhost;

-- Adding for dev on TK desktop
GRANT SELECT, INSERT, UPDATE
ON *.* TO webwsl@172.21.7.167;

FLUSH privileges;