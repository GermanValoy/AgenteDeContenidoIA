import os, json, re, urllib.request, urllib.parse, datetime as dt
K=os.environ['YOUTUBE_API_KEY']; B='https://www.googleapis.com/youtube/v3/'
def get(ep,**p):
    p['key']=K; u=B+ep+'?'+urllib.parse.urlencode(p)
    return json.load(urllib.request.urlopen(u,timeout=30))
now=dt.datetime.now(dt.timezone.utc); after=(now-dt.timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%SZ')
Q=["artificial intelligence","AI tools","ChatGPT","make money with AI","automate with AI","AI agents","Gemini AI","Claude AI","free AI tools","AI tutorial"]
ids={}
for q in Q:
    r=get('search',part='id',q=q,type='video',order='viewCount',publishedAfter=after,relevanceLanguage='en',maxResults=25)
    for it in r.get('items',[]): ids.setdefault(it['id']['videoId'],q)
ids=list(ids); vids=[]
for i in range(0,len(ids),50):
    vids+=get('videos',part='snippet,statistics,contentDetails',id=','.join(ids[i:i+50]))['items']
chs=list({v['snippet']['channelId'] for v in vids}); subs={}
for i in range(0,len(chs),50):
    for c in get('channels',part='statistics',id=','.join(chs[i:i+50]))['items']:
        subs[c['id']]=int(c['statistics'].get('subscriberCount',0) or 0)
def dur(s):
    m=re.match(r'P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?',s); d,h,mi,se=[int(x or 0) for x in m.groups()]; return d*86400+h*3600+mi*60+se
out=[]
for v in vids:
    s=v['snippet']; st=v['statistics']; pub=dt.datetime.fromisoformat(s['publishedAt'].replace('Z','+00:00'))
    days=max((now-pub).total_seconds()/86400,0.5); views=int(st.get('viewCount',0)); likes=int(st.get('likeCount',0)); com=int(st.get('commentCount',0))
    sb=subs.get(s['channelId'],0)
    out.append(dict(id=v['id'],title=s['title'],channel=s['channelTitle'],lang=s.get('defaultAudioLanguage') or s.get('defaultLanguage'),pub=s['publishedAt'][:10],days=round(days,1),dur=dur(v['contentDetails']['duration']),views=views,likes=likes,comments=com,subs=sb,vpd=round(views/days),vps=round(views/sb,2) if sb else None,eng=round((likes+com)/views*100,2) if views else 0,tags=s.get('tags',[])[:10]))
out.sort(key=lambda x:-x['views'])
json.dump(out,open('yt_en.json','w'),ensure_ascii=False,indent=1)
print(len(out),'videos')
