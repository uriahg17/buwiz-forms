import sys,os,time,json,traceback
sys.path.insert(0,'/Users/devin/moneybox-542e4844/helpers/bin')
import simutil
from huntlib import *
from case1 import open_filings,open_form,update_2551q,keypad_all,wait_field
from case3 import launch,locale
from comma_sentence import clear_real
from navrows import open_row_controlled
ROOT='/Users/devin/moneybox-542e4844/proof/ios-money-box-542e4844/german-comma'
def activate_done(W,blurxy=None):
 # Blur through inert Tax Rate, then use fresh visible Done geometry only.
 if blurxy:
  for _ in range(5):
   if not keypad_all(W): break
   live=next((n for n in simutil.nodes(W) if n.get('id')=='fp-txtATCRate1'),None)
   xy=(round(live['pos'][0]+24),round(live['pos'][1]+live['size'][1]/2)) if live and live.get('pos') else blurxy
   click_xy(*xy);time.sleep(.45)
 for _ in range(8):
  kp=keypad_all(W);dn=simutil.find(W,idpart='fp-table-drpATC1-done')
  if dn and (not kp or dn[0]['pos'][1]+dn[0]['size'][1] < min(y for x,y in kp.values())-5):
   fs=simutil.find(W,role='AXTextField');afterblur=fs[0].get('value') if fs else None
   click_node(dn[0],.6);return {'activated':True,'after_blur':afterblur}
  time.sleep(.3)
 return {'activated':False,'after_blur':None}

def run(W,udid,db):
 sub='iphone' if W==IPHONE else 'ipad';cdir=os.path.join(ROOT,sub);os.makedirs(cdir,exist_ok=True)
 rec={'device':sub,'case':'german-comma'}
 try:
  locale(udid,'de_DE','de');launch(udid,db);time.sleep(1.5)
  open_filings(W);update_2551q(db,1000.0);open_form(W,'2551Q');open_row_controlled(W);wait_field(W,2);rate=next((n for n in simutil.nodes(W) if n.get('id')=='fp-txtATCRate1'),None);ratexy=(round(rate['pos'][0]+24),round(rate['pos'][1]+rate['size'][1]/2)) if rate else None
  ff=wait_field(W,2);click_xy(round(ff['pos'][0]+ff['size'][0]-12),round(ff['pos'][1]+ff['size'][1]/2));time.sleep(.8)
  clear_real(W);shot(udid,cdir+'/000-cleared.jpg')
  vals=[]
  for c in '1500,50':
   kp=keypad_all(W)
   if c not in kp:raise RuntimeError('missing key '+c+' have '+repr(sorted(kp)))
   click_xy(*kp[c]);time.sleep(.18);fs=simutil.find(W,role='AXTextField');vals.append((c,fs[0].get('value') if fs else None))
  rec['values_after_keys']=vals;fs=simutil.find(W,role='AXTextField');rec['shown_after_typing']=fs[0].get('value') if fs else None;shot(udid,cdir+'/001-after-typing.jpg')
  doneinfo=activate_done(W,ratexy);rec['done_activated']=doneinfo['activated'];rec['shown_after_blur']=doneinfo['after_blur'];time.sleep(.7);shot(udid,cdir+'/002-after-done.jpg')
  rec['saved_after_done']=draft_money(db)
  open_filings(W);open_form(W,'2551Q');open_row_controlled(W);rec['shown_after_reopen']=wait_field(W).get('value');rec['saved_after_reopen']=draft_money(db);shot(udid,cdir+'/003-after-reopen.jpg')
  rec['pass']=rec['saved_after_reopen'] and abs(rec['saved_after_reopen'].get('taxable_amount')-1500.5)<.005
 except Exception as e:
  rec['exception']=repr(e);rec['trace']=traceback.format_exc()[-1200:]
  try:shot(udid,cdir+'/099-exception.jpg')
  except Exception:pass
 open(cdir+'/result.json','w').write(json.dumps(rec,indent=1));print(json.dumps(rec))
if __name__=='__main__':run(IPHONE if sys.argv[1]=='iphone' else IPAD,IPHONE_UDID if sys.argv[1]=='iphone' else IPAD_UDID,'/tmp/money542-iphone.db' if sys.argv[1]=='iphone' else '/tmp/money542-ipad.db')
