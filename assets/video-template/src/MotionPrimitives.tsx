import React,{useEffect,useState} from 'react';
import {delayRender,continueRender,interpolate,Easing,Img,staticFile} from 'remotion';
import {isClean} from './Content';
export const progress=(f:number,a:number,b:number)=>interpolate(f,[a,b],[0,1],{extrapolateLeft:'clamp',extrapolateRight:'clamp',easing:Easing.bezier(.16,1,.3,1)});
export const blend=(a:number,b:number,p:number)=>a+(b-a)*p;
export const Copy=({children,style}:{children:React.ReactNode;style?:React.CSSProperties})=>isClean?null:<div style={style}>{children}</div>;
export const Paint=()=>{const [h]=useState(()=>delayRender('Paint motion layers'));useEffect(()=>{let a=0,b=0;let timer:ReturnType<typeof setTimeout>;a=requestAnimationFrame(()=>b=requestAnimationFrame(()=>{timer=setTimeout(()=>continueRender(h),90)}));return()=>{cancelAnimationFrame(a);cancelAnimationFrame(b);clearTimeout(timer);continueRender(h)}},[h]);return null;};
export const Screen=({file,w=320,style={}}:{file:string;w?:number;style?:React.CSSProperties})=><div style={{position:'absolute',width:w,height:w*16/9,borderRadius:24,padding:6,boxSizing:'border-box',background:'linear-gradient(140deg,#FFF,#7C8497)',boxShadow:'0 20px 65px #0004',...style}}><div style={{width:'100%',height:'100%',overflow:'hidden',borderRadius:19,background:'#FFF'}}><Img src={staticFile('screenshots/'+file)} style={{display:'block',width:'100%',height:'100%',objectFit:'contain'}}/></div></div>;
