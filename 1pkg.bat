@echo off
chcp 936
call d:\ProgramData\anaconda3\Scripts\activate C:\Users\pp\.conda\envs\pyside6
start cmd.exe \K "d:\ProgramData\anaconda3\Scripts\activate.bat" "C:\Users\pp\.conda\envs\pyside6" >C:\Users\pp\AppData\Roaming\.anaconda\navigator\scripts\pyside6\console_shortcut-out-2.txt 2>C:\Users\pp\AppData\Roaming\.anaconda\navigator\scripts\pyside6\console_shortcut-err-2.txt

"C:\Users\pp\.conda\envs\pyside6\Scripts\pyinstaller.exe" -w main.py
@echo Done, PySide6 pkg success!
pause