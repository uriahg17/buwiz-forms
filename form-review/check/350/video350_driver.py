#!/usr/bin/env python3
import json, os, subprocess, sys, time, pathlib, re
OUT=pathlib.Path.home()/"BuwizNsh/proof350/form-review/check/350"
E=os.environ.copy(); E.update({'GPUI_AGENT_ADDR':'127.0.0.1:17521','GPUI_AGENT_TOKEN':'check350local','DISPLAY':':99','XAUTHORITY':'/tmp/xauth99'})
def agent(*args,ok=True):
 p=subprocess.run(['gpui-agent']+list(args),capture_output=True,text=True,env=E)
 try:d=json.loads(p.stdout)
 except:d={'ok':p.returncode==0,'raw':p.stdout+p.stderr}
 if ok and (p.returncode or d.get('ok') is False): raise RuntimeError(str(d)[:600])
 return d
def nodes():
 d=agent('snapshot'); out=[]
 def rec(xs):
  for n in xs: out.append(n); rec(n.get('children',[]))
 rec(d['tree']['nodes']); return out
def node(id): return next((n for n in nodes() if n.get('id')==id),None)
def center(n):return (round(n['bounds']['x']+n['bounds']['w']/2),round(n['bounds']['y']+n['bounds']['h']/2))
def press_node(id,wait=.8):
 n=node(id)
 if not n: raise RuntimeError('missing '+id)
 x,y=center(n); agent('press','--x',str(x),'--y',str(y),'--no-read-back'); time.sleep(wait)
def press_point(x,y,wait=.8): agent('press','--x',str(round(x)),'--y',str(round(y)),'--no-read-back'); time.sleep(wait)
def text_point(row):
 # x inside the visible title text, center height
 return (round(row['bounds']['x']+170),round(row['bounds']['y']+row['bounds']['h']/2))
def count():
 n=node('tp-forms-count'); return n and n.get('name')
def wait_ready():
 for _ in range(80):
  try:
   if node('tp-forms-edit'): return
  except Exception: pass
  time.sleep(.25)
 raise RuntimeError('picker did not become ready')
def ffmpeg_start(path,w,h):
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','x11grab','-video_size',f'{w}x{h}','-framerate','15','-i',':99.0+0,0','-c:v','libx264','-preset','veryfast','-pix_fmt','yuv420p',str(path)]
 return subprocess.Popen(cmd,env=E,stdin=subprocess.DEVNULL,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
def ffmpeg_stop(p):
 p.terminate()
 try:p.wait(timeout=5)
 except: p.kill();p.wait()

def flow(width):
 log=[]
 wait_ready(); time.sleep(.8)
 if width=='phone':
  agent('viewport','--width','390','--height','844'); time.sleep(1.2)
 else:
  agent('viewport','--width','1440','--height','900'); time.sleep(1.0)
 # window outer dimensions are logical+10 on this GTK build
 dims=(1450,910) if width=='desktop' else (430,854)
 vid=OUT/f'picker-head-{width}.mp4'
 ff=ffmpeg_start(vid,*dims); time.sleep(1.0)
 try:
  press_node('tp-forms-edit',1.4); log.append(('open_edit',count()))
  if width=='phone':
   # search results are part of the claim and keep 1601C visible at the narrowest width
   press_node('tp-forms-search',.5)
   agent('type','tp-forms-search','1601C','--no-read-back',ok=False); time.sleep(1.0)
  rows=[n for n in nodes() if n.get('id')=='tp-form-1601C']
  if not rows and width=='phone':
   agent('set-value','tp-forms-search','1601C','--no-read-back');time.sleep(.8);rows=[n for n in nodes() if n.get('id')=='tp-form-1601C']
  if not rows: raise RuntimeError('1601C row not visible')
  x,y=text_point(rows[0])
  press_point(x,y,1.5);log.append(('text_uncheck_1601C',count()))
  press_point(x,y,1.5);log.append(('text_check_1601C',count()))
  # choose one more form by its visible title when it is on screen; on the phone, use the filtered row only
  if width=='desktop':
   r=node('tp-form-0619E')
   if r:
    x,y=text_point(r);press_point(x,y,1.3);log.append(('text_check_0619E',count()))
  press_node('tp-forms-save',1.8);log.append(('save',count()))
  press_node('tp-tabs-templates',1.3)
  press_node('tp-tabs-forms',1.8);log.append(('reopened','forms-tab'))
  time.sleep(1.5)
 finally:
  ffmpeg_stop(ff)
 (OUT/f'video-head-{width}-log.json').write_text(json.dumps(log,indent=2))
 print(json.dumps({'video':str(vid),'log':log},indent=2))

if __name__=='__main__':flow(sys.argv[1])
