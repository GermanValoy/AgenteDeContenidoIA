"""Arma los clips verticales de Solved w/ Mark Manson (campaña ClipFarm).

Mismo diseño que los de Lovable: fondo desenfocado + cuadro al centro, subtítulos
palabra por palabra en todo el clip (obligatorio) y gancho en pantalla los primeros 3 s.
Cada tramo de video se descarga aparte con yt-dlp --download-sections.

Uso (desde esta carpeta): python -I build.py [id_clip ...]
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lovable"))
import build as base  # noqa: E402  (reutiliza subtitulos(), t_ass() y el estilo)

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTES = os.path.join(AQUI, "..", "fuentes", "manson")
SALIDA = os.path.join(AQUI, "salida")

# Tramo descargado: nombre -> (archivo, segundo absoluto de inicio, x del recorte cuadrado 1080x1080).
# Mark aparece a un costado del plano 16:9; el recorte cuadrado lo deja centrado y grande.
TRAMOS = {
    "t1": ("luck_t1.mp4", 240.0, 840),
    "t2": ("luck_t2.mp4", 890.0, 360),
    "t3": ("luck_t3.mp4", 1030.0, 840),
}

# id: (gancho en 2 líneas, archivo de palabras, [(tramo, desde, hasta)])
CLIPS = {
    "01-poker": (("LIFE IS A", "GAME OF POKER"), "luck_palabras.json", [("t1", 244.0, 270.9)]),
    "02-control": (("ACT LIKE YOU", "CONTROL EVERYTHING"), "luck_palabras.json", [("t2", 898.7, 931.6)]),
    # Se salta la frase "Annie talked a lot about how..." para llegar antes a la historia
    "03-wife": (("THE BEST BET", "OF MY LIFE"), "luck_palabras.json", [("t3", 1034.0, 1037.9), ("t3", 1046.5, 1079.2)]),
}

# El video cuadrado termina en y=1500: los subtítulos van justo debajo
base.ASS_HEAD = base.ASS_HEAD.replace(",50,50,400,1", ",50,50,290,1")

base.CLAVE |= {"luck", "poker", "cards", "table", "choices", "control", "everything", "decisions", "honest",
               "hindsight", "asymmetric", "bets", "failing", "success", "nothing", "partner", "life.", "wife"}
base.CORREGIR.update({"um": "", "uh": "", "andy": "Annie"})


def armar(cid):
    gancho, palabras_json, cortes = CLIPS[cid]
    palabras = json.load(open(os.path.join(FUENTES, palabras_json), encoding="utf-8"))
    pal, total = base.palabras_del_clip(palabras, cortes)
    tmp = os.path.join(AQUI, "tmp")
    os.makedirs(tmp, exist_ok=True)
    os.makedirs(SALIDA, exist_ok=True)
    base.subtitulos(pal, total, os.path.join(tmp, f"{cid}.ass"))
    for n, txt in enumerate(gancho, 1):
        open(os.path.join(tmp, f"{cid}_h{n}.txt"), "w", encoding="utf-8").write(txt)

    entradas, partes = [], []
    for i, (tr, a, b) in enumerate(cortes):
        archivo, inicio, x = TRAMOS[tr]
        entradas += ["-ss", f"{a - inicio:.2f}", "-t", f"{b - a:.2f}", "-i", os.path.join(FUENTES, archivo)]
        partes.append(f"[{i}:v]fps=30,setpts=PTS-STARTPTS,split[f{i}][c{i}];"
                      f"[f{i}]scale=-2:1920,crop=1080:1920:{x * 16 // 9}:0,boxblur=24:2,eq=brightness=-0.12[fb{i}];"
                      f"[c{i}]crop=1080:1080:{x}:0[cc{i}];"
                      f"[fb{i}][cc{i}]overlay=0:420,setsar=1[v{i}];"
                      f"[{i}:a]aresample=48000,asetpts=PTS-STARTPTS[a{i}];")
    n = len(cortes)
    fuente = "C\\:/Users/German/Nico_Robot/fonts/Anton-Regular.ttf"
    filtro = "".join(partes) + "".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[cv][ca];"
    filtro += (f"[cv]ass={cid}.ass:fontsdir='C\\:/Users/German/Nico_Robot/fonts',"
               f"drawbox=x=0:y=230:w=1080:h=300:color=black@0.55:t=fill:enable='lt(t,3.2)',"
               f"drawtext=fontfile='{fuente}':textfile={cid}_h1.txt:fontsize=112:fontcolor=white:x=(w-text_w)/2:y=250:borderw=7:bordercolor=black:enable='lt(t,3.2)',"
               f"drawtext=fontfile='{fuente}':textfile={cid}_h2.txt:fontsize=112:fontcolor=0xFFE500:x=(w-text_w)/2:y=385:borderw=7:bordercolor=black:enable='lt(t,3.2)'[v];"
               f"[ca]loudnorm=I=-14:TP=-1.5:LRA=11[a]")
    script = os.path.join(tmp, f"{cid}_filtro.txt")
    open(script, "w", encoding="utf-8").write(filtro)
    out = os.path.join(SALIDA, f"manson_{cid}.mp4")
    cmd = ["ffmpeg", "-v", "error", "-y", *entradas, "-/filter_complex", script, "-map", "[v]", "-map", "[a]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-threads", "2", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out]
    base.subprocess.run(cmd, check=True, cwd=tmp)
    print(f"{cid}: {total:.1f} s -> {out}")


if __name__ == "__main__":
    for cid in sys.argv[1:] or CLIPS:
        armar(cid)
