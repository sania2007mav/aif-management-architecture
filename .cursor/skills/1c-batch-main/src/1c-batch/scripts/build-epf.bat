@echo off
chcp 65001 >nul

REM ============================================================
REM Сборка внешней обработки/отчёта из XML
REM
REM Параметры:
REM   %1 - корневой XML-файл обработки
REM   %2 - путь к результирующему EPF/ERF файлу
REM
REM Требует: .1c-devbase.bat в корне репозитория (см. resolve-1c-repo.bat)
REM ============================================================

call "%~dp0resolve-1c-repo.bat"
if errorlevel 1 exit /b 1
call .\.1c-devbase.bat
setlocal enabledelayedexpansion

REM Если в .1c-devbase.bat указан несуществующий ONEC_PATH — ищем любой каталог 8.3.*
if exist "%ONEC_PATH%" goto onec_path_ok
for /d %%V in ("C:\Program Files\1cv8\8.3.*") do if exist "%%~V\bin\1cv8.exe" set "ONEC_PATH=%%~V\bin\1cv8.exe"
for /d %%V in ("C:\Program Files (x86)\1cv8\8.3.*") do if exist "%%~V\bin\1cv8.exe" set "ONEC_PATH=%%~V\bin\1cv8.exe"
:onec_path_ok
if not exist "%ONEC_PATH%" (
	echo Ошибка: не найден 1cv8.exe. Укажите ONEC_PATH в .1c-devbase.bat.
	exit /b 1
)

if "%~2"=="" (
    echo Использование: build-epf.bat ^<XML_FILE^> ^<OUTPUT_FILE^>
    echo.
    echo Пример: build-epf.bat "src\epf\МояОбработка.xml" "build\МояОбработка.epf"
    exit /b 1
)

set "XML_FILE=%~1"
set "OUTPUT_FILE=%~2"

REM Корневой XML — только полное имя файла (не 8.3: иначе пути к Forms/*.xml не совпадут с каталогом выгрузки).
REM Определяем тип подключения: сервер или файловая база
REM IB_PARAMS: avoid nested quotes in set IB_PARAMS (paths with spaces).
if not "%ONEC_SERVER%"=="" (
    set IB_PARAMS=/S "%ONEC_SERVER%\%ONEC_BASE%"
) else if not "%ONEC_FILEBASE_PATH%"=="" (
    set IB_PARAMS=/F "%ONEC_FILEBASE_PATH%"
) else (
    echo Ошибка: не указан ни сервер ^(ONEC_SERVER^), ни путь к файловой базе ^(ONEC_FILEBASE_PATH^)
    exit /b 1
)

REM Формируем параметры авторизации
set "AUTH_PARAMS="
if not "%ONEC_USER%"=="" set AUTH_PARAMS=/N"%ONEC_USER%"
if not "%ONEC_PASSWORD%"=="" set AUTH_PARAMS=!AUTH_PARAMS! /P"%ONEC_PASSWORD%"

echo Сборка обработки...
echo   Платформа: %ONEC_PATH%
echo   Источник: %XML_FILE%
echo   Результат: %OUTPUT_FILE%

"%ONEC_PATH%" DESIGNER !IB_PARAMS! !AUTH_PARAMS! /DisableStartupDialogs /LoadExternalDataProcessorOrReportFromFiles "%XML_FILE%" "%OUTPUT_FILE%" /Out "build\build_epf_last.txt"

if %ERRORLEVEL% equ 0 (
    echo Сборка завершена успешно
) else (
    echo Ошибка сборки
    exit /b 1
)

exit /b 0
