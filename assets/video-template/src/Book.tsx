import {project,isClean} from './Content';
import React,{useLayoutEffect,useRef} from 'react';
import {AbsoluteFill,continueRender,delayRender,staticFile,useCurrentFrame} from 'remotion';
const W=640,H=760,X=960,Y=160;
const INK='#172B46',BLUE=project.accent,PAPER='#FAF8F2';
export const chapters=project.pages;
export const OPEN_END=90;
export const HOLD=project.holdFrames;
export const TURN=42;
export const TURNS=chapters.slice(1).map((_,i)=>OPEN_END+HOLD+i*(TURN+HOLD));
export const CLOSE_START=OPEN_END+chapters.length*HOLD+(chapters.length-1)*TURN;
export const DURATION=CLOSE_START+102;
const ease=(t:number)=>t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2;
const clamp=(x:number)=>Math.max(0,Math.min(1,x));
const smooth=(f:number,a:number,b:number)=>ease(clamp((f-a)/(b-a)));
const round=(ctx:CanvasRenderingContext2D,x:number,y:number,w:number,h:number,r:number,fill:string)=>{ctx.fillStyle=fill;ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fill();};
const font=(ctx:CanvasRenderingContext2D,s:number,weight=400)=>{ctx.font=`${weight} ${s}px Arial, Helvetica, sans-serif`;};
const text=(ctx:CanvasRenderingContext2D,str:string,x:number,y:number,s:number,color=INK,weight=400)=>{if(isClean)return;font(ctx,s,weight); if(s>=24 && ctx.measureText(str).width>W-116){font(ctx,Math.max(14,s*(W-116)/ctx.measureText(str).width),weight);}ctx.fillStyle=color;ctx.fillText(str,x,y);};
const canvas=()=>{const c=document.createElement('canvas');c.width=W*2;c.height=H*2;const ctx=c.getContext('2d')!;ctx.scale(2,2);return {c,ctx};};
const grain=(ctx:CanvasRenderingContext2D,dark=false)=>{ctx.fillStyle=dark?'#FFFFFF09':'#5D513307';for(let i=0;i<2400;i++){const x=(i*137.31)%W,y=(i*79.71)%H;ctx.fillRect(x,y,.6,.6);}};
const ruled=(ctx:CanvasRenderingContext2D,n:number,side:string)=>{ctx.strokeStyle='#D8D6CC';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(46,697);ctx.lineTo(W-46,697);ctx.stroke();text(ctx,project.brand.toUpperCase()+' / PRODUCT BOOK',46,726,13,'#7E867F',600);text(ctx,String(n).padStart(2,'0'),W-73,726,15,'#7E867F',600);};
let texturePromise:Promise<{left:HTMLCanvasElement[],right:HTMLCanvasElement[],cover:HTMLCanvasElement,closing:HTMLCanvasElement}>|null=null;
function textures(){if(texturePromise)return texturePromise;
 texturePromise=Promise.all(chapters.map(ch=>new Promise<HTMLImageElement>((res,rej)=>{const i=new window.Image();i.onload=()=>res(i);i.onerror=rej;i.src=staticFile(`screenshots/${ch.file}`);}))).then(images=>{
 const left:HTMLCanvasElement[]=[],right:HTMLCanvasElement[]=[];
 chapters.forEach((ch,i)=>{
 let {c,ctx}=canvas();ctx.fillStyle=PAPER;ctx.fillRect(0,0,W,H);grain(ctx);text(ctx,`CHAPTER ${String(i+1).padStart(2,'0')}`,58,69,17,BLUE,700);text(ctx,ch.tag,58,105,13,'#7D8B98',600);
 let y=200;ch.title.forEach(line=>{text(ctx,line,56,y,64,INK,700);y+=69;});
 ctx.fillStyle=BLUE;ctx.fillRect(58,y+4,54,4);y+=63;
 ch.body.forEach(line=>{text(ctx,line,58,y,24,'#596A7B');y+=36;});
 text(ctx,ch.detail,58,641,24,INK,600);ruled(ctx,i*2+1,'left');left.push(c);
 ({c,ctx}=canvas());ctx.fillStyle=PAPER;ctx.fillRect(0,0,W,H);grain(ctx);text(ctx,ch.key,48,54,16,BLUE,700);
 // Preserve every screenshot pixel: fitted full-height, never crop app controls.
 const fit=Math.min(544/images[i].naturalWidth,586/images[i].naturalHeight); const iw=images[i].naturalWidth*fit,ih=images[i].naturalHeight*fit,ix=(W-iw)/2,iy=86+(586-ih)/2;
 ctx.save();ctx.shadowColor='#182B4035';ctx.shadowBlur=20;ctx.shadowOffsetY=9;round(ctx,ix-5,iy-5,iw+10,ih+10,15,'#E3E7EC');ctx.restore();
 ctx.save();ctx.beginPath();ctx.roundRect(ix,iy,iw,ih,11);ctx.clip();ctx.drawImage(images[i],ix,iy,iw,ih);ctx.restore();ruled(ctx,i*2+2,'right');right.push(c);
 });
 const cover=(close:boolean)=>{const {c,ctx}=canvas();ctx.fillStyle=project.accent;ctx.fillRect(0,0,W,H);grain(ctx,true);
 const grad=ctx.createLinearGradient(0,0,W,0);grad.addColorStop(0,'#0007');grad.addColorStop(.035,'#0002');grad.addColorStop(.055,'#FFFFFF12');grad.addColorStop(.08,'#0000');grad.addColorStop(1,'#071A3319');ctx.fillStyle=grad;ctx.fillRect(0,0,W,H);
 ctx.strokeStyle='#FFFFFF33';ctx.lineWidth=1;ctx.strokeRect(34,34,W-68,H-68);
 text(ctx,project.brand.toUpperCase(),69,110,31,'#FFF',700);text(ctx,'THE PRODUCT BOOK',70,149,14,'#B5CEF0',600);
 const lines=close?project.closingTitle:project.coverTitle;lines.forEach((l,i)=>text(ctx,l,66,295+i*83,73,'#FFF',700));
 text(ctx,close?project.cta:project.tagline,70,632,close?27:17,'#DAE9FF',600);text(ctx,project.tagline,70,685,12,'#A6C4EB',500);return c;};
 return {left,right,cover:cover(false),closing:cover(true)};
 });return texturePromise;
}
type Pt={x:number,y:number};
function leaf(ctx:CanvasRenderingContext2D,front:HTMLCanvasElement,back:HTMLCanvasElement,p:number,rigid=false){
 if(p<0.00001){ctx.drawImage(front,X,Y,W,H);return;}if(p>0.99999){ctx.drawImage(back,X-W,Y,W,H);return;}
 const theta=p*Math.PI,face=p<.5?front:back,N=160;
 const point=(u:number,v:number)=>{const curl=(rigid?0:42)*Math.sin(Math.PI*p)*Math.sin(Math.PI*u);const xx=Math.cos(theta)*u*W+curl;const z=Math.sin(theta)*u*W+curl*.6;const k=3000/(3000-z);return{x:X+xx*k,y:Y+H/2+(v-.5)*H*k-12*Math.sin(Math.PI*p)*u};};
 const top:Pt[]=[],bottom:Pt[]=[];for(let i=0;i<=N;i++){top.push(point(i/N,0));bottom.push(point(i/N,1));}
 ctx.save();ctx.beginPath();ctx.moveTo(top[0].x,top[0].y);top.forEach(q=>ctx.lineTo(q.x,q.y));[...bottom].reverse().forEach(q=>ctx.lineTo(q.x,q.y));ctx.closePath();ctx.shadowColor='#15223855';ctx.shadowBlur=25*Math.sin(Math.PI*p)+2;ctx.shadowOffsetX=-24*Math.sin(Math.PI*p);ctx.shadowOffsetY=18*Math.sin(Math.PI*p);ctx.fillStyle=rigid?project.accent:PAPER;ctx.fill();ctx.restore();
 for(let i=0;i<N;i++){
 const su0=(p<.5?i/N:1-i/N)*face.width,su1=(p<.5?(i+1)/N:1-(i+1)/N)*face.width;
 const a=top[i],b=top[i+1],c=bottom[i+1],d=bottom[i];
 const dx=Math.min(a.x,b.x),dy=(a.y+b.y)/2,dw=Math.abs(b.x-a.x),dh=(c.y+d.y)/2-dy;
 // Slight strip overlap closes subpixel antialias seams across printed letters.
 ctx.drawImage(face,Math.min(su0,su1),0,Math.abs(su1-su0),face.height,dx-.4,dy,dw+.8,dh);

 }
 // One continuous lighting overlay avoids seams between adjacent mesh strips.
 ctx.beginPath();ctx.moveTo(top[0].x,top[0].y);top.forEach(q=>ctx.lineTo(q.x,q.y));[...bottom].reverse().forEach(q=>ctx.lineTo(q.x,q.y));ctx.closePath();
 ctx.fillStyle=`rgba(21,32,49,${Math.sin(Math.PI*p)*.11})`;ctx.fill();
}
function base(ctx:CanvasRenderingContext2D,spread:boolean){
 const left=spread?X-W:X,width=spread?W*2:W;
 ctx.save();ctx.shadowColor='#1D24394D';ctx.shadowBlur=48;ctx.shadowOffsetY=28;round(ctx,left-12,Y-10,width+24,H+31,7,project.accent);ctx.restore();
 for(let j=13;j>=0;j--){ctx.fillStyle=j%3===0?'#C2C4BE':'#E4E1D8';ctx.fillRect(left-1,Y+j,width+2,H+3);}
}
function draw(ctx:CanvasRenderingContext2D,f:number,tex:Awaited<ReturnType<typeof textures>>){
 ctx.clearRect(0,0,1920,1080);let bg=ctx.createLinearGradient(0,0,1700,1080);bg.addColorStop(0,'#F3F2EF');bg.addColorStop(1,'#CFD8E0');ctx.fillStyle=bg;ctx.fillRect(0,0,1920,1080);
 text(ctx,project.brand.toUpperCase(),82,70,25,INK,700);text(ctx,'A BETTER WAY TO WORK — ONE PAGE AT A TIME',82,101,13,'#687785',500);
 const close=smooth(f,CLOSE_START,CLOSE_START+42),open=smooth(f,45,90),shift=-W/2*(1-open+close);
 ctx.save();ctx.translate(shift,0);
 if(f<90){base(ctx,false);ctx.drawImage(tex.right[0],X,Y,W,H);leaf(ctx,tex.cover,tex.left[0],open,true);}
 else if(f>=CLOSE_START){base(ctx,false);ctx.drawImage(tex.right[chapters.length-1],X,Y,W,H);leaf(ctx,tex.closing,tex.left[chapters.length-1],1-close,true);}
 else{
 let index=0,turn=-1;TURNS.forEach((start,i)=>{if(f>=start+42)index=i+1;else if(f>=start)turn=i;});
 base(ctx,true);
 if(turn>=0){ctx.drawImage(tex.left[turn],X-W,Y,W,H);ctx.drawImage(tex.right[turn+1],X,Y,W,H);leaf(ctx,tex.right[turn],tex.left[turn+1],smooth(f,TURNS[turn],TURNS[turn]+42));}
 else{ctx.drawImage(tex.left[index],X-W,Y,W,H);ctx.drawImage(tex.right[index],X,Y,W,H);}
 const g=ctx.createLinearGradient(X-35,0,X+38,0);g.addColorStop(0,'#17233100');g.addColorStop(.40,'#1723310B');g.addColorStop(.5,'#17233130');g.addColorStop(.6,'#17233112');g.addColorStop(1,'#17233100');ctx.fillStyle=g;ctx.fillRect(X-35,Y,73,H);
 }
 ctx.restore();
 if(f>=90&&f<CLOSE_START){let idx=0;TURNS.forEach((st,i)=>{if(f>=st+42)idx=i+1;});text(ctx,`${String(idx+1).padStart(2,'0')} / ${String(chapters.length).padStart(2,'0')}`,1740,1006,18,'#596A7B',600);text(ctx,project.tagline,82,1006,16,'#596A7B',500);}
 else{text(ctx,f<90?'OPEN A NEW CHAPTER.':'MAKE YOUR NEXT CHAPTER A PRODUCTIVE ONE.',82,1006,17,'#596A7B',500);}
}
export const Book=()=>{const f=useCurrentFrame(),ref=useRef<HTMLCanvasElement>(null);
 useLayoutEffect(()=>{const h=delayRender('Paint book mesh'),controller={cancel:false};textures().then(tex=>{if(controller.cancel)return;draw(ref.current!.getContext('2d')!,f,tex);requestAnimationFrame(()=>continueRender(h));}).catch(err=>{continueRender(h);throw err;});return()=>{controller.cancel=true;continueRender(h);};},[f]);
 return <AbsoluteFill><canvas ref={ref} width={1920} height={1080}/></AbsoluteFill>;
};
