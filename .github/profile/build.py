"""Render original SVG profile panels. Python standard library only."""
from __future__ import annotations
import argparse
from datetime import date
from html import escape
import json
import math
import os
from pathlib import Path
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
BG, PAPER, LIME, MUTED, LINE = '#171B17', '#F3F0DF', '#C4F464', '#B8C0AF', '#434B3D'

def text(x,y,value,size=28,color=PAPER,weight=400,mono=False,anchor='start'):
    family="'Courier New',monospace" if mono else 'Arial,Helvetica,sans-serif'
    tracking='-1.7' if size>=50 else ('1' if mono else '0')
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="{family}" font-size="{size}" font-weight="{weight}" letter-spacing="{tracking}" text-anchor="{anchor}">{escape(str(value))}</text>'

def lines(x,y,values,size=28,gap=39,color=MUTED,weight=400):
    return ''.join(text(x,y+i*gap,v,size,color,weight) for i,v in enumerate(values))

def line(x1,y1,x2,y2,color=LINE,width=1):
    return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="{width}"/>'

def arrow(x,y,size=40,color=LIME):
    return f'<path d="M{x} {y+size}l{size} -{size}m-{size} 0h{size}v{size}" stroke="{color}" stroke-width="3" fill="none"/>'

def frame(w,h,title,content,desc='',css=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc" fill="none"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc or title)}</desc><style>{css}@media(prefers-reduced-motion:reduce){{.snake{{animation:none!important}}.motion{{display:none}}}}</style><path fill="{BG}" d="M0 0h{w}v{h}H0z"/><path fill="{LIME}" d="M0 0h{8 if w==640 else 12}v{h}H0z"/>{content}</svg>'

def intro(m):
    if m:
        c=line(34,35,606,35)+lines(32,111,['EU JUNTO','AS PEÇAS.'],66,72,PAPER,800)
        c+=lines(34,243,['Da regra de negócio à interface.','Da API ao banco de dados.'],29,40,LIME)
        c+=lines(34,357,['Sou Gabriel Francisconi.','Construo aplicações web, sistemas','de gestão e automações.','','Entre projetos para clientes, pesquisa','aplicada e experimentos, gosto de','fazer as peças trabalharem juntas.'],27,39)
        return frame(640,660,'Gabriel Francisconi — Eu junto as peças',c)
    c=line(54,30,1226,30)+lines(50,135,['EU JUNTO','AS PEÇAS.'],76,82,PAPER,800)
    c+=text(54,310,'GABRIEL FRANCISCONI',17,LIME,mono=True)
    c+=lines(600,110,['Da regra de negócio à interface.','Da API ao banco de dados.'],30,41,PAPER)
    c+=lines(600,230,['Aplicações web, sistemas de gestão','e automações. Projetos para clientes,','pesquisa aplicada e experimentos.'],27,39)
    return frame(1280,390,'Gabriel Francisconi — Eu junto as peças',c)

PROJECTS=[
('sicc','SICC','GESTÃO DE CONTRATOS',['Processos, tramitação, documentos','versionados, auditoria e relatórios.'],['Java / Spring Boot','React / PostgreSQL'],'https://github.com/moments342/SICC'),
('manyevents','MANYEVENTS','REGRAS QUE SE CONECTAM',['Eventos, inscrições e indicações.','Uma API com ranking de participantes.'],['Java / Spring Boot / MySQL'],'https://github.com/moments342/ManyEvents_API'),
('weather','WEATHER API','DADOS QUE VÊM DE FORA',['Consulta meteorológica por cidade.','Integração com um serviço externo.'],['Java / Spring / API externa'],'https://github.com/moments342/WeatherAPI')]

def diagram(kind,x,y,scale=1):
    if kind=='sicc':
        c=f'<path d="M0 40h82v85h82v85h82" stroke="{LIME}" stroke-width="3"/>'
        for xx,yy,label in [(0,40,'PROCESSO'),(82,125,'CONTRATO'),(164,210,'DOCUMENTO')]:
            c+=f'<rect x="{xx-8}" y="{yy-8}" width="16" height="16" fill="{BG}" stroke="{LIME}" stroke-width="2"/>'+text(xx+20,yy-18,label,14,MUTED,mono=True)
    elif kind=='manyevents':
        c=f'<path d="M40 20v65h140v65M40 85v65m140-65h75" stroke="{LIME}" stroke-width="2"/>'
        for xx,yy in [(40,20),(40,150),(180,150),(255,85)]:c+=f'<circle cx="{xx}" cy="{yy}" r="12" fill="{BG}" stroke="{LIME}" stroke-width="2"/>'
        c+=text(75,45,'INSCRIÇÃO',14,MUTED,mono=True)+text(75,125,'INDICAÇÃO',14,MUTED,mono=True)
    else:
        c=f'<circle cx="130" cy="85" r="70" stroke="{LINE}"/><circle cx="130" cy="85" r="42" stroke="{LIME}" stroke-width="2"/><path d="M0 85h260M130 0v170" stroke="{LINE}"/><path d="M0 85h88m84 0h88" stroke="{LIME}" stroke-width="3"/><circle cx="130" cy="85" r="7" fill="{LIME}"/>'
    return f'<g transform="translate({x} {y}) scale({scale})">{c}</g>'

def project(item,m):
    kind,name,label,description,tech,_=item
    if m:
        c=line(34,22,606,22)+text(32,110,name,84 if kind=='sicc' else 54,PAPER,800)+arrow(552,65,37)
        c+=text(34,160,label,18,LIME,mono=True)+lines(34,225,description,27,39)
        c+=diagram(kind,180,306,.9)+line(34,550,606,550)+lines(34,597,tech,23,34,PAPER)
        c+=text(606,675,'ABRIR REPOSITÓRIO',17,LIME,mono=True,anchor='end')
        return frame(640,710,name,c,name+'. '+' '.join(description+tech)+'. Abra o repositório.')
    h=470 if kind=='sicc' else 400
    c=line(54,20,1226,20)+text(50,154 if kind=='sicc' else 130,name,132 if kind=='sicc' else 73,PAPER,800)
    c+=text(54,203 if kind=='sicc' else 176,label,17,LIME,mono=True)+lines(54,270 if kind=='sicc' else 232,description,27,39)
    c+=diagram(kind,900,85 if kind=='sicc' else 65)+arrow(1184,h-72,29)+line(54,h-88,1226,h-88)
    c+=text(54,h-42,' / '.join(tech),22,PAPER)+text(1155,h-42,'ABRIR REPOSITÓRIO',15,LIME,mono=True,anchor='end')
    return frame(1280,h,name,c,name+'. '+' '.join(description+tech)+'. Abra o repositório.')

def stack(m):
    rows=[('INTERFACE',['TypeScript / React / Vite']),('BACKEND',['Java / Spring Boot','Node.js / NestJS']),('DADOS',['PostgreSQL / MySQL']),('EXECUÇÃO E QUALIDADE',['Docker / Git / GitHub Actions','Playwright'])]
    if m:
        c=lines(32,94,['AS PEÇAS','SE CONECTAM.'],57,65,PAPER,800)+text(34,219,'MINHA STACK DE TRABALHO',17,LIME,mono=True)
        y=294
        for label,values in rows:
            c+=line(34,y-32,606,y-32)+text(34,y,label,19,LIME,mono=True)+lines(34,y+49,values,28,39,PAPER);y+=160
        return frame(640,950,'Minha stack de trabalho',c)
    c=text(50,100,'AS PEÇAS SE CONECTAM.',65,PAPER,800);y=205
    for label,values in rows:
        c+=line(54,y-40,1226,y-40)+text(54,y+7,label,18,LIME,mono=True)+f'<circle cx="365" cy="{y}" r="6" fill="{LIME}"/>'+lines(415,y+9,values,32,41,PAPER)
        if y<595:c+=line(365,y+9,365,y+123)
        y+=130
    return frame(1280,760,'Minha stack de trabalho',c)

def method(m):
    if m:
        c=lines(32,100,['POR BAIXO','DA INTERFACE.'],57,65,PAPER,800);y=251
        for title,body in [('ENTENDER',['O domínio vem antes da','estrutura de pastas.']),('CONSTRUIR',['Permissões, estados e recuperação','fazem parte da experiência.']),('CONFERIR',['Testar o comportamento, olhar','a interface e voltar aos detalhes.'])]:
            c+=text(34,y,title,32,LIME,800)+lines(34,y+47,body,27,38);y+=171
        c+=line(34,765,606,765)+text(34,819,'CONTINUA NO CÓDIGO.',37,PAPER,800)+arrow(550,786,38)+text(34,869,'MOMENTS342 / REPOSITÓRIOS',17,LIME,mono=True)
        return frame(640,910,'Entender, construir e conferir. Explorar repositórios.',c)
    c=text(50,100,'POR BAIXO DA INTERFACE.',65,PAPER,800)
    for x,title,body in [(54,'ENTENDER',['O domínio vem antes da','estrutura de pastas.']),(453,'CONSTRUIR',['Permissões, estados e falhas','fazem parte da experiência.']),(854,'CONFERIR',['Testar o comportamento.','Olhar. Refinar. Repetir.'])]:c+=text(x,194,title,29,LIME,800)+lines(x,241,body,24,35)
    c+=line(54,329,1226,329)+text(54,405,'CONTINUA NO CÓDIGO.',57,PAPER,800)+arrow(1170,361,48)+text(54,455,'MOMENTS342 / EXPLORAR REPOSITÓRIOS',17,LIME,mono=True)
    return frame(1280,495,'Entender, construir e conferir. Explorar repositórios.',c)

def validate_calendar(calendar):
    days=[d for w in calendar['weeks'] for d in w['contributionDays']]
    if not days or len(calendar['weeks'])>54:raise ValueError('Invalid contribution calendar')
    seen=set()
    for d in days:
        date.fromisoformat(d['date'])
        if d['date'] in seen or not isinstance(d['contributionCount'],int) or d['contributionCount']<0 or d['weekday'] not in range(7):raise ValueError('Invalid contribution day')
        seen.add(d['date'])
    if sum(d['contributionCount'] for d in days)!=calendar['totalContributions']:raise ValueError('Calendar total does not match its days')
    return days

def activity(calendar,m):
    days=validate_calendar(calendar);weeks=calendar['weeks'][-26:] if m else calendar['weeks'];w,h=(640,850) if m else (1280,620);x=34 if m else 54
    c=lines(x,94,['CÓDIGO EM','MOVIMENTO.'],58,65,PAPER,800) if m else text(x,99,'CÓDIGO EM MOVIMENTO.',66,PAPER,800)
    c+=text(x,226 if m else 155,'UM MAPA VIVO DAS CONTRIBUIÇÕES',17,LIME,mono=True)
    ox,oy,step,depth=(143,342,15.1,8.3) if m else (192,235,19.2,4.4)
    palette=['#242D22','#526D33','#7BA546',LIME];maximum=max(d['contributionCount'] for d in days) or 1;route=[];tiles=[]
    for i,week in enumerate(weeks):
        actual=week['contributionDays']
        for d in actual:
            j=d['weekday'];count=d['contributionCount'];xx=ox+(i-j)*step;yy=oy+(i+j)*depth
            elevation=0 if count==0 else 8+math.log1p(count)/math.log1p(maximum)*(46 if m else 62)
            color=palette[0 if count==0 else min(3,1+int(count/maximum*2))];a,b=step*.85,depth*.85
            points=f'{xx},{yy-elevation-b} {xx+a},{yy-elevation} {xx},{yy-elevation+b} {xx-a},{yy-elevation}'
            tile=f'<g><title>{d["date"]}: {count} contribuições</title>'
            if elevation:tile+=f'<path d="M{xx-a} {yy-elevation}l{a} {b}v{elevation}l-{a} -{b}Z" fill="#40542D"/><path d="M{xx} {yy-elevation+b}l{a} -{b}v{elevation}l-{a} {b}Z" fill="#2E3C25"/>'
            tile+=f'<polygon points="{points}" fill="{color}" stroke="{LINE}" stroke-width=".55"/></g>';tiles.append((i+j,tile))
        for d in (actual if i%2==0 else list(reversed(actual))):
            j=d['weekday'];route.append((ox+(i-j)*step,oy+(i+j)*depth+3))
    c+=''.join(tile for _,tile in sorted(tiles,key=lambda t:t[0]))
    path=' '.join(('M' if i==0 else 'L')+f'{p[0]:.2f} {p[1]:.2f}' for i,p in enumerate(route))
    c+=f'<path d="{path}" stroke="{LIME}" stroke-width="1" stroke-opacity=".12"/><path class="snake" d="{path}" pathLength="1000" stroke="{PAPER}" stroke-width="{5 if m else 6}" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="9 991"/><circle class="motion" r="{4 if m else 5}" fill="{LIME}"><animateMotion dur="32s" repeatCount="indefinite" path="{path}"/></circle>'
    count=calendar['totalContributions'];stamp=days[-1]['date']
    if m:c+=line(34,650,606,650)+text(34,699,f'{count} contribuições / 12 meses',26,PAPER)+lines(34,749,['Cada bloco é um dia.','A altura acompanha a atividade.','Recorte do mapa: últimas 26 semanas.'],22,32)
    else:c+=line(54,500,1226,500)+text(54,548,f'{count} contribuições / últimos 12 meses',26,PAPER)+text(1226,548,'CADA BLOCO = UM DIA',16,LIME,mono=True,anchor='end')+text(54,589,f'Dados do GitHub • {stamp}',17,MUTED)+text(1226,589,'A ALTURA ACOMPANHA A ATIVIDADE',14,MUTED,mono=True,anchor='end')
    return frame(w,h,'Mapa animado das contribuições de Gabriel Francisconi',c,f'{count} contribuições nos últimos 12 meses. Cada bloco é um dia. Dados do GitHub até {stamp}.','.snake{animation:travel 32s linear infinite}@keyframes travel{to{stroke-dashoffset:-1000}}')

def fetch_calendar():
    token=os.environ.get('GH_TOKEN') or os.environ.get('GITHUB_TOKEN')
    if not token:raise RuntimeError('GH_TOKEN or GITHUB_TOKEN is required')
    query='query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{contributionCount date weekday}}}}}}'
    request=Request('https://api.github.com/graphql',data=json.dumps({'query':query,'variables':{'login':'moments342'}}).encode(),headers={'Authorization':'Bearer '+token,'Content-Type':'application/json','User-Agent':'moments342-profile'})
    with urlopen(request,timeout=30) as response:payload=json.load(response)
    if payload.get('errors'):raise RuntimeError('GitHub refused the contribution calendar query')
    calendar=payload['data']['user']['contributionsCollection']['contributionCalendar'];validate_calendar(calendar);return calendar

def render(calendar):
    output={}
    for m in (False,True):
        suffix='-mobile' if m else ''
        def put(name,value):
            ET.fromstring(value)
            if any(t in value.lower() for t in ['godot','gdscript','foreignobject','<script']):raise ValueError('Unwanted panel content')
            output[f'assets/{name}{suffix}.svg']=value+'\n'
        put('intro',intro(m));put('activity',activity(calendar,m))
        c=text(34 if m else 54,90,'PROJETOS ABERTOS.',49 if m else 66,PAPER,800)+lines(34 if m else 54,139,['Sistemas com contexto.','Código para explorar.'] if m else ['Sistemas com contexto. Código para explorar.'],24 if m else 26,34)
        put('projects',frame(640 if m else 1280,220 if m else 195,'Projetos abertos',c))
        for item in PROJECTS:put(item[0],project(item,m))
        put('stack',stack(m));put('method',method(m))
    return output

def main():
    p=argparse.ArgumentParser();p.add_argument('--calendar',type=Path);p.add_argument('--activity-only',action='store_true');args=p.parse_args()
    calendar=json.loads(args.calendar.read_text(encoding='utf-8-sig')) if args.calendar else fetch_calendar();output=render(calendar)
    if args.activity_only:output={k:v for k,v in output.items() if k.startswith('assets/activity')}
    # Validate every panel before updating output. Failed fetches preserve the last good map.
    for path,body in output.items():
        target=ROOT/path;target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists() or target.read_text(encoding='utf-8')!=body:target.write_text(body,encoding='utf-8')
    print(f'Rendered {len(output)} panels from {calendar["totalContributions"]} real contributions.')

if __name__=='__main__':main()
