import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from lupa.lua51 import LuaRuntime
ROOT=Path(__file__).resolve().parents[1]
def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/f'{name}.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
client=load('elevenlabs_client');installer=load('install_menu_audit')
class HelperTests(unittest.TestCase):
    def test_lua_paths_are_literal(self):
        lua=LuaRuntime()
        for text in ['normal',"path 'quote' \\", 'brackets ]] and ]=]', 'unicode café']:
            self.assertEqual(lua.eval(installer.lua_string(text)),text)
    def test_environment_credential_precedes_file(self):
        with patch.dict(os.environ,{'ELEVENLABS_API_KEY':'fake-test-key','DAVINCI_ELEVENLABS_ENV_FILE':'/missing'},clear=True):
            self.assertEqual(client.credential(),'fake-test-key')
    def test_explicit_profile_file(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'profile.env';p.write_text('OTHER=x\nexport ELEVENLABS_API_KEY="fake-profile-key"\n')
            with patch.dict(os.environ,{'DAVINCI_ELEVENLABS_ENV_FILE':str(p)},clear=True):
                self.assertEqual(client.credential(),'fake-profile-key')
    def test_missing_credential(self):
        with patch.dict(os.environ,{},clear=True):
            with self.assertRaises(RuntimeError):client.credential()
    def test_existing_output_prevents_paid_request(self):
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)/'voice.mp3';out.write_bytes(b'original')
            with patch.object(sys,'argv',['client','generate','--voice','voice1','--text-file','unused','--output',str(out)]),patch.object(client,'request') as request:
                with self.assertRaises(SystemExit):client.main()
                request.assert_not_called();self.assertEqual(out.read_bytes(),b'original')
    def test_generation_payload_and_uncertain_reservation(self):
        with tempfile.TemporaryDirectory() as d:
            text=Path(d)/'text.txt';text.write_text('Come on in.');out=Path(d)/'voice.mp3'
            with patch.object(sys,'argv',['client','generate','--voice','voice1','--text-file',str(text),'--output',str(out)]),patch.object(client,'request',side_effect=RuntimeError('uncertain')) as req:
                with self.assertRaises(RuntimeError):client.main()
                self.assertEqual(req.call_args.args[1]['voice_settings']['style'],.08)
                self.assertTrue(out.exists());self.assertEqual(out.stat().st_size,0)
    def test_installer_and_wrong_project_guard(self):
        with tempfile.TemporaryDirectory() as d:
            base=Path(d);dest=base/'utility';reports=base/'reports'
            cmd=[sys.executable,str(ROOT/'scripts/install_menu_audit.py'),'--project','Expected Project','--dest',str(dest),'--reports',str(reports)]
            subprocess.run(cmd,check=True,capture_output=True)
            target=dest/'Codex - Resolve 19 read-only audit.lua';lua=LuaRuntime()
            lua.execute("resolve={GetProjectManager=function()return {GetCurrentProject=function()return {GetName=function()return 'Different Project' end}end}end}")
            with self.assertRaisesRegex(Exception,'Project mismatch'):lua.execute(target.read_text())
            self.assertEqual(list(reports.glob('*.json')),[])
            self.assertIn('success=false',next(reports.glob('*.log')).read_text())
            old=target.read_text();cmd[cmd.index('Expected Project')]='Changed Project'
            result=subprocess.run(cmd,capture_output=True);self.assertNotEqual(result.returncode,0);self.assertEqual(target.read_text(),old)
    def test_skills_install_together_and_refuse_difference(self):
        with tempfile.TemporaryDirectory() as d:
            cmd=[sys.executable,str(ROOT/'scripts/install_skills.py'),'--dest',d]
            subprocess.run(cmd,check=True,capture_output=True);subprocess.run(cmd,check=True,capture_output=True)
            self.assertEqual(len(list(Path(d).glob('*/SKILL.md'))),4)
            p=Path(d)/'edit-davinci-video/SKILL.md';p.write_text('custom')
            self.assertNotEqual(subprocess.run(cmd,capture_output=True).returncode,0);self.assertEqual(p.read_text(),'custom')
if __name__=='__main__':unittest.main()
