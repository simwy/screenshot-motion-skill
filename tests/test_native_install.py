import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from install_editor_draft import install, media_relative
from install_editor_bundle import install_bundle


class NativeInstallTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name).resolve();self.source=self.root/'source';self.source.mkdir()
        (self.source/'media').mkdir();(self.source/'media/截图.png').write_bytes(b'example')
        self.data={'id':'old','duration':1000000,'fps':30,'canvas_config':{'width':1920,'height':1080},'tracks':[{'type':'text','segments':[]}], 'materials':{'videos':[{'id':'v','path':r'C:\old\media\截图.png'}],'audios':[],'texts':[{'content':'测试'}]}}
        self.write(self.source/'draft_content.json',self.data)
        self.write(self.source/'draft_meta_info.json',{'draft_id':'old','draft_name':'source'})

    def write(self,p,d):p.write_text(json.dumps(d,ensure_ascii=False),encoding='utf-8')
    def read(self,p):return json.loads(p.read_text(encoding='utf-8'))

    def test_cross_host_paths_and_unicode(self):
        for path in ('media/截图.png','/Users/test/project/media/截图.png',r'C:\old\media\截图.png'):
            self.assertEqual(media_relative(path,self.source),Path('截图.png'))
        out=self.root/'新草稿';install(self.source,None,out,'jianying')
        payload=self.read(out/'draft_content.json');meta=self.read(out/'draft_meta_info.json')
        self.assertEqual(payload['materials']['videos'][0]['path'],str(out/'media/截图.png'))
        self.assertEqual(meta['draft_id'],payload['id'])
        self.assertNotEqual(payload['id'],'old')
        self.assertEqual(payload['materials']['texts'][0]['content'],'测试')
        self.assertEqual(self.read(self.source/'draft_content.json'),self.data)

    def test_reject_traversal_missing_and_symlink(self):
        (self.root/'secret').write_text('secret');(self.source/'media/link').symlink_to(self.root/'secret')
        for path in ('media/../secret','media/C:/secret','media/missing','outside.png','media/link'):
            with self.subTest(path=path),self.assertRaises(ValueError):media_relative(path,self.source)

    def test_modern_timeline_ids_and_payload_match(self):
        template=self.root/'empty';template.mkdir();(template/'Timelines').mkdir()
        self.write(template/'draft_info.json',{'id':'template','duration':0,'tracks':[],'materials':{'videos':[],'audios':[]}})
        self.write(template/'draft_meta_info.json',{'draft_id':'template','draft_cloud_template_id':'private'})
        self.write(template/'Timelines/project.json',{'id':'project','main_timeline_id':'template','timelines':[{'id':'template'}]})
        before=(template/'draft_info.json').read_bytes()
        out=self.root/'capcut';install(self.source,template,out,'capcut')
        payload=self.read(out/'draft_info.json');index=self.read(out/'Timelines/project.json')
        self.assertEqual(payload['id'],index['main_timeline_id'])
        self.assertEqual(payload,self.read(out/'Timelines'/payload['id']/'draft_info.json'))
        self.assertEqual(before,(template/'draft_info.json').read_bytes())
        self.assertNotIn('draft_cloud_template_id',self.read(out/'draft_meta_info.json'))
        with self.assertRaises(FileExistsError):install(self.source,template,out,'capcut')

    def test_template_guards(self):
        with self.assertRaises(ValueError):install(self.source,None,self.root/'out','capcut')
        template=self.root/'empty';template.mkdir();(template/'draft_info.json').write_text('encrypted payload')
        with self.assertRaisesRegex(ValueError,'not readable JSON'):install(self.source,template,self.root/'out','capcut')
        self.write(template/'draft_info.json',self.data);self.write(template/'draft_meta_info.json',{})
        with self.assertRaisesRegex(ValueError,'empty'):install(self.source,template,self.root/'out','capcut')
        self.assertFalse((self.root/'out').exists())


if __name__=='__main__':unittest.main()
