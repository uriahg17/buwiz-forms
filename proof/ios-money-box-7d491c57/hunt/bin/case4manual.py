#!/usr/bin/env python3
# Controlled 2550M 13A/13B test using real keypad digits for 100 and hardware Tab/5 for focus test.
import sys,os,time,json,sqlite3,subprocess
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
from case3 import launch
from lifelib import set_hardware

def reset2550(db):
 con=sqlite3.connect(db); row=con.execute("select id,data_json from form_drafts where form_code='2550M'").fetchone(); j=json.loads(row[1])
 for k in ['sales_to_government','output_tax_government','zero_rated_sales']: j[k]=0.0
 con.execute('update form_drafts set data_json=? where id=?',(json.dumps(j),row[0])); con.commit(); con.close()
def vals(db):
 j=json.loads(sqlite3.connect(db).execute("select data_json from form_drafts where form_code='2550M'").fetchone()[0]); return {k:j.get(k) for k in ['sales_to_government','output_tax_government','zero_rated_sales','total_sales','total_output_tax']}
def small_scroll(W,up=True):
 x=250 if W==IPHONE else 800
 if up: subprocess.run(['cliclick',f'dd:{x},750',f'dm:{x},650',f'du:{x},650'],stdout=subprocess.DEVNULL)
 else: subprocess.run(['cliclick',f'dd:{x},650',f'dm:{x},750',f'du:{x},750'],stdout=subprocess.DEVNULL)
 time.sleep(.45)
def nodeid(W,id):
 return next((n for n in simutil.nodes(W) if n.get('id')==id),None)
def open_return2(W):
 for n in simutil.nodes(W):
  if n.get('id')=='tab-filings': click_node(n,.7); break
 for _ in range(10):
  n=nodeid(W,'return-2')
  if n: click_node(n,1); return
  time.sleep(.3)
 raise RuntimeError('return-2 missing')
def nav_13a(W):
 def stxt(txt):
  return next((n for n in simutil.nodes(W) if n.get('role')=='AXStaticText' and (n.get('desc') or '')==txt),None)
 # Small controlled scrolling. Part II may already be expanded from editor state; only click its
 # toggle when its fields are absent, otherwise that click collapses it.
 expanded=False
 for i in range(18):
  if stxt('13A'): expanded=True; break
  b=nodeid(W,'fp-part-2-toggle')
  if b and b.get('pos'):
   y=b['pos'][1]
   if 300<y<790 and not stxt('12A'):
    click_node(b,.8); continue
   small_scroll(W,up=(y>790))
  else: small_scroll(W,up=True)
 for i in range(18):
  st=stxt('13A')
  if st and st.get('pos'):
   y=st['pos'][1]
   if 430<y<720: return st
   small_scroll(W,up=(y>720))
  else: small_scroll(W,up=True)
 raise RuntimeError('13A not positioned')
def menu_hardware():
 subprocess.run(['osascript','-e','tell application "System Events" to tell process "Simulator" to click menu item "Connect Hardware Keyboard" of menu "Keyboard" of menu item "Keyboard" of menu "I/O" of menu bar 1'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.55)
def run(W,udid,db):
 outsub='iphone' if W==IPHONE else 'ipad'; cdir=os.path.join(ROOT,outsub,'case4','2550m-final'); os.makedirs(cdir,exist_ok=True)
 rec={'device':outsub,'case':'case4-2550m-final'}
 reset2550(db); launch(udid,db); set_hardware(W,False); open_return2(W); nav_13a(W); shot(udid,cdir+'/000-13A-visible.jpg')
 st=next(n for n in simutil.nodes(W) if n.get('role')=='AXStaticText' and (n.get('desc') or '')=='13A')
 fs=[n for n in simutil.nodes(W) if n.get('role')=='AXTextField' and n.get('pos') and st['pos'][1]<n['pos'][1]<st['pos'][1]+130]
 if not fs: raise RuntimeError('no field below 13A '+repr([(n.get('value'),n.get('pos')) for n in simutil.nodes(W) if n.get('role')=='AXTextField']))
 click_node(fs[0],.7); rec['pre_fields']=[n.get('value') for n in simutil.nodes(W) if n.get('role')=='AXTextField']; shot(udid,cdir+'/001-focused.jpg')
 kp=keypad(W); rec['keypad_visible']=bool(kp); rec['keypad_labels']=sorted(kp)
 if not kp: raise RuntimeError('software keypad not visible')
 rec['keys']=[]
 for i,ch in enumerate('100',1):
  kp=keypad(W); click_xy(*kp[ch]); time.sleep(.17); fn=cdir+f'/key-{i}-{ch}.jpg'; shot(udid,fn)
  rec['keys'].append({'key':ch,'shot':fn,'fields':[n.get('value') for n in simutil.nodes(W) if n.get('role')=='AXTextField']})
 time.sleep(.8); rec['db_after_100']=vals(db); shot(udid,cdir+'/004-after-100.jpg')
 # setup hardware keyboard; software pad has no Next/Done. Full Keyboard Access was enabled in device settings.
 set_hardware(W,True); rec['keys_after_hardware_connect']=len(keypad(W))
 subprocess.run(['cliclick','kp:tab'],stdout=subprocess.DEVNULL); time.sleep(.8); shot(udid,cdir+'/005-after-tab.jpg')
 rec['after_tab_fields']=[n.get('value') for n in simutil.nodes(W) if n.get('role')=='AXTextField']
 subprocess.run(['cliclick','t:5'],stdout=subprocess.DEVNULL); time.sleep(.55); shot(udid,cdir+'/006-after-5.jpg')
 rec['after_5_fields']=[n.get('value') for n in simutil.nodes(W) if n.get('role')=='AXTextField']
 subprocess.run(['cliclick','kp:tab'],stdout=subprocess.DEVNULL); time.sleep(.8); shot(udid,cdir+'/007-after-blur-tab.jpg')
 rec['saved_after_blur']=vals(db)
 open_return2(W); time.sleep(.5); shot(udid,cdir+'/008-after-reopen.jpg'); rec['saved_after_reopen']=vals(db)
 logjson(os.path.join(ROOT,'observations.jsonl'),rec); return rec
if __name__=='__main__': print(json.dumps(run(sys.argv[1],sys.argv[2],sys.argv[3]),indent=1)[:5000])
