import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from convert import batch_convert_wav_to_mp3, get_ffmpeg_path


class ConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WAV → MP3 Converter")
        self.root.geometry("520x560")
        self.root.resizable(False, False)

        # File list
        self.wav_files = []

        self._build_ui()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        pad = {"padx": 10, "pady": 5}

        # ── File buttons ──
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", **pad)

        ttk.Button(btn_frame, text="Add Files",
                   command=self.add_files).pack(side="left", padx=(0, 5))
        ttk.Button(btn_frame, text="Add Folder",
                   command=self.add_folder).pack(side="left")
        ttk.Button(btn_frame, text="Clear",
                   command=self.clear_files).pack(side="right")

        # ── File listbox ──
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill="both", expand=True, **pad)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.file_listbox = tk.Listbox(
            list_frame, selectmode=tk.EXTENDED,
            yscrollcommand=scrollbar.set,
            font=("Consolas", 10),
        )
        self.file_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.file_listbox.yview)

        # ── Settings ──
        settings_frame = ttk.LabelFrame(self.root, text="Settings")
        settings_frame.pack(fill="x", **pad)

        # Bitrate
        ttk.Label(settings_frame, text="Bitrate:").grid(
            row=0, column=0, sticky="w", padx=5, pady=5)
        self.bitrate_var = tk.StringVar(value="320k")
        bitrate_combo = ttk.Combobox(
            settings_frame, textvariable=self.bitrate_var,
            values=["128k", "192k", "256k", "320k"],
            state="readonly", width=8,
        )
        bitrate_combo.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        # Output folder
        ttk.Label(settings_frame, text="Output:").grid(
            row=1, column=0, sticky="w", padx=5, pady=5)
        self.output_var = tk.StringVar(
            value=os.path.join(os.getcwd(), "mp3"))
        ttk.Entry(settings_frame, textvariable=self.output_var).grid(
            row=1, column=1, sticky="ew", padx=5, pady=5)
        ttk.Button(settings_frame, text="Browse",
                   command=self.browse_output).grid(
            row=1, column=2, padx=5, pady=5)

        settings_frame.columnconfigure(1, weight=1)

        # ── Convert button ──
        self.convert_btn = ttk.Button(
            self.root, text="Convert All", command=self.start_conversion)
        self.convert_btn.pack(fill="x", **pad)

        # ── Progress ──
        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            self.root, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill="x", **pad)

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.root, textvariable=self.status_var).pack(
            fill="x", padx=10)

        # ── Log ──
        log_frame = ttk.LabelFrame(self.root, text="Log")
        log_frame.pack(fill="both", expand=True, **pad)

        log_scroll = ttk.Scrollbar(log_frame)
        log_scroll.pack(side="right", fill="y")

        self.log_text = tk.Text(
            log_frame, height=8, state="disabled",
            yscrollcommand=log_scroll.set,
            font=("Consolas", 9),
        )
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scroll.config(command=self.log_text.yview)

    # -------------------------------------------------------------- actions
    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select WAV files",
            filetypes=[("WAV files", "*.wav"), ("All files", "*.*")],
        )
        for f in files:
            if f not in self.wav_files:
                self.wav_files.append(f)
                self.file_listbox.insert("end", os.path.basename(f))

    def add_folder(self):
        folder = filedialog.askdirectory(title="Select folder with WAV files")
        if not folder:
            return
        for name in sorted(os.listdir(folder)):
            if name.lower().endswith(".wav"):
                full = os.path.join(folder, name)
                if full not in self.wav_files:
                    self.wav_files.append(full)
                    self.file_listbox.insert("end", name)

    def clear_files(self):
        self.wav_files.clear()
        self.file_listbox.delete(0, "end")

    def browse_output(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_var.set(folder)

    def start_conversion(self):
        if not self.wav_files:
            messagebox.showwarning("No files", "Add WAV files first.")
            return

        self.convert_btn.config(state="disabled")
        self.progress_var.set(0)
        self._log_clear()

        bitrate = self.bitrate_var.get()
        output_dir = self.output_var.get()

        thread = threading.Thread(
            target=self._convert_thread,
            args=(list(self.wav_files), bitrate, output_dir),
            daemon=True,
        )
        thread.start()

    def _convert_thread(self, files, bitrate, output_dir):
        def on_progress(index, total, filename, status):
            pct = (index / total) * 100
            self.root.after(0, self._update_progress,
                            pct, index, total, filename, status)

        batch_convert_wav_to_mp3(
            files, bitrate=bitrate, output_dir=output_dir,
            progress_callback=on_progress,
        )
        self.root.after(0, self._conversion_finished)

    # ------------------------------------------------------------- updates
    def _update_progress(self, pct, index, total, filename, status):
        self.progress_var.set(pct)
        name = os.path.basename(filename)
        if status == "done":
            self._log(f"✓ {name}")
            self.status_var.set(f"[{index}/{total}] Done: {name}")
        else:
            self._log(f"✗ {name} (error)")
            self.status_var.set(f"[{index}/{total}] Error: {name}")

    def _conversion_finished(self):
        self.convert_btn.config(state="normal")
        self.status_var.set("Conversion finished.")
        self._log("── Done ──")

    def _log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    def _log_clear(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", "end")
        self.log_text.config(state="disabled")


def main():
    root = tk.Tk()
    ConverterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
