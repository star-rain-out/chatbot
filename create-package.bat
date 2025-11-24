@echo off
echo ========================================
echo 项目打包工具
echo ========================================
echo.

REM 获取当前日期作为版本号
set yyyy=%date:~0,4%
set mm=%date:~5,2%
set dd=%date:~8,2%
set version=%yyyy%%mm%%dd%

REM 设置打包文件名
set package_name=chatbot-project-%version%.zip

echo 正在创建项目压缩包...
echo 文件名: %package_name%
echo.

REM 使用 git archive 创建干净的压缩包（自动排除 .gitignore 中的文件）
git archive -o ..\%package_name% HEAD

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo ✓ 打包成功！
    echo ========================================
    echo.
    echo 压缩包位置: ..\%package_name%
    echo.
    echo 已自动排除以下文件/文件夹:
    echo   - node_modules/
    echo   - __pycache__/
    echo   - .venv/
    echo   - build/
    echo   - .git/
    echo   - 其他 .gitignore 中的文件
    echo.
) else (
    echo.
    echo ========================================
    echo ✗ 打包失败！
    echo ========================================
    echo.
    echo 请确保：
    echo 1. 当前目录是 Git 仓库
    echo 2. 所有更改已提交到 Git
    echo.
    echo 如果你还没有提交更改，请先运行：
    echo   git add .
    echo   git commit -m "准备打包"
    echo.
)

pause
