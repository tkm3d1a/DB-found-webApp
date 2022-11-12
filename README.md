# DB-found-webApp

## SQL Tasks

- [ ] TODO: Create analysis table
  - [x] Main Table creation
    - does not includie updating all custom calculations yet
  - [ ] Park-adjusted runs created
    - Calculation is done by pulling info from the Teams Table, BPF
      1. Create RC table
      2. Use home field as BPF value for a player
      3. Adjustment percent = BPF + 100 / 200
      4. PARC = RC/Adjustment percent
  - [ ] Park-adjusted runs created per 27 outs
    - same calculation as above, just using RC27 instead of RC
  - [ ] Any other benefical items to add?
- [ ] TODO: Create a summary table?
  - This could be a way to link player full names a little better?
  - Or an easier link from someone inserting a name to get to a playerid
- [ ] TODO: Create trigger to update tables as needed?

## Python/Website tasks

- [ ] TODO: Setup user auth as module for flask env
  - Pawan todo week of 11/7
- [ ] TODO: ORM for neede info to be dev
  - [x] ORM for Analysis created
- [ ] TODO: Search field for searching by first and last name
  - Can use wildcards to convert to search fields
- [ ] TODO: Way to save a users preferences/favorite players
- [ ] TODO: Format output of table

## Misc Tasks

- [ ] TODO: Add TOC here for readme
- [ ] TODO: Make sure to update [Worklog](#worklog) with each PR or commit
  - Format for update should be:
    - Date in italics
    - Initials of commenter in square brackets
    - Bullets with each main change
- [ ] TODO: Add link for MariaDB install
- [ ] TODO: Add instructions for setting up base DB instance
- [ ] TODO: User info setup required as well
- [ ] TODO: decomp requirements for assigning tasks 
  - Tim and Kevin todo
  - (complete by 11-5-22)
- [ ] TODO: gather reference material and images
- [ ] TODO: Mark todo lines with assignee names if possible to avoid double work
- [ ] TODO: Work on installation instructions for setting up DB
  - Tim to do (no date set)


# Installation information

- [ ] TODO: Any dep installs needed to be detailed here

# Environment information

MariaDB
- 10.x.x

LahmanBaseballDB
- 2019, MySQL

Python 
- 3.8.10 (Running on WSL2 - Ubuntu)

Flask
- 2.2.2

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

# Worklog

_11-12-22 [TK]_
- Got search working finally
- Issue was with running all the venv in WSL2 but MariaDB is run on windows
  - Some helpful links if you run into this:
    - [Find WSL 'localhost' equivelant to put in conn variable](https://devdojo.com/mvnarendrareddy/access-windows-localhost-from-wsl2)
    - [Enable MariaDB user to have remote access from the seperate 'machine'](https://webdock.io/en/docs/how-guides/database-guides/how-enable-remote-access-your-mariadbmysql-database#:~:text=By%20default%2C%20MariaDB%20allows%20connection,IP%20addresses%20on%20the%20system.&text=Change%20the%20value%20of%20the,0.1%20to%200.0.)
      - This one requires getting the IP that maria DB reports as attempting to connect when first setting up
      - Use the main server running window to get this info
      - I also had a lot of success testing with the VScode sql tools and mariaDB extensions
- Added note in search.html about variable names
  - they must match exact to the ORM, DO NOT TREAT LIKE NORMAL SQL QUERY HERE

_11-11-22 [TK]_
- Tried small debugging of connection error but no luck
-  Cant connect to the database for some reason
- Verified onnection is running
- Verifed 'web' user is created with 'dbrules' password
- Verifed direct maraiDB client login
- Still same error message:
  ```
  "Traceback (most recent call last):
  File "/mnt/c/Users/timkl/Desktop/repos/DB-found-webApp/venv/lib/python3.8/site-packages/pymysql/connections.py", line 613, in connect
    sock = socket.create_connection(
  File "/usr/lib/python3.8/socket.py", line 808, in create_connection
    raise err
  File "/usr/lib/python3.8/socket.py", line 796, in create_connection
    sock.connect(sa)
  ConnectionRefusedError: [Errno 111] Connection refused"
  ```
- Found reference in flask-sqlalchemy docs to try on next chance
  - [flask-sqlalchemy query](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/queries/)

_11-10-22 [TK]_
- Setting up environment variables and config.py as defaults
  - .flaskenv and config.py setup
  - SECRETKEY not set as actual key
  - User/password to be added to DB for use at this stage:
    - Added using users.sql script
      - user: web
      - pw: dbrules
      - SELECT, INSERT, UPDATE on all tables
- Modified search route to return results from previously build analysis table
- Socket onnection error currently, debug using config.py and .flaskenv setup for web@localhost and dbrules password

_11-9-22 [TK]_
- Had issue with ```flask run``` command
  - error on loading flask_sqlalchemy module
  - added pip install command to correct
  - working after adding flask-sqlalchemy v3.0.2
- Fixed search route bug
  - Typo in search.html
  - corrected if formatting in routes.py
  - Adjusted validation rules in forms.py
- Commented out DB connections to continue test runs
- Added wtforms docs link to references

_11-8-22 [TK]_
- Updated createAnalysisTable script to update some items
  - Issue with setting OBP
  - Getting "ERROR 1242 (21000): Subquery returns more than 1 row"
    - Fixed, needed to account that this table has stints for players
  - All other portions of Scripts work
  - Still missing PARC and PARC27 updates

_11-5-22 [TK]_
- Adding base sql file to base folder
- Adding structure for holding all sql scripts/database dumps
- Added check boxes and some more detail in todo section
- Updated worklog instructions
- add 'search' route
  - Basic form setup
  - Route added, can do post and get methods
  - Not confirmed on displaying correctly
  - Screen does not refresh when trying to hardcode a results test
- Added script for creating and inserting base values into analysis table
  - Verified correct, essentially just copies batting so we cna utilize a single ORM
  - May need to create a secondary people table later still to concat the player name
  - Or may just update the table creation for this one
- Added ORM for Analysis table
- Added SQLAlchemy
- Updated init.py for db connection setup
  - Have not set up and/or tested connection yet

_11-3-22 [TK]_
- Added reference folder to hold any reference material needed
  - included image from baseballreference.com
  - also included marked up image with first thoughts on page needs
- added todo items to top tracking
  - This should be broken out a little bit better?

_11-2-22 [TK]_
- Set up repo
- began basic instructions
- setup flask mvp
- stopped before working on webforms
  - added webforms before final sign off
  - based off template in reference tutorial
- Added DB link direct
- next steps
  - complete webforms
  - work on building orm's
  - try simple web app mvp with actual db information

# References

- [Flask Mega Tutorial post 3](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms)
- [DB Link](https://www.seanlahman.com/baseball-archive/statistics/)
- [WTForms documents v3.0.x](https://wtforms.readthedocs.io/en/3.0.x/)
- [flask-sqlalchemy docs v3.0.x](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)
