@echo off
REM Disable the command output to prevent the command from being displayed on the console
chcp 936
call d:\ProgramData\anaconda3\Scripts\activate C:\Users\pp\.conda\envs\pyside6
start cmd.exe \K "d:\ProgramData\anaconda3\Scripts\activate.bat" "C:\Users\pp\.conda\envs\pyside6" >C:\Users\pp\AppData\Roaming\.anaconda\navigator\scripts\pyside6\console_shortcut-out-2.txt 2>C:\Users\pp\AppData\Roaming\.anaconda\navigator\scripts\pyside6\console_shortcut-err-2.txt



REM Define the name of the folder to delete and the name of the file and destination folder to move
set folder_to_delete1=build
set folder_to_delete2=dist
set file_to_move1=config.ini
set file_to_move2=database.db
set target_folder=dist\main

REM Define the folder to copy and the destination path
set folder_to_copy=animation
set folder_copy_target_path=dist\main


REM Check and delete the specified folder
if exist "%cd%\%folder_to_delete1%" (
    echo Deleting folder: %folder_to_delete1%
    rmdir /s /q "%cd%\%folder_to_delete1%"
) else (
    echo folder %folder_to_delete1% dose not exist.
)
if exist "%cd%\%folder_to_delete2%" (
    echo Deleting folder: %folder_to_delete2%
    rmdir /s /q "%cd%\%folder_to_delete2%"
) else (
    echo folder %folder_to_delete2% dose not exist.
)

"C:\Users\pp\.conda\envs\pyside6\Scripts\pyinstaller.exe" -w main.py

REM Check whether the destination folder exists. If it does not exist, create it
if not exist "%cd%\%target_folder%" (
    echo destination folder: %target_folder% dose not exist，it is being created...
    mkdir "%cd%\%target_folder%"
)

REM Move the file to the destination folder
if exist "%cd%\%file_to_move1%" (
    echo Moving file: %file_to_move1% to %target_folder%
    copy "%cd%\%file_to_move1%" "%cd%\%target_folder%"
) else (
    echo file: %file_to_move1% dose not exist.
)
if exist "%cd%\%file_to_move2%" (
    echo Moving file: %file_to_move2% to %target_folder%
    copy "%cd%\%file_to_move2%" "%cd%\%target_folder%"
) else (
    echo file: %file_to_move2% dose not exist.
)

REM Check and copy the entire folder and its contents to the destination path
if exist "%cd%\%folder_to_copy%" (
    echo Moving file: %folder_to_copy% to %folder_copy_target_path%
    xcopy /e /i "%cd%\%folder_to_copy%" "%folder_copy_target_path%\%folder_to_copy%"
) else (
    echo folder: %folder_to_copy% dose not exist.
)

echo Operation Complete.


@echo Done, PySide6 pkg success!
pause