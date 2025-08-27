@echo off
echo Starting Elasticsearch for Movie Search Engine...
echo ==================================================

cd /d "e:\_SoftEng\_BeCode\database-advanced\elasticsearch_movie_search"

echo Checking Docker status...
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not running or not accessible.
    echo Please ensure Docker Desktop is running and try again.
    pause
    exit /b 1
)

echo Starting Elasticsearch and Kibana containers...
docker-compose up -d

echo Waiting for Elasticsearch to be ready...
timeout /t 10 /nobreak >nul

echo SUCCESS: Elasticsearch should now be starting!
echo ==================================================
echo Elasticsearch: http://localhost:9200
echo Kibana (optional): http://localhost:5601
echo.
echo Check if it's ready with: docker-compose logs elasticsearch
echo To stop: docker-compose down
pause
