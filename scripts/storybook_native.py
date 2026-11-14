#!/usr/bin/env python3
"""Editable Storybook draft: native images/text and synchronized page-fold keyframes.

No rendered screenshot plates. Paper is procedural artwork; the mesh curl is
approximated by a horizontal page fold. Requires pyJianYingDraft and Pillow.
"""
import argparse
import json
from pathlib import Path
import shutil
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import pyJianYingDraft as draft


def ease(t):
    t = max(0, min(1, t))
    return 4*t**3 if t < .5 else 1-(-2*t+2)**3/2


def export(job, out):
    job, out = Path(job).resolve(), Path(out).resolve()
    p = json.loads((job/'project.json').read_text())
    if p['template'] != 'storybook':
        raise ValueError('Native layout currently supports storybook only')
    if out.exists():
        raise ValueError(f'Refusing to overwrite {out}')
    sources = []
    for page in p['pages']:
        source = (job/'public/screenshots'/page['file']).resolve()
        if not source.is_relative_to(job/'public/screenshots') or not source.is_file():
            raise ValueError('Missing or unsafe screenshot')
        sources.append(source)
    fontroot = Path('/System/Library/Fonts/Supplemental')
    if not (fontroot/'Arial.ttf').exists():
        raise ValueError('This macOS exporter needs locally installed Arial fonts')
    n, hold = len(sources), p['holdFrames']
    close = 90+n*hold+(n-1)*42
    total = close+102
    us = lambda f: round(f*1_000_000/30)
    out.parent.mkdir(parents=True, exist_ok=True)
    script = draft.DraftFolder(str(out.parent)).create_draft(out.name,1920,1080,fps=30,maintrack_adsorb=False)
    media = out/'media'; media.mkdir()
    accent = p['accent']
    # These geometric plates contain no screenshot pixels or text.
    bg = Image.new('RGB',(1920,1080))
    px = bg.load()
    for y in range(1080):
        for x in range(1920):
            t = min(1,(x/1920+y/1080)/2)
            px[x,y] = tuple(round(a+(b-a)*t) for a,b in zip((243,242,239),(207,216,224)))
    bg.save(media/'background.png')
    paper = Image.new('RGB',(640,760),'#FAF8F2'); dr=ImageDraw.Draw(paper)
    dr.line((46,697,594,697), fill='#D8D6CC', width=1)
    paper.save(media/'paper.png')
    cover=Image.new('RGB',(640,760),accent); dr=ImageDraw.Draw(cover)
    dr.rectangle((34,34,606,726),outline='#7AA7DF',width=1)
    for x in range(45):
        shade=Image.new('RGBA',cover.size,(0,0,0,0)); ImageDraw.Draw(shade).line((x,0,x,760),fill=(0,0,0,int(85*(1-x/45))))
        cover=Image.alpha_composite(cover.convert('RGBA'),shade)
    cover.save(media/'cover.png')
    Image.new('RGB',(54,4),accent).save(media/'rule.png')
    # Shadow/binding remains separate from the editable page surfaces.
    for name,w in [('spread',1280),('closed',640)]:
        plate=Image.new('RGBA',(w+120,880)); shadow=Image.new('RGBA',plate.size)
        ImageDraw.Draw(shadow).rounded_rectangle((48,55,w+72,835),radius=9,fill=(29,36,57,90))
        plate=Image.alpha_composite(plate,shadow.filter(ImageFilter.GaussianBlur(22)))
        d=ImageDraw.Draw(plate); d.rounded_rectangle((48,40,w+72,831),radius=7,fill=accent)
        for j in range(13,-1,-1):
            d.rectangle((59,50+j,w+61,813+j),fill='#C2C4BE' if j%3==0 else '#E4E1D8')
        plate.save(media/f'{name}.png')
    serial=0
    def add(seg, name, z, kind):
        nonlocal serial
        serial+=1; track=f'{serial:03d} {name}'
        script.add_track(kind,track,absolute_index=z)
        script.add_segment(seg,track)
    def shift(f):
        return -320*(1-ease((f-45)/45)+ease((f-close)/42))
    def animate(seg,start,end,x,y,sx,sy,fold=None,moving=True):
        frames={start,end-1}
        for a,b in [(45,90),(close,close+42)]+([fold[:2]] if fold else []):
            frames.update(range(max(start,a),min(end,b+1),2))
            for f in (a,b):
                if start<=f<end: frames.add(f)
        for f in sorted(frames):
            q=1
            if fold:
                a,b,incoming=fold
                q=ease((f-a)/(b-a)) if incoming else 1-ease((f-a)/(b-a))
                q=max(.001,q)
            xx=960+(x-960)*q+(shift(f) if moving else 0)
            for key,value in [(draft.KeyframeProperty.position_x,(xx-960)/960),
                              (draft.KeyframeProperty.position_y,(540-y)/540),
                              (draft.KeyframeProperty.scale_x,sx*q),
                              (draft.KeyframeProperty.scale_y,sy)]:
                seg.add_keyframe(key,us(f-start),value)
    def pic(file,start,end,x,y,w,h,name,z,fold=None,moving=True):
        path=media/file; im=Image.open(path); iw,ih=im.size
        fit=min(1920/iw,1080/ih)
        seg=draft.VideoSegment(str(path),draft.trange(us(start),us(end-start)))
        animate(seg,start,end,x,y,w/(iw*fit),h/(ih*fit),fold,moving)
        add(seg,name,z,draft.TrackType.video)
    def text(value,start,end,x,baseline,size,name,z,color='#172B46',bold=False,fold=None,moving=True,maxwidth=524):
        # Jianying renders text above video on legacy projects. Delay underlying
        # right-page labels until the turning face passes the spine.
        if 382 <= z <= 502 and name.startswith('第') and ('截图标题' in name or 'right' in name):
            start = max(start, 68 if start == 0 else start+21)
            if end == close+42: end = close+21
        if not value or end <= start: return
        font=ImageFont.truetype(str(fontroot/('Arial Bold.ttf' if bold else 'Arial.ttf')),size)
        width=font.getlength(value)
        if width>maxwidth:
            size=max(10,size*maxwidth/width); width=maxwidth
        # pyJianYingDraft uses a size unit equivalent to 12 canvas pixels at 1080p.
        seg=draft.TextSegment(value,draft.trange(us(start),us(end-start)),
            style=draft.TextStyle(size=size/12,bold=bold,color=tuple(int(color.lstrip('#')[i:i+2],16)/255 for i in (0,2,4)),align=0))
        animate(seg,start,end,x+width/2,baseline-size*.35,1,1,fold,moving)
        add(seg,name,z,draft.TrackType.text)
    pic('background.png',0,total,960,540,1920,1080,'背景',0,moving=False)
    pic('closed.png',0,90,1280,550,760,880,'开场书脊与阴影',1)
    pic('spread.png',90,close,960,550,1400,880,'书脊与阴影',1)
    pic('closed.png',close,total,1280,550,760,880,'结尾书脊与阴影',1)
    text(p['brand'].upper(),0,total,82,70,25,'品牌',900,bold=True,moving=False)
    text('A BETTER WAY TO WORK — ONE PAGE AT A TIME',0,total,82,101,13,'页眉',900,color='#687785',moving=False,maxwidth=1000)
    for i,page in enumerate(p['pages']):
        previous=45 if i==0 else 90+(i-1)*(hold+42)+hold
        turn=90+i*(hold+42)+hold
        for side in ('left','right'):
            if side=='left':
                start=68 if i==0 else previous+21
                end=close+21 if i==n-1 else turn+21
                fold=(68 if i==0 else previous+21,90 if i==0 else previous+42,True)
                # Last left page contracts into the spine during closing.
                x0,z=320,100+i*10
            else:
                start=0 if i==0 else previous
                end=close+42 if i==n-1 else turn+21
                fold=None if i==n-1 else (turn,turn+21,False)
                x0,z=960,500-i*10
            label=f'第{i+1}页'
            pic('paper.png',start,end,x0+320,540,640,760,label+'纸张',z,fold)
            if side=='right':
                target=f'screenshot-{i+1:02d}{sources[i].suffix}'
                shutil.copy2(sources[i],media/target)
                iw,ih=Image.open(media/target).size; ratio=min(544/iw,586/ih)
                pic(target,start,end,1280,539,iw*ratio,ih*ratio,label+'截图（右键替换）',z+1,fold)
                text(page['key'],start,end,1008,214,16,label+'截图标题',z+2,accent,True,fold)
            else:
                text(f'CHAPTER {i+1:02d}',start,end,378,229,17,label+'章节',z+2,accent,True,fold)
                text(page['tag'],start,end,378,265,13,label+'标签',z+2,'#7D8B98',False,fold)
                y=360
                for j,line in enumerate(page['title']):
                    text(line,start,end,376,y,64,label+f'标题{j+1}',z+2,bold=True,fold=fold); y+=69
                pic('rule.png',start,end,405,y+6,54,4,label+'装饰线',z+1,fold)
                y+=63
                for j,line in enumerate(page['body']):
                    text(line,start,end,378,y,24,label+f'正文{j+1}',z+2,'#596A7B',fold=fold); y+=36
                text(page['detail'],start,end,378,801,24,label+'补充说明',z+2,bold=True,fold=fold)
            text(p['brand'].upper()+' / PRODUCT BOOK',start,end,x0+46,886,13,label+side+'页脚',z+2,'#7E867F',fold=fold)
            text(str(i*2+(1 if side=='left' else 2)).zfill(2),start,end,x0+567,886,15,label+side+'页码',z+2,'#7E867F',fold=fold)
    for closing,start,end,fold in [(False,0,68,(45,68,False)),(True,close+21,total,(close+21,close+42,True))]:
        name='封底' if closing else '封面'; z=800
        pic('cover.png',start,end,1280,540,640,760,name+'纸张',z,fold)
        text(p['brand'].upper(),start,end,1029,270,31,name+'品牌',z+1,'#FFFFFF',True,fold)
        text('THE PRODUCT BOOK',start,end,1030,309,14,name+'副标题',z+1,'#B5CEF0',fold=fold)
        for j,line in enumerate(p['closingTitle'] if closing else p['coverTitle']):
            text(line,start,end,1026,455+j*83,73,name+f'标题{j+1}',z+1,'#FFFFFF',True,fold)
        text(p['cta'] if closing else p['tagline'],start,end,1030,792,27 if closing else 17,name+'行动文案',z+1,'#DAE9FF',fold=fold)
        text(p['tagline'],start,end,1030,845,12,name+'底部文字',z+1,'#A6C4EB',fold=fold)
    text(p['tagline'],0,total,82,1006,16,'底部标语',900,'#596A7B',moving=False,maxwidth=1300)
    # Preserve optional independently mixed audio stems.
    if (job/'audio-manifest.json').exists():
        from motion import mix
        for role in ('music','effects'):
            source = mix(job, role)
            if source:
                target = media/f'{role}.wav'; shutil.copy2(source,target)
                script.add_track(draft.TrackType.audio,role)
                script.add_segment(draft.AudioSegment(str(target),draft.trange(0,us(total))),role)
    script.save()
    meta_path=out/'draft_meta_info.json'; meta=json.loads(meta_path.read_text())
    meta.update(draft_name=out.name,draft_fold_path=str(out),draft_root_path=str(out.parent),tm_duration=us(total))
    meta_path.write_text(json.dumps(meta,ensure_ascii=False))
    (out/'EDITING.md').write_text('''# Storybook 原生可编辑草稿
截图为独立图片片段：在时间线选中截图，右键替换素材。文字为原生文字片段：选中后在文本面板修改。
每一行文字独立，保留原版行位置；较长的新文字可能需要调整字号。请保留片段关键帧。
原版纸面弯曲、透视和动态阴影以原生水平折页近似，不是逐帧复刻。
没有包含预渲染截图视频，换图后不会在转场中出现旧截图。截图比例变化后请检查尺寸。
本版本仅支持 Storybook。草稿路径为绝对路径，移动位置后应重新生成。
''')
    print(out)

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--job',required=True,type=Path); parser.add_argument('--out',required=True,type=Path)
    args=parser.parse_args(); export(args.job,args.out)
