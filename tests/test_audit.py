import json
from pathlib import Path
import tempfile
import unittest
from lupa.lua51 import LuaRuntime

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/edit-davinci-video/scripts/inspect_resolve.lua'
MOCK = r'''
print = function(...) end
function obj(values)
  return setmetatable({}, {__index=function(_, method)
    assert(method:sub(1,3) == 'Get', 'Mutation attempted: '..method)
    local value = values[method]
    assert(value ~= nil, 'Unsupported getter: '..method)
    if type(value) == 'function' then return value end
    return function() return value end
  end})
end
clip = obj({GetName='clip "one"\nscene', GetUniqueId='clip1', GetClipProperty={['File Path']='/source/a.mov', FPS='29.97'}})
folder = obj({GetName='Master', GetUniqueId='folder1', GetClipList={clip,clip}, GetSubFolderList={}})
item = obj({GetName='clip1', GetUniqueId='item1', GetMediaPoolItem=clip, GetStart=108000,
  GetEnd=108100, GetDuration=100, GetLeftOffset=10, GetRightOffset=10})
timeline = obj({GetName='working', GetUniqueId='timeline1', GetSetting='29.97',
  GetStartFrame=108000, GetEndFrame=108100, GetStartTimecode='01:00:00;00',
  GetCurrentTimecode='01:00:00;00', GetTrackCount=function(_, t) return t == 'video' and 1 or 0 end,
  GetTrackName='Video 1', GetIsTrackEnabled=false, GetIsTrackLocked=true, GetItemListInTrack={item}})
active = nil
project = obj({GetName='tommy-fox-show', GetUniqueId='project1',
  GetSetting=function(_, key) return key == 'timelineFrameRate' and '30' or '1080' end,
  GetTimelineCount=function() return active and 1 or 0 end, GetTimelineByIndex=function() return active end,
  GetCurrentTimeline=function() return active end, GetMediaPool=obj({GetRootFolder=folder}),
  GetRenderFormats={MP4='mp4'}, GetRenderCodecs={H264='H264'}})
resolve = obj({GetProductName='DaVinci Resolve', GetVersionString='19.1.4.11', GetCurrentPage='cut',
  GetProjectManager=obj({GetCurrentProject=project})})
'''


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.lua = LuaRuntime()
        self.lua.execute(MOCK)
        self.run_audit = self.lua.execute(SCRIPT.read_text())
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.output = Path(self.tmp.name) / 'audit.json'

    def run_report(self, **kwargs):
        opts = {'expected_project': 'tommy-fox-show', 'output_path': str(self.output), **kwargs}
        self.run_audit(self.lua.table_from(opts))
        return json.loads(self.output.read_text())

    def test_no_timeline_does_not_invent_fps(self):
        report = self.run_report()
        self.assertFalse(report['has_active_timeline'])
        self.assertNotIn('current_timeline', report)
        self.assertEqual(report['project']['frame_rate_setting'], '30')
        self.assertEqual(report['timelines'], [])
        self.assertEqual(report['errors'], [])
        self.assertEqual(report['media'][0]['name'], 'clip "one"\nscene')
        self.assertEqual(report['status'], 'complete_read_only_snapshot')

    def test_timeline_fractional_fps_track_state_and_ranges(self):
        self.lua.execute('active=timeline')
        report = self.run_report()
        self.assertEqual(report['current_timeline']['fps'], '29.97')
        track = report['current_timeline']['tracks'][0]
        self.assertFalse(track['enabled'])
        self.assertTrue(track['locked'])
        self.assertEqual(track['items'][0]['start_frame'], 108000)
        self.assertEqual(report['status'], 'complete_read_only_snapshot')

    def test_wrong_project_writes_nothing(self):
        with self.assertRaisesRegex(Exception, 'Project mismatch'):
            self.run_report(expected_project='another-project')
        self.assertFalse(self.output.exists())

    def test_bounded_scan_reports_partial(self):
        report = self.run_report(max_media=1)
        self.assertTrue(report['scan_truncated'])
        self.assertEqual(report['media_count'], 1)
        self.assertEqual(report['status'], 'partial')

    def test_getter_error_not_silently_complete(self):
        self.lua.execute('project.GetRenderCodecs=function() error("unavailable") end')
        report = self.run_report()
        self.assertEqual(report['status'], 'partial')
        self.assertEqual(report['errors'][0]['method'], 'GetRenderCodecs')

    def test_preserve_existing_report(self):
        self.output.write_text('preserve')
        with self.assertRaisesRegex(Exception, 'Report exists'):
            self.run_report()
        self.assertEqual(self.output.read_text(), 'preserve')


if __name__ == '__main__':
    unittest.main()
