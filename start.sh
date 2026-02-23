#!/bin/bash

echo "===================================="
echo " Unst2st 本地启动脚本"
echo "===================================="
echo ""

# 检查是否在项目根目录
if [ ! -f "backend/main.py" ]; then
    echo "错误: 请在项目根目录下运行此脚本"
    exit 1
fi

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未检测到Python3，请先安装Python 3.11+"
    exit 1
fi

echo "[1/4] 检查虚拟环境..."
if [ ! -d "backend/venv" ]; then
    echo "创建虚拟环境..."
    cd backend
    python3 -m venv venv
    cd ..
fi

echo "[2/4] 激活虚拟环境并安装依赖..."
source backend/venv/bin/activate
pip install -r backend/requirements.txt

echo "[3/4] 检查环境变量配置..."
if [ ! -f ".env" ]; then
    echo "警告: 未找到.env文件，请复制.env.example并配置ZHIPU_API_KEY"
    echo ""
    read -p "按Enter继续..."
fi

echo "[4/4] 启动服务..."
echo ""
echo "服务将在 http://localhost:8000 启动"
echo "按 Ctrl+C 可停止服务"
echo ""
python3 -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
