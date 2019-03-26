python -m venv venv\meansunz
"%cd%\venv\meansunz\Scripts\pip.exe" install -r requirements.txt
echo Successfully Created Virtual Environment
"%cd%\venv\meansunz\Scripts\python.exe" meansunz_project/manage.py makemigrations
"%cd%\venv\meansunz\Scripts\python.exe" meansunz_project/manage.py migrate
"%cd%\venv\meansunz\Scripts\python.exe" meansunz_project/populate_meansunz.py
start "" http://127.0.0.1:8000/
"%cd%\venv\meansunz\Scripts\python.exe" meansunz_project/manage.py runserver
pause