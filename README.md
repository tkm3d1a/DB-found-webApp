# DB-found-webApp

# Installation information

# Environment information

MariaDB
- 10.x.x

LahmanBaseballDB
- 2019, MySQL

Python 
- 3.8.10 (Running on WSL Ubuntu)

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
```

If running vscode as editor, add the following environment settings...

_.vscode/settings.json_
```json
{
  "python.analysis.extraPaths": [
    "./baseball-web-app"
  ]
}
```

# Worklog

_11-2-22_
- Set up repo
- began basic instructions
- setup flask mvp
- stopped before working on webforms
- next steps
  - complete webforms
  - work on building orm's
  - try simple web app mvp with actual db information