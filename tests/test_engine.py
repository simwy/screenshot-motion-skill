"""Agent-free entry point, template preparation and portable draft contract."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import engine
import generate


class EngineTests(unittest.TestCase):
    def config(self, root, name):
        d = json.loads((engine.ROOT / 'examples' / (name + '.json')).read_text())
        image = root / 'screen.png'
        image.write_bytes(b'fixture')
        for page in d['pages']:
            page['image'] = image.name
        config = root / (name + '.json')
        config.write_text(json.dumps(d))
        return config

    def test_all_eight_prepare_without_agent_and_without_audio(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.assertEqual(len(engine.registry()), 8)
            for name in engine.registry():
                config = self.config(root, name)
                original = config.read_bytes()
                job = engine.prepare(config, root / name, name)
                payload = json.loads((job / 'project.json').read_text())
                self.assertEqual(payload['template'], name)
                self.assertGreater(engine.duration(payload)[1], 0)
                self.assertTrue((job / 'package-lock.json').is_file())
                self.assertFalse((job / 'audio-manifest.json').exists())
                self.assertEqual(config.read_bytes(), original)
                self.assertNotIn(str(root), (job / 'project.json').read_text())
                with self.assertRaises(ValueError):
                    engine.prepare(config, job, name)

    def test_invalid_config_does_not_create_job(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            config = self.config(root, 'entrance')
            d = json.loads(config.read_text()); d['pages'].pop()
            config.write_text(json.dumps(d))
            with self.assertRaises(ValueError):
                engine.prepare(config, root / 'job')
            self.assertFalse((root / 'job').exists())

    def test_entrance_native_rejected_before_any_work(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            with self.assertRaisesRegex(ValueError, 'no native draft'):
                generate.generate(self.config(root, 'entrance'), root / 'out', draft=True)
            self.assertFalse((root / 'out').exists())

    def test_portable_zip_rebases_media_and_preserves_source(self):
        def native_export(job, out):
            (out / 'media').mkdir(parents=True)
            (out / 'media/screen.png').write_bytes(b'image')
            (out / 'draft_content.json').write_text(json.dumps({'materials': {'videos': [{'path': str(out / 'media/screen.png')}]}}))
            (out / 'draft_meta_info.json').write_text(json.dumps({'draft_fold_path': str(out)}))
        from types import SimpleNamespace
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            with patch.dict(sys.modules, {'motion_native': SimpleNamespace(export=native_export)}), patch.object(generate, 'run'), patch.object(generate, 'render'), patch.object(generate, 'finalize', return_value=root / 'video.mp4'):
                result = generate.generate(self.config(root, 'orbit'), root / 'out', draft=True)
            with zipfile.ZipFile(result['draftZip']) as archive:
                payload = json.loads(archive.read('draft/draft_content.json'))
                self.assertEqual(payload['materials']['videos'][0]['path'], 'media/screen.png')
                self.assertIn('install_editor_draft.py', archive.namelist())
                self.assertEqual(json.loads(archive.read('draft/draft_meta_info.json'))['draft_fold_path'], '')
            source = json.loads((root / 'out/native/draft_content.json').read_text())
            self.assertTrue(Path(source['materials']['videos'][0]['path']).is_absolute())


if __name__ == '__main__':
    unittest.main()
