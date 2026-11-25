@echo off
REM Legacy OSS Guard launcher for Windows
SET DIR=%~dp0
"%DIR%.venv\Scripts\python.exe" -m app.cli %*
