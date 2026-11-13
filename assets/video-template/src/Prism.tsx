import React from 'react';
import {AbsoluteFill,useCurrentFrame} from 'remotion';
import {project} from './Content';
import {Copy,Paint,Screen,progress as p,blend} from './MotionPrimitives';

export const Prism=()=>{
 const f=useCurrentFrame(),a=project.accent;
 const scene=f<100?-1:f<370?Math.floor((f-100)/90):3;
 const t=scene<0?f:scene===3?f-370:f-100-scene*90;
 const opening=p(f,0,65),end=p(f,370,420);
 const page=project.pages[Math.min(3,Math.max(0,scene+1))];
 return <AbsoluteFill style={{background:'#161127',color:'#F9F3FF',fontFamily:'Arial,Helvetica,sans-serif',overflow:'hidden'}}>
 <Paint key={f}/>
 <AbsoluteFill style={{background:`radial-gradient(ellipse at 75% 55%,${a}45,transparent 65%),linear-gradient(135deg,#141120,#25153D 65%,#152B3F)`}}/>
 {[0,1,2,3].map(i=><div key={i} style={{position:'absolute',left:800+i*210+Math.sin(f/180)*35,top:-550,width:150,height:2000,background:`linear-gradient(90deg,transparent,${i%2?a:'#8CE9FF'}18,transparent)`,borderLeft:'1px solid #FFFFFF12',transform:'rotate(35deg)'}}/>)}
 <div style={{position:'absolute',left:0,right:0,top:927,height:1,background:'linear-gradient(90deg,transparent,#DCBBFF66,transparent)'}}/>
 <Copy style={{position:'absolute',left:80,top:54,fontSize:28,fontWeight:700,letterSpacing:2,zIndex:50}}><span style={{color:a,marginRight:17}}>◇</span>{project.brand}</Copy>
 <Copy style={{position:'absolute',right:80,top:61,fontSize:17,letterSpacing:2,color:'#B9ABC9',zIndex:50}}>{project.tagline}</Copy>
 {scene===-1&&<>
  <Copy style={{position:'absolute',left:100,top:235,width:620,opacity:p(f,8,35)}}><div style={{color:a,fontSize:19,letterSpacing:4,marginBottom:28}}>EVERY ANGLE. ONE STORY.</div><div style={{fontSize:88,fontWeight:700,lineHeight:1.04,letterSpacing:-5}}>{project.coverTitle.map((x,i)=><div key={i}>{x}</div>)}</div></Copy>
  <div style={{position:'absolute',inset:0,perspective:2200}}>{project.pages.map((page,i)=>{
   const unfold=p(f,10+i*6,45+i*6);
   return <Screen key={i} file={page.file} w={225} style={{left:blend(1250,790+i*190,unfold),top:305+Math.abs(i-2)*39,transformOrigin:'0% 50%',transform:`rotateY(${blend(86,i%2?-24:24,unfold)}deg) rotateZ(-6deg)`,opacity:unfold,boxShadow:`0 25px 75px #0008,0 0 0 1px ${a}70`}}/>;
  })}</div>
 </>}
 {scene>=0&&scene<3&&<>
  <Copy style={{position:'absolute',left:108,top:310,width:715,opacity:p(t,9,30),transform:`translateX(${(1-p(t,8,32))*-65}px)`}}>
   <div style={{fontSize:18,color:a,letterSpacing:4,marginBottom:30}}>{page.tag}</div>
   <div style={{fontSize:86,fontWeight:700,letterSpacing:-4,lineHeight:1.04}}>{page.title.map((x,i)=><div key={i}>{x}</div>)}</div>
   <div style={{fontSize:26,color:'#BDAFCF',marginTop:34,lineHeight:1.45,width:600}}>{page.body.join(' ')}</div>
   <div style={{fontSize:17,color:a,letterSpacing:3,marginTop:40}}>0{scene+1} / 03</div>
  </Copy>
  <div style={{position:'absolute',left:960,top:160,width:800,height:780,perspective:1900}}>
   {[2,1,0].map(layer=><div key={layer} style={{position:'absolute',inset:0,transformOrigin:'70% 50%',transform:`translateX(${layer*110+(1-p(t,layer*3,32+layer*3))*420}px) rotateY(${blend(-67,-13+layer*12,p(t,layer*3,32+layer*3))}deg) rotateZ(${layer*4-3}deg)`,opacity:1-layer*.27}}><Screen file={project.pages[(scene+1+layer)%5].file} w={355} style={{left:110,top:20+layer*35,boxShadow:`0 25px 80px #000A,0 0 0 1px ${a}80`}}/></div>)}
  </div>
  <div style={{position:'absolute',left:900,top:880,width:850,height:100,background:`radial-gradient(ellipse,${a}25,transparent 65%)`,transform:'skewX(-25deg)'}}/>
 </>}
 {scene===3&&<>
  <Copy style={{position:'absolute',left:200,right:200,top:177,textAlign:'center',opacity:end}}><div style={{color:a,fontSize:19,letterSpacing:5,marginBottom:20}}>{project.brand}</div><div style={{fontSize:78,lineHeight:1.05,fontWeight:700,letterSpacing:-4}}>{project.closingTitle.join(' ')}</div><div style={{fontSize:24,marginTop:26,color:'#DDC5FF'}}>{project.cta} ↗</div></Copy>
  <div style={{position:'absolute',inset:0,perspective:2300}}>{project.pages.map((page,i)=><Screen key={i} file={page.file} w={238} style={{left:310+i*267,top:510+(i%2)*38+(1-p(t,5+i*4,35+i*4))*480,transform:`rotateY(${blend(78,i%2?-18:18,p(t,5+i*4,35+i*4))}deg)`,transformOrigin:'0 50%',boxShadow:`0 25px 75px #0009,0 0 0 1px ${a}80`}}/>)}</div>
 </>}
 {[100,190,280,370].map(c=>f>=c-9&&f<c+12?<div key={c} style={{position:'absolute',top:-100,height:1400,left:-500+p(f,c-9,c+12)*2800,width:330,background:`linear-gradient(90deg,transparent,${a}A0,#FFF9,transparent)`,transform:'skewX(-25deg)',zIndex:100}}/>:null)}
 <div style={{position:'absolute',bottom:40,left:80,right:80,height:1,background:'#FFFFFF22'}}/><div style={{position:'absolute',bottom:40,left:80,height:2,width:1760*f/539,background:a}}/>
 </AbsoluteFill>;
};
