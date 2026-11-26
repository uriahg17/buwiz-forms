#!/usr/bin/env python3
import sys,os,time,json,sqlite3
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
from case1 import open_filings,open_form,keypad_all,wait_field

def set_sheets(db,v):
 con=sqlite3.connect(db); row=con.execute("select id,data_json from form_drafts where form_code='2551Q'").fetchone(); j=json.loads(row[1]); j['number_of_attached_sheets']=v; con.execute('update form_drafts set data_json=? where id=?',(json.dumps(j),row[0])); con.commit(); con.close()
def sheets(db):
 con=sqlite3.connect('file:'+db+'?mode=ro',uri=True); row=con.execute("select data_json from form_drafts where form_code='2551Q'").fetchone(); con.close(); return json.loads(row[0]).get('number_of_attached_sheets') if row else None
def sheets_field(W):
 fs=simutil.find(W,role='AXTextField')
 # Number of sheets is the lowest return-details input; sheet modal fields are excluded by y/layout heuristics
 fs=[f for f in fs if f.get('pos') and f['pos'][1]<900]
 return sorted(fs,key=lambda n:n['pos'][1])[-1] if fs else None
def run(W,udid,db):
 outsub='iphone' if W==IPHONE else 'ipad'; cdir=os.path.join(ROOT,outsub,'case5'); os.makedirs(cdir,exist_ok=True)
 open_filings(W); set_sheets(db,0); open_form(W,'2551Q')
 # expand return details if needed and scroll until the sheets input is visible
 f=None
 for _ in range(10):
  f=sheets_field(W)
  if f and 330<f['pos'][1]<850: break
  drag_scroll(W,up=True)
 if not f: raise RuntimeError('sheets field not found')
 x=round(f['pos'][0]+f['size'][0]-8); y=round(f['pos'][1]+f['size'][1]/2); click_xy(x,y); time.sleep(.3)
 shot(udid,os.path.join(cdir,'000-zero-focused.jpg'))
 rec={'device':outsub,'case':'case5-sheets','precondition':sheets_field(W).get('value') if sheets_field(W) else None,'keys':[]}
 kp=keypad_all(W)
 for i,k in enumerate('42',1):
  x,y=kp[k]; click_xy(x,y); time.sleep(.13); fn=os.path.join(cdir,f'key-{i}-{k}.jpg'); shot(udid,fn); rec['keys'].append({'key':k,'shown':sheets_field(W).get('value') if sheets_field(W) else None,'screenshot':fn})
 try: simutil.click_id(W,'fp-part-0-toggle',.5)
 except Exception: click_xy(250,500)
 time.sleep(.6); shot(udid,os.path.join(cdir,'010-after-leaving.jpg')); rec['saved_after_leaving']=sheets(db)
 open_filings(W); open_form(W,'2551Q')
 for _ in range(5):
  if sheets_field(W): break
  drag_scroll(W,up=True)
 rec['shown_after_reopening']=sheets_field(W).get('value') if sheets_field(W) else None; rec['saved_after_reopening']=sheets(db)
 shot(udid,os.path.join(cdir,'020-after-reopening.jpg'))
 logjson(os.path.join(ROOT,'observations.jsonl'),rec); return rec
if __name__=='__main__': print(json.dumps(run(sys.argv[1],sys.argv[2],sys.argv[3]),indent=1))
