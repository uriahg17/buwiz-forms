#!/usr/bin/env python3
import sys,os,time,json,sqlite3
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
WIN=IPHONE; UDID=IPHONE_UDID
DB='/Users/devin/Library/Developer/CoreSimulator/Devices/405F45A9-B471-47B7-A5D9-E545EA624713/data/Containers/Data/Application/0973CEBB-8D01-4458-8873-616214E0F25C/tmp/ebirforms-door/66407-0/bir_data.db'
cdir=os.path.join(ROOT,'iphone','h6-repro'); os.makedirs(cdir,exist_ok=True)
def set_sheets_db(v):
 con=sqlite3.connect(DB); row=con.execute("select id,data_json from form_drafts where form_code='2551Q'").fetchone(); j=json.loads(row[1]); j['number_of_attached_sheets']=v; con.execute('update form_drafts set data_json=? where id=?',(json.dumps(j),row[0])); con.commit(); con.close()
def sheets_saved():
 con=sqlite3.connect('file:'+DB+'?mode=ro',uri=True); row=con.execute("select data_json from form_drafts where form_code='2551Q'").fetchone(); con.close(); return json.loads(row[0]).get('number_of_attached_sheets') if row else None
def sheets_field():
 fs=simutil.find(WIN,role='AXTextField')
 # lower of the return-details text fields; ignore any row-sheet field by y/form state heuristics
 return sorted(fs,key=lambda n:n['pos'][1])[-1] if fs else None
def val():
 f=sheets_field(); return f.get('value') if f else None
# close row sheet, leave return, force exact zero setup, reopen fresh
try: press_done(WIN)
except Exception: pass
try: simutil.click_id(WIN,'nb-back',.5)
except Exception: pass
set_sheets_db(0)
simutil.click_id(WIN,'tab-filings',.5)
rs=simutil.find(WIN,idpart='return-1'); click_node(rs[0],1.0)
# expand return details and scroll until second field visible
try: simutil.click_id(WIN,'fp-part-0-toggle',.5)
except Exception: pass
for _ in range(8):
 fs=simutil.find(WIN,role='AXTextField')
 if len(fs)>=2:
  f=sorted(fs,key=lambda n:n['pos'][1])[-1]
  if 350<f['pos'][1]<850: break
 drag_scroll(WIN,up=True)
f=sheets_field()
if not f: raise RuntimeError('sheets field not found')
x=round(f['pos'][0]+f['size'][0]-8); y=round(f['pos'][1]+f['size'][1]/2)
click_xy(x,y); time.sleep(.35)
shot(UDID,os.path.join(cdir,'000-zero-after-tap-before-keys.png'))
rec={'device':'iphone','case':'h6-repro','form_box':'2551Q Return details item 5 Number of Sheet/s','sequence':'42 into count box holding 0','shown_after_tap_before_keys':val(),'keys':[]}
kp=keypad(WIN)
for i,k in enumerate('42',1):
 x,y=kp[k]; click_xy(x,y); time.sleep(.12)
 fn=os.path.join(cdir,f'key-{i:02d}-{k}.png'); shot(UDID,fn)
 rec['keys'].append({'key':k,'shown':val(),'screenshot':fn})
# leave by tapping Return details header, save, reopen return
simutil.click_id(WIN,'fp-part-0-toggle',.6)
shot(UDID,os.path.join(cdir,'010-after-leaving.png'))
time.sleep(.5); rec['saved_after_leaving']=sheets_saved()
simutil.click_id(WIN,'nb-back',.5); simutil.click_id(WIN,'tab-filings',.5)
rs=simutil.find(WIN,idpart='return-1'); click_node(rs[0],1.0)
shot(UDID,os.path.join(cdir,'020-after-reopening-return.png'))
rec['saved_after_reopening']=sheets_saved()
# try reading visible field after expanding again
try:
 simutil.click_id(WIN,'fp-part-0-toggle',.4)
except Exception: pass
for _ in range(5):
 fs=simutil.find(WIN,role='AXTextField')
 if len(fs)>=2: break
 drag_scroll(WIN,up=True)
rec['shown_after_reopening_field']=val()
shot(UDID,os.path.join(cdir,'021-after-reopening-sheets.png'))
logjson(os.path.join(ROOT,'observations.jsonl'),rec)
print(json.dumps(rec,indent=2))
