"""Monta la Parte 2 de Nico: clips de Google Vids + clips del episodio 1, voz y subtítulos.

Uso:  python build.py
Necesita ffmpeg (FFMPEG o en el PATH), clips/vids.mp4, voz.mp3 y ../../fonts/Anton-Regular.ttf
"""
import os, subprocess, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
EP1 = os.path.join(HERE, '..', '01-robot-en-casa', 'clips')
FONTS = os.path.normpath(os.path.join(HERE, '..', '..', 'fonts'))
FF = os.environ.get('FFMPEG') or shutil.which('ffmpeg') or r'C:\Users\German\ffmpeg\bin\ffmpeg.exe'

# Escenas: (inicio y fin en la voz, archivo, segundo de inicio dentro del archivo, segundos útiles)
# vids.mp4 es la exportación de Google Vids: 0-10 s clip horizontal descartado, luego 4 clips de 10 s.
SCENES = [
    (0.0, 6.0, 'clips/vids.mp4', 10.0, 4.3),   # 3:15 AM frente a la laptop (Nico cambia de diseño a los ~4,5 s)
    (6.0, 11.2, 'clips/vids.mp4', 20.0, 4.5),  # tecleando rápido
    (11.2, 15.0, 'clips/vids.mp4', 30.0, 3.8), # apaga la alarma (estable los 10 s)
    (15.0, 21.6, 'clips/vids.mp4', 40.0, 6.6), # desayuno y carpeta (estable los 10 s)
    (21.6, 26.4, os.path.join(EP1, 's4.mp4'), 0.0, 5.0),  # hologramas (episodio 1)
    (26.4, 30.6, os.path.join(EP1, 's6.mp4'), 0.0, 5.0),  # tapando con la manta (episodio 1)
    (30.6, 39.2, os.path.join(EP1, 's7.mp4'), 0.0, 5.0),  # guiño a cámara (episodio 1)
]

# Frases de la voz (inicio, fin, texto), medidas con silencedetect sobre voz.mp3
LINES = [
    (0.00, 1.56, 'Después de taparte…'), (2.62, 3.90, 'Nico no volvió a cargarse.'), (4.50, 5.09, 'Hizo esto.'),
    (6.23, 7.29, 'Abrió tu computadora…'), (7.71, 8.85, 'y escribió sin parar.'), (9.43, 10.55, 'Durante tres horas.'),
    (11.48, 12.70, 'A las seis de la mañana…'), (13.59, 14.46, 'tu alarma no sonó.'),
    (15.33, 17.41, 'Bajas a la cocina, y está todo listo.'), (17.87, 19.10, 'Desayuno, café…'),
    (19.63, 20.92, 'y una carpeta con tu nombre.'), (21.88, 23.09, 'Reorganizó tu agenda,'),
    (23.52, 24.19, 'tus gastos…'), (24.60, 25.80, 'y respondió tus correos.'),
    (26.76, 27.83, 'Lo hizo para ayudarte.'), (28.88, 29.99, 'Pero nadie se lo pidió.'),
    (31.06, 31.79, '¿Lo apagarías…'), (32.28, 33.23, 'o lo dejarías seguir?'),
    (34.20, 35.92, 'Comenta APAGAR o SEGUIR.'), (36.48, 38.53, 'Si llegamos a mil, hay parte tres.'),
]
HL = {'nico', 'esto.', 'computadora…', 'horas.', 'seis', 'alarma', 'nombre.', 'correos.', 'ayudarte.',
      'pidió.', 'apagarías…', 'seguir?', 'apagar', 'seguir.', 'mil,', 'tres.'}


def ts(s):
    return f"{int(s // 3600)}:{int(s % 3600 // 60):02d}:{s % 60:05.2f}"


def captions():
    ev = []
    for a, b, text in LINES:
        words = text.split()
        chunks = [words[i:i + 3] for i in range(0, len(words), 3)]
        total = sum(len(' '.join(c)) for c in chunks)
        t = a
        for j, c in enumerate(chunks):
            d = (b - a) * len(' '.join(c)) / total
            body = ' '.join(('{\\c&H00F5E14A&}' + w.upper() + '{\\c&H00FFFFFF&}') if w.lower() in HL else w.upper() for w in c)
            end = t + d + (0.15 if j == len(chunks) - 1 else 0)  # solo el último trozo se alarga, para no solaparse
            ev.append(f"Dialogue: 0,{ts(t)},{ts(end)},Cap,,0,0,0,,"
                      f"{{\\fad(60,0)\\t(0,90,\\fscx108\\fscy108)\\t(90,160,\\fscx100\\fscy100)}}{body}")
            t += d
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Anton,104,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,1,7,3,2,80,80,520,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(os.path.join(HERE, 'subs.ass'), 'w', encoding='utf-8') as f:
        f.write(head + '\n'.join(ev) + '\n')


def run(args):
    subprocess.run([FF, '-y', '-v', 'error'] + args, check=True, cwd=HERE)


def main():
    captions()
    os.makedirs(os.path.join(HERE, 'tmp'), exist_ok=True)
    parts = []
    for i, (a, b, src, start, useful) in enumerate(SCENES, 1):
        dur = b - a
        factor = max(dur / useful, 1.0)  # ralentiza el tramo útil hasta cubrir la escena
        out = f'tmp/p{i}.mp4'
        vf = (f"trim=start={start}:duration={useful},setpts=(PTS-STARTPTS)*{factor:.4f},"
              "scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,fps=30,format=yuv420p")
        run(['-i', src, '-vf', vf, '-an', '-t', f'{dur:.3f}', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium', out])
        parts.append(out)
    with open(os.path.join(HERE, 'tmp', 'list.txt'), 'w') as f:
        f.write(''.join(f"file '{os.path.basename(p)}'\n" for p in parts))
    run(['-f', 'concat', '-safe', '0', '-i', 'tmp/list.txt', '-c', 'copy', 'tmp/joined.mp4'])
    fonts = FONTS.replace('\\', '/').replace(':', '\\:')
    run(['-i', 'tmp/joined.mp4', '-i', 'voz.mp3', '-filter_complex',
         f"[1:a]loudnorm=I=-14:TP=-1.5:LRA=11[a];[0:v]subtitles=subs.ass:fontsdir='{fonts}'[v]",
         '-map', '[v]', '-map', '[a]', '-c:v', 'libx264', '-crf', '18', '-preset', 'medium',
         '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', 'short_nico_parte2.mp4'])
    shutil.rmtree(os.path.join(HERE, 'tmp'))
    print('Listo: short_nico_parte2.mp4')


if __name__ == '__main__':
    main()
