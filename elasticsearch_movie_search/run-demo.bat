@echo off
echo ===============================================
echo ELASTICSEARCH MOVIE SEARCH ENGINE - DEMO
echo ===============================================
echo.

cd /d "e:\_SoftEng\_BeCode\database-advanced\elasticsearch_movie_search"

echo Step 1: Checking if virtual environment exists...
if not exist ".venv" (
    echo ERROR: Virtual environment not found!
    echo Please run setup-env.sh first
    pause
    exit /b 1
)

echo Step 2: Activating virtual environment...
call .venv\Scripts\activate.bat

echo Step 3: Checking Elasticsearch connection...
python -c "import requests; r = requests.get('http://localhost:9200'); print('Elasticsearch status:', r.status_code)" 2>nul
if errorlevel 1 (
    echo ERROR: Elasticsearch is not running!
    echo Please start Elasticsearch first using Docker Desktop
    echo or run: docker-compose up -d
    pause
    exit /b 1
)

echo Step 4: Running Movie Search Demo...
echo.
python main.py

echo.
echo Demo completed!
pause
