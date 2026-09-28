import os
import subprocess
import sys

def batch_convert_wav_to_mp3(bitrate="320k"):
    wav_files = [f for f in os.listdir('.') if f.lower().endswith('.wav')]
    if not wav_files:
        print("No .wav files found in this folder.")
        return
    output_folder = "mp3"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print(f"Converting {len(wav_files)} files\n")
    for index, wav_file in enumerate(wav_files, start=1):
        base_name = os.path.splitext(wav_file)[0]
        mp3_file = os.path.join(output_folder, f"{base_name}.mp3")
        print(f"[{index}/{len(wav_files)}] Converting: {wav_file}...", end="\r")
        command = [
            "ffmpeg", 
            "-i", wav_file, 
            "-codec:a", "libmp3lame", 
            "-b:a", bitrate, 
            "-y", 
            mp3_file
        ]
        try:
            # Run the command, hiding ffmpeg's technical logs
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"[{index}/{len(wav_files)}] Done: {base_name}.mp3    ")
        except subprocess.CalledProcessError:
            print(f"[{index}/{len(wav_files)}] Error processing: {wav_file}")
        except FileNotFoundError:
            print("\n Critical error: FFmpeg was not found in the system PATH.")
            return

    print(f"\n Conversion finished.")

if __name__ == "__main__":
    batch_convert_wav_to_mp3()
