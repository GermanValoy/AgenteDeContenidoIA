import json,re
AI=re.compile(r'\b(ia|ai|a\.i\.|gpt|chatgpt|chat gpt|claude|gemini|agente?s?|agents?|robots?|inteligencia|intelligence|artificial|openai|anthropic|deepseek|llm|grok|copilot|siri|muse|astra|npu|jev|hugging face|altman|amodei|dreamina)\b',re.I)
TH=[('Riesgo y futuro',r'\b(milenio|millennium|frena|advierte|warns?|secret[ao]?|d[eé]cada|progress|godfather|peligro|matar|kill|extinci|human(os|ity)|frenar|scary|terrif|lying|mienten|amenaza|threat|alarm|preocupante|destro|control|whistleblower|hack|ciberataque|cyberattack|crisis|esc[aá]ndalo|scandal|leak|rebel|sufrir|sentir|deprimi|freed|liberad)'),
('Dinero','dinero|money|rico|plata|negocio|side hustle|earn|income|/mo|\$\d|₹|invers|acciones|job'),
('Agentes','agente|agent'),
('Tutorial y curso','tutorial|curso|clase|course|lec |c[oó]mo |how to|how i|paso a paso|explic|explain|guide|gu[ií]a|build|crea |aprende|learn|en \d+ min|in \d+ min'),
('Comparativa',r' vs\.? |versus|mejor(es)? ia|best ai|top \d'),
('Robots','robot|humanoid|moya|agibot'),
('Lanzamientos',r'lanza|launch|nuevo|new |introducing|gpt[- ]?6|astra|muse|2\.0|update|acaba de'),
]
def theme(t):
    for n,p in TH:
        if re.search(p,t,re.I): return n
    return 'Humor y entretenimiento'
out={}
for code,f,pre in (('es','yt.json','es'),('en','yt_en.json','en')):
    rows=[]
    for x in json.load(open(f)):
        if not (x['lang'] or '').startswith(pre): continue
        txt=x['title']+' '+' '.join(x['tags'])
        if not AI.search(txt): continue
        if x['channel'] in ('Maisak','IGN','NEON','CarlosReaccionaTV'): continue
        rows.append(dict(t=x['title'],c=x['channel'],id=x['id'],p=x['pub'],d=x['dur'],v=x['views'],l=x['likes'],k=x['comments'],s=x['subs'],vpd=x['vpd'],vps=x['vps'],e=x['eng'],th=theme(x['title']),f='Short' if x['dur']<180 else 'Largo'))
    out[code]=rows
    from collections import Counter
    print(code,len(rows),Counter(r['th'] for r in rows))
json.dump(out,open('data.json','w'),ensure_ascii=False,separators=(',',':'))
