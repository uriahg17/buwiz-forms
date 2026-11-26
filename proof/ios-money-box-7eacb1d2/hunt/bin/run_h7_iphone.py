#!/usr/bin/env python3
import sys,os,time,json
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
WIN=IPHONE; UDID=IPHONE_UDID
DB='/Users/devin/Library/Developer/CoreSimulator/Devices/405F45A9-B471-47B7-A5D9-E545EA624713/data/Containers/Data/Application/0973CEBB-8D01-4458-8873-616214E0F25C/tmp/ebirforms-door/66407-0/bir_data.db'
cdir=os.path.join(ROOT,'iphone','h7'); os.makedirs(cdir,exist_ok=True)
# open copied 2551Q draft, row sheet, clear by real delete
simutil.click_id(WIN,'tab-filings',.6)
rs=simutil.find(WIN,idpart='return-1')
if rs: click_node(rs[0],1.0)
ensure_row_sheet(WIN)
focus_amount_end(WIN); kp=keypad(WIN)
if 'Delete' in kp:
 x,y=kp['Delete']
 for _ in range(14): click_xy(x,y); time.sleep(.055)
time.sleep(.2)
shot(UDID,os.path.join(cdir,'000-empty-and-pad.png'))
labels=[]
for n in simutil.find(WIN,role='AXButton'):
 d=n.get('desc') or ''
 if n.get('pos') and n['pos'][1]>650: labels.append(d)
minuskeys=[d for d in labels if d in ('-','−','minus')]
rec={'device':'iphone','case':'h7','empty_before':amount_field(WIN).get('value'),'keyboard_labels':labels,'minus_on_pad':bool(minuskeys),'method':'inspected software decimal pad; no hardware-key fallback required by case brief'}
if minuskeys:
 kp2=keypad(WIN)
 # no normal path here; keypad() does not map minus, click by label
 xs=[n for n in simutil.find(WIN,role='AXButton') if (n.get('desc') or '') in ('-','−','minus')]
 click_node(xs[0],.2); shot(UDID,os.path.join(cdir,'key-01-minus.png'))
 rec['shown_after_minus']=amount_field(WIN).get('value')
 press_done(WIN); time.sleep(.5); shot(UDID,os.path.join(cdir,'020-after-leaving.png'))
 rec['saved_after_leaving']=draft_money(DB)
else:
 rec['result']='no minus key available on iPhone software decimal pad; negative cannot be typed through pad'
logjson(os.path.join(ROOT,'observations.jsonl'),rec)
print(json.dumps(rec,indent=2))
