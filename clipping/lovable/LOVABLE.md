# Lovable Clipping: kit de publicación

Campaña: Content Rewards → **Lovable Clipping** ($1 por 1.000 vistas en YouTube, Instagram y TikTok; pago mínimo $0,99).
Fuente: entrevista de Anton Osika en **20VC with Harry Stebbings 2025** (`DHLczPQj9rA`, de la lista oficial de la campaña).

## Reglas que hay que cumplir en cada clip

- [ ] Sale Anton y/o Lovable, y el tema es Lovable (✔ en los 4 clips).
- [ ] Solo podcasts de la lista oficial (✔).
- [ ] Cuenta nueva o de temática IA/startups, **en inglés** (público mayoritario tier 1: EE. UU., Reino Unido, Canadá, Australia).
- [ ] **#LovablePartner** en la descripción.
- [ ] Comentarios activados y **al menos 1 comentario** (fija el tuyo).
- [ ] **Enviar el clip en Content Rewards antes de 10 minutos** después de publicarlo ("Enviar clip" → pegar el enlace).
- [ ] Estar en el Discord de la campaña.

## Los clips (`salida/`)

| Archivo | Duración | Gancho en pantalla |
|---|---|---|
| `lovable_01-weekend.mp4` | 40 s | HE BUILT IT IN ONE WEEKEND |
| `lovable_02-2m-week.mp4` | 36 s | +$2M ARR EVERY WEEK |
| `lovable_03-retention.mp4` | 36 s | BETTER THAN CHATGPT? |
| `lovable_04-claude.mp4` | 30 s | 40,000 PAYING USERS |

## Títulos y descripciones (copiar y pegar)

En YouTube Shorts, el título va en el campo "Título" y el resto en la descripción. En TikTok e Instagram todo va junto en la descripción.

### 01 – One weekend
**Título:** He built the first version of Lovable in one weekend 🤯
```
He put an LLM in a for loop, drank a lot of coffee… and built an AI that writes code in one weekend. Millions of people used it. 🚀
Anton Osika (Lovable) on 20VC
#LovablePartner #lovable #ai #startup #vibecoding #buildinpublic
```
**Comentario para fijar:** `Would you build your app with AI? 👇`

### 02 – $2M ARR every week
**Título:** This AI startup adds $2M in revenue EVERY WEEK 📈
```
Lovable went from $1M to $2M ARR per week… just months after launch. 🤯
Anton Osika (Lovable) on 20VC
#LovablePartner #lovable #ai #startup #saas #founder
```
**Comentario para fijar:** `Fastest growing startup in Europe? 👀`

### 03 – Better retention than ChatGPT
**Título:** "Our retention is better than ChatGPT's" – Lovable CEO
```
Is AI revenue just "sugar revenue"? Lovable's CEO says their month-1 retention beats ChatGPT: 85% 🔥
Anton Osika (Lovable) on 20VC
#LovablePartner #lovable #ai #chatgpt #startup #saas
```
**Comentario para fijar:** `Hype or the real deal? 👇`

### 04 – 40,000 paying users
**Título:** 40,000 paying users… and Claude does the coding 🤖
```
Lovable already has 40,000 paying users. Which AI model does the heavy lifting? Anthropic's Claude. 👀
Anton Osika (Lovable) on 20VC
#LovablePartner #lovable #ai #claude #startup #vibecoding
```
**Comentario para fijar:** `Which AI do you use to code? 👇`

## Cómo publicar

1. Sube **1–2 clips por día** por red, no los 4 juntos (las cuentas nuevas que suben mucho de golpe parecen spam).
2. Horario: **18:00–21:00 de EE. UU. (Este)** = 19:00–22:00 en Argentina/Chile, 17:00–20:00 en Colombia/México CDMX.
3. En TikTok activa **"Contenido generado por IA": NO** (es contenido real del podcast). Idioma de la cuenta: inglés.
4. Fija tu comentario → copia el enlace → **Content Rewards → "Enviar clip"** (antes de 10 min).
5. A las 48 h revisa en cada red **el país del público**: si la mayoría no es tier 1, avísame y ajustamos.

## Registro de publicaciones

Canal: **AI Founders Daily** · https://www.youtube.com/@AIFoundersDailyHQ

| Clip | Red | Publicación | Enlace | Enviado a Content Rewards |
|---|---|---|---|---|
| 02 – $2M every week | YouTube | 10 oct 2026, 19:00 (programado) | https://youtube.com/shorts/OIk3zstaUbY | ☐ |

Ajustes usados en YouTube: portada `salida/portada_*.jpg`, "No es contenido para niños", **Promoción de pago: Sí** (es una campaña pagada por Lovable), Uso de IA: No (es metraje real del podcast).

## Regenerar

```
cd clipping/lovable
python -I build.py            # los 4 clips
python -I build.py 02-2m-week # uno solo
```
Los tramos del podcast están en `clipping/fuentes/tramoN.mp4` (descargados con yt-dlp `--download-sections`).
