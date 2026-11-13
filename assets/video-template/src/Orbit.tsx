import React, {useEffect,useState} from 'react';
import {AbsoluteFill,Img,staticFile,useCurrentFrame,interpolate,Easing,delayRender,continueRender} from 'remotion';
import {project,isClean} from './Content';

const ease=Easing.bezier(.16,1,.3,1);
const p=(f:number,a:number,b:number)=>interpolate(f,[a,b],[0,1],{easing:ease,extrapolateLeft:'clamp',extrapolateRight:'clamp'});
const lerp=(a:number,b:number,t:number)=>a+(b-a)*t;
const TAU=Math.PI*2;
const Barrier=()=>{const [h]=useState(()=>delayRender('Paint orbital cards'));useEffect(()=>{let a=0,b=0;let timer:ReturnType<typeof setTimeout>;a=requestAnimationFrame(()=>{b=requestAnimationFrame(()=>{timer=setTimeout(()=>continueRender(h),90);});});return()=>{cancelAnimationFrame(a);cancelAnimationFrame(b);clearTimeout(timer);continueRender(h);};},[h]);return null;};
const Copy=({children,style}:{children:React.ReactNode,style?:React.CSSProperties})=>isClean?null:<div style={style}>{children}</div>;

export const Orbit=()=>{
 const f=useCurrentFrame();
 const outro=p(f,420,465),intro=p(f,0,42);
 const scene=f<90?-1:Math.min(2,Math.floor((f-90)/110));
 const local=scene<0?f:f-(90+scene*110);
 // Each feature settles in front before the next orbital move.
 const angle=lerp(-.6,-TAU/5*p(f,90,124),p(f,45,90))-(p(f,200,234)+p(f,310,344))*TAU/5;
 const fade=scene<0?p(f,8,38):p(local,10,34);
 const page=project.pages[Math.max(0,scene)+1];
 const title=scene<0?project.coverTitle:page.title;
 const a=project.accent;
 return <AbsoluteFill style={{background:'#07090E',color:'#F5F8FF',fontFamily:'Arial, Helvetica, sans-serif',overflow:'hidden'}}>
 <Barrier key={f}/>
 <AbsoluteFill style={{background:`radial-gradient(ellipse at 70% 55%, ${a}25, transparent 53%), radial-gradient(ellipse at 20% 100%, #7152FF24, transparent 60%)`}}/>
 {/* Deterministic stars and a low horizon give the camera move depth. */}
 {Array.from({length:36},(_,i)=><div key={i} style={{position:'absolute',left:(i*193+71)%1920,top:(i*137+f*(.04+(i%4)*.02))%1080,width:i%4===0?3:2,height:i%4===0?3:2,borderRadius:'50%',background:i%3===0?a:'#9BA6B8',opacity:.18+(i%4)*.1}}/>)}
 <div style={{position:'absolute',left:-700,right:-700,top:740,height:1000,backgroundImage:`linear-gradient(${a}18 1px,transparent 1px),linear-gradient(90deg,${a}18 1px,transparent 1px)`,backgroundSize:'100px 100px',transform:'perspective(450px) rotateX(66deg)',transformOrigin:'50% 0',opacity:.5}}/>
 <svg width="1920" height="1080" style={{position:'absolute',opacity:1-outro*.6}}>
 {[0,1,2].map(i=><ellipse key={i} cx="1250" cy="630" rx={460+i*90} ry={185+i*42} fill="none" stroke={a} strokeWidth={i===0?2:1} opacity={.28-i*.07} transform={`rotate(${-24+i*12} 1250 630)`}/>)}
 <ellipse cx="1250" cy="935" rx="430" ry="37" fill={a} opacity=".08"/>
 </svg>
 <Copy style={{position:'absolute',left:80,top:53,fontSize:27,fontWeight:700,letterSpacing:2,zIndex:40}}><span style={{color:a,marginRight:15}}>✳</span>{project.brand}</Copy>
 <Copy style={{position:'absolute',right:80,top:60,fontSize:16,letterSpacing:3,color:'#A5B0C4',zIndex:40}}>{project.tagline}</Copy>
 <Copy style={{position:'absolute',left:94,top:166,fontSize:220,fontWeight:900,letterSpacing:-15,color:'transparent',WebkitTextStroke:'1px #FFFFFF12',opacity:(1-outro)*.65}}>IN MOTION</Copy>
 <div style={{position:'absolute',inset:0,perspective:2000}}>
 {project.pages.map((page,i)=>{
   const theta=angle+i*TAU/5;
   const depth=Math.cos(theta),z=(depth+1)/2;
   const w=lerp(185,365,z),h=w*16/9;
   const cx=1250+Math.sin(theta)*460,cy=550+Math.sin(theta)*50-(1-z)*130;
   const fw=228,fh=fw*16/9;
   const x=lerp(cx,410+i*275,outro),y=lerp(cy,758+Math.abs(i-2)*13,outro);
   const width=lerp(w,fw,outro),height=lerp(h,fh,outro);
   const tilt=lerp(-Math.sin(theta)*37,(i-2)*-4,outro);
   return <div key={page.file} style={{position:'absolute',left:x-width/2,top:y-height/2+(1-intro)*160,width,height,opacity:intro,zIndex:Math.round(z*20),transform:`rotateY(${tilt}deg) rotateZ(${lerp(-Math.sin(theta)*9,(i-2)*3,outro)}deg)`,transformStyle:'flat'}}>
    <div style={{position:'absolute',inset:-7,borderRadius:30,background:`linear-gradient(150deg,#A5AEC4,${a}80 45%,#151D29)`,boxShadow:`0 25px 65px #000A,0 0 ${45*z}px ${a}20`}}/>
    <div style={{position:'absolute',inset:0,borderRadius:24,overflow:'hidden',background:'#fff'}}><Img src={staticFile('screenshots/'+page.file)} style={{width:'100%',height:'100%',objectFit:'contain',display:'block'}}/><div style={{position:'absolute',inset:0,background:'#07090E',opacity:(1-z)*.72*(1-outro)}}/></div>
   </div>;
 })}
 </div>
 <Copy style={{position:'absolute',left:105,top:345,width:650,opacity:fade*(1-outro),zIndex:30,transform:`translateY(${Math.round((1-fade)*25)}px)`}}>
  <div style={{color:a,fontSize:18,letterSpacing:4,fontWeight:700,marginBottom:27}}>{scene<0?'A NEW PERSPECTIVE':page.tag}</div>
  <div style={{fontSize:88,fontWeight:800,lineHeight:1.01,letterSpacing:-5}}>{title.map((line,i)=><div key={i}>{line}</div>)}</div>
  <div style={{marginTop:32,fontSize:25,lineHeight:1.45,color:'#A5B0C4',maxWidth:555}}>{scene<0?project.tagline:page.body.join(' ')}</div>
  <div style={{display:'flex',gap:8,marginTop:38}}>{[0,1,2].map(i=><div key={i} style={{height:3,width:i===scene?70:24,background:i===scene?a:'#344052'}}/>)}</div>
 </Copy>
 <Copy style={{position:'absolute',top:172,left:220,right:220,textAlign:'center',opacity:outro,zIndex:30,transform:`translateY(${Math.round((1-outro)*35)}px)`}}>
  <div style={{color:a,fontSize:18,letterSpacing:5,marginBottom:19}}>{project.brand}</div>
  <div style={{fontSize:78,fontWeight:800,letterSpacing:-4,lineHeight:1.04}}>{project.closingTitle.join(' ')}</div>
  <div style={{display:'inline-block',marginTop:26,padding:'15px 27px',background:a,borderRadius:40,color:'#080B0E',fontSize:22,fontWeight:700}}>{project.cta} ↗</div>
 </Copy>
 <div style={{position:'absolute',left:80,right:80,bottom:49,height:1,background:'#FFFFFF20'}}/><div style={{position:'absolute',left:80,bottom:49,height:2,width:1760*f/539,background:a}}/>
 </AbsoluteFill>;
};
