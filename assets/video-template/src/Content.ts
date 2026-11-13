import raw from '../project.json';
import {getInputProps} from 'remotion';

// Preserve line counts and geometry while removing promotional copy for an edit pack.
// Screenshot pixels are never changed. Render in a separate browser bundle per mode.
export const isClean = getInputProps().editorClean === true;
const blank = '\u00a0';
export const project = isClean ? {
  ...raw, brand: blank, tagline: blank, cta: blank,
  coverTitle: raw.coverTitle.map(()=>blank), closingTitle: raw.closingTitle.map(()=>blank),
  pages: raw.pages.map(p=>({...p, tag:blank, key:blank, detail:blank,
    title:p.title.map(()=>blank), body:p.body.map(()=>blank)})),
} : raw;
