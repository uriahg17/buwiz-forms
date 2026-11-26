#!/usr/bin/env python3
# German comma unreadable-amount sentence proof. Digit input is real keypad clicks only.
import sys,os,time,json,sqlite3,subprocess
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
from case1 import open_filings,open_form,update_2551q,keypad_all,wait_field
from case3 import locale,launch,software_keyboard

def open_row_fast(W):
 for _ in range(20):
  if simutil.find(W,idpart='fp-table-drpATC1-done'): return
  rows=simutil.find(W,idpart='fp-row-drpATC1-0')
  if rows and rows[0].get("pos") and 150 < rows[0]["pos"][1] < (1030 if W==IPHONE else 1100):
   click_node(rows[0],.7)
   if simutil.find(W,idpart='fp-table-drpATC1-done'): return
   continue
  tog=simutil.find(W,idpart='fp-part-4-toggle')
  if tog and tog[0].get("pos") and 150 < tog[0]["pos"][1] < (1030 if W==IPHONE else 1100): click_node(tog[0],.5)
  else: drag_scroll(W,up=True)
 raise RuntimeError('row not open')

def clear_real(W):
 kp=keypad_all(W)
 if 'Delete' not in kp: return
 x,y=kp['Delete']
 for _ in range(10): click_xy(x,y); time.sleep(.05)

def run(W,udid,db):
 outsub='iphone' if W==IPHONE else 'ipad'; cdir=os.path.join(ROOT,outsub,'case3','comma-sentence'); os.makedirs(cdir,exist_ok=True)
 locale(udid,'de_DE','de'); launch(udid,db)
 open_filings(W); update_2551q(db,1000.0); open_form(W,'2551Q'); open_row_fast(W)
 focus_amount_end(W); time.sleep(.3)
 if not keypad_all(W):
  click_xy(250,100); time.sleep(.2); software_keyboard(); focus_amount_end(W); time.sleep(.2)
 clear_real(W); time.sleep(.2)
 shot(udid,cdir+'/000-held-zero.jpg')
 rec={'device':outsub,'case':'case3-comma-sentence','keys':[]}
 # initial held amount is zero; clear is unnecessary, type real regional keypad keys
 for i,c in enumerate('1500,50',1):
  kp=keypad_all(W)
  if c not in kp: raise RuntimeError('missing '+c+' '+repr(kp))
  x,y=kp[c]; click_xy(x,y); time.sleep(.14)
  fn=cdir+f'/key-{i}-{c.replace(",","comma")}.jpg'; shot(udid,fn)
  fs=simutil.find(W,role='AXTextField'); rec['keys'].append({'key':c,'shown':fs[0].get('value') if fs else None,'shot':fn})
 # blur within the row sheet by opening the ATC picker; this is navigation/focus, not digit input
 tr=simutil.find(W,idpart='fp-drpATC1-trigger')
 if tr: click_node(tr[0],.6)
 time.sleep(.8); shot(udid,cdir+'/010-after-blur-picker.jpg')
 # dismiss picker without editing if open; Escape is a navigation key, then capture row sheet note
 subprocess.run(['cliclick','kp:esc'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.5)
 shot(udid,cdir+'/020-note-visible.jpg')
 texts=[]
 for n in simutil.nodes(W):
  if n.get('role')=='AXStaticText': texts.append(n.get('desc') or n.get('title') or n.get('value') or '')
 fs=simutil.find(W,role='AXTextField')
 rec['shown_after_blur']=fs[0].get('value') if fs else None
 rec['texts_after_blur']=texts
 rec['sentence']=[t for t in texts if 'is not an amount' in t]
 rec['saved_immediately_after_blur']=draft_money(db)
 press_done(W); time.sleep(.7); shot(udid,cdir+'/030-after-done.jpg'); rec['saved_after_done']=draft_money(db)
 # reopen return/row and see whether note survives a new session view
 open_filings(W); open_form(W,'2551Q'); open_row_fast(W); shot(udid,cdir+'/040-after-reopen.jpg')
 texts=[]
 for n in simutil.nodes(W):
  if n.get('role')=='AXStaticText': texts.append(n.get('desc') or n.get('title') or n.get('value') or '')
 rec['texts_after_reopen']=texts; rec['saved_after_reopen']=draft_money(db)
 logjson(os.path.join(ROOT,'observations.jsonl'),rec)
 locale(udid,'en_PH','en'); launch(udid,db)
 return rec
if __name__=='__main__': print(json.dumps(run(sys.argv[1],sys.argv[2],sys.argv[3]),indent=1)[:5000])
