"""Arma los clips verticales de Lovable a partir de los tramos del podcast 20VC.

Cada clip une uno o más cortes (segundo absoluto del podcast), recorta en vertical,
agrega subtítulos en inglés palabra por palabra y un gancho en pantalla los primeros 3 s.

Uso (desde esta carpeta): python -I build.py [id_clip ...]
"""
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTES = os.path.join(AQUI, "..", "fuentes")
FONTS = os.path.join(AQUI, "..", "..", "fonts")
SALIDA = os.path.join(AQUI, "salida")

# Inicio (segundo absoluto del podcast) de cada tramo descargado
TRAMOS = {1: 430, 2: 1165, 3: 1918, 4: 2095}

# id: (gancho en 2 líneas, [(tramo, desde, hasta)])
CLIPS = {
    "01-weekend": (("HE BUILT IT", "IN ONE WEEKEND"), [(1, 466.4, 498.0), (1, 527.0, 535.4)]),
    "02-2m-week": (("+$2M ARR", "EVERY WEEK"), [(2, 1180.5, 1199.8), (2, 1242.4, 1252.3), (2, 1277.0, 1283.6)]),
    "03-retention": (("BETTER THAN", "CHATGPT?"), [(3, 1928.2, 1964.3)]),
    "04-claude": (("40,000 PAYING", "USERS"), [(4, 2097.6, 2112.6), (4, 2181.3, 2196.5)]),
}

# Palabras resaltadas en amarillo
CLAVE = {"lovable", "million", "2", "two", "1", "85%", "weekend", "40,000", "chatgpt", "chat", "gpt's",
         "claude", "anthropic's", "arr", "retention", "snake", "agent", "code", "coffee", "millions", "ai", "week"}

# Errores típicos del reconocimiento automático de YouTube
CORREGIR = {"chbt": "ChatGPT", "lavall": "Lovable", "lavable": "Lovable", "loveable": "Lovable",
            "ar": "ARR", "claud": "Claude", "anthropics": "Anthropic's", "um": "", "uh": ""}

ASS_HEAD ="""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: S,Anton,118,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,8,3,2,50,50,400,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def t_ass(t):
    h, r = divmod(max(t, 0), 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def palabras_del_clip(palabras, cortes):
    """Palabras de cada corte con el tiempo reubicado en la línea de tiempo del clip."""
    out, base = [], 0.0
    for _, a, b in cortes:
        for t, w in palabras:
            if a <= t < b - 0.05:
                w = CORREGIR.get(w.lower(), w)
                if w:
                    out.append((base + t - a, w))
        base += b - a
    return out, base


def subtitulos(pal, total, ruta):
    lineas = [ASS_HEAD]
    grupos = [pal[i:i + 3] for i in range(0, len(pal), 3)]
    for i, g in enumerate(grupos):
        ini = g[0][0]
        fin = grupos[i + 1][0][0] if i + 1 < len(grupos) else total
        fin = min(fin, ini + 2.5)
        txt = " ".join(
            "{\\c&H00E5FF&}" + w.upper() + "{\\c&HFFFFFF&}" if w.lower().strip(".,?!") in CLAVE else w.upper()
            for _, w in g)
        lineas.append(f"Dialogue: 0,{t_ass(ini)},{t_ass(fin)},S,,0,0,0,,{txt}\n")
    open(ruta, "w", encoding="utf-8").write("".join(lineas))


def armar(cid):
    gancho, cortes = CLIPS[cid]
    palabras = json.load(open(os.path.join(FUENTES, "20vc_palabras.json"), encoding="utf-8"))
    pal, total = palabras_del_clip(palabras, cortes)
    tmp = os.path.join(AQUI, "tmp")
    os.makedirs(tmp, exist_ok=True)
    os.makedirs(SALIDA, exist_ok=True)
    subtitulos(pal, total, os.path.join(tmp, f"{cid}.ass"))
    for n, txt in enumerate(gancho, 1):
        open(os.path.join(tmp, f"{cid}_h{n}.txt"), "w", encoding="utf-8").write(txt)

    entradas, partes = [], []
    for i, (tr, a, b) in enumerate(cortes):
        ini = a - TRAMOS[tr]
        entradas += ["-ss", f"{ini:.2f}", "-t", f"{b - a:.2f}", "-i", os.path.join(FUENTES, f"tramo{tr}.mp4")]
        # Fondo desenfocado + cuadro completo (recortado al 86 % de ancho) al centro:
        # sirve igual para planos de una persona y para pantalla dividida.
        partes.append(f"[{i}:v]fps=30,setpts=PTS-STARTPTS,split[f{i}][c{i}];"
                      f"[f{i}]scale=-2:1920,crop=1080:1920,boxblur=24:2,eq=brightness=-0.12[fb{i}];"
                      f"[c{i}]crop=iw*0.86:ih,scale=1080:-2[cc{i}];"
                      f"[fb{i}][cc{i}]overlay=0:580,setsar=1[v{i}];"
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
    out = os.path.join(SALIDA, f"lovable_{cid}.mp4")
    cmd = ["ffmpeg", "-v", "error", "-y", *entradas, "-/filter_complex", script, "-map", "[v]", "-map", "[a]",
           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-threads", "2", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True, cwd=tmp)
    print(f"{cid}: {total:.1f} s -> {out}")


if __name__ == "__main__":
    for cid in sys.argv[1:] or CLIPS:
        armar(cid)
