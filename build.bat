@echo off
setlocal
cd tools
call py2 parse_shadertoy_json.py WdVXWy 
if errorlevel 1 exit /b
copy /Y ..\build\release\kinderegg.exe "prods\molten bismuth\kinderegg.exe"
copy /Y ..\build\kinderegg.exe "prods\molten bismuth\kinderegg.exe"
cd "prods\molten bismuth"
call "kinderegg.exe"