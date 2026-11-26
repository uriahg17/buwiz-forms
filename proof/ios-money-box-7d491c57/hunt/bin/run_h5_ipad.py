#!/usr/bin/env python3
import sys,os,time,json
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
import run_h1h2_ipad as base
WIN=base.WIN; UDID=base.UDID; DB=base.DB
cdir=os.path.join(ROOT,'ipad','h5'); os.makedirs(cdir,exist_ok=True)
def kp(): return base.ipad_keypad()
def val(): return amount_field(WIN).get('value')
def key_tap(c):
 x,y=kp()[c]; click_xy(x,y); time.sleep(.18)
base.open_row_sheet(); base.clear_ipad_amount()
shot(UDID,os.path.join(cdir,'000-empty-after-real-delete.jpg'))
rec={'device':'ipad','case':'h5','keys_before_home':[],'keys_after_return':[]}
for i,k in enumerate('123',1):
 key_tap(k); fn=os.path.join(cdir,f'key-{i:02d}-{k}-before-home.jpg'); shot(UDID,fn)
 rec['keys_before_home'].append({'key':k,'shown':val(),'screenshot':fn})
prehome=val()
home=[x for x in simutil.find(WIN,text='Home',role='AXButton') if x.get('pos') and x['pos'][1]<100][0]
click_node(home,0); time.sleep(5)
shot(UDID,os.path.join(cdir,'010-home-after-5s.jpg'))
app=simutil.find(WIN,text='NshDev',role='AXButton')[0]
click_node(app,1.2)
shot(UDID,os.path.join(cdir,'011-after-return-before-4.jpg'))
afterreturn=val()
key_tap('4'); fn=os.path.join(cdir,'key-04-4-after-return.jpg'); shot(UDID,fn)
after4=val()
simutil.click_id(WIN,'fp-table-drpATC1-done',.7)
shot(UDID,os.path.join(cdir,'020-after-leaving.jpg'))
saved=draft_money(DB)
base.reopen_return(); base.open_row_sheet(); shot(UDID,os.path.join(cdir,'030-after-reopening-row.jpg'))
reopenv=val(); savedafter=draft_money(DB)
rec.update({'shown_before_home':prehome,'shown_after_return_before_4':afterreturn,'shown_after_4':after4,'saved_after_leaving':saved,'shown_after_reopening':reopenv,'saved_after_reopening':savedafter})
logjson(os.path.join(ROOT,'observations.jsonl'),rec)
print(json.dumps(rec,indent=2))
