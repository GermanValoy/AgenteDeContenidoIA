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
    # "How to Feel Lucky No Matter What Happens" (-rKZe8TEOik). Mark es el de remera negra; Drew, el de gris.
    "fl1": ("fl_t1.mp4", 0.0, 610),
    "fl3": ("fl_t3.mp4", 1334.0, None),  # aparece el tuit a la izquierda: cuadro completo
    # "How to Increase Your Luck in Life" (gMynmU0owYc). Cambia de plano seguido: cada corte lleva su propio x.
    "il1": ("il_t1.mp4", 0.0, 700),
    "il2": ("il_t2.mp4", 429.0, 700),
    "il3": ("il_t3.mp4", 1700.0, 420),
    # Pareja y relaciones, para Instagram. "Bad Relationships, Solved" (Yru-7iow6Zw): Mark de remera marrón.
    "br1": ("bad_v1.mp4", 2470.0, 620),
    "br2": ("bad_v2.mp4", 5450.0, 660),
    # "Romantic Love, Solved" (6ZV8YReYA6U): Mark de remera negra, a la derecha del plano.
    "rl1": ("love_v1.mp4", 140.0, 780),
    "rl2": ("love_v2.mp4", 370.0, 780),
    "rl3": ("love_v3.mp4", 3965.0, 780),
    "rl4": ("love_v4.mp4", 4170.0, 780),
    "rl5": ("love_v5.mp4", 4298.0, 780),
    "rl6": ("love_v6.mp4", 5212.0, 780),
}

# Planos abiertos acercados a la cara de Mark: (x, y, lado del recorte)
BR_ABIERTO = (1240, 280, 640)
RL_ABIERTO = (1200, 100, 720)

# id: (gancho en 2 líneas, archivo de palabras, [(tramo, desde, hasta)])
CLIPS = {
    "01-poker": (("LIFE IS A", "GAME OF POKER"), "luck_palabras.json", [("t1", 244.0, 270.9)]),
    "02-control": (("ACT LIKE YOU", "CONTROL EVERYTHING"), "luck_palabras.json", [("t2", 898.7, 931.6)]),
    # Se salta la frase "Annie talked a lot about how..." para llegar antes a la historia
    "03-wife": (("THE BEST BET", "OF MY LIFE"), "luck_palabras.json", [("t3", 1034.0, 1037.9), ("t3", 1046.5, 1079.2)]),
    "04-buffett": (("BUFFETT'S", "#1 SECRET?"), "feel_lucky_palabras.json", [("fl1", 9.1, 51.5)]),
    "05-ancestors": (("YOUR ANCESTORS", "SURVIVED THIS"), "feel_lucky_palabras.json", [("fl3", 1338.1, 1357.0)]),
    # Cortes con un 4.º valor = x del recorte para ese plano (plano abierto 840, reacción de Drew 200)
    "06-willsmith": (("WILL SMITH'S DAD", "ON LUCK"), "increase_luck_palabras.json", [
        ("il1", 0.0, 5.6), ("il1", 59.9, 75.3, 570), ("il1", 75.3, 89.7, 840), ("il1", 89.7, 97.96),
        ("il1", 97.96, 100.2, 200), ("il1", 100.2, 110.4)]),
    "07-newspaper": (("LUCKY PEOPLE", "SEE THIS"), "increase_luck_palabras.json", [
        ("il2", 431.2, 433.0, 420), ("il2", 433.0, 449.7, 840), ("il2", 449.7, 473.4)]),
    "08-real-job": (("THEY TOLD ME", "GET A REAL JOB"), "increase_luck_palabras.json", [
        ("il3", 1704.5, 1716.0, 840), ("il3", 1716.0, 1739.5), ("il3", 1739.5, 1744.2, 840)]),
    # --- Instagram: pareja y relaciones ---
    "ig1-addicted": (("TOXIC LOVE IS", "AN ADDICTION"), "bad_abs_palabras.json", [("br1", 2474.6, 2528.3)]),
    "ig2-boring": (("WHY HEALTHY LOVE", "FEELS BORING"), "bad_abs_palabras.json", [
        ("br2", 5459.8, 5465.7, BR_ABIERTO), ("br2", 5465.7, 5481.9),
        ("br2", 5517.25, 5535.1), ("br2", 5535.1, 5540.2, BR_ABIERTO), ("br2", 5540.2, 5545.3)]),
    "ig3-feeling": (("LOVE ISN'T", "A FEELING"), "love_abs_palabras.json", [
        ("rl1", 142.7, 157.3), ("rl1", 234.8, 243.8, RL_ABIERTO), ("rl1", 243.8, 265.2)]),
    "ig4-awful": (("DATING A", "RED FLAG?"), "love_abs_palabras.json", [
        ("rl2", 373.1, 378.7, RL_ABIERTO), ("rl2", 378.7, 390.4), ("rl2", 390.4, 404.5, RL_ABIERTO),
        ("rl2", 404.5, 411.7), ("rl2", 411.7, 426.2, RL_ABIERTO)]),
    # Drew (izquierda, remera gris) solo aparece 2 s reaccionando
    "ig5-conman": (("LOVE IS", "NATURE'S CON MAN"), "love_abs_palabras.json", [
        ("rl2", 514.6, 532.4, RL_ABIERTO), ("rl2", 532.4, 539.0), ("rl2", 539.0, 541.0, 300),
        ("rl2", 541.0, 547.5, RL_ABIERTO), ("rl2", 595.4, 614.2, 750), ("rl2", 614.2, 618.5, RL_ABIERTO)]),
    "ig6-chemistry": (("INSTANT CHEMISTRY", "IS A RED FLAG"), "love_abs_palabras.json", [
        ("rl3", 3969.1, 3984.8, RL_ABIERTO), ("rl3", 3984.8, 4002.7), ("rl3", 4002.7, 4017.8, RL_ABIERTO)]),
    "ig7-lovebomb": (("LOVE BOMBING", "ONLY WORKS IF..."), "love_abs_palabras.json", [
        ("rl4", 4173.1, 4192.6), ("rl5", 4301.8, 4323.3, RL_ABIERTO)]),
    # Se salta el "Oh, shucks" de Drew (5244.5-5248.3)
    "ig8-couch": (("WHAT REAL LOVE", "LOOKS LIKE"), "love_abs_palabras.json", [
        ("rl6", 5216.9, 5229.4), ("rl6", 5229.4, 5242.2, RL_ABIERTO), ("rl6", 5242.2, 5244.6),
        ("rl6", 5248.3, 5259.6, RL_ABIERTO), ("rl6", 5259.6, 5267.5), ("rl6", 5267.5, 5279.3, RL_ABIERTO)]),
}

