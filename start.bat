@echo off
echo ====================================
echo  Unst2st 本地启动脚本
echo ====================================
echo.

REM 检查是否在项目根目录
if not exist "backend\main.py" (
    echo 错误: 请在项目根目录下运行此脚本
    pause
    exit /b
)

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未检测到Python，请先安装Python 3.11+
    pause
    exit /b
)

echo [1/4] 检查虚拟环境...
if not exist "backend\venv" (
    echo 创建虚拟环境...
    cd backend
    python -m venv venv
    cd ..
)

echo [2/4] 激活虚拟环境并安装依赖...
call backend\venv\Scripts\activate
pip install -r backend\requirements.txt

echo [3/4] 检查环境变量配置...
if not exist ".env" (
    echo 警告: 未找到.env文件，请复制.env.example并配置ZHIPU_API_KEY
    echo.
    pause
)

echo [4/4] 启动服务...
echo.
echo 服务将在 http://localhost:8000 启动
echo 按 Ctrl+C 可停止服务
echo.
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

pause
