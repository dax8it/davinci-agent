#!/usr/bin/env python3
"""Small ElevenLabs REST client. No MCP required; never logs the API key."""
import argparse
import json
import os
from pathlib import Path
import re
import urllib.error
import urllib.request

def credential():
    key=os.environ.get('ELEVENLABS_API_KEY','').strip()
    if key:return key
    filename=os.environ.get('DAVINCI_ELEVENLABS_ENV_FILE')
    if filename:
        for line in Path(filename).expanduser().read_text().splitlines():
            line=line.strip()
            if line.startswith('export '):line=line[7:].strip()
            name,sep,value=line.partition('=')
            if sep and name.strip()=='ELEVENLABS_API_KEY':
                key=value.strip().strip('\"').strip("'")
                if key:return key
    raise RuntimeError('Set ELEVENLABS_API_KEY or DAVINCI_ELEVENLABS_ENV_FILE; never paste the key in chat.')

def request(endpoint,payload=None):
    key=credential()
    req=urllib.request.Request('https://api.elevenlabs.io/v1/'+endpoint,
        data=json.dumps(payload).encode() if payload is not None else None,
        headers={'xi-api-key':key,'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=90) as response:return response.read()
    except urllib.error.HTTPError as e:
        # Avoid provider response bodies: they may echo submitted text or credentials.
        raise RuntimeError(f'ElevenLabs HTTP {e.code}. Check key permissions, voice access and account quota.') from None
    except urllib.error.URLError:
        raise RuntimeError('ElevenLabs connection failed. Check request history before repeating a generation.') from None

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('action',choices=['inspect','generate'])
    p.add_argument('--voice');p.add_argument('--text-file',type=Path);p.add_argument('--output',type=Path)
    p.add_argument('--model',default='eleven_multilingual_v2');p.add_argument('--stability',type=float,default=.4)
    p.add_argument('--similarity',type=float,default=.75);p.add_argument('--style',type=float,default=.08)
    a=p.parse_args()
    for v in [a.stability,a.similarity,a.style]:
        if not 0<=v<=1:p.error('Voice settings must be between 0 and 1')
    if a.output and a.output.exists():p.error('Output exists; choose a new version to preserve it')
    if a.action=='inspect':
        data=json.loads(request('voices'))
        rows=[{k:v.get(k) for k in ['voice_id','name','labels']} for v in data.get('voices',[])]
        result=json.dumps(rows,indent=2)+'\n'
        if a.output:
            a.output.parent.mkdir(parents=True,exist_ok=True)
            with a.output.open('x') as f:f.write(result)
        else:print(result)
        return
    if not a.voice or not re.fullmatch(r'[A-Za-z0-9_-]+',a.voice) or not a.text_file or not a.output:
        p.error('generate requires a valid --voice, --text-file and --output')
    text=a.text_file.read_text().strip()
    if not text:p.error('Text file is empty')
    a.output.parent.mkdir(parents=True,exist_ok=True)
    # Reserve the output before a billable call. On failure, leave an empty reservation
    # so an uncertain request cannot be accidentally repeated by rerunning this command.
    with a.output.open('xb') as f:
        result=request('text-to-speech/'+a.voice+'?output_format=mp3_44100_128',{
            'text':text,'model_id':a.model,'voice_settings':{'stability':a.stability,
            'similarity_boost':a.similarity,'style':a.style,'use_speaker_boost':True}})
        if not result:raise RuntimeError('Empty response; check request history before retrying')
        f.write(result)
    print('Generated',a.output,len(result),'bytes')
if __name__=='__main__':
    try:main()
    except (RuntimeError,OSError) as e:raise SystemExit(str(e)) from None
