# Short 01 — Un robot vive en tu casa

**Título:** Un Robot Vive en Tu Casa… y a las 3 AM Hizo Esto 🤖
**Formato:** Short vertical 1080×1920, 40 s, animación 3D estilo Pixar
**Voz:** Jhony (ElevenLabs v3, voz `yWVniEEvuUuglO3fXPga`), latino neutro
**Personaje:** Nico, robot doméstico blanco con paneles celestes, pantalla negra con ojos cian y antena naranja

| # | Corte (s) | Escena | Voz en off |
|---|---|---|---|
| 1 | 0–5,7 | Nico enciende los ojos en una cocina a oscuras | Este robot vive en tu casa… y esta noche hizo algo que no le pediste. |
| 2 | 5,7–12,5 | Mañana soleada: sirve café, las tostadas saltan | Las empresas ya están probando robots humanoides en fábricas. El siguiente paso… es tu casa. |
| 3 | 12,5–17,6 | Dobla ropa a toda velocidad, el perro lo mira | Dobla la ropa, cocina, saca al perro… y nunca se queja. |
| 4 | 17,6–23,6 | Hologramas con la agenda, fotos y mensajes | Pero para ayudarte, necesita saberlo todo: tus horarios, tus gustos… tus conversaciones. |
| 5 | 23,6–30,5 | Pasillo a las 3:00, frente a la puerta del dormitorio | Y una noche, a las tres de la mañana… lo encuentras mirándote dormir. |
| 6 | 30,5–34,5 | Tapa al dueño con una manta | Solo quería taparte. ¿…O no? |
| 7 | 34,5–40 | Mira a cámara y guiña | ¿Tú dejarías entrar un robot a tu casa? Comenta sí o no. |

## Producción
- Imágenes: Seedream 4.5 (9:16, 2K), con la imagen de Nico como referencia en cada escena.
- Animación: Kling V3 Turbo, imagen a video, 5 s, 720p (luego escalado a 1080×1920).
- Montaje: `build.py` (ffmpeg y libass). Necesita la fuente Anton instalada.

```bash
python3 build.py   # usa clips/s1..s7.mp4, voz.mp3, words.json → short_nico_v1.mp4
```

## Publicación
- Descripción: ¿Dejarías entrar un robot a tu casa? 🤖 Comenta SÍ o NO 👇 #robots #inteligenciaartificial #IA #humanoides #shorts
- Marca **Contenido alterado o sintético: Sí** en YouTube Studio.
- Pendiente: añadir música (biblioteca de audio de YouTube o CapCut).
