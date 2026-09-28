@echo off
REM Build script - creates a standalone WAV2MP3Converter.exe
REM Requires: pip install pyinstaller

echo Building WAV2MP3Converter.exe...
pyinstaller --onefile --windowed --name "WAV2MP3Converter" --add-data "ffmpeg/ffmpeg.exe;ffmpeg" main.py

echo.
echo Done! EXE is in: dist\WAV2MP3Converter.exe
pause
