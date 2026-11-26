#!/usr/bin/env python3
import sys,os,time,json
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
from case1 import open_filings,open_form,update_2551q,keypad_all,wait_field
from navrows import open_row_controlled

def run(W,udid,db):
 outsub='iphone' if W==IPHONE else 'ipad'; cdir=os.path.join(ROOT,outsub,'case2'); os.makedirs(cdir,exist_ok=True)
 open_filings(W); update_2551q(db,1234.56); open_form(W,'2551Q'); open_row_controlled(W)
 shot(udid,cdir+'/000-filled-unfocused.jpg')
 f=wait_field(W); rec={'device':outsub,'case':'case2-caret-digit-delete','initial':f.get('value')}
 # tap in the visible digits, slightly left of center of the right-aligned amount; not at the field end
 x=round(f['pos'][0]+f['size'][0]-58); y=round(f['pos'][1]+f['size'][1]/2)
 click_xy(x,y); time.sleep(.35); shot(udid,cdir+'/001-after-tap-filled.jpg')
 rec['tap']={'x':x,'y':y,'field':f['pos']+f['size'],'shown_after_tap':wait_field(W).get('value')}
 kp=keypad_all(W)
 for name,k in [('digit','7'),('delete','Delete')]:
  x,y=kp[k]; click_xy(x,y); time.sleep(.22); fn=cdir+('/002-after-digit.jpg' if name=='digit' else '/003-after-delete.jpg'); shot(udid,fn)
  rec[name]={'key':k,'shown':wait_field(W).get('value'),'shot':fn}
 press_done(W); time.sleep(.7); shot(udid,cdir+'/010-after-leaving.jpg'); rec['saved_after_leaving']=draft_money(db)
 open_filings(W); open_form(W,'2551Q'); open_row_controlled(W); shot(udid,cdir+'/020-after-reopen.jpg')
 rec['shown_after_reopening']=wait_field(W).get('value'); rec['saved_after_reopening']=draft_money(db)
 rec['saved_equals_shown']=rec['saved_after_leaving']['taxable_amount']==float((rec['delete']['shown'] or '0').replace(',',''))
 logjson(os.path.join(ROOT,'observations.jsonl'),rec); return rec
if __name__=='__main__': print(json.dumps(run(sys.argv[1],sys.argv[2],sys.argv[3]),indent=1))
