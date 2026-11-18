import React from 'react';
import {AbsoluteFill,Img,staticFile,useCurrentFrame,interpolate,spring} from 'remotion';
import {project, isClean} from './Content';
const files=project.pages.map(p=>p.file);
const labels=project.pages.map(p=>p.key);
const clamp={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const};
export function Entrance(){
 const f=useCurrentFrame();
 const fan=spring({frame:f-90,fps:30,config:{damping:19,stiffness:80}});
 const intro=interpolate(f,[4,17,78,94],[0,1,1,0],clamp);
 const active=Math.min(4,Math.max(0,Math.floor((f-7)/13)));
 const title=interpolate(f,[133,151],[0,1],clamp);
 return <AbsoluteFill style={{background:'radial-gradient(ellipse at 50% 20%, #ffffff 0%, #f0f3f7 48%, #dce3ec 100%)',fontFamily:'Arial, "PingFang SC", sans-serif',overflow:'hidden'}}>
 <div style={{position:'absolute',top:64,left:90,fontSize:19,color:'#76808b',letterSpacing:3}}>{project.brand}</div>
 <div style={{position:'absolute',top:64,right:90,fontSize:18,color:'#76808b',letterSpacing:3}}>{project.tagline}</div>
 <div style={{position:'absolute',left:380,top:850,width:1160,height:65,borderRadius:'50%',background:'#70839b',filter:'blur(45px)',opacity:.20*fan}}/>
 <div style={{position:'absolute',top:130,width:'100%',textAlign:'center',opacity:title,transform:`translateY(${(1-title)*35}px)`}}><div style={{fontSize:Math.min(72,1420/(project.closingTitle.join(' ').length*.9)),fontWeight:750,letterSpacing:-3,color:'#111923'}}>{project.closingTitle.join(' ')}</div><div style={{fontSize:25,marginTop:22,color:'#737e8c'}}>{project.cta}</div></div>
 <div style={{position:'absolute',left:170,top:350,width:410,opacity:intro,transform:`translateX(${(1-intro)*-25}px)`}}>
 <div style={{fontSize:14,color:'#6984aa',letterSpacing:4,marginBottom:25}}>{project.pages[0].tag}</div>
 <div style={{fontSize:Math.min(56,400/Math.max(...project.coverTitle.map(t=>t.length))),fontWeight:750,lineHeight:1.3,color:'#17202c'}}>{project.coverTitle.map((line,i)=><React.Fragment key={i}>{i>0&&<br/>}{line}</React.Fragment>)}</div>
 <div style={{fontSize:Math.min(25,400/Math.max(...project.pages[0].body.map(t=>t.length))),lineHeight:1.9,color:'#788492',marginTop:28}}>{project.pages[0].body.map((line,i)=><React.Fragment key={i}>{i>0&&<br/>}{line}</React.Fragment>)}</div>
 <div style={{width:64,height:4,background:project.accent,marginTop:32,borderRadius:2}}/>
 </div>
 <div style={{position:'absolute',right:155,top:320,width:410,opacity:intro,transform:`translateX(${(1-intro)*25}px)`}}>
 <div style={{fontSize:14,color:'#6984aa',letterSpacing:4,marginBottom:25}}>{project.pages[1].tag}</div>
 {project.pages.map(p=>p.detail).map((line,i)=><div key={i} style={{display:'flex',gap:19,alignItems:'center',padding:'15px 0',borderBottom:'1px solid #dde3ec',opacity:i<=active?1:.42}}><span style={{fontSize:17,color:i===active?project.accent:'#96a3b4',fontWeight:600}}>{!isClean&&`0${i+1}`}</span><div><div style={{fontSize:Math.min(24,360/labels[i].length),fontWeight:650,color:'#263445'}}>{labels[i]}</div><div style={{fontSize:Math.min(18,360/line.length),color:'#7c8897',marginTop:7}}>{line}</div></div></div>)}
 </div>
 {files.map((src,i)=>{
 const enter=spring({frame:f-(7+i*13),fps:30,config:{damping:17,stiffness:170}});
 const d=i-2;const x=d*(35*(1-fan)+245*fan)+(1-enter)*d*30*(1-fan);
 const lifted=i===2?interpolate(f,[132,151],[0,65],clamp):0;
 const y=(1-enter)*540 + (1-fan)*Math.abs(d)*9 + fan*(78+Math.abs(d)*27)-lifted;
 const angle=d*(4*(1-fan)+10*fan)+(1-enter)*d*3*(1-fan);
 return <div key={src} style={{position:'absolute',left:960-150,top:310,width:300,height:460,opacity:interpolate(f,[7+i*13,10+i*13],[0,1],clamp),transform:`translate(${x}px,${y}px) rotate(${angle}deg) scale(${.91+.09*enter})`,transformOrigin:'50% 95%',zIndex:fan>.7?(i===2?20:10-Math.abs(d)):i,background:'#fff',border:'3px solid #fff',borderRadius:18,boxShadow:'0 14px 25px #54637d20, 0 2px 5px #54637d12',overflow:'hidden'}}>
 <div style={{height:365,background:'#f5f7fb',margin:8,borderRadius:10,overflow:'hidden'}}><Img src={staticFile('screenshots/'+src)} style={{width:'100%',height:'100%',objectFit:'contain'}}/></div>
 <div style={{padding:'10px 16px',fontSize:Math.min(23,260/labels[i].length),fontWeight:700,color:'#17202c'}}>{labels[i]}</div><div style={{padding:'0 16px',fontSize:12,color:'#95a0ac',letterSpacing:2}}>{!isClean&&`${project.brand} / 0${i+1}`}</div>
 </div>})}
 </AbsoluteFill>
}
