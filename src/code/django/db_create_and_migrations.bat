@echo off
setlocal enabledelayedexpansion

REM List of databases to process
set "DATABASES=django"

set /p REPLY="This will create new databases and delete the existing ones. The existing data will be lost. Do you want to continue? [Y/n] "

if /i "%REPLY%"=="y" (
    set /p PGPASSWORD="Enter PostgreSQL password: "
    echo Starting migration of VNF DBs...

    echo ^>^> Recreating django DBs

    for %%d in (%DATABASES%) do (
        echo ^>^> Recreating %%d DB
        psql -U postgres -c "DROP DATABASE IF EXISTS %%d" -q
        psql -U postgres -c "CREATE DATABASE %%d WITH OWNER django ENCODING 'UTF8'" -q

        if !ERRORLEVEL! neq 0 (
            echo Error creating database %%d
            pause
            exit /b 1
        )
    )

    echo ^>^> Deleting old migrations
    :: Delete all migration files except __init__.py
    for /r %%G in (migrations\*.py) do (
        echo "%%G" | findstr /i "\venv" >nul
        if errorlevel 1 (
            if not "%%~nG"=="__init__.py" (
                echo Deleting migration file: %%G
                del "%%G"
            )
        )
    )

    echo ">> Migrate django_db"
    python manage.py makemigrations django
    python manage.py migrate --database=django_db django

    echo ^>^> Applying migrations
    :: Apply all migrations
    python manage.py migrate

    :: Wait for 3 seconds
    timeout /t 3 >nul

    echo ^>^> Create superuser
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', '', 'admin')" | python manage.py shell

    echo ^>^> Load data to DBs
	python manage.py loaddata --database=django_db django/app/database/data.json

    echo ^>^> Done
)

endlocal