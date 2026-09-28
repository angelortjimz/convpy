import os
import subprocess
import sys

def batch_convert_wav_to_mp3(bitrate="320k"):
    archivos_wav = [f for f in os.listdir('.') if f.lower().endswith('.wav')]
    if not archivos_wav:
        print("No se encontraron archivos .wav en esta carpeta.")
        return
    output_folder = "mp3"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print(f"Convirtiendo {len(archivos_wav)} archivos\n")
    for index, wav_file in enumerate(archivos_wav, start=1):
        nombre_base = os.path.splitext(wav_file)[0]
        mp3_file = os.path.join(output_folder, f"{nombre_base}.mp3")
        print(f"[{index}/{len(archivos_wav)}] Convirtiendo: {wav_file}...", end="\r")
        comando = [
            "ffmpeg", 
            "-i", wav_file, 
            "-codec:a", "libmp3lame", 
            "-b:a", bitrate, 
            "-y", 
            mp3_file
        ]
        try:
            # Ejecutamos el comando ocultando los logs técnicos de ffmpeg
            subprocess.run(comando, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"[{index}/{len(archivos_wav)}] Completado: {nombre_base}.mp3    ")
        except subprocess.CalledProcessError:
            print(f"[{index}/{len(archivos_wav)}] Error al procesar: {wav_file}")
        except FileNotFoundError:
            print("\n Error crítico: FFmpeg no se encuentra en el PATH global.")
            return

    print(f"\n Conversión finalizada.")

if __name__ == "__main__":
    batch_convert_wav_to_mp3()