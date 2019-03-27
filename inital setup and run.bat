@echo off
echo Setting up virtual environment.. ^
 && python -m venv venv\meansunz ^
 && "%cd%\venv\meansunz\Scripts\activate.bat" ^
 && "%cd%\venv\meansunz\Scripts\pip.exe" install -r requirements.txt ^
 && "%cd%\venv\meansunz\Scripts\python.exe" meansunz_project/manage.py makemigrations ^
 && "%cd%\venv\meansunz\Scripts\python.exe" meansunz_project/manage.py migrate ^
 && "%cd%\venv\meansunz\Scripts\python.exe" meansunz_project/populate_meansunz.py ^
 && start "Meansunz" cmd /c "run meansunz (only use after initial setup).bat" ^
 && pause ^
 ||echo. && echo FAILED TO SETUP ENVIRONMENT PLEASE SET IT UP MANUALLY & pause
