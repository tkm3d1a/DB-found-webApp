# Format for terminal is: python [filename] [playerID]
import pymysql
import sys

# Check that the correct number of arguments are input by the user
# In the case where this is not correct, output information for expected input
params = ['NULL']

if len(sys.argv) != 2:
	exit(0)

params[0] = sys.argv [1]

# Create connection to database
# Make sure web@localhost has permissions to access analysis table
con = pymysql.connect(host='localhost', user='web', password='dbrules', db='baseball')

try:
	cur = con.cursor()
	sql = "SELECT Name, CASE WHEN birthMonth = 1 THEN 'January' WHEN birthMonth = 2 THEN 'February' WHEN birthMonth = 3 THEN 'March' WHEN birthMonth = 4 THEN 'April' WHEN birthMonth = 5 THEN 'May' WHEN birthMonth = 6 THEN 'June' WHEN birthMonth = 7 THEN 'July' WHEN birthMonth = 8 THEN 'August' WHEN birthMonth = 9 THEN 'September' WHEN birthMonth = 10 THEN 'October' WHEN birthMonth = 11 THEN 'November' WHEN birthMonth = 12 THEN 'December' END, birthDay, birthYear FROM analysis WHERE playerID = %s LIMIT 1;"
	cur.execute(sql, params)
	results = cur.fetchall()

# Print header line
	print("{: <30} {: <10}".format("Name", "Birthday"))
# For each row of results, print in specified format
	for row in results:
		row = [str(x) for x in row]
		print("{: <30} {: <10} {: <2} {: <4}".format(*row))

	print()
	cur = con.cursor()
	sql = "SELECT yearID, stint, teamID, lgID, G, AB, R, H, B2, B3, HR, RBI, SB, CS, BB, SO, IBB, HBP, SH, SF, GIDP, OBP, SLG, TB, RC, RC27, PARC, PARC27, W, SSB, TOB, OUTS, PA, BA FROM analysis WHERE playerID = %s;"
	cur.execute(sql, params)
	results = cur.fetchall()

# Print header line
	print("{: ^4} {: ^5} {: ^4} {: ^6} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^4} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^6} {: ^6} {: ^6} {: ^6} {: ^6} {: ^6} {: ^6}".format("Year", "Stint", "Team", "League", "G", "AB", "R", "H", "2B", "3B", "HR", "RBI", "SB", "CS", "BB", "SO", "IBB", "HBP", "SH", "SF", "GIDP", "OBP", "SLG", "TB", "RC", "RC27", "PARC", "PARC27", "W", "SSB", "TOB", "OUTS", "PA", "BA"))
# For each row of results, print in specified format
	for row in results:
		row = [str(x) for x in row]
		print("{: ^4} {: ^5} {: ^4} {: ^6} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^4} {: ^5} {: ^5} {: ^5} {: ^5} {: ^5} {: ^6} {: ^6} {: ^6} {: ^6} {: ^6} {: ^6} {: ^6}".format(*row))

except Exception:
	print("Database exception.")
	raise

finally:
	con.close()
