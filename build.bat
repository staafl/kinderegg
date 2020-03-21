@echo off
setlocal
call py-set-envvar.bat 2
set PATH=%PYTHON_HOME%;%PATH%
cd tools
call py2 parse_shadertoy_json.py MdSXzz 
if errorlevel 1 exit /b
copy /Y ..\build\release\kinderegg.exe "prods\molten bismuth\kinderegg.exe"
copy /Y ..\build\kinderegg.exe "prods\molten bismuth\kinderegg.exe"
cd "prods\molten bismuth"
call "kinderegg.exe"