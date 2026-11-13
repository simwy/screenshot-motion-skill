import React from 'react';
import {AbsoluteFill,useCurrentFrame} from 'remotion';
import {project} from './Content';
import {Copy,Paint,Screen,progress as p} from './MotionPrimitives';

export const Kinetic=()=>{
 const f=useCurrentFrame(),a=project.accent;
 const idx=f<60?-1:f>=360?4:Math.floor((f-60)/75);
 const local=idx<0?f:idx===4?f-360:f-60-idx*75;
 const enter=p(local,0,23),dark=idx===1||idx===3;
 const ink=dark?'#F7F3E9':'#171819',bg=dark?'#191A1C':'#F6F1E8';
 const page=project.pages[Math.min(3,Math.max(0,idx))];
 return <AbsoluteFill style={{background:bg,color:ink,fontFamily:'Arial,Helvetica,sans-serif',overflow:'hidden'}}>
 <Paint key={f}/>
 <Copy style={{position:'absolute',left:76,top:47,fontSize:26,fontWeight:800,letterSpacing:1,zIndex:60}}>{project.brand}<span style={{color:a}}>✳</span></Copy>
 <Copy style={{position:'absolute',right:76,top:53,fontSize:16,letterSpacing:2,zIndex:60}}>{project.tagline}</Copy>
 {idx===-1&&<>
  <div style={{position:'absolute',left:0,top:490,width:1920,height:620,background:a,transform:`translateY(${(1-p(f,5,30))*650}px)`}}/>
  <Copy style={{position:'absolute',left:95,top:160,right:95,fontSize:112,fontWeight:900,letterSpacing:-7,lineHeight:.94,zIndex:30,transform:`translateX(${(1-enter)*-700}px)`}}>{project.coverTitle.map((t,i)=><div key={i}>{t}</div>)}</Copy>
  {project.pages.map((page,i)=><Screen key={i} file={page.file} w={240} style={{left:245+i*294,top:548+(i%2)*55+(1-p(f,8+i*3,35+i*3))*520,transform:`rotate(${(i-2)*-5}deg)`}}/>)}
 </>}
 {idx>=0&&idx<4&&<>
  <div style={{position:'absolute',left:idx%2?0:1030,top:0,width:890,height:1080,background:a,transform:`translateX(${(1-enter)*(idx%2?-950:950)}px)`}}/>
  <Copy style={{position:'absolute',left:idx%2?900:90,top:113,fontSize:360,lineHeight:1,fontWeight:900,letterSpacing:-30,opacity:.075}}>{String(idx+1).padStart(2,'0')}</Copy>
  <div style={{position:'absolute',left:idx%2?190:1120,top:160,width:580,height:790,transform:`translateY(${(1-enter)*170}px) rotate(${(1-enter)*(idx%2?-12:12)}deg)`}}>
   <Screen file={project.pages[(idx+4)%5].file} w={290} style={{left:idx%2?-30:240,top:125,transform:`rotate(${idx%2?-14:14}deg)`,opacity:.65}}/>
   <Screen file={page.file} w={405} style={{left:45,top:5}}/>
  </div>
  <Copy style={{position:'absolute',left:idx%2?990:95,top:300,width:740}}>
   <div style={{display:'inline-block',background:ink,color:bg,padding:'10px 17px',fontSize:18,letterSpacing:2,fontWeight:700,marginBottom:34}}>{page.tag}</div>
   <div style={{fontSize:89,lineHeight:1.02,fontWeight:900,letterSpacing:-5}}>{page.title.map((t,i)=><div key={i} style={{overflow:'hidden'}}><div style={{transform:`translateY(${(1-p(local,3+i*3,23+i*3))*120}%)`}}>{t}</div></div>)}</div>
   <div style={{fontSize:26,lineHeight:1.4,opacity:.65,marginTop:33,maxWidth:650}}>{page.body.join(' ')}</div>
   <div style={{marginTop:40,width:130,height:8,background:a}}/>
  </Copy>
 </>}
 {idx===4&&<>
  <div style={{position:'absolute',left:-150,top:560,width:2200,height:650,background:a,transform:`rotate(-5deg) translateY(${(1-enter)*600}px)`}}/>
  <Copy style={{position:'absolute',left:120,top:150,width:1700,textAlign:'center',fontSize:90,lineHeight:1.05,fontWeight:900,letterSpacing:-5,opacity:enter}}>{project.closingTitle.join(' ')}<div style={{fontSize:27,letterSpacing:0,marginTop:30}}>{project.cta} ↗</div></Copy>
  {project.pages.map((page,i)=><Screen key={i} file={page.file} w={215} style={{left:310+i*270,top:546+Math.abs(i-2)*28+(1-p(local,5+i*2,32+i*2))*600,transform:`rotate(${(i-2)*5}deg)`}}/>)}
 </>}
 {/* Graphic edits traverse the frame rather than flashing the whole screen. */}
 {[60,135,210,285,360].map(c=>f>=c-6&&f<c+8?<div key={c} style={{position:'absolute',inset:0,zIndex:100,background:a,clipPath:`inset(0 ${Math.max(0,100-(f-c+6)*100/7)}% 0 ${Math.max(0,(f-c-1)*100/7)}%)`}}/>:null)}
 <div style={{position:'absolute',bottom:36,left:76,width:1768,height:3,background:dark?'#FFF2':'#0002'}}/><div style={{position:'absolute',bottom:36,left:76,width:1768*f/479,height:3,background:ink}}/>
 </AbsoluteFill>;
};
