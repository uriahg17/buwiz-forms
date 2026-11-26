#!/usr/bin/env python3
import sys,os,time,json,sqlite3
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
WIN=IPHONE; UDID=IPHONE_UDID
DB='/Users/devin/Library/Developer/CoreSimulator/Devices/405F45A9-B471-47B7-A5D9-E545EA624713/data/Containers/Data/Application/0973CEBB-8D01-4458-8873-616214E0F25C/tmp/ebirforms-door/60325-0/bir_data.db'
cdir=os.path.join(ROOT,'iphone','h6'); os.makedirs(cdir,exist_ok=True)
LOG=os.path.join(ROOT,'observations.jsonl')
rec={'device':'iphone','case':'h6','form_box':'2551Q Return details item 5 Number of Sheet/s','sequence':'42 into count box holding 0','keys':[]}
def sheets_field():
 fs=simutil.find(WIN,role='AXTextField')
 return fs[-1] if fs else None
def sheets_value():
 f=sheets_field(); return f.get('value') if f else None
def sheets_saved():
 con=sqlite3.connect('file:'+DB+'?mode=ro',uri=True)
 row=con.execute("select data_json from form_drafts where form_code='2551Q'").fetchone(); con.close()
 return json.loads(row[0]).get('number_of_attached_sheets') if row else None
shot(UDID,os.path.join(cdir,'000-zero-after-tap-before-keys.jpg'))
rec['shown_after_tap_before_keys']=sheets_value()
kp=keypad(WIN)
for i,k in enumerate('42',1):
 x,y=kp[k]; click_xy(x,y); time.sleep(.18)
 fn=os.path.join(cdir,f'key-{i:02d}-{k}.jpg'); shot(UDID,fn)
 rec['keys'].append({'key':k,'shown':sheets_value(),'screenshot':fn})
# leave by collapsing Return details, then expand it again to see the settled value in place
simutil.click_id(WIN,'fp-part-0-toggle',.6)
shot(UDID,os.path.join(cdir,'010-after-leaving-collapsed.jpg'))
rec['saved_after_leaving']=sheets_saved()
# reopen section within same return to capture settled display
simutil.click_id(WIN,'fp-part-0-toggle',.6)
shot(UDID,os.path.join(cdir,'011-after-leaving-section-reexpanded.jpg'))
rec['shown_after_leaving']=sheets_value()
# close/reopen the return in same process and inspect again
simutil.click_id(WIN,'nb-back',.5)
simutil.click_id(WIN,'tab-filings',.5)
rs=simutil.find(WIN,idpart='return-1'); click_node(rs[0],.9)
shot(UDID,os.path.join(cdir,'020-after-reopening-return.jpg'))
# open return details and scroll until sheets visible enough; capture regardless
try:
 simutil.click_id(WIN,'fp-part-0-toggle',.4)
except Exception: pass
# bring it into view if needed
for _ in range(3):
 fs=simutil.find(WIN,role='AXTextField')
 if len(fs)>=2 and fs[-1]['pos'][1]>300 and fs[-1]['pos'][1]<850: break
 drag_scroll(WIN,up=True)
shot(UDID,os.path.join(cdir,'021-after-reopening-sheets.jpg'))
fs=simutil.find(WIN,role='AXTextField')
rec['shown_after_reopening_field']=fs[-1].get('value') if fs else None
rec['saved_after_reopening']=sheets_saved()
logjson(LOG,rec)
print(json.dumps(rec,indent=2))
