#!/usr/bin/env python3
import sys,os,time,json,subprocess
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
from case1 import open_filings,open_form,update_2551q,keypad_all,wait_field
from navrows import open_row_controlled

def keyseq(W,seq):
 out=[]
 for c in seq:
  kp=keypad_all(W); x,y=kp[c]; click_xy(x,y); time.sleep(.13)
  fs=simutil.find(W,role='AXTextField'); out.append({'key':c,'shown':fs[0].get('value') if fs else None})
 return out

def home5(W,udid):
 subprocess.run(['cliclick','kd:cmd,shift','t:h','ku:cmd,shift'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 time.sleep(5)
 # Prefer tapping the real visible NshDev icon when AX exposes it; fall back to simctl launch foregrounding the existing app.
 ns=simutil.find(W,text='NshDev')
 if ns: click_node(ns[0],1.2)
 else:
  subprocess.run(['xcrun','simctl','launch',udid,'com.longbridge.nsh.host'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  time.sleep(1.5)

def run(W,udid,db):
 outsub='iphone' if W==IPHONE else 'ipad'; cdir=os.path.join(ROOT,outsub,'case4','home-resume'); os.makedirs(cdir,exist_ok=True)
 open_filings(W); update_2551q(db,0.0); open_form(W,'2551Q'); open_row_controlled(W); focus_amount_end(W); time.sleep(.25)
 rec={'device':outsub,'case':'case4-home-resume','before':wait_field(W).get('value')}
 rec['keys_before_home']=keyseq(W,'123'); shot(udid,cdir+'/000-before-home.jpg')
 home5(W,udid); time.sleep(1); shot(udid,cdir+'/010-after-return-before-4.jpg')
 fs=simutil.find(W,role='AXTextField'); rec['shown_after_return']=fs[0].get('value') if fs else None
 rec['keys_after_return']=keyseq(W,'4'); shot(udid,cdir+'/020-after-4.jpg')
 press_done(W); time.sleep(.7); rec['saved_after_leaving']=draft_money(db); shot(udid,cdir+'/030-after-leaving.jpg')
 open_filings(W); open_form(W,'2551Q'); open_row_controlled(W); rec['shown_after_reopening']=wait_field(W).get('value'); rec['saved_after_reopening']=draft_money(db); shot(udid,cdir+'/040-after-reopen.jpg')
 logjson(os.path.join(ROOT,'observations.jsonl'),rec); return rec
if __name__=='__main__': print(json.dumps(run(sys.argv[1],sys.argv[2],sys.argv[3]),indent=1))
