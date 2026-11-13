import React from 'react';
import {Composition,registerRoot} from 'remotion';
import {Book,DURATION} from './Book';
registerRoot(()=> <Composition id="ScreenshotBook" component={Book} width={1920} height={1080} fps={30} durationInFrames={DURATION}/>);
