import sys,os,time,json
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
from case1 import open_filings,open_form,update_2551q,keypad_all,wait_field
from navrows import open_row_controlled

def cent(n): return (round(n['pos'][0]+n['size'][0]/2),round(n['pos'][1]+n['size'][1]/2))
def nodeid(ns,id): return next((n for n in ns if n.get('id')==id),None)
def run(W,udid,db):
 cdir=os.path.join(ROOT,'ipad','case2'); os.makedirs(cdir,exist_ok=True)
 open_filings(W); update_2551q(db,1234.56); open_form(W,'2551Q'); open_row_controlled(W)
 shot(udid,cdir+'/000-filled-unfocused.jpg')
 ns=simutil.nodes(W); f=next(n for n in ns if n.get('role')=='AXTextField'); dn=nodeid(ns,'fp-table-drpATC1-done'); done_xy=cent(dn)
 rec={'device':'ipad','case':'case2-caret-digit-delete','initial':f.get('value')}
 x=round(f['pos'][0]+f['size'][0]-58); y=round(f['pos'][1]+f['size'][1]/2); click_xy(x,y); time.sleep(.35); shot(udid,cdir+'/001-after-tap-filled.jpg')
 kp=keypad_all(W); rec['keypad']=sorted(kp)
 for name,k,fn in [('digit','7','002-after-digit.jpg'),('delete','Delete','003-after-delete.jpg')]:
  click_xy(*kp[k]); time.sleep(.35); shot(udid,cdir+'/'+fn); rec[name]={'key':k,'shot':cdir+'/'+fn,'shown':None}
 click_xy(*done_xy); time.sleep(.5); shot(udid,cdir+'/010-after-leaving.jpg'); rec['saved_after_leaving']=draft_money(db)
 open_filings(W); open_form(W,'2551Q'); open_row_controlled(W); shot(udid,cdir+'/020-after-reopen.jpg')
 rec['shown_after_reopening']=wait_field(W).get('value'); rec['saved_after_reopening']=draft_money(db)
 logjson(os.path.join(ROOT,'observations.jsonl'),rec); return rec
if __name__=='__main__': print(json.dumps(run(sys.argv[1],sys.argv[2],sys.argv[3]),indent=1))
