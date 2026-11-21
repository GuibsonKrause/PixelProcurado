"""Handshake MCP real na cópia local do Concat, com timeout e encerramento."""
import json
from pathlib import Path
import queue
import subprocess
import threading
import sys
import time

root=Path(__file__).resolve().parent.parent
exe=root/'.production-tools/concat-portable/PFiles64/Concat/concat.exe'
dest=root/'producao/L01/testes'
dest.mkdir(parents=True,exist_ok=True)
q=queue.Queue()
err=open(dest/'concat-stderr.log','w',encoding='utf-8')
p=subprocess.Popen([str(exe),'--mcp','headless'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,
                   stderr=err,text=True,encoding='utf-8',errors='replace')
def read():
    for line in p.stdout: q.put(line)
threading.Thread(target=read,daemon=True).start()
def request(id,method,params):
    p.stdin.write(json.dumps({'jsonrpc':'2.0','id':id,'method':method,'params':params})+'\n'); p.stdin.flush()
    while True:
        line=q.get(timeout=30)
        try: value=json.loads(line)
        except json.JSONDecodeError: continue
        if value.get('id')==id:
            if 'error' in value: raise RuntimeError(value['error'])
            return value
try:
    init=request(1,'initialize',{'protocolVersion':'2025-03-26','capabilities':{},'clientInfo':{'name':'pixel-local-test','version':'1'}})
    p.stdin.write(json.dumps({'jsonrpc':'2.0','method':'notifications/initialized'})+'\n'); p.stdin.flush()
    listing=request(2,'tools/list',{})
    names=[t['name'] for t in listing['result']['tools']]
    version=request(3,'tools/call',{'name':'concat_version','arguments':{}}) if 'concat_version' in names else None
    (dest/'concat-mcp.json').write_text(json.dumps({'initialize':init,'tool_names':names,'version':version},indent=2),encoding='utf-8')
    (dest/'concat-schemas.json').write_text(json.dumps(listing,indent=2),encoding='utf-8')
    print(json.dumps({'status':'connected','tools':len(names),'version':version},ensure_ascii=False))
    if '--export' in sys.argv:
        counter=10
        def call(name,args):
            global counter
            counter+=1
            r=request(counter,'tools/call',{'name':name,'arguments':args})['result']
            if r.get('isError'): raise RuntimeError(r)
            value=r.get('structuredContent')
            if value is None: value=json.loads(r['content'][0]['text'])
            print(name, json.dumps(value,ensure_ascii=False)[:1800],flush=True)
            return value
        project_name='concat-teste-'+time.strftime('%H%M%S')
        project=str(dest/project_name)
        call('project_create',{'location':str(dest),'name':project_name})
        imported=call('media_import',{'path':project,'file':str(root/'producao/L01/arte/cartela_confirmado.png')})
        timeline=call('timeline_read',{'path':project})
        call('clip_add',{'path':project,'mediaId':imported['createdId'],
                        'trackId':timeline['timeline']['tracks'][0]['id'],'start':0})
        (dest/'concat-edit-state.json').write_text(json.dumps({'path':project,'import':imported,'timeline':timeline},indent=2),encoding='utf-8')
        call('project_save',{'path':project})
        job=call('export_start',{'path':project,'output':str(dest/(project_name+'.mp4')),'preset':'fast'})
        result=call('export_wait',{'job':job['job'],'timeoutSeconds':25})
        (dest/'concat-export-result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
finally:
    p.terminate()
    try: p.wait(timeout=5)
    except subprocess.TimeoutExpired: p.kill(); p.wait()
    err.close()
