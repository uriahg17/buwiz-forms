#!/usr/bin/env python3
import sys,os,time,json
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
WIN=IPAD; UDID=IPAD_UDID
DB='/Users/devin/Library/Developer/CoreSimulator/Devices/41A2AFE3-9E35-4EE8-BEF0-21AA02B68BC3/data/Containers/Data/Application/AFAFDA8B-1B88-41B0-8CAB-5B3E0D597490/tmp/ebirforms-door/64572-0/bir_data.db'
cdir=os.path.join(ROOT,'ipad','h6'); os.makedirs(cdir,exist_ok=True)
def kp():
 out={}
 for n in simutil.find(WIN,role='AXButton'):
  d=n.get('desc') or ''
  if d in list('1234567890.'): out[d]=center(n)
  elif d.lower()=='delete': out['Delete']=center(n)
 return out
def sheets_field():
 fs=simutil.find(WIN,role='AXTextField')
 # Return details has month first and sheets second; sheets is the lower numeric text field.
 if len(fs)<2: raise RuntimeError('need return-details fields '+repr(fs))
 return sorted(fs,key=lambda n:n['pos'][1])[-1]
def sheets_value(): return sheets_field().get('value')
def reopen():
 simutil.click_id(WIN,'tb-back',.6); simutil.click_id(WIN,'nav-filings',.6)
 rs=simutil.find(WIN,idpart='return-1'); click_node(rs[0],1.0)
# go back and reopen fresh at top
try: reopen()
except Exception as e: print('reopen setup issue',e)
f=sheets_field(); x=round(f['pos'][0]+f['size'][0]-8); y=round(f['pos'][1]+f['size'][1]/2)
click_xy(x,y); time.sleep(.4)
shot(UDID,os.path.join(cdir,'000-focused-before-clear.png'))
keys=kp()
if 'Delete' in keys:
 dx,dy=keys['Delete']
 for _ in range(5): click_xy(dx,dy); time.sleep(.07)
time.sleep(.2)
shot(UDID,os.path.join(cdir,'001-zero-or-empty-before-keys.png'))
rec={'device':'ipad','case':'h6','form_box':'2551Q Return details item 5 Number of Sheet/s','sequence':'42 into count box after clearing existing 4','before_clear':f.get('value'),'after_clear':sheets_value(),'keys':[]}
keys=kp()
for i,c in enumerate('42',1):
 x,y=keys[c]; click_xy(x,y); time.sleep(.2)
 fn=os.path.join(cdir,f'key-{i:02d}-{c}.png'); shot(UDID,fn)
 rec['keys'].append({'key':c,'shown':sheets_value(),'screenshot':fn})
# leave field by tapping neutral section header, then reopen
simutil.click_id(WIN,'fp-part-0-toggle',.6)
shot(UDID,os.path.join(cdir,'020-after-leaving-field.png'))
time.sleep(.5)
saved0=None
for r in sqlite_values(DB):
 if r['form_code']=='2551Q': saved0=r['data'].get('number_of_attached_sheets')
reopen(); time.sleep(.3)
shot(UDID,os.path.join(cdir,'030-after-reopening-return.png'))
try: shownreopen=sheets_value()
except Exception: shownreopen=None
saved=None
for r in sqlite_values(DB):
 if r['form_code']=='2551Q': saved=r['data'].get('number_of_attached_sheets')
rec.update({'saved_after_leaving':saved0,'shown_after_reopening':shownreopen,'saved_after_reopening':saved})
logjson(os.path.join(ROOT,'observations.jsonl'),rec)
print(json.dumps(rec,indent=2))
