"""Extrae cada palabra con su segundo exacto de los subtítulos automáticos de YouTube (.vtt).

Uso: python vtt_palabras.py entrada.vtt salida.json
"""
import json
import re
import sys

src, dst = sys.argv[1], sys.argv[2]


def seg(h, m, s):
    return int(h) * 3600 + int(m) * 60 + float(s)


cue = re.compile(r"(\d+):(\d+):([\d.]+) -->")
tag = re.compile(r"<(\d+):(\d+):([\d.]+)><c>([^<]*)</c>")
palabras = []
inicio = 0.0
for linea in open(src, encoding="utf-8"):
    m = cue.match(linea)
    if m:
        inicio = seg(*m.groups())
        continue
    if "<c>" not in linea:
        continue
    primera = linea.split("<", 1)[0].strip()
    if primera:
        palabras.append([round(inicio, 2), primera])
    for h, mi, s, w in tag.findall(linea):
        if w.strip():
            palabras.append([round(seg(h, mi, s), 2), w.strip()])

json.dump(palabras, open(dst, "w", encoding="utf-8"))
print(len(palabras), "palabras")
