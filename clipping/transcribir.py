"""Transcribe un audio en inglés con Whisper local (faster-whisper) y guarda:
- <base>_palabras.json: [[segundo, palabra], ...] (mismo formato que vtt_palabras.py)
- <base>.txt: transcripción legible con [mm:ss] al inicio de cada frase

Sirve cuando YouTube bloquea los subtítulos automáticos (error 429).
Uso: python transcribir.py audio.m4a salida_base [modelo]
"""
import json
import subprocess
import sys

import numpy as np
from faster_whisper import WhisperModel

audio, base = sys.argv[1], sys.argv[2]
modelo = sys.argv[3] if len(sys.argv) > 3 else "base.en"

# Se decodifica con ffmpeg (el decodificador interno falla con algunas versiones de PyAV)
pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", audio, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                     capture_output=True, check=True).stdout
muestras = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768.0

m = WhisperModel(modelo, device="cpu", compute_type="int8", cpu_threads=2)
segmentos, _ = m.transcribe(muestras, language="en", word_timestamps=True)

palabras, lineas = [], []
for s in segmentos:
    mm, ss = divmod(int(s.start), 60)
    lineas.append(f"[{mm}:{ss:02d}] {s.text.strip()}")
    for w in s.words:
        if w.word.strip():
            palabras.append([round(w.start, 2), w.word.strip()])
    print(lineas[-1], flush=True)

json.dump(palabras, open(base + "_palabras.json", "w", encoding="utf-8"))
open(base + ".txt", "w", encoding="utf-8").write("\n".join(lineas) + "\n")
print(len(palabras), "palabras")
