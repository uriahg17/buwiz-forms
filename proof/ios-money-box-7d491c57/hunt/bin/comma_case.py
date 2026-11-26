#!/usr/bin/env python3
# One regional comma input case. Real keypad clicks for every tested key.
import sys,os,time,json
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
from case1 import open_filings,open_form,update_2551q,keypad_all,wait_field
from comma_sentence import clear_real
from navrows import open_row_controlled

def statics(W):
 return [n.get('desc') or n.get('title') or n.get('value') or '' for n in simutil.nodes(W) if n.get('role')=='AXStaticText']
def run(W,udid,db,name,seq):
 outsub='iphone' if W==IPHONE else 'ipad'; cdir=os.path.join(ROOT,outsub,'case3',name); os.makedirs(cdir,exist_ok=True)
 open_filings(W); update_2551q(db,1000.0); open_form(W,'2551Q'); open_row_controlled(W); focus_amount_end(W); time.sleep(.3)
 clear_real(W); time.sleep(.2); shot(udid,cdir+'/000-held-cleared.jpg')
 rec={'device':outsub,'case':'case3-'+name,'sequence':seq,'keys':[]}
 for i,c in enumerate(seq,1):
  kp=keypad_all(W)
  if c not in kp: raise RuntimeError('missing '+c+' keys '+repr(kp))
  x,y=kp[c]; click_xy(x,y); time.sleep(.14)
  fn=cdir+f'/key-{i}-{c.replace(",","comma").replace(".","dot")}.jpg'; shot(udid,fn)
  fs=simutil.find(W,role='AXTextField'); rec['keys'].append({'key':c,'shown':fs[0].get('value') if fs else None,'shot':fn})
 press_done(W); time.sleep(.7); shot(udid,cdir+'/010-after-done.jpg'); rec['saved_after_done']=draft_money(db)
 # Reopen the row in the same form session; the note is expected under the restored amount.
 open_row_controlled(W); time.sleep(.3); shot(udid,cdir+'/020-row-reopened-same-session.jpg')
 texts=statics(W); fs=simutil.find(W,role='AXTextField')
 rec['shown_after_row_reopen']=fs[0].get('value') if fs else None; rec['texts']=texts; rec['sentence']=[t for t in texts if 'is not an amount' in t or 'you typed' in t]
 rec['saved_after_row_reopen']=draft_money(db)
 logjson(os.path.join(ROOT,'observations.jsonl'),rec); return rec
if __name__=='__main__': print(json.dumps(run(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5]),indent=1)[:4000])