# El video cuadrado termina en y=1500: los subtítulos van justo debajo
base.ASS_HEAD = base.ASS_HEAD.replace(",50,50,400,1", ",50,50,290,1")

base.CLAVE |= {"luck", "poker", "cards", "table", "choices", "control", "everything", "decisions", "honest",
               "hindsight", "asymmetric", "bets", "failing", "success", "nothing", "partner", "wife",
               "buffett", "ovarian", "lottery", "richest", "ancestors", "survived", "toilet", "internet"}
base.CORREGIR.update({"um": "", "uh": "", "andy": "Annie",
                      # Palabrotas: el audio queda igual, pero en pantalla van censuradas
                      "fucking": "f*cking", "bullshit.": "bullsh*t.", "motherfucking": "motherf*cker"})
base.CLAVE |= {"will", "smith's", "luckiest", "newspaper", "photos", "100", "pounds", "lucky", "unlucky.",
               "blogging", "future", "upside", "job?", "fortunate."}


def armar(cid):
    gancho, palabras_json, cortes = CLIPS[cid]
    palabras = json.load(open(os.path.join(FUENTES, palabras_json), encoding="utf-8"))
    pal, total = base.palabras_del_clip(palabras, [c[:3] for c in cortes])
    tmp = os.path.join(AQUI, "tmp")
    os.makedirs(tmp, exist_ok=True)
    os.makedirs(SALIDA, exist_ok=True)
    base.subtitulos(pal, total, os.path.join(tmp, f"{cid}.ass"))
    for n, txt in enumerate(gancho, 1):
        open(os.path.join(tmp, f"{cid}_h{n}.txt"), "w", encoding="utf-8").write(txt)

    entradas, partes = [], []
    for i, (tr, a, b, *propio_x) in enumerate(cortes):
        archivo, inicio, x = TRAMOS[tr]
        if propio_x:
            x = propio_x[0]
        entradas += ["-ss", f"{a - inicio:.2f}", "-t", f"{b - a:.2f}", "-i", os.path.join(FUENTES, archivo)]
        if x is None:  # cuadro 16:9 completo (p. ej. cuando hay un gráfico al costado que se debe leer)
            fondo_x, recorte, y = 1166, "scale=1080:-2", 700
        elif isinstance(x, tuple):  # (x, y, lado): acerca un plano abierto para que la cara de Mark se vea grande
            cx, cy, lado = x
            fondo_x, recorte, y = min(cx * 16 // 9, 2333), f"crop={lado}:{lado}:{cx}:{cy},scale=1080:1080", 420
        else:
            fondo_x, recorte, y = x * 16 // 9, f"crop=1080:1080:{x}:0", 420
        partes.append(f"[{i}:v]fps=30,setpts=PTS-STARTPTS,split[f{i}][c{i}];"
                      f"[f{i}]scale=-2:1920,crop=1080:1920:{fondo_x}:0,boxblur=24:2,eq=brightness=-0.12[fb{i}];"
                      f"[c{i}]{recorte}[cc{i}];"
                      f"[fb{i}][cc{i}]overlay=0:{y},setsar=1[v{i}];"
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
