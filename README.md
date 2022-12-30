# DB-found-webApp

This is a class project for ~~blanked out~~.  It is built using the Flask/SQLAlchmey framework with a MariaDB backend.  Currently, the MaraiDB server needs to be run locally and requires some setup on inital use(See [Environment Info](#environment-information) for details on the environment needed).  Once Setup, a user can search through the Lahman Baseball database to find information on players that have played in the major leagues, with data stopping at the 2019 season.  Currently, only Batting information is retrieved, so if the player has no batting information they will not be present in this database.

### TOC
- [Using the site](#using-the-appsite)
- [Environment Setup](#environment-setup)
- [Worklog](#worklog)

---

# Using the app/site

## Setting up Database
- First, ensure MariaDB 10.6.8 is installed and operational on your local machine
  - No previous database setup is required besides initial setup
  - No testing on other versions were conducted, but newer version should work, and most versions of modern MariaDB should work
- 2 user profiles will be required from here
  - A root user to run all initial scripts
  - A limited access web user for interacting with the DB from the web application
    - This can be done using the script `updateDatabaseUsers.sql`
      - Ensure the proper IP is set for the user that is accessing the database
      - This can normally be local host if MariaDB is running on the same machine as the webApp.
      - If the webapp is being run on WSL while MariaDB is on native windows, this will require extra configuration steps
- All relevant scripts have been combined into a single file
  - Two options for loading from here:
    - DB dump located in `/sql/dbDumps/530_webapp_dump_12-1-22.sql`
      - This will create a database called `webapp_baseball` for use in the web application
      - Will also have test login's enabled, with saved searches already populate
      - Login information:
        - Username: `test_login`
        - password: `nohash`
        - **OR**
        - Username: `timtest`
        - Password `tim`
    - Init script located in `/sql/scripts/init_webapp_baseball.sql`
      - this will be a fresh database install with only one login and no saved searches
      - Login Information:
        - Username: `test_login`
        - password: `nohash`
- Leave MariaDB running for the webapplication to access

## Homepage
- After configuring the virtual environment as shown in [Environment setup](#environment-setup) navigate to `/baseball-web-app`
- From the shell, run `flask run` to initalize the devolpment environment
- Navigate to `127.0.0.1:5000` from a web browser to be presented with the homepage
- From the home page, a user must log in before any player searches can be done
- All navigation is done through a top navbar, that changes based on logged in status of the session

## Sign in
- Sign in information is located above, and is based on which method was used to init the database
- New users can also be registered from the `register` link at the bottom of the sign in form
  - New users require a unique username and email
  - Form validation is used to ensure fields are populated
- Once signed in, the user is presented with a welcomepage where the can either view saved players or start a new search

## Searching
- When earching, a minimum of two(2) letters for first name and one(1) letter for last name is required
  - If no resuts, the user will be prompted that no results are returned and can search again
  - If multiple results, see [Multiple Results](#multiple-results) section below
  - If a single result s returned, see [Single Results](#single-results) section below
- `POST` requests should only occur when form fields contain data
- WARNING: No SQL injection detection is implemented on this step

### Single results
- A single result will return a new page with a url ending in `/ba-analysis/<PlayerID>` where <playerID> is the searched players playerID as listed in the database
- The players name will be presented at the top of the page, alogn with a `Save player` button
  - Clicking the save player button will save this searched playerID to the currently logged in user for future searching
  - A success or failure message will occur after clicking the button
    - If the player has not been saved for this user, a success message will be returned and the playerid will be saved to the databse
    - If the player has been saved for this user, an error will occur, and no data will be saved to the database
- Below the player name, a table with rows matching baseballreference.com are shown
  - Reference image used for this can be seen in `/reference/MikeTroutPage_BBRef_web.png`
- If a user would like to search for another player, the user must navigate back to the search page

### Multiple results
- When a search has multiple matching player names, a table is returned showing all of the results
- The user can select from a dop down on which player they would like to continue searching on
- When selecting from the drop down, only players shown on the page are included, and once `submit` is clicked, the single result page is returned to the user

## Searching a saved player
- If a logged in user has any saved searches, they will be able to select from them to complete a search without having to re-enter the player name
- The display will include a table of the playerID and player name that is saved to the user
- A drop down selection will allow the user to select which player they would like to see
- Once submit is clicked, the single result page for the selected player is returned

## logging out
- When a user is done browsing, clicking the `Logout` button in the navigation bar will log the user out
- Once logged out, the navbar will revert to the default state
- A user cna either log back in, register a new account, or navigate away from the application at this point

---

# Installation information

- [ ] TODO: Any dep installs needed to be detailed here

---

# Environment information

MariaDB
- 10.6.8

LahmanBaseballDB
- 2019, MySQL

Python 
- 3.8.10 (Running on WSL2 - Ubuntu)
-
Flask
- 2.2.2

---

# Environment setup

In the terminal, run the following commands to install dependicies...

_bash terminal_
```
sudo apt install python3.8-venv
python3 -m venv venv
. venv/bin/activate
pip install flask==2.2.2
pip install pymysql==1.0.2
pip install python-dotenv==0.21.0
pip install flask-wtf==1.0.1
pip install sqlalchemy==1.4.43
pip install flask-sqlalchemy==3.0.2
pip install flask-session==0.4.0
```

If running vscode as editor, add the following environment settings...

_.vscode/settings.json_
```json
{
  "python.analysis.extraPaths": [
    "./baseball-web-app",
    "./venv/lib/python3.8/site-packages"
  ]
}
```

# Database prep
- All steps can be done from a fresh database install or be used to overwrite a previously modifed table
- Database is created as `webapp_baseball` once script is completed
  - The custom script is a combination of `2019lahman_base_dump.sql` and other customer scripts for creating tables and users for web application MVP
- script it located in `<parentDir>/sql/scripts/init_webapp_baseball.sql`
- script load time varies, around a minute to clean and then load and create all nessecary tables
  
Sql command to run script inside MariaDB *must be run as root user of DB*
```sql
source ./sql/scripts/init_webapp_baseball.sql
```

---
# References

- [Flask Mega Tutorial post 3](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms)
- [DB Link](https://www.seanlahman.com/baseball-archive/statistics/)
- [WTForms documents v3.0.x](https://wtforms.readthedocs.io/en/3.0.x/)
- [flask-sqlalchemy docs v3.0.x](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)
