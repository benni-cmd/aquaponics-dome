@echo off
rem Startet den Kuppel-Viewer (Port 4410) falls noetig und oeffnet ihn im Browser.
rem Laeuft der Server schon, wird nichts doppelt gestartet.
set PY=C:\Users\benkn\AppData\Local\Programs\Python\Python312\python.exe
cd /d "%~dp0.."

netstat -ano | findstr /r /c:":4410 .*0\.0\.0\.0:0" >nul
if %errorlevel%==0 goto open

start "Kuppel Viewer Server" /min "%PY%" viewer\serve.py 4410

set /a tries=0
:wait
ping -n 2 127.0.0.1 >nul
netstat -ano | findstr /r /c:":4410 .*0\.0\.0\.0:0" >nul
if %errorlevel%==0 goto open
set /a tries+=1
if %tries% LSS 15 goto wait

:open
start "" http://localhost:4410
