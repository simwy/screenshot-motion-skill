#!/usr/bin/env python3
"""Native 2D editor previews for all registered effects; 3D is approximated.

Run in an isolated environment with pyJianYingDraft 0.2.7 and Pillow.
"""
import argparse
import json
import math
import shutil
from pathlib import Path
from PIL import Image, ImageDraw
import pyJianYingDraft as draft
from motion import duration, mix


def progress(f, a, b):
    t = max(0, min(1, (f-a)/(b-a)))
    return 1-(1-t)**3


def lerp(a, b, t):
    return a+(b-a)*t


def export(job, out):
    job, out = Path(job).resolve(), Path(out).resolve()
    d = json.loads((job/'project.json').read_text(encoding='utf-8'))
    name = d['template']
    if name == 'storybook':
        from storybook_native import export as book_export
        return book_export(job, out)
    if name not in ('spotlight', 'launch', 'orbit', 'kinetic', 'prism', 'flipstack'):
        raise ValueError('No native recipe for '+name)
    if out.exists():
        raise FileExistsError(out)
    sources = [(job/'public/screenshots'/p['file']).resolve() for p in d['pages']]
    if len(sources) != 5 or any(not p.is_file() or not p.is_relative_to(job/'public/screenshots') for p in sources):
        raise ValueError('Five safe source screenshots are required')
    total = duration(d)[1]
    out.parent.mkdir(parents=True, exist_ok=True)
    s = draft.DraftFolder(str(out.parent)).create_draft(out.name,1920,1080,fps=30,maintrack_adsorb=False)
    media = out/'media'; media.mkdir()
    for i, source in enumerate(sources):
        shutil.copy2(source, media/f'screen-{i}{source.suffix}')
    dark = name not in ('spotlight','kinetic')
    bg = {'spotlight':'#F5F7FC','launch':'#090D14','orbit':'#07090E','kinetic':'#F6F1E8','prism':'#161127','flipstack':'#050906'}[name]
    ink = '#F4F7FC' if dark else '#172B46'
    accent = d['accent']; serial = 0
    us = lambda f: round(f*1000000/30)
    def plate(key, size, color, border=None):
        im=Image.new('RGBA',size,color)
        if border: ImageDraw.Draw(im).rectangle((1,1,size[0]-2,size[1]-2),outline=border,width=3)
        im.save(media/(key+'.png'))
        return media/(key+'.png')
    background=plate('background',(1920,1080),bg)
    rule=plate('accent',(16,16),accent)
    paper=plate('card-frame',(480,854),'#FAF8F2','#D3D9E4')
    def add(seg, label, z, kind):
        nonlocal serial
        serial+=1; track=f'{serial:03d} {label}'
        s.add_track(kind,track,absolute_index=z);s.add_segment(seg,track)
    # State is center x/y, width/height, rotation degrees, opacity.
    # Sampling preserves easing within the editor's 2D keyframe vocabulary.
    def animate(seg, start, end, state, dims=None):
        for f in sorted(set(range(start,end,3))|{end-1}):
            x,y,w,h,rot,alpha=state(f)
            values=[(draft.KeyframeProperty.position_x,(x-960)/960),
                    (draft.KeyframeProperty.position_y,(540-y)/540),
                    (draft.KeyframeProperty.rotation,rot),
                    (draft.KeyframeProperty.alpha,max(0,min(1,alpha)))]
            if dims:
                iw,ih=dims; fit=min(1920/iw,1080/ih)
                values += [(draft.KeyframeProperty.scale_x,max(.001,w/(iw*fit))),
                           (draft.KeyframeProperty.scale_y,max(.001,h/(ih*fit)))]
            for key,value in values:seg.add_keyframe(key,us(f-start),value)
    def image(path,start,end,state,label,z):
        seg=draft.VideoSegment(str(path),draft.trange(us(start),us(end-start)))
        with Image.open(path) as im: dims=im.size
        animate(seg,start,end,state,dims);add(seg,label,z,draft.TrackType.video)
    def text(value,start,end,x,y,size,label,z=900,color=ink,bold=False,alpha=None):
        if not value:return
        lines=value if isinstance(value,list) else [value]
        for i,line in enumerate(lines):
            # Native multiline copy stays independently editable. Approximate width
            # is used only to place left-aligned text; native font metrics may differ.
            fs=min(size,700/max(1,len(line))/.56)
            width=len(line)*fs*.53
            seg=draft.TextSegment(line,draft.trange(us(start),us(end-start)),style=draft.TextStyle(size=fs/12,bold=bold,color=tuple(int(color[j:j+2],16)/255 for j in (1,3,5)),align=0))
            animate(seg,start,end,lambda f,i=i:(x+width/2,y+i*size*1.12,1,1,0,alpha(f) if alpha else 1))
            add(seg,label,z,draft.TrackType.text)
    def card(i,start,end,state,z=20):
        image(paper,start,end,lambda f:(state(f)[0],state(f)[1],state(f)[2]+12,state(f)[3]+12,state(f)[4],state(f)[5]),f'Frame {i+1}',z)
        path=media/f'screen-{i}{sources[i].suffix}'
        with Image.open(path) as im: iw,ih=im.size
        def fitted(f):
            x,y,w,h,r,a=state(f);fit=min(w/iw,h/ih)
            return x,y,iw*fit,ih*fit,r,a
        image(path,start,end,fitted,f'Replace screenshot {i+1}',z+1)
    def copy(page,start,end,x=100,y=330,size=82,closing=False):
        fade=lambda f:progress(f,start,start+24)
        title=d['closingTitle'] if closing else d['coverTitle'] if page is None else page['title']
        tag=d['brand'] if page is None or closing else page['tag']
        body=[d['cta'] if closing else d['tagline']] if page is None or closing else page['body']
        text(tag,start,end,x,y-65,20,'Label',color=accent,alpha=fade)
        text(title,start,end,x,y,size,'Headline',bold=True,alpha=fade)
        text(body,start,end,x,y+len(title)*size*1.12+35,25,'Body',alpha=fade)
    image(background,0,total,lambda f:(960,540,1920,1080,0,1),'Background',0)
    text(d['brand'],0,total,80,65,28,'Brand',bold=True)
    text(d['tagline'],0,total,1120,65,18,'Tagline')
    image(rule,0,total,lambda f:(80+880*f/(total-1),1030,1760*f/(total-1),3,0,1),'Progress',800)
    if name=='spotlight':
        for i in range(5):
            def state(f,i=i):
                order=[3,1,0,2,4][i];q=progress(f,30+order*7-order*order*.45,77+order*7-order*order*.45)
                focus=progress(f,130,168)*(1-progress(f,262,300));intro=progress(f,0,27)
                ex=310+i*325;x=lerp(960+(i-2)*17,ex,q);y=lerp(650+(i-2)*9,628+abs(i-2)*18,q)-math.sin(math.pi*q)*70
                w=lerp(272,425 if i==2 else 240,focus)
                return lerp(x,1320 if i==2 else ex+(-400 if i<2 else 400),focus),lerp(y,563 if i==2 else y+55,focus)+(1-intro)*160,w,w*16/9,lerp((i-2)*5,(i-2)*3,q)*(1-focus),intro*(1 if i==2 else 1-focus)
            card(i,0,total,state,50 if i==2 else 20+i*2)
        copy(None,0,145,480,205,70);copy(d['pages'][2],151,275,143,390,80);copy(None,300,total,470,210,65,True)
    elif name=='orbit':
        for i in range(5):
            def state(f,i=i):
                end=progress(f,420,465);intro=progress(f,0,42)
                angle=lerp(-.6,-math.tau/5*progress(f,90,124),progress(f,45,90))-(progress(f,200,234)+progress(f,310,344))*math.tau/5
                theta=angle+i*math.tau/5;z=(math.cos(theta)+1)/2;w=lerp(lerp(185,365,z),228,end)
                return lerp(1250+math.sin(theta)*460,410+i*275,end),lerp(550+math.sin(theta)*50-(1-z)*130,758+abs(i-2)*13,end)+(1-intro)*160,w,w*16/9,lerp(-math.sin(theta)*9,(i-2)*3,end),intro
            def rank(f):
                angle=lerp(-.6,-math.tau/5*progress(f,90,124),progress(f,45,90))-(progress(f,200,234)+progress(f,310,344))*math.tau/5
                return sorted(range(5),key=lambda j:math.cos(angle+j*math.tau/5)).index(i)
            start=0
            for f in range(1,total+1):
                if f==total or rank(f)!=rank(start):
                    card(i,start,f,state,20+rank(start)*2)
                    start=f
        copy(None,0,90)
        for i in range(3):copy(d['pages'][i+1],90+i*110,200+i*110)
        copy(None,465,total,400,220,65,True)
    elif name=='prism':
        for i in range(5):
            card(i,0,100,lambda f,i=i:(lerp(1250,790+i*190,progress(f,10+i*6,45+i*6))+112,505+abs(i-2)*39,225*max(.04,progress(f,10+i*6,45+i*6)),400,-6,progress(f,10+i*6,45+i*6)),20+i*2)
        copy(None,0,100,100,330)
        for scene in range(3):
            start=100+scene*90;copy(d['pages'][scene+1],start,start+90)
            for layer in [2,1,0]:
                card((scene+1+layer)%5,start,start+90,lambda f,l=layer,st=start:(1247+l*110+(1-progress(f,st+l*3,st+32+l*3))*420,495+l*35,355,631,l*4-3,1-l*.27),30-layer*2)
        copy(None,370,total,390,235,65,True)
        for i in range(5):card(i,370,total,lambda f,i=i:(429+i*267,722+(i%2)*38+(1-progress(f,375+i*4,405+i*4))*480,238,423,0,1),20+i*2)
    elif name=='kinetic':
        copy(None,0,60,95,205,100)
        for i in range(5):card(i,0,60,lambda f,i=i:(365+i*294,761+(i%2)*55+(1-progress(f,8+i*3,35+i*3))*520,240,427,(i-2)*-5,1),20+i*2)
        for i in range(4):
            start=60+i*75;end=start+75;x=990 if i%2 else 95
            image(rule,start,end,lambda f,i=i,st=start:((445 if i%2 else 1475)+(1-progress(f,st,st+23))*(-950 if i%2 else 950),540,890,1080,0,1),'Color panel',2)
            copy(d['pages'][i],start,end,x,370)
            card((i+4)%5,start,end,lambda f,i=i,st=start:((305 if i%2 else 1505),543+(1-progress(f,st,st+23))*170,290,516,-14 if i%2 else 14,.65),20)
            card(i,start,end,lambda f,i=i,st=start:((437 if i%2 else 1367),525+(1-progress(f,st,st+23))*170,405,720,(1-progress(f,st,st+23))*(-12 if i%2 else 12),1),30)
        copy(None,360,total,450,220,70,True)
        for i in range(5):card(i,360,total,lambda f,i=i:(417+i*270,737+abs(i-2)*28+(1-progress(f,365+i*2,392+i*2))*600,215,382,(i-2)*5,1),20+i*2)
    elif name=='launch':
        copy(None,0,90,110,335,100)
        for i in range(5):card(i,0,90,lambda f,i=i:(1100+(i%3)*280,300+(i//3)*550+(1-progress(f,0,55))*180,300,533,-12,.48),20+i*2)
        for i,(start,end) in enumerate([(90,195),(195,300),(300,405),(405,480)]):
            x=1050 if i==1 else 100;copy(d['pages'][i],start,end,x,320,85)
            box=[(1340,545,900,750),(551,547,662,774),(1395,550,850,760),(960,730,1720,300)][i]
            card(i,start,end,lambda f,b=box,st=start:(b[0]+120*(1-progress(f,st,st+30)),b[1],b[2],b[3],0,progress(f,st,st+15)),20)
        copy(None,480,total,110,305,90,True)
        card(4,480,total,lambda f:(1492,500,325,578,8,progress(f,480,500)),20)
        card(0,480,total,lambda f:(1255,512,390,693,-6,progress(f,480,500)),30)
    elif name=='flipstack':
        sheet=plate('sheet',(760,500),'#F8FAF6','#D3D9D0')
        for i in range(5):
            start=0 if i==0 else 60+i*90;end=150+i*90 if i<4 else total
            def state(f,st=start):
                q=progress(f,st,st+28);w=912*max(.04,q)
                return 1416-w/2,500, w,600, (1-q)*18,1
            image(sheet,start,end,state,'Editable page',20)
            card(i,start,end,lambda f,st=start:(730,500,270*max(.04,progress(f,st,st+28)),510,(1-progress(f,st,st+28))*18,1),30)
            copy(d['pages'][i],start,end,920,340,42)
        copy(None,510,total,100,910,35,True)
    # Native directional wipes, kept separate from editable screenshots/copy.
    cuts={'kinetic':[60,135,210,285,360],'launch':[90,300],'prism':[100,190,280,370]}.get(name,[])
    for c in cuts:image(rule,c-6,c+8,lambda f,c=c:(-1000+4000*progress(f,c-6,c+8),540,1900 if name!='prism' else 220,1080,0,.9),'Transition',1000)
    for role in ('music','effects'):
        if (job/'audio-manifest.json').exists():
            path=mix(job,role)
            if path:
                dest=media/f'{role}.wav';shutil.copy2(path,dest);track='Audio '+role;s.add_track(draft.TrackType.audio,track);s.add_segment(draft.AudioSegment(str(dest),draft.trange(0,us(total))),track)
    s.save()
    meta_path=out/'draft_meta_info.json';meta=json.loads(meta_path.read_text(encoding='utf-8'));meta.update(draft_name=out.name,draft_fold_path=str(out),draft_root_path=str(out.parent),tm_duration=us(total));meta_path.write_text(json.dumps(meta))
    (out/'EDITING.md').write_text(f'''# {name} native 2D preview
Screenshots and text are independent native segments. Keep keyframes when replacing images.
This is a 2D reconstruction, not a pixel-identical render: perspective, mesh bending,
blur, lighting, typography, crop regions and some decorative details differ.
Orbit uses short native image segments to preserve depth ordering; replace every
occurrence of an image, or regenerate through the skill for a consistent replacement.
Use the accompanying rendered reference to compare the original effect.
Client compatibility requires testing in the actual installed build.
''')
    print(out)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--job',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();export(a.job,a.out)
