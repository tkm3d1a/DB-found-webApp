-- This script is for generating a non-root user for testing access
-- This user should be able to update, insert and select on all DB tables
-- This user should not be able to delete or remove information
-- The wsl user is created for Tim Klimpel's personal scripts, the normal localhost should work on non-wsl machine setups

CREATE USER web@localhost IDENTIFIED BY 'dbrules';

-- Adding for dev on TK desktop
CREATE USER webwsl@172.27.137.12 IDENTIFIED BY 'dbrules';

-- Adding for dev on TK Laptop
CREATE USER webwsl@172.24.252.44 IDENTIFIED BY 'dbrules';

GRANT SELECT, INSERT, UPDATE
ON baseball.* TO web@localhost;

-- Adding for dev on TK desktop
GRANT SELECT, INSERT, UPDATE
ON *.* TO webwsl@172.27.137.12;

-- Adding for dev on TK laptop
GRANT SELECT, INSERT, UPDATE
on *.* TO webwsl@172.24.252.44;