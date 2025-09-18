@echo off
REM TailoRent Setup Script for Windows

echo Setting up TailoRent project...

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Copy environment file
echo Setting up environment...
copy .env.example .env

REM Run migrations
echo Running migrations...
python manage.py makemigrations
python manage.py migrate

REM Create superuser
echo Creating superuser...
python manage.py createsuperuser

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

REM Create logs directory
echo Creating logs directory...
mkdir logs

echo Setup complete! Run 'python manage.py runserver' to start the development server.
pause
