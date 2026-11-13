import {project,isClean} from './Content';
import React, {useEffect, useState} from 'react';
import {AbsoluteFill, continueRender, delayRender, Easing, Img, interpolate, staticFile, useCurrentFrame} from 'remotion';

// Standalone, deterministic effect. All user content is supplied through props.
export type SpotlightProps = {
  brand: string;
  accent: string;
  opening: string;
  headline: string;
  closing: string;
  screenshots: string[];
};
export const defaults: SpotlightProps = {
 brand: project.brand, accent: project.accent,
 opening: project.coverTitle.join(' '), headline: project.pages[2].title.join('\n'),
 closing: project.closingTitle.join(' '), screenshots: project.pages.map(p=>p.file)
};
const ease = Easing.bezier(0.22, 1, 0.36, 1);
const smooth = Easing.bezier(0.65, 0, 0.35, 1);
const ramp = (f: number, a: number, b: number, easing = ease) => interpolate(f, [a, b], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing});
const mix = (a: number, b: number, t: number) => a + (b - a) * t;

// Chrome can report React ready before a transformed image layer has painted.
// Remount for each requested frame and hold capture until two paint opportunities
// plus a short compositor settle. This changes capture timing, not animation time.
const FramePaintBarrier: React.FC = () => {
  const [handle] = useState(() => delayRender('Wait for screenshot layers to paint'));
  useEffect(() => {
    let first = 0;
    let second = 0;
    let timer: ReturnType<typeof setTimeout> | undefined;
    first = requestAnimationFrame(() => {
      second = requestAnimationFrame(() => {
        timer = setTimeout(() => continueRender(handle), 80);
      });
    });
    return () => {
      cancelAnimationFrame(first);
      cancelAnimationFrame(second);
      clearTimeout(timer);
      continueRender(handle);
    };
  }, [handle]);
  return null;
};

