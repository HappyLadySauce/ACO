@echo off
echo 启动多智能体协作运维系统后端服务...
echo.

REM 激活虚拟环境
call .venv\Scripts\activate.bat

REM 启动服务器
python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

pause 