"""Timeline and export safety checks; run with unittest discovery."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from editor_pack import scenes, captions, timestamp, export_pack
from motion import duration, job_fingerprint, registry


def project(name, count=5, hold=120):
    d=json.loads((ROOT/'examples'/(name+'.json')).read_text())
    d['holdFrames']=hold
    d['pages']=[copy.deepcopy(d['pages'][i%len(d['pages'])]) for i in range(count)]
    d['templateSpec']=registry()[name]
    return d


class EditingTests(unittest.TestCase):
    def test_fixed_shots_cover_every_frame_without_overlap(self):
        for name,total in [('spotlight',360),('launch',600),('orbit',540),('kinetic',480),('prism',540)]:
            d=project(name); cuts=scenes(d)
            self.assertEqual(cuts[0][0],0)
            self.assertEqual(cuts[-1][1],total)
            for previous,current in zip(cuts,cuts[1:]):self.assertEqual(previous[1],current[0])
            self.assertTrue(all(end>start for start,end,*_ in cuts))
            for c in captions(d):self.assertTrue(0<=c['startFrame']<c['endFrame']<=total)

    def test_books_cover_single_and_many_pages_at_all_supported_holds(self):
        for count in [1,2,5,12]:
            for hold in [90,120,360]:
                d=project('storybook',count,hold); cuts=scenes(d); total=duration(d)[1]
                self.assertEqual(sum(b-a for a,b,*_ in cuts),total)
                self.assertEqual(cuts[0][0],0);self.assertEqual(cuts[-1][1],total)
                for previous,current in zip(cuts,cuts[1:]):self.assertEqual(previous[1],current[0])
                caps=captions(d)
                for i,c in enumerate(caps[1:-1]):
                    self.assertEqual(c['endFrame']-c['startFrame'],hold)
                    self.assertEqual(c['startFrame'],90+i*(hold+42))

    def test_caption_sources_match_visible_orbit_heroes(self):
        d=project('orbit')
        for i,p in enumerate(d['pages']):p['title']=[f'Page {i}']
        self.assertEqual([c['title'] for c in captions(d)[1:-1]],['Page 1','Page 2','Page 3'])

    def test_srt_rounding_and_hour_rollover(self):
        self.assertEqual(timestamp(1),'00:00:00,033')
        self.assertEqual(timestamp(539),'00:00:17,967')
        self.assertEqual(timestamp(108000),'01:00:00,000')

    def test_source_fingerprint_detects_copy_code_and_media_changes(self):
        with tempfile.TemporaryDirectory() as folder:
            job=Path(folder);(job/'src').mkdir();(job/'public/screenshots').mkdir(parents=True)
            paths=[job/'project.json',job/'src/Scene.tsx',job/'public/screenshots/page.png']
            for path in paths:path.write_bytes(b'original')
            old=job_fingerprint(job)
            for path in paths:
                path.write_bytes(b'changed');self.assertNotEqual(old,job_fingerprint(job));path.write_bytes(b'original')

    def test_export_never_overwrites_existing_folder(self):
        with tempfile.TemporaryDirectory() as folder:
            out=Path(folder)/'keep';out.mkdir();(out/'user.txt').write_text('preserve')
            with self.assertRaisesRegex(ValueError,'overwrite'):export_pack(Path(folder)/'missing-job',out)
            self.assertEqual((out/'user.txt').read_text(),'preserve')

    def test_unknown_effect_requires_explicit_editor_mapping(self):
        d=project('orbit');d['template']='future-effect'
        with self.assertRaisesRegex(ValueError,'mapping'):scenes(d)


if __name__=='__main__':unittest.main()