export const ScreenshotSpotlight: React.FC<SpotlightProps> = (p) => {
  const f = useCurrentFrame();
  const focus = ramp(f, 130, 168, smooth) * (1 - ramp(f, 262, 300, smooth));
  const close = ramp(f, 278, 308);
  const openText = ramp(f, 3, 28) * (1 - ramp(f, 122, 145));
  const heroText = ramp(f, 151, 177) * (1 - ramp(f, 255, 275));
  const label = project.pages.map(p=>p.key);
  return <AbsoluteFill style={{background: '#F5F7FC', fontFamily: 'Arial, Helvetica, sans-serif', color: '#142139', overflow: 'hidden'}}>
    <FramePaintBarrier key={f} />
    <AbsoluteFill style={{background: `radial-gradient(ellipse at 68% 64%, ${p.accent}19, transparent 55%), linear-gradient(125deg, #fff, #F0F4FC)`}} />
    <div style={{position: 'absolute', width: 1200, height: 1200, border: '1px solid #087cff0b', borderRadius: '50%', left: 780, top: -110}} />
    <div style={{position: 'absolute', width: 1450, height: 1450, border: '1px solid #087cff0a', borderRadius: '50%', left: 655, top: -235}} />
    <div style={{position: 'absolute', left: 82, top: 58, display: 'flex', alignItems: 'center', gap: 16}}>
      <div style={{width: 38, height: 38, background: p.accent, borderRadius: 12, color: 'white', fontSize: 28, fontWeight: 700, textAlign: 'center', lineHeight: '38px'}}>✓</div>
      <span style={{fontSize: 29, fontWeight: 750, letterSpacing: '0.08em'}}>{p.brand}</span>
    </div>
    <div style={{position: 'absolute', right: 82, top: 66, fontSize: 21, letterSpacing: '0.14em', color: '#7c879c'}}>{project.tagline}</div>

    <div style={{position: 'absolute', top: 171, width: '100%', textAlign: 'center', opacity: openText, transform: `translateY(${(1-openText)*24}px)`}}>
      <div style={{fontSize: 76, fontWeight: 750, letterSpacing: '-0.06em'}}>{p.opening}</div>
      <div style={{marginTop: 17, fontSize: 29, color: '#6a778b'}}>{project.tagline}</div>
    </div>

    {/* The same five cards remain alive through the whole shot. No video crossfades. */}
    <AbsoluteFill style={{perspective: 2200, perspectiveOrigin: '50% 55%'}}>
      {p.screenshots.map((name, i) => {
        const order = [3,1,0,2,4][i];
        const deal = ramp(f, 30 + order*7 - order*order*0.45, 77 + order*7 - order*order*0.45);
        const intro = ramp(f, 0, 27);
        const endX = [310,635,960,1285,1610][i];
        const x = mix(960+(i-2)*17, endX, deal);
        const y = mix(650+(i-2)*9, 628 + Math.abs(i-2)*18, deal);
        const isHero = i===2;
        const targetX = isHero ? 1320 : endX + (i<2 ? -400 : 400);
        const targetY = isHero ? 563 : y+55;
        const w = mix(272, isHero?425:240, focus);
        const h = w*1920/1080;
        const rotation = mix((i-2)*5, (i-2)*3, deal)*(1-focus);
        const ry = mix(-16+(i-2)*4, -(i-2)*5, deal)*(1-focus) + (isHero ? -7*focus : 0);
        const opacity = intro*(isHero ? 1 : 1-focus);
        const lift = Math.sin(Math.PI*deal)*70;
        const shownX = mix(x,targetX,focus);
        const shownY = mix(y-lift,targetY,focus)+(1-intro)*160;
        // The screenshot, frame and outline are coplanar: flatten them BEFORE
        // rotating the card, instead of asking Chrome to composite nested 3D layers.
        return <div key={name} style={{position:'absolute', left:shownX-w/2, top:shownY-h/2, width:w, height:h, opacity, zIndex:isHero?20:10-Math.abs(i-2), transform:`rotateY(${ry}deg) rotateZ(${rotation}deg)`, transformStyle:'flat'}}>
          <div style={{position:'absolute', inset:-7, borderRadius:31, background:'linear-gradient(130deg,#fff,#d4ddeb)', boxShadow:`0 ${24+focus*16}px ${60+focus*20}px -22px #19335d42, 0 3px 8px #21345010`}} />
          <div style={{position:'absolute', inset:0, borderRadius:24, overflow:'hidden', background:'#fff'}}>
            <Img src={staticFile('screenshots/'+name)} style={{width:'100%',height:'100%',objectFit:'contain',display:'block'}} />
          </div>
          {isHero && focus>0 && <svg width={w+20} height={h+20} style={{position:'absolute',left:-10,top:-10,overflow:'visible',opacity:focus}}>
            <rect x={3} y={3} width={w+14} height={h+14} rx={32} fill="none" stroke={p.accent} strokeWidth={2} opacity={0.20}/>
            {f>=170 && f<224 && <rect x={3} y={3} width={w+14} height={h+14} rx={32} fill="none" stroke={p.accent} strokeWidth={3.5} pathLength={1} strokeDasharray="0.15 1" strokeDashoffset={-(f-170)/27} strokeLinecap="round"/>}
          </svg>}
        </div>;
      })}
    </AbsoluteFill>

    {/* Labels belong to the screen, not to the moving 3D card texture.
        Fixed integer positions avoid perspective/subpixel glyph rasterization.
        Show only once ALL cards have settled; fade out before the focus move. */}
    <AbsoluteFill style={{pointerEvents:'none'}}>
      {label.map((text, i) => {
        const visibility = ramp(f, 100, 112) * (1-ramp(f, 120, 130)) + ramp(f, 302, 314);
        return <div key={text} style={{
          position:'absolute', left:[310,635,960,1285,1610][i]-150,
          top:Math.round(628+Math.abs(i-2)*18+272*1920/1080/2+36),
          width:300, overflowWrap:'anywhere', textAlign:'center', fontSize:16, lineHeight:'21px',
          fontWeight:600, letterSpacing:'0.12em', color:'#6f7d93', opacity:visibility,
        }}>{text}</div>;
      })}
    </AbsoluteFill>

    <div style={{position:'absolute',left:143,top:317,width:800,opacity:heroText,transform:`translateY(${(1-heroText)*28}px)`}}>
      <div style={{fontSize:22,letterSpacing:'0.17em',fontWeight:700,color:p.accent,marginBottom:27}}>{project.pages[2].tag}</div>
      <div style={{fontSize:80,lineHeight:1.05,fontWeight:750,letterSpacing:'-0.06em',whiteSpace:'pre-line'}}>{p.headline}</div>
      <div style={{width:86,height:6,background:p.accent,borderRadius:4,margin:'37px 0 30px'}}/>
      <div style={{fontSize:32,lineHeight:1.6,color:'#69768c'}}>{project.pages[2].body.join(" ")}</div>
      <div style={{display:'flex',gap:12,marginTop:35}}>{project.pages.slice(0,3).map(p=>p.tag).map(t=><div key={t} style={{border:'1px solid #dce4ef',background:'#ffffff90',padding:'12px 20px',fontSize:20,borderRadius:50}}>{t}</div>)}</div>
    </div>

    <div style={{position:'absolute',top:179,width:'100%',textAlign:'center',opacity:close,transform:`translateY(${(1-close)*22}px)`}}>
      <div style={{fontSize:76,fontWeight:750,letterSpacing:'-0.06em'}}>{p.closing}</div>
      <div style={{fontSize:29,color:'#69768c',marginTop:17}}>{project.cta}</div>
    </div>
    <div style={{position:'absolute',bottom:40,left:82,right:82,height:1,background:'#dce3ef'}}/>
    <div style={{position:'absolute',bottom:56,left:82,fontSize:18,color:'#8b96a9',letterSpacing:'0.10em'}}>{isClean?'':project.brand+' / SCREENSHOT SPOTLIGHT'}</div>
    <div style={{position:'absolute',bottom:56,right:82,fontSize:18,color:'#8b96a9'}}>{isClean?'':'01 — SCREENSHOT SPOTLIGHT'}</div>
  </AbsoluteFill>;
};

export const Spotlight=()=> <ScreenshotSpotlight {...defaults}/>;
