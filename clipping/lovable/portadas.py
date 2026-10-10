"""Genera la portada (1080x1920) de cada clip: un fotograma del podcast con el mismo
diseño del clip (fondo desenfocado + cuadro al centro) y el gancho en grande.

Uso (desde esta carpeta): python -I portadas.py
"""
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import AQUI, CLIPS, FUENTES, SALIDA, TRAMOS

# Segundo absoluto del podcast elegido como fotograma de portada (Anton en cámara)
FOTOGRAMA = {"01-weekend": 478.0, "02-2m-week": 1196.0, "03-retention": 1953.0, "04-claude": 2109.0}

FUENTE = "C\\:/Users/German/Nico_Robot/fonts/Anton-Regular.ttf"

for cid, ((l1, l2), cortes) in CLIPS.items():
    tramo = cortes[0][0]
    tmp = os.path.join(AQUI, "tmp")
    for n, txt in enumerate((l1, l2, "ANTON OSIKA  ·  LOVABLE CEO"), 1):
        open(os.path.join(tmp, f"{cid}_p{n}.txt"), "w", encoding="utf-8").write(txt)
    filtro = (
        "split[f][c];"
        "[f]scale=-2:1920,crop=1080:1920,boxblur=24:2,eq=brightness=-0.18[fb];"
        "[c]crop=iw*0.86:ih,scale=1080:-2[cc];"
        "[fb][cc]overlay=0:700,"
        f"drawtext=fontfile='{FUENTE}':textfile={cid}_p1.txt:fontsize=150:fontcolor=white:x=(w-text_w)/2:y=200:borderw=9:bordercolor=black,"
        f"drawtext=fontfile='{FUENTE}':textfile={cid}_p2.txt:fontsize=150:fontcolor=0xFFE500:x=(w-text_w)/2:y=390:borderw=9:bordercolor=black,"
        f"drawtext=fontfile='{FUENTE}':textfile={cid}_p3.txt:fontsize=58:fontcolor=white:x=(w-text_w)/2:y=1500:borderw=5:bordercolor=black"
    )
    script = os.path.join(tmp, f"{cid}_portada.txt")
    open(script, "w", encoding="utf-8").write(filtro)
    out = os.path.join(SALIDA, f"portada_{cid}.jpg")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{FOTOGRAMA[cid] - TRAMOS[tramo]:.2f}",
                    "-i", os.path.join(FUENTES, f"tramo{tramo}.mp4"), "-/vf", script,
                    "-frames:v", "1", "-q:v", "2", out], check=True, cwd=tmp)
    print(out)
