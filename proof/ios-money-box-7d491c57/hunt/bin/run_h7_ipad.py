#!/usr/bin/env python3
import sys,os,time,json,subprocess
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
WIN=IPAD; UDID=IPAD_UDID
DB='/Users/devin/Library/Developer/CoreSimulator/Devices/41A2AFE3-9E35-4EE8-BEF0-21AA02B68BC3/data/Containers/Data/Application/AFAFDA8B-1B88-41B0-8CAB-5B3E0D597490/tmp/ebirforms-door/64572-0/bir_data.db'
cdir=os.path.join(ROOT,'ipad','h7'); os.makedirs(cdir,exist_ok=True)
# Assumes row sheet is open from H2. Clear via onscreen delete (setup), then use real hardware key events for '-' and '5'.
def kp():
 out={}
 for n in simutil.find(WIN,role='AXButton'):
  d=n.get('desc') or ''
  if d in list('1234567890.'): out[d]=center(n)
  elif d.lower()=='delete': out['Delete']=center(n)
 return out
focus_amount_end(WIN)
if 'Delete' in kp():
 x,y=kp()['Delete']
 for _ in range(14): click_xy(x,y); time.sleep(.05)
time.sleep(.25)
shot(UDID,os.path.join(cdir,'000-empty-after-real-delete.jpg'))
empty=amount_field(WIN).get('value')
subprocess.run(['cliclick','kp:num-minus'],check=True); time.sleep(.25)
shot(UDID,os.path.join(cdir,'key-01-hardware-minus.jpg'))
afterminus=amount_field(WIN).get('value')
subprocess.run(['cliclick','kp:num-5'],check=True); time.sleep(.25)
shot(UDID,os.path.join(cdir,'key-02-hardware-num5.jpg'))
after5=amount_field(WIN).get('value')
# settle and read saved
simutil.click_id(WIN,'fp-table-drpATC1-done',.7)
shot(UDID,os.path.join(cdir,'020-after-leaving.jpg'))
saved=draft_money(DB)
rec={'device':'ipad','case':'h7','method':'hardware num-minus and num-5 after real keypad clearing','empty_before':empty,'shown_after_minus':afterminus,'shown_after_5':after5,'saved_after_leaving':saved,'minus_on_software_pad': any((x.get('desc') or '') in ('-','minus') for x in simutil.find(WIN,role='AXButton'))}
logjson(os.path.join(ROOT,'observations.jsonl'),rec)
print(json.dumps(rec,indent=2))
