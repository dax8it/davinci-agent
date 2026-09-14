#!/usr/bin/env python3
"""Bounded read-only probe of the installed macOS Resolve external API.

No shell profile changes. Free normally cannot expose an external connection;
use the in-process Lua audit instead. An import success is not a connection.
"""
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

API = Path('/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting')
LIB = Path('/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so')


def child():
    sys.path.insert(0, str(API / 'Modules'))
    os.environ['RESOLVE_SCRIPT_LIB'] = str(LIB)
    try:
        import DaVinciResolveScript as dvr
        resolve = dvr.scriptapp('Resolve')
        if not resolve:
            return {'status': 'no_external_connection', 'module_imported': True,
                    'note': 'Free requires the in-process console. For Studio, also check running app and Local scripting preference.'}
        project = resolve.GetProjectManager().GetCurrentProject()
        timeline = project.GetCurrentTimeline() if project else None
        return {'status': 'connected_read_only', 'product': resolve.GetProductName(),
                'version': resolve.GetVersionString(), 'project': project.GetName() if project else None,
                'timeline': timeline.GetName() if timeline else None,
                'timeline_fps': timeline.GetSetting('timelineFrameRate') if timeline else None}
    except Exception as exc:
        return {'status': 'probe_error', 'error_type': type(exc).__name__, 'error': str(exc)}


def main():
    if '--child' in sys.argv:
        print(json.dumps(child()))
        return
    report = {'python': sys.version.split()[0], 'architecture': platform.machine(),
              'api_module_exists': (API / 'Modules/DaVinciResolveScript.py').is_file(),
              'scripting_library_exists': LIB.is_file()}
    try:
        result = subprocess.run([sys.executable, str(Path(__file__).resolve()), '--child'],
                                capture_output=True, text=True, timeout=15)
        report['exit_code'] = result.returncode
        report['stdout'] = result.stdout.strip()
        report['stderr'] = result.stderr.strip()
        report['status'] = 'child_finished' if result.returncode == 0 else 'child_failed'
    except subprocess.TimeoutExpired:
        report['status'] = 'timeout'
        report['note'] = 'External probe terminated after 15 seconds; use the internal console.'
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
