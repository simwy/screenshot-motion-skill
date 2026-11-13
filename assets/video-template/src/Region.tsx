import React,{useState} from 'react';
import {Img,staticFile} from 'remotion';
type Page={file:string;region?:number[]};
export const Region=({page}:{page:Page})=>{
 const [size,setSize]=useState<[number,number]>([1080,1920]);
 const [x,y,w,h]=page.region??[0,0,1,1];const src=staticFile('screenshots/'+page.file);
 return <><Img src={src} style={{position:'absolute',opacity:0,width:1,height:1}} onLoad={e=>setSize([e.currentTarget.naturalWidth,e.currentTarget.naturalHeight])}/>
 <svg width="100%" height="100%" viewBox={`${x*size[0]} ${y*size[1]} ${w*size[0]} ${h*size[1]}`} preserveAspectRatio="xMidYMid meet"><image href={src} width={size[0]} height={size[1]}/></svg></>;
};
