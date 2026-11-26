import sys,os,time,json,subprocess
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
from case1 import open_filings,open_form,update_2551q,keypad_all,wait_field
from navrows import open_row_controlled
from case6 import setrows

def cent(n): return (round(n['pos'][0]+n['size'][0]/2),round(n['pos'][1]+n['size'][1]/2))
def nodeid(ns,id): return next((n for n in ns if n.get('id')==id),None)
def home5(udid):
 subprocess.run(['cliclick','kd:cmd,shift','t:h','ku:cmd,shift'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(5)
 subprocess.run(['xcrun','simctl','launch',udid,'com.longbridge.nsh.host'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1.2)
def run(W,udid,db):
 cdir=os.path.join(ROOT,'ipad','case4','home-resume'); os.makedirs(cdir,exist_ok=True)
 open_filings(W); setrows(db,[(0.0,"PT010")]); open_form(W,'2551Q'); open_row_controlled(W)
 ns=simutil.nodes(W); f=next(n for n in ns if n.get('role')=='AXTextField'); done_xy=cent(nodeid(ns,'fp-table-drpATC1-done'))
 click_xy(round(f['pos'][0]+f['size'][0]-12),round(f['pos'][1]+f['size'][1]/2)); time.sleep(.3); kp=keypad_all(W)
 rec={'device':'ipad','case':'case4-home-resume','before':f.get('value'),'keypad':sorted(kp)}
 for c in '123': click_xy(*kp[c]); time.sleep(.16)
 shot(udid,cdir+'/000-before-home.jpg'); home5(udid); shot(udid,cdir+'/010-after-return-before-4.jpg')
 kp2=keypad_all(W) or kp
 click_xy(*kp2['4']); time.sleep(.3); shot(udid,cdir+'/020-after-4.jpg')
 click_xy(*done_xy); time.sleep(.5); rec['saved_after_leaving']=draft_money(db); shot(udid,cdir+'/030-after-leaving.jpg')
 open_filings(W); open_form(W,'2551Q'); open_row_controlled(W); rec['shown_after_reopening']=wait_field(W).get('value'); rec['saved_after_reopening']=draft_money(db); shot(udid,cdir+'/040-after-reopen.jpg')
 logjson(os.path.join(ROOT,'observations.jsonl'),rec); return rec
if __name__=='__main__': print(json.dumps(run(sys.argv[1],sys.argv[2],sys.argv[3]),indent=1))
