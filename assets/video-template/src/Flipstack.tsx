import React,{useLayoutEffect,useRef} from 'react';
import {AbsoluteFill,useCurrentFrame,staticFile,delayRender,continueRender,cancelRender} from 'remotion';
import {project as p,isClean} from './Content';
// Shared-spine riffle with group camera push, followed by five page holds.
const W=760,H=500;
const clamp=(v:number)=>Math.max(0,Math.min(1,v));
const ease=(v:number)=>{v=clamp(v);return v*v*(3-2*v);};
const mix=(a:number,b:number,t:number)=>a+(b-a)*t;
let loaded:Promise<HTMLCanvasElement[]>|undefined;
function textures(){return loaded??=Promise.all(p.pages.map(page=>new Promise<HTMLImageElement>((resolve,reject)=>{
 const im=new Image();im.onload=()=>resolve(im);im.onerror=()=>reject(new Error(`Cannot load ${page.file}`));im.src=staticFile('screenshots/'+page.file);
}))).then(images=>images.map((im,index)=>{
 const c=document.createElement('canvas');c.width=W*2;c.height=H*2;
 const g=c.getContext('2d')!;g.scale(2,2);g.fillStyle='#f8faf6';g.fillRect(0,0,W,H);
 const portrait=im.width<im.height;
 const fit=Math.min((portrait?240:W-64)/im.width,(H-72)/im.height),w=im.width*fit,h=im.height*fit;
 g.fillStyle='#eef2eb';g.fillRect(24,24,portrait?272:W-48,H-48);
 g.drawImage(im,portrait?40+(240-w)/2:(W-w)/2,(H-h)/2,w,h);
 if(!isClean && portrait){const page=p.pages[index];
 g.fillStyle='#63715e';g.font='bold 12px Arial';g.fillText(page.tag,326,70,394);
 g.fillStyle='#16251a';g.font='bold 34px Arial';page.title.forEach((line,i)=>g.fillText(line,326,132+i*44,394));
 const by=164+page.title.length*44;
 g.fillStyle='#52604e';g.font='18px Arial';page.body.forEach((line,i)=>g.fillText(line,326,by+i*28,394));
 g.fillStyle='#c9d5c4';g.fillRect(326,412,394,1);
 g.fillStyle='#52604e';g.font='bold 13px Arial';g.fillText(p.brand.toUpperCase(),326,450);g.fillText(String(index+1).padStart(2,'0')+' / 05',657,450);
 }
 return c;
}));}
// Project a curved sheet as affine strips. Screen-space copy never rides a mesh.
function sheet(g:CanvasRenderingContext2D,tex:HTMLCanvasElement,x:number,y:number,scale:number,yaw:number,tilt:number,roll:number,alpha=1){
 if(alpha<=0)return;
 const point=(u:number,v:number)=>{
  const bend=95*Math.sin(Math.PI*u)*Math.sin(yaw);
  const xx=(u-1)*W*Math.cos(yaw),z=-(u-1)*W*Math.sin(yaw)+bend,yy=(v-1)*H;
  const cy=yy*Math.cos(tilt)-z*Math.sin(tilt),cz=yy*Math.sin(tilt)+z*Math.cos(tilt);
  const k=2800/(2800-cz);
  return {x:x+(xx*Math.cos(roll)-cy*Math.sin(roll))*k*scale,y:y+(xx*Math.sin(roll)+cy*Math.cos(roll))*k*scale};
 };
 const N=160,top=Array.from({length:N+1},(_,i)=>point(i/N,0)),bottom=Array.from({length:N+1},(_,i)=>point(i/N,1));
 const path=()=>{g.beginPath();g.moveTo(top[0].x,top[0].y);top.forEach(q=>g.lineTo(q.x,q.y));[...bottom].reverse().forEach(q=>g.lineTo(q.x,q.y));g.closePath();};
 g.save();g.globalAlpha=alpha;path();g.fillStyle='#f4f5f0';g.fill();
 if(Math.cos(yaw)>.01){
  if(Math.abs(yaw)+Math.abs(tilt)+Math.abs(roll)<.00001)g.drawImage(tex,x-W*scale,y-H*scale,W*scale,H*scale);
  else for(let i=0;i<N;i++){
   const a=top[i],b=top[i+1],d=bottom[i],sw=W/N;
   g.save();g.transform((b.x-a.x)/sw,(b.y-a.y)/sw,(d.x-a.x)/H,(d.y-a.y)/H,a.x,a.y);
   g.beginPath();g.rect(-.45,0,sw+.9,H);g.clip();g.drawImage(tex,-i*sw,0,W,H);g.restore();
  }
 }
 path();g.fillStyle=`rgba(18,28,24,${Math.abs(Math.sin(yaw))*.12})`;g.fill();g.strokeStyle='#ffffff90';g.lineWidth=1;g.stroke();g.restore();
}
function riffle(g:CanvasRenderingContext2D,tex:HTMLCanvasElement[],target:number,t:number){
 // One continuous curve: no stop/restart easing at intermediate waypoints.
 const u=ease(t/44),v=1-u;
 const intro=target===0;
 const x=intro?v*v*v*1120+3*v*v*u*300+3*v*u*u*900+u*u*u*1416:1416-140*Math.sin(Math.PI*u);
 const y=intro?mix(600,800,u):800-30*Math.sin(Math.PI*u);
 const scale=intro?mix(.34,1.2,u):1.2-.12*Math.sin(Math.PI*u);
 const tilt=intro?.95*(1-u):.32*Math.sin(Math.PI*u);
 const roll=intro?.46*(1-u)-.28*Math.sin(Math.PI*u):-.14*Math.sin(Math.PI*u);
 const finish=u;
 // Every leaf uses the exact same right edge/spine and camera transform.
 sheet(g,tex[target],x,y,scale,-.08*(1-finish),tilt,roll);
 for(let i=3;i>=0;i--){
  const turn=ease((t-i*5)/24),yaw=Math.PI*turn;
  const alpha=1-ease((t-(i*5+20))/10);
  sheet(g,tex[(target+4-i)%5],x,y,scale,yaw,tilt,roll,alpha);
 }
}
function text(g:CanvasRenderingContext2D,s:string,x:number,y:number,size:number,color='#f1f6ed',width=780,weight=600){
 if(isClean)return;g.font=`${weight} ${size}px Arial`;const m=g.measureText(s).width;if(m>width)g.font=`${weight} ${size*width/m}px Arial`;
 g.fillStyle=color;g.fillText(s,x,y);
}
function draw(g:CanvasRenderingContext2D,f:number,tex:HTMLCanvasElement[]){
 g.fillStyle='#050906';g.fillRect(0,0,1920,1080);
 const glow=g.createRadialGradient(1250,510,20,1250,510,950);glow.addColorStop(0,'#233823');glow.addColorStop(1,'#050906');g.fillStyle=glow;g.fillRect(0,0,1920,1080);
 // Both grid planes extend farther inward; white lines recede into depth.
 g.lineWidth=1.5;
 for(const ceiling of [true,false]){
  const horizon=ceiling?460:620,edge=ceiling?0:1080;
  g.save();g.beginPath();g.rect(0,ceiling?0:740,1920,ceiling?350:340);g.clip();
  g.strokeStyle='#ffffff42';
  for(let x=-3840;x<=5760;x+=140){g.beginPath();g.moveTo(960,horizon);g.lineTo(x,edge);g.stroke();}
  for(let j=0;j<24;j++){
   const z=60+((j*72+f*5.5)%1728+1728)%1728;
   const y=horizon+(ceiling?-1:1)*46000/z;
   g.beginPath();g.moveTo(0,y);g.lineTo(1920,y);g.stroke();
  }
  g.restore();
 }
 text(g,p.brand.toUpperCase(),80,72,30);text(g,p.tagline,1130,72,18,'#a4b19f',710,500);
 const closing=f>=510;
 const index=f<60?0:closing?4:Math.min(4,Math.floor((f-60)/90));
 const local=f<60?f:closing?f-510:f-(60+index*90);
 const motion=f<60?f:closing?44+local*.3:index===0?44+local*.3:local*1.6;
 riffle(g,tex,index,motion);
 g.save();g.globalAlpha=ease((motion-36)/8);
 const title=closing?p.closingTitle:f<60?p.coverTitle:p.pages[index].title;
 title.forEach((line,i)=>text(g,line,110,900+i*43,37,'#f1f6ed',1600));
 if(closing)text(g,p.cta,1350,990,24,p.accent,480);
 else if(f>=60)text(g,p.pages[index].tag,110,160,22,p.accent,1600);
 g.restore();
 g.fillStyle='#c8e9b41f';g.fillRect(80,1050,1760,2);g.fillStyle=p.accent;g.fillRect(80,1050,1760*f/599,2);
}
export const Flipstack=()=>{
 const f=useCurrentFrame(),ref=useRef<HTMLCanvasElement>(null);
 useLayoutEffect(()=>{const handle=delayRender('Paint floating page stack');let active=true;
 textures().then(tex=>{if(!active)return;draw(ref.current!.getContext('2d')!,f,tex);requestAnimationFrame(()=>continueRender(handle));}).catch(cancelRender);
 return()=>{active=false;continueRender(handle);};},[f]);
 return <AbsoluteFill><canvas ref={ref} width={1920} height={1080}/></AbsoluteFill>;
};
