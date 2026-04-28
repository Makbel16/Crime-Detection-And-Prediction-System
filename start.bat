@echo off
echo ========================================
echo Crime Hotspot Detection System
echo ========================================
echo.

echo Starting Backend Server...
start cmd /k "cd backend && py -m uvicorn app.main:app --reload --port 8000"

timeout /t 3 /nobreak > nul

echo Starting Frontend Server...
start cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Both servers are starting...
echo ========================================
echo.
echo Backend: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:5173
echo.
echo Press any key to exit this window...
pause > nul
