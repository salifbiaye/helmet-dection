@echo off
echo === Helmet Detection API - Lancement local ===
cd /d "%~dp0backend"

echo Installation des dependances...
pip install fastapi uvicorn python-multipart ultralytics Pillow opencv-python-headless -q

echo.
echo Demarrage de l'API...
echo Swagger UI disponible sur : http://localhost:8000/docs
echo.
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
