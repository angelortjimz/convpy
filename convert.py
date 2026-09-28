import os
import subprocess
import sys


def get_ffmpeg_path():
    """Return path to ffmpeg executable.

    When running as a PyInstaller bundle, ffmpeg.exe is extracted to
    sys._MEIPASS.  Otherwise fall back to whatever is on PATH.
    """
    if getattr(sys, "frozen", False):
        bundle_dir = sys._MEIPASS
        bundled = os.path.join(bundle_dir, "ffmpeg", "ffmpeg.exe")
        if os.path.isfile(bundled):
            return bundled
    return "ffmpeg"


def batch_convert_wav_to_mp3(wav_files, bitrate="320k", output_dir="mp3",
                             progress_callback=None):
    """Convert a list of WAV files to MP3.

    Parameters
    ----------
    wav_files : list[str]
        Paths to .wav files.
    bitrate : str
        Lame bitrate, e.g. "320k".
    output_dir : str
        Destination folder (created if missing).
    progress_callback : callable, optional
        Called after each file with (index, total, filename, status)
        where status is "done" or "error".

    Returns
    -------
    list[tuple[str, str]]
        (filename, status) pairs – status is "done" or "error".
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    ffmpeg = get_ffmpeg_path()
    total = len(wav_files)
    results = []

    for index, wav_file in enumerate(wav_files, start=1):
        base_name = os.path.splitext(os.path.basename(wav_file))[0]
        mp3_file = os.path.join(output_dir, f"{base_name}.mp3")

        command = [
            ffmpeg,
            "-i", wav_file,
            "-codec:a", "libmp3lame",
            "-b:a", bitrate,
            "-y",
            mp3_file,
        ]

        try:
            subprocess.run(
                command,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            results.append((wav_file, "done"))
            if progress_callback:
                progress_callback(index, total, wav_file, "done")
        except subprocess.CalledProcessError:
            results.append((wav_file, "error"))
            if progress_callback:
                progress_callback(index, total, wav_file, "error")
        except FileNotFoundError:
            results.append((wav_file, "error"))
            if progress_callback:
                progress_callback(index, total, wav_file, "error")

    return results
