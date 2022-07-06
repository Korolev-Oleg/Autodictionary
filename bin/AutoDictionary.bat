@echo on
set batdir=%~dp0
powershell.exe -windowstyle hidden -command "%batdir%\..\venv\Scripts\python %batdir%\..\entrypoint.py"

