#!/usr/bin/env python3
import json, subprocess, time, os, sys, re
AXREAD='/tmp/axread'

def tree(pid=None):
    if pid is None:
        pid=subprocess.check_output(['pgrep','-x','Simulator'],text=True).splitlines()[0]
    out=subprocess.check_output([AXREAD,str(pid),'30'],stderr=subprocess.DEVNULL)
    return json.loads(out)

def walk(x):
    yield x
    for c in x.get('children',[]): yield from walk(c)

def windows(t=None):
    if t is None: t=tree()
    return [n for n in walk(t) if n.get('role')=='AXWindow']

def window(namepart):
    ws=windows()
    for w in ws:
        if namepart.lower() in (w.get('title') or '').lower(): return w
    raise RuntimeError('window not found '+namepart+' have '+repr([w.get('title') for w in ws]))

def nodes(winpart):
    w=window(winpart)
    return list(walk(w))

def label(n):
    return n.get('desc') or n.get('title') or n.get('value') or ''

def center(n):
    p=n.get('pos'); s=n.get('size')
    if not p or not s: raise RuntimeError('no geometry '+repr(n))
    return (round(p[0]+s[0]/2), round(p[1]+s[1]/2))

def find(winpart, text=None, idpart=None, role=None, value=None):
    out=[]
    for n in nodes(winpart):
        if role and n.get('role')!=role: continue
        if text is not None and text.lower() not in label(n).lower(): continue
        if idpart is not None and idpart.lower() not in (n.get('id') or '').lower(): continue
        if value is not None and value != (n.get('value') or ''): continue
        out.append(n)
    return out

def click(n, wait=0.15):
    x,y=center(n)
    subprocess.run(['cliclick',f'c:{x},{y}'],check=True,stdout=subprocess.DEVNULL)
    if wait: time.sleep(wait)
    return (x,y,time.time())

def click_text(winpart,text,role=None,wait=0.2,index=0):
    xs=find(winpart,text=text,role=role)
    if not xs: raise RuntimeError(f'not found {text}')
    return click(xs[index],wait)

def click_id(winpart,idpart,wait=0.2,index=0):
    xs=find(winpart,idpart=idpart)
    if not xs: raise RuntimeError(f'id not found {idpart}')
    return click(xs[index],wait)

def dump(winpart, roles=('AXButton','AXTextField','AXStaticText')):
    rows=[]
    for n in nodes(winpart):
        if n.get('role') in roles and (label(n) or n.get('id')):
            rows.append({'role':n.get('role'),'label':label(n),'value':n.get('value') or '', 'id':n.get('id') or '', 'pos':n.get('pos'), 'size':n.get('size')})
    return rows

if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='dump':
        print(json.dumps(dump(sys.argv[2]),indent=2))
    elif cmd=='clicktext': print(click_text(sys.argv[2],sys.argv[3]))
    elif cmd=='clickid': print(click_id(sys.argv[2],sys.argv[3]))
    elif cmd=='find': print(json.dumps(find(sys.argv[2],text=(sys.argv[3] if len(sys.argv)>3 else None),idpart=(sys.argv[4] if len(sys.argv)>4 else None)),indent=2))
