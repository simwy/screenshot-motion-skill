import {project,isClean} from './Content';
import {Region} from './Region';
import React,{useEffect,useState} from 'react';
import {AbsoluteFill,Img,staticFile,useCurrentFrame,interpolate,Easing,delayRender,continueRender} from 'remotion';
const C={bg:'#090D14',panel:'#141C29',blue:project.accent,white:'#F4F7FC',muted:'#91A0B6'};
export const SHOTS=[{id:'hook',from:0,duration:90},{id:'plan',from:90,duration:105},{id:'create',from:195,duration:105},{id:'team',from:300,duration:105},{id:'progress',from:405,duration:75},{id:'end',from:480,duration:120}];
const e=Easing.bezier(.16,1,.3,1);
const p=(f:number,a:number,b:number)=>interpolate(f,[a,b],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:e});
const css:React.CSSProperties={position:'absolute'};
const Image=({name,style}:{name:string,style?:React.CSSProperties})=><Img src={staticFile('screenshots/'+name)} style={{display:'block',...style}}/>;
const Mark=({large=false}:{large?:boolean})=><div style={{display:'flex',gap:large?22:13,alignItems:'center'}}><div style={{width:large?58:32,height:large?58:32,background:C.blue,borderRadius:large?16:9,display:'flex',alignItems:'center',justifyContent:'center',fontSize:large?39:24,color:'white'}}>✓</div><span style={{fontSize:large?51:29,fontWeight:800,letterSpacing:'-.035em'}}>{project.brand}</span></div>;
const Kicker=({children,style={}}:{children:React.ReactNode,style?:React.CSSProperties})=><div style={{fontSize:24,letterSpacing:'.16em',fontWeight:700,color:C.blue,...style}}>{children}</div>;
const Head=({lines,f=100,size=128,style={}}:{lines:string[],f?:number,size?:number,style?:React.CSSProperties})=><div style={{fontSize:size,lineHeight:.98,fontWeight:800,letterSpacing:'-.065em',...style}}>{lines.map((line,i)=><div key={i} style={{overflow:'hidden',paddingBottom:10}}><div style={{transform:`translateY(${Math.round((1-p(f,i*5,i*5+24))*125)}%)`}}>{line}</div></div>)}</div>;
const Phone=({name,x,y,w,rotate=0,opacity=1}:{name:string,x:number,y:number,w:number,rotate?:number,opacity?:number})=><div style={{...css,left:x,top:y,width:w,height:w*16/9,padding:7,borderRadius:32,background:'#B9C3D1',boxShadow:'0 25px 80px #0008',transform:`rotate(${rotate}deg)`,opacity,overflow:'hidden'}}><Image name={name} style={{width:'100%',height:'100%',objectFit:'contain',borderRadius:25}}/></div>;
const Crop=({name,x,y,w,h,style={}}:{name:string,x:number,y:number,w:number,h:number,sx?:number,sy?:number,iw?:number,style?:React.CSSProperties})=><div style={{...css,left:x,top:y,width:w,height:h,overflow:'hidden',borderRadius:24,background:'#fff',...style}}><Region page={project.pages.find(p=>p.file===name)!}/></div>;
const Barrier=()=>{const [h]=useState(()=>delayRender('settle'));useEffect(()=>{const t=setTimeout(()=>continueRender(h),100);return()=>{clearTimeout(t);continueRender(h)}},[h]);return null;};
export const Launch=()=>{
const f=useCurrentFrame();const shot=SHOTS.find(s=>f>=s.from&&f<s.from+s.duration)!;const t=f-shot.from;
return <AbsoluteFill style={{background:C.bg,color:C.white,fontFamily:'Arial, Helvetica, sans-serif',overflow:'hidden'}}>
<Barrier key={f}/>
<AbsoluteFill style={{background:'radial-gradient(ellipse at 75% 80%, #16305470, transparent 65%)'}}/>
<div style={{...css,left:80,top:54,zIndex:50}}><Mark/></div>
<div style={{...css,right:80,top:62,color:'#9BA8BA',fontSize:21,letterSpacing:'.12em',zIndex:50}}>{project.tagline}</div>
{shot.id==='hook'&&<>
 <div style={{...css,left:910,top:-180,width:990,height:1450,transform:`translateY(${Math.round((1-p(t,0,55))*180)}px) rotate(-12deg)`,opacity:.48}}>
 {[0,1,2].map((n)=><div key={n} style={{...css,left:n*340,top:n%2?-190:40}}><Phone name={[project.pages[4].file,project.pages[0].file,project.pages[2].file][n]} x={0} y={0} w={300}/><Phone name={[project.pages[1].file,project.pages[3].file,project.pages[4].file][n]} x={0} y={580} w={300}/></div>)}
 </div>
 <AbsoluteFill style={{background:'linear-gradient(90deg,#090D14 28%,#090D14cc 42%,transparent 75%)'}}/>
 <div style={{...css,left:110,top:270,width:760}}><Kicker>{project.brand}</Kicker><Head lines={project.coverTitle} f={t} size={100} style={{marginTop:29}}/><div style={{fontSize:31,color:C.muted,marginTop:28,opacity:p(t,24,45)}}>{project.tagline}</div></div>
 <div style={{...css,left:110,top:850,width:Math.round(165*p(t,5,60)),height:5,background:C.blue}}/>
</>}
{shot.id==='plan'&&<>
 <div style={{...css,left:100,top:255,width:720}}><Kicker>{project.pages[0].tag}</Kicker><Head lines={project.pages[0].title} f={t} size={95} style={{marginTop:35}}/><div style={{fontSize:30,color:C.muted,lineHeight:1.5,marginTop:28}}>{project.pages[0].body.join(" ")}</div></div>
 <div style={{...css,left:890+Math.round(120*(1-p(t,0,30))),top:170,width:900,height:750,background:'#F8FAFE',borderRadius:34,overflow:'hidden'}}>
 <Region page={project.pages[0]}/>
 </div>
</>}
{shot.id==='create'&&<>
 <div style={{...css,left:220,top:160,width:680,height:800,transform:`translateX(${Math.round(-130*(1-p(t,0,28)))}px)`,opacity:p(t,0,14)}}>
 <Crop name={project.pages[1].file} x={0} y={0} w={662} h={774} sx={89} sy={362} iw={840} style={{borderRadius:34,boxShadow:'0 30px 100px #0007'}}/>
 </div>
 <div style={{...css,left:1050,top:230,width:760}}><Kicker>{project.pages[1].tag}</Kicker><Head lines={project.pages[1].title} f={t} size={88} style={{marginTop:34}}/><div style={{fontSize:30,color:C.muted,lineHeight:1.5,marginTop:35}}>{project.pages[1].body.join(" ")}</div>
 <div style={{display:'inline-block',marginTop:45,border:'1px solid #3E597E',borderRadius:50,padding:'17px 25px',fontSize:24,color:'#A9CCFF',opacity:p(t,32,55)}}>{project.pages[1].detail}</div></div>

</>}
{shot.id==='team'&&<>
 <div style={{...css,left:100,top:200,width:760}}><Kicker>{project.pages[2].tag}</Kicker><Head lines={project.pages[2].title} f={t} size={88} style={{marginTop:29}}/><div style={{fontSize:29,color:C.muted,marginTop:25}}>{project.pages[2].body.join(" ")}</div></div>
 <div style={{...css,left:100,top:650,width:720,height:220,background:'#142135',borderRadius:28,padding:37,opacity:p(t,35,55)}}>
 <div style={{fontSize:24,color:C.muted}}>{project.pages[2].key}</div><div style={{fontSize:32,marginTop:19,fontWeight:700}}>{project.pages[2].detail}</div>
 </div>
 <Crop name={project.pages[2].file} x={970+Math.round(150*(1-p(t,0,28)))} y={170} w={850} h={760} iw={850} sy={195} style={{borderRadius:32}}/>

</>}
{shot.id==='progress'&&<>
 <div style={{...css,left:100,top:207}}><Kicker>{project.pages[3].tag}</Kicker><Head lines={project.pages[3].title} f={t} size={88} style={{marginTop:30}}/></div>
 <div style={{...css,left:100,top:580,width:1720,height:300,transform:`translateY(${Math.round(85*(1-p(t,12,40)))}px)`,opacity:p(t,12,32),borderRadius:32,overflow:'hidden'}}><Region page={project.pages[3]}/></div>
 <div style={{...css,left:109,top:925,fontSize:25,color:C.muted,opacity:p(t,25,45)}}>{project.pages[3].detail}</div>
</>}
{shot.id==='end'&&<>
 <div style={{...css,left:1030,top:145,opacity:p(t,0,20)}}><Phone name={project.pages[4].file} x={300+Math.round(80*(1-p(t,0,35)))} y={65} w={325} rotate={8}/><Phone name={project.pages[0].file} x={30-Math.round(70*(1-p(t,0,35)))} y={20} w={390} rotate={-6}/></div>
 <div style={{...css,left:110,top:230,width:790}}><Head lines={project.closingTitle} f={t} size={95}/><div style={{fontSize:31,color:C.muted,lineHeight:1.6,marginTop:30}}>{project.tagline}</div>
 <div style={{marginTop:55,display:'inline-flex',alignItems:'center',gap:58,background:C.blue,borderRadius:18,padding:'24px 32px',fontSize:32,fontWeight:700,opacity:p(t,28,48),transform:`translateY(${Math.round(25*(1-p(t,28,48)))}px)`}}>{project.cta} <span>{isClean?'':'↗'}</span></div>
 </div>
 <div style={{...css,left:110,top:931,color:C.muted,fontSize:24,letterSpacing:'.05em',opacity:p(t,48,65)}}>{project.tagline}</div>
</>}
{/* Two directional edits; no flash frames or whole-frame shake. */}
{[90,300].map(c=>f>=c-9&&f<c+10?<div key={c} style={{...css,top:0,bottom:0,left:`${-110+p(f,c-9,c+10)*220}%`,width:'105%',background:C.blue,zIndex:100,transform:'skewX(-12deg)'}}/>:null)}
<div style={{...css,left:80,right:80,bottom:48,height:1,background:'#FFFFFF16'}}/>
<div style={{...css,left:80,bottom:48,height:2,width:1760*(f/599),background:C.blue}}/>
</AbsoluteFill>;
};
