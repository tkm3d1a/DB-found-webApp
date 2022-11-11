-- This script is for generating a non-root user for testing access
-- This user should be able to update, insert and select on all DB tables
-- This user should not be able to delete or remove information

CREATE USER web@localhost IDENTIFIED BY 'dbrules';

GRANT SELECT, INSERT, UPDATE
ON baseball.* TO web@localhost;