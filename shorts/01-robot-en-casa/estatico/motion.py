import subprocess
cuts=[0,5.7,12.5,17.6,23.6,30.5,34.5,40.0]
C="iw/2-(iw/zoom/2)"; M="ih/2-(ih/zoom/2)"
fx=[ # zoom, x, y, extra filter
 ("1+0.14*on/N", C, M, "fade=in:st=0:d=0.6"),
 ("1.06+0.10*on/N", f"{C}+(iw/zoom/6)*on/N", f"{M}-ih*0.03*on/N", ""),
 ("1.08+0.10*on/N", f"{C}+8*sin(on*1.7)", f"{M}+6*cos(on*2.1)", ""),
 ("1.22-0.16*on/N", C, M, ""),
 ("1+0.20*on/N", f"{C}-iw*0.04*on/N", M, "vignette=PI/4,eq=brightness='-0.02+0.03*sin(t*9)'"),
 ("1.05+0.12*on/N", C, f"{M}-ih*0.05*on/N", ""),
 ("1+0.25*on/N", C, f"{M}-ih*0.06*on/N", ""),
]
parts=[]
for i,(z,x,y,ex) in enumerate(fx):
    d=cuts[i+1]-cuts[i]; N=round(d*30)
    vf=f"scale=2160:3840:flags=lanczos,zoompan=z='{z.replace('N',str(N))}':x='{x.replace('N',str(N))}':y='{y.replace('N',str(N))}':d={N}:s=1080x1920:fps=30"+(","+ex if ex else "")+",format=yuv420p"
    out=f"m{i+1}.mp4"
    subprocess.run(['ffmpeg','-y','-v','error','-loop','1','-i',f'img{i+1}.jpg','-vf',vf,'-frames:v',str(N),'-c:v','libx264','-preset','medium','-crf','18',out],check=True)
    parts.append(out)
open('list.txt','w').write(''.join(f"file '{p}'\n" for p in parts))
subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i','list.txt','-c','copy','joined.mp4'],check=True)
subprocess.run(['ffmpeg','-y','-v','error','-i','joined.mp4','-i','voz.mp3','-filter_complex',"[1:a]loudnorm=I=-14:TP=-1.5:LRA=11,apad[a];[0:v]ass=subs.ass[v]",'-map','[v]','-map','[a]','-shortest','-c:v','libx264','-preset','medium','-crf','18','-c:a','aac','-b:a','192k','-movflags','+faststart','short_nico_estatico.mp4'],check=True)
