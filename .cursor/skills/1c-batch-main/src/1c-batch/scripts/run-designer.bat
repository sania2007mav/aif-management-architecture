@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM ============================================================
REM Запуск конфигуратора 1С
REM
REM Требует: .1c-devbase.bat в корне репозитория (см. resolve-1c-repo.bat)
REM ============================================================

call "%~dp0resolve-1c-repo.bat"
if errorlevel 1 exit /b 1
call .\.1c-devbase.bat

REM Определяем тип подключения: сервер или файловая база
if not "%ONEC_SERVER%"=="" (
    set "IB_PARAMS=/S "%ONEC_SERVER%\%ONEC_BASE%""
) else if not "%ONEC_FILEBASE_PATH%"=="" (
    set "IB_PARAMS=/F "%ONEC_FILEBASE_PATH%""
) else (
    echo Ошибка: не указан ни сервер ^(ONEC_SERVER^), ни путь к файловой базе ^(ONEC_FILEBASE_PATH^)
    exit /b 1
)

REM Формируем параметры авторизации
set "AUTH_PARAMS="
if not "%ONEC_USER%"=="" set AUTH_PARAMS=/N"%ONEC_USER%"
if not "%ONEC_PASSWORD%"=="" set AUTH_PARAMS=!AUTH_PARAMS! /P"%ONEC_PASSWORD%"

echo Запуск конфигуратора...

start "" "%ONEC_PATH%" DESIGNER !IB_PARAMS! !AUTH_PARAMS!

echo Конфигуратор запущен
exit /b 0
