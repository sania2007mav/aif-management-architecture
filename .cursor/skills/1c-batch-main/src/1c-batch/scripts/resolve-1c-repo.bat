@echo off
REM Поднимаемся от каталога этого файла (обычно .../scripts) к корню репозитория,
REM где лежит .1c-devbase.bat — чтобы build-epf и др. работали при любом текущем каталоге (CI, агент).
cd /d "%~dp0"
:devloop
if exist ".1c-devbase.bat" exit /b 0
set "PREV=%CD%"
cd ..
if /i "%CD%"=="%PREV%" goto :fail
goto devloop
:fail
echo Ошибка: не найден .1c-devbase.bat при подъёме от каталога скриптов %~dp0
echo Скопируйте .1c-devbase.bat.example в корень проекта как .1c-devbase.bat
exit /b 1
