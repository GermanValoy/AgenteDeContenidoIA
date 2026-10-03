import json,subprocess,re
W=json.load(open('words.json'))
W=[(a,b,('al' if t=='el' else 'necesita' if t=='necesitas' else t)) for a,b,t in W]
HL={'robot','casa','casa.','casa?','noche','pediste.','fábricas.','todo,','conversaciones.','tres','dormir.','taparte.','no?','sí','no.','queja.'}
def ts(s):
    h=int(s//3600);m=int(s%3600//60);x=s%60;return f"{h}:{m:02d}:{x:05.2f}"
# group words: max 3 words, break after punctuation
groups=[];cur=[]
for w in W:
    cur.append(w)
    if len(cur)==3 or re.search(r'[.,?…]$',w[2]): groups.append(cur);cur=[]
if cur: groups.append(cur)
ev=[]
for i,g in enumerate(groups):
    st=g[0][0]; en=groups[i+1][0][0] if i+1<len(groups) else g[-1][1]+0.6
    en=min(en,g[-1][1]+0.5)
    txt=' '.join(('{\\c&H00F5E14A&}'+t.upper()+'{\\c&H00FFFFFF&}') if t.lower() in HL else t.upper() for _,_,t in g)
    ev.append(f"Dialogue: 0,{ts(st)},{ts(en)},Cap,,0,0,0,,{{\\fad(60,0)\\t(0,90,\\fscx108\\fscy108)\\t(90,160,\\fscx100\\fscy100)}}{txt}")
ass=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Anton,104,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,1,7,3,2,80,80,520,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""+"\n".join(ev)+"\n"
open('subs.ass','w').write(ass)
cuts=[0,5.7,12.5,17.6,23.6,30.5,34.5,40.0]
parts=[]
for i in range(7):
    d=cuts[i+1]-cuts[i]; src=f'clips/s{i+1}.mp4'; f=max(d/5.04,1.0); out=f'clips/p{i+1}.mp4'
    vf=f"setpts={f:.4f}*PTS,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p"
    af=f"atempo={1/f:.4f},volume=0.35" if f>1 else "volume=0.35"
    subprocess.run(['ffmpeg','-y','-v','error','-i',src,'-vf',vf,'-af',af,'-t',f'{d:.3f}','-c:v','libx264','-preset','medium','-crf','18','-c:a','aac','-ar','44100','-ac','2',out],check=True)
    parts.append(out)
open('clips/list.txt','w').write(''.join(f"file '{p.split('/')[1]}'\n" for p in parts))
subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i','clips/list.txt','-c','copy','clips/joined.mp4'],check=True)
subprocess.run(['ffmpeg','-y','-v','error','-i','clips/joined.mp4','-i','voz.mp3','-filter_complex',
  "[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,apad[v];[0:a][v]amix=inputs=2:duration=first:normalize=0[a];[0:v]ass=subs.ass[vv]",
  '-map','[vv]','-map','[a]','-c:v','libx264','-preset','medium','-crf','18','-c:a','aac','-b:a','192k','-movflags','+faststart','short_nico_v1.mp4'],check=True)
print(open('subs.ass').read().split('[Events]')[1][:1500])
