"""Small local MCP client for the already configured Unity endpoint."""
import json, urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')
headers={'Content-Type':'application/json','Accept':'application/json, text/event-stream'}
def rpc(method,params):
    req=urllib.request.Request('http://127.0.0.1:8080/mcp',json.dumps({'jsonrpc':'2.0','id':1,'method':method,'params':params}).encode(),headers)
    with urllib.request.urlopen(req,timeout=180) as r:
        if r.headers.get('Mcp-Session-Id'): headers['Mcp-Session-Id']=r.headers['Mcp-Session-Id']
        body=r.read().decode()
        data=[line[5:].strip() for line in body.splitlines() if line.startswith('data:')]
        return json.loads(data[-1] if data else body)
if __name__=='__main__':
    rpc('initialize',{'protocolVersion':'2025-03-26','capabilities':{},'clientInfo':{'name':'TidyBuilder','version':'1'}})
    if sys.argv[1]=='list':
        result=rpc('tools/list',{})['result']['tools']
        result=[t for t in result if t['name'] in sys.argv[2:]] if len(sys.argv)>2 else [t['name'] for t in result]
    elif sys.argv[1]=='resources': result=rpc('resources/list',{})
    elif sys.argv[1]=='read': result=rpc('resources/read',{'uri':sys.argv[2]})
    else: result=rpc('tools/call',{'name':sys.argv[1],'arguments':json.loads(sys.argv[2]) if len(sys.argv)>2 else {}})
    print(json.dumps(result,ensure_ascii=False,indent=2))
