# WAV → MP3 Converter

A simple, self-contained desktop tool to convert WAV files to MP3 using FFmpeg.

## Features

- Add individual files or entire folders
- Choose bitrate (128k / 192k / 256k / 320k)
- Custom output folder
- Progress bar and conversion log
- Fully standalone EXE — no external dependencies

## Usage (EXE)

1. Run `dist/WAV2MP3Converter.exe`
2. Click **Add Files** or **Add Folder** to load WAV files
3. Pick a bitrate and output folder
4. Click **Convert All**

## Usage (Development)

```bash
pip install -r requirements.txt
py main.py
```

## Building the EXE

```bash
pip install pyinstaller
build.bat
```

The EXE will be created at `dist/WAV2MP3Converter.exe`.

## Requirements

- Windows 10/11 (64-bit)
- No other dependencies — FFmpeg is bundled inside the EXE
