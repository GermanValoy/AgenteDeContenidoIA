# AgenteDeContenidoIA
Este es un agente especializado en contenido viral para redes sociales: investiga tendencias en YouTube, propone conceptos y produce videos hechos al 100 % con IA (canal sin rostro ni voz propia).

## Estructura
```
investigacion/
  buscar_es.py, buscar_en.py   Busca los videos de IA más vistos de los últimos 30 días (YouTube Data API v3)
  clasificar_temas.py          Filtra y clasifica por tema → datos/videos_ia_clasificados.json
  datos/                       Resultados del 3 oct 2026 (español e inglés) y CSV
  dashboard/                   Radar Viral IA (página HTML con los datos incluidos)
shorts/
  01-robot-en-casa/            Short de Nico: guion, clips, voz, subtítulos, montaje y video final
```

## Requisitos
- Variable de entorno `YOUTUBE_API_KEY` para los scripts de investigación (nunca la guardes en el repositorio).
- `ffmpeg` con libass y la fuente Anton para montar los Shorts.
- Las imágenes, los videos y las voces se generan con Creative Studio IA (gastan monedas).

## Uso rápido
```bash
cd investigacion && python3 buscar_es.py && python3 buscar_en.py && python3 clasificar_temas.py
```
Los scripts leen y escriben `yt.json`, `yt_en.json` y `data.json` en la carpeta actual.
