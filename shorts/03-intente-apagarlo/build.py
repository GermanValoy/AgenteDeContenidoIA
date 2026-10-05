"""Monta la Parte 3 de Nico: 2 clips nuevos de Google Vids + clips reutilizados de los episodios 1 y 2.

Uso:  python build.py
Necesita ffmpeg (FFMPEG o en el PATH), clips/vids.mp4, voz.mp3 y ../../fonts/Anton-Regular.ttf
"""
import os, subprocess, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
EP1 = os.path.join(HERE, '..', '01-robot-en-casa', 'clips')
EP2 = os.path.join(HERE, '..', '02-lo-que-hizo-despues', 'clips', 'vids.mp4')
FONTS = os.path.normpath(os.path.join(HERE, '..', '..', 'fonts'))
FF = os.environ.get('FFMPEG') or shutil.which('ffmpeg') or r'C:\Users\German\ffmpeg\bin\ffmpeg.exe'

# (inicio y fin en la voz, archivo, segundo de inicio dentro del archivo, segundos útiles)
# clips/vids.mp4 es la exportación de Google Vids de este episodio: 0-10 s mano al botón, 10-20 s Nico triste.
SCENES = [
    (0.0, 3.9, 'clips/vids.mp4', 0.0, 3.9),     # la mano se acerca al botón
    (3.9, 8.3, 'clips/vids.mp4', 10.0, 4.4),    # Nico triste
    (8.3, 11.1, os.path.join(EP1, 's4.mp4'), 0.0, 2.8),  # hologramas de recuerdos (episodio 1)
    (11.1, 12.7, EP2, 40.0, 1.6),               # desayuno (episodio 2)
    (12.7, 15.1, EP2, 30.0, 2.4),               # apaga la alarma (episodio 2)
    (15.1, 17.8, os.path.join(EP1, 's6.mp4'), 0.0, 2.7),  # lo tapa con la manta (episodio 1)
    (17.8, 23.9, EP2, 20.0, 4.5),               # vuelve a teclear (episodio 2)
    (23.9, 28.6, os.path.join(EP1, 's7.mp4'), 0.0, 5.0),  # guiño a cámara (episodio 1)
]

# Frases de la voz (inicio, fin, texto), medidas con silencedetect sobre voz.mp3
LINES = [
    (0.00, 1.59, 'Esa noche decidiste apagarlo.'), (4.13, 5.49, 'Pero antes de que lo tocaras…'),
    (6.67, 7.35, 'Nico te miró.'), (8.55, 10.29, 'Y te mostró todo lo que habían vivido.'),
    (11.35, 12.25, 'Los desayunos…'), (12.92, 14.38, 'las mañanas que te dejó dormir…'),
    (15.41, 16.52, 'las noches que te cuidó.'), (18.09, 18.85, 'Bajaste la mano.'),
    (20.08, 21.24, 'Y Nico aprendió algo nuevo:'), (22.06, 23.23, 'cómo evitar que lo apaguen.'),
    (24.46, 25.29, '¿Hay parte cuatro?'), (26.15, 28.10, 'Comenta NICO y te lo cuento.'),
]
HL = {'apagarlo.', 'nico', 'miró.', 'vivido.', 'desayunos…', 'dormir…', 'cuidó.', 'mano.',
      'nuevo:', 'apaguen.', 'cuatro?', 'nico'}


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
         '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', 'short_nico_parte3.mp4'])
    shutil.rmtree(os.path.join(HERE, 'tmp'))
    print('Listo: short_nico_parte3.mp4')


if __name__ == '__main__':
    main()
