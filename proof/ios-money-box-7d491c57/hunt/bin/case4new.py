#!/usr/bin/env python3
# 2550M 13A -> computed 13B hardware-Tab test. Hardware key events are used only where the case requires Tab/keyboard input.
import sys,os,time,json,sqlite3,subprocess
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
from case1 import open_filings,open_form,keypad_all
from case3 import launch

def vals(db):
 j=json.loads(sqlite3.connect(db).execute("select data_json from form_drafts where form_code='2550M'").fetchone()[0]); return {k:j.get(k) for k in ['sales_to_government','output_tax_government','zero_rated_sales']}
def reset(db):
 con=sqlite3.connect(db); j=json.loads(con.execute("select data_json from form_drafts where form_code='2550M'").fetchone()[0])
 for k in ['sales_to_government','output_tax_government','zero_rated_sales']: j[k]=0.0
 con.execute("update form_drafts set data_json=? where form_code='2550M'",(json.dumps(j),)); con.commit(); con.close()
def drag(W,up=False):
 x,y1,y2=((200,350,650) if W==IPHONE else (760,500,900))
 if up: y1,y2=y2,y1
 subprocess.run(['cliclick',f'dd:{x},{y1}',f'du:{x},{y2}'],stdout=subprocess.DEVNULL); time.sleep(.45)
def static(W,txt):
 for n in simutil.nodes(W):
  if n.get('role')=='AXStaticText' and (n.get('desc') or '')==txt: return n
def button(W,id):
 for n in simutil.nodes(W):
  if n.get('id')==id: return n
def bring_static(W,txt,lo=250,hi=800):
 for i in range(24):
  n=static(W,txt)
  if n and n.get('pos'):
   y=n['pos'][1]
   if lo<=y<=hi: return n
   drag(W,up=(y<lo))
  else: drag(W,up=False)
  if i==5:
   b=button(W,'fp-part-2-toggle')
   if b and b.get('pos') and 120<b['pos'][1]<980: click_node(b,.5)
 raise RuntimeError('no '+txt)
def key(ch): subprocess.run(['cliclick','t:'+ch],stdout=subprocess.DEVNULL); time.sleep(.14)
def tab(): subprocess.run(['cliclick','kp:tab'],stdout=subprocess.DEVNULL); time.sleep(.55)
def run(W,udid,db):
 outsub='iphone' if W==IPHONE else 'ipad'; cdir=os.path.join(ROOT,outsub,'case4','2550m'); os.makedirs(cdir,exist_ok=True)
 reset(db); launch(udid,db); open_filings(W); open_form(W,'2550M')
 # expand part II if needed, then bring item 13A visible
 b=button(W,'fp-part-2-toggle')
 for i in range(12):
  b=button(W,'fp-part-2-toggle')
  if b and b.get('pos') and 150<b['pos'][1]<950: click_node(b,.5); break
  drag(W,up=bool(b and b.get('pos') and b['pos'][1]<150))
 n=bring_static(W,'13A'); shot(udid,cdir+'/000-13A-visible.jpg')
 # first visible text field below 13A label
 fs=[f for f in simutil.nodes(W) if f.get('role')=='AXTextField' and f.get('pos') and f['pos'][1]>n['pos'][1] and f['pos'][1]<n['pos'][1]+180]
 if not fs: raise RuntimeError('no 13A field '+repr([(f.get('value'),f.get('pos')) for f in simutil.nodes(W) if f.get('role')=='AXTextField']))
 f=fs[0]; click_node(f,.5); shot(udid,cdir+'/001-focused13A.jpg')
 rec={'device':outsub,'case':'case4-2550m','keys':[]}
 for i,ch in enumerate('100',1):
  key(ch); fn=cdir+f'/key-{i}-{ch}.jpg'; shot(udid,fn); rec['keys'].append({'key':ch,'shot':fn,'fields':[x.get('value') for x in simutil.nodes(W) if x.get('role')=='AXTextField']})
 tab(); shot(udid,cdir+'/004-after-tab.jpg'); rec['after_tab_fields']=[x.get('value') for x in simutil.nodes(W) if x.get('role')=='AXTextField']
 key('5'); shot(udid,cdir+'/005-after-5.jpg'); rec['after_5_fields']=[x.get('value') for x in simutil.nodes(W) if x.get('role')=='AXTextField']
 tab(); time.sleep(.7); shot(udid,cdir+'/006-after-blur.jpg'); rec['saved_after_blur']=vals(db)
 open_form(W,'2550M'); time.sleep(.5); rec['saved_after_reopen']=vals(db); shot(udid,cdir+'/007-after-reopen.jpg')
 logjson(os.path.join(ROOT,'observations.jsonl'),rec); return rec
if __name__=='__main__': print(json.dumps(run(sys.argv[1],sys.argv[2],sys.argv[3]),indent=1)[:4000])
