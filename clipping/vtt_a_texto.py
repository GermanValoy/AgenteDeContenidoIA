"""Convierte subtítulos automáticos de YouTube (.vtt) en texto limpio con marcas de tiempo.

Uso: python vtt_a_texto.py entrada.vtt salida.txt [segundos_por_bloque]
"""
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
bloque = int(sys.argv[3]) if len(sys.argv) > 3 else 20

ts = re.compile(r"(\d+):(\d+):(\d+)\.(\d+) -->")
palabras = []  # (segundo, palabra) sin las repeticiones de los subtítulos "rodantes"
t = 0.0
vistos = set()
for linea in open(src, encoding="utf-8"):
    m = ts.match(linea)
    if m:
        h, mi, s, ms = map(int, m.groups())
        t = h * 3600 + mi * 60 + s + ms / 1000
        continue
    if "<c>" not in linea:
        continue  # en el formato automático, las líneas nuevas traen etiquetas <c>
    limpio = re.sub(r"<[^>]+>", "", linea).split()
    for w in limpio:
        palabras.append((t, w))

out = []
actual, texto = 0, []
for sec, w in palabras:
    if sec >= actual + bloque and texto:
        out.append(f"[{int(actual)//60:02d}:{int(actual)%60:02d}] " + " ".join(texto))
        actual, texto = int(sec // bloque * bloque), []
    texto.append(w)
if texto:
    out.append(f"[{int(actual)//60:02d}:{int(actual)%60:02d}] " + " ".join(texto))
open(dst, "w", encoding="utf-8").write("\n".join(out))
print(len(out), "bloques")
