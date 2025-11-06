@echo off
echo ===========================================
echo 1. ATIVANDO AMBIENTE VIRTUAL (.venv)
echo ===========================================
call .\.venv\Scripts\activate

echo.
echo ===========================================
echo 2. NAVEGANDO PARA A PASTA DO SERVIDOR
echo ===========================================
cd server

echo.
echo ===========================================
echo 3. INICIANDO SERVIDOR FASTAPI (em 0.0.0.0)
echo Pressione CTRL+C para parar o servidor
echo ===========================================
uvicorn app.main:app --reload --host 0.0.0.0

echo.
echo Servidor foi finalizado.
pause