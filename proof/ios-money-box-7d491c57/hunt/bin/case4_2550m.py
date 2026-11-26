#!/usr/bin/env python3
import sys,os,time,json,sqlite3,subprocess
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
from case1 import open_filings,open_form,keypad_all

def set_2550m(db,base=0.0,tax=0.0):
 con=sqlite3.connect(db); row=con.execute("select id,data_json from form_drafts where form_code='2550M'").fetchone(); j=json.loads(row[1]); j['sales_to_government']=base; j['output_tax_government']=tax; con.execute('update form_drafts set data_json=? where id=?',(json.dumps(j),row[0])); con.commit(); con.close()
def vals2550m(db):
 con=sqlite3.connect('file:'+db+'?mode=ro',uri=True); row=con.execute("select data_json from form_drafts where form_code='2550M'").fetchone(); con.close(); j=json.loads(row[0]); return {k:j.get(k) for k in ('sales_to_government','output_tax_government','zero_rated_sales','total_sales','total_output_tax')}
def textnodes(W,needle):
 return [n for n in simutil.nodes(W) if n.get('role')=='AXStaticText' and needle.lower() in (n.get('desc') or n.get('title') or n.get('value') or '').lower()]
def visible(n):
 return n.get('pos') and 250<n['pos'][1]<830
def scroll_to_label(W,needles):
 for _ in range(24):
  for needle in needles:
   xs=textnodes(W,needle)
   if xs and visible(xs[0]): return xs[0]
  # expand Part II when its toggle is visible
  for tid in ('fp-part-2-toggle','fp-part-1-toggle','fp-part-3-toggle'):
   xs=simutil.find(W,idpart=tid)
   if xs and visible(xs[0]) and tid=='fp-part-2-toggle': click_node(xs[0],.4); break
  drag_scroll(W,up=True)
 raise RuntimeError('label not found '+repr(needles))
def nearest_field_below(W,label):
 fs=[f for f in simutil.find(W,role='AXTextField') if f.get('pos')]
 if not fs: return None
 lx,ly=label['pos'][0],label['pos'][1]
 cand=[f for f in fs if 0 <= f['pos'][1]-ly < 120]
 return sorted(cand,key=lambda f:(f['pos'][1]-ly,abs(f['pos'][0]-lx)))[0] if cand else None
def hardkey(k):
 subprocess.run(['cliclick','t:'+k],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def tab():
 subprocess.run(['cliclick','kp:tab'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
def run(W,udid,db):
 outsub='iphone' if W==IPHONE else 'ipad'; cdir=os.path.join(ROOT,outsub,'case4','2550m-computed'); os.makedirs(cdir,exist_ok=True)
 open_filings(W); set_2550m(db,0.0,0.0); open_form(W,'2550M')
 lab=scroll_to_label(W,['Sales to Government','13A'])
 shot(udid,cdir+'/000-item13-visible.jpg')
 f=nearest_field_below(W,lab)
 if not f: raise RuntimeError('13A field not found')
 x=round(f['pos'][0]+f['size'][0]-8); y=round(f['pos'][1]+f['size'][1]/2); click_xy(x,y); time.sleep(.4)
 rec={'device':outsub,'case':'case4-2550m-computed','keys':[]}
 for i,k in enumerate('100',1):
  kp=keypad_all(W)
  if k not in kp: raise RuntimeError('keypad missing '+repr(kp))
  xx,yy=kp[k]; click_xy(x,y) if False else click_xy(xx,yy); time.sleep(.14)
  fn=cdir+f'/key-{i}-{k}.jpg'; shot(udid,fn)
  rec['keys'].append({'key':k,'fields':[z.get('value') for z in simutil.find(W,role='AXTextField')],'shot':fn})
 shot(udid,cdir+'/004-before-tab.jpg'); rec['before_tab_fields']=[z.get('value') for z in simutil.find(W,role='AXTextField')]
 tab(); time.sleep(.5); shot(udid,cdir+'/005-after-tab.jpg'); rec['after_tab_fields']=[z.get('value') for z in simutil.find(W,role='AXTextField')]
 hardkey('5'); time.sleep(.3); shot(udid,cdir+'/006-after-hardware-5.jpg'); rec['after_5_fields']=[z.get('value') for z in simutil.find(W,role='AXTextField')]
 # blur with another hardware Tab; then wait for rounding/save
 tab(); time.sleep(.9); shot(udid,cdir+'/007-after-blur.jpg'); rec['after_blur_fields']=[z.get('value') for z in simutil.find(W,role='AXTextField')]
 rec['saved_after_leaving']=vals2550m(db)
 open_filings(W); open_form(W,'2550M'); time.sleep(.5); rec['saved_after_reopening']=vals2550m(db); shot(udid,cdir+'/008-after-reopen.jpg')
 logjson(os.path.join(ROOT,'observations.jsonl'),rec); return rec
if __name__=='__main__': print(json.dumps(run(sys.argv[1],sys.argv[2],sys.argv[3]),indent=1)[:5000])
