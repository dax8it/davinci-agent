#!/usr/bin/env python3
"""Install a project-guarded, read-only Resolve Utility menu script on macOS."""
import argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def lua_string(value):
    value=str(value)
    for n in range(20):
        eq='='*n
        if ']'+eq+']' not in value:
            return '['+eq+'['+value+']'+eq+']'
    raise ValueError('Cannot quote Lua string')
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--project',required=True)
    p.add_argument('--reports',type=Path,default=ROOT/'reports')
    p.add_argument('--dest',type=Path,default=Path.home()/'Library/Application Support/Blackmagic Design/DaVinci Resolve/Fusion/Scripts/Utility')
    a=p.parse_args();reports=a.reports.expanduser().resolve()
    text="return dofile(%s)({root=%s, expected_project=%s, reports=%s})\n" % tuple(map(lua_string,[ROOT/'scripts/menu_audit.lua',ROOT,a.project,reports]))
    target=a.dest.expanduser()/'Codex - Resolve 19 read-only audit.lua'
    if target.exists() and target.read_text()!=text:
        p.error(f'Existing launcher differs; back it up before replacing: {target}')
    reports.mkdir(parents=True,exist_ok=True);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(text);print(target)
if __name__=='__main__':main()
