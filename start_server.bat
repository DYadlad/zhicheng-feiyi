@echo off
chcp 65001 >nul
echo ========================================
echo   智承非遗 - 服务器启动脚本
echo ========================================
echo.

echo [1/4] 进入项目目录...
echo 当前目录: %CD%

echo [2/4] 检查Python...
python --version
if %errorlevel% neq 0 (
    echo [错误] Python未找到
    pause
    exit /b 1
)

echo [3/4] 激活虚拟环境...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo 虚拟环境激活成功
) else (
    echo [错误] 虚拟环境不存在
    echo 正在创建虚拟环境...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [错误] 创建虚拟环境失败
        pause
        exit /b 1
    )
    call venv\Scripts\activate.bat
)

echo [4/4] 安装依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [错误] 安装依赖失败
    pause
    exit /b 1
)
echo 依赖安装成功

echo [5/5] 启动服务器...
echo.
echo ========================================
echo   服务器启动中...
echo   请在浏览器中访问: http://localhost:5000
echo   按 Ctrl+C 停止服务器
echo ========================================
echo.

python app.py

pause