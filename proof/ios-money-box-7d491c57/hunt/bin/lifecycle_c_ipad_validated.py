import sys,os,time,json,traceback
sys.path.insert(0,'/Users/devin/moneybox-7d491c57/proof/ios-money-box-7d491c57/hunt/bin')
from lifelib import *
from case1 import open_filings,open_form,keypad_all,wait_field
from huntlib import ensure_row_sheet
from case3 import launch
OUT='/Users/devin/moneybox-7d491c57/proof/ios-money-box-7d491c57/lifecycle-c-ipad'
os.makedirs(OUT,exist_ok=True)
W=IPAD;udid='41A2AFE3-9E35-4EE8-BEF0-21AA02B68BC3';db='/tmp/money7d-ipad.db'
def log(x):
 with open(OUT+'/observations.jsonl','a') as f:f.write(json.dumps(x,sort_keys=True)+'\n')
def ctr(n):return (round(n['pos'][0]+n['size'][0]/2),round(n['pos'][1]+n['size'][1]/2))
def done_node():return (simutil.find(W,idpart='fp-table-drpATC1-done') or [None])[0]
def finish_done(done_xy):
 # The first press while the floating pad is up can merely dismiss the pad. Press again only when the sheet is still present.
 click_xy(*done_xy);time.sleep(.65)
 for _ in range(2):
  d=done_node()
  if not d:break
  click_xy(*ctr(d));time.sleep(.55)
def one(pos):
 r={'case':'lifecycle-c-validated','device':'ipad','position':pos}
 try:
  launch(udid,db);time.sleep(1.5);set_hardware(W,False)
  open_filings(W);time.sleep(.2);set_amount(db,1234.56);open_form(W,'2551Q');ensure_row_sheet(W)
  f=wait_field(W,2);d=done_node();done_xy=ctr(d) if d else (1101,1037)
  x0,y0=f['pos'];wid,hei=f['size']
  if pos=='left':tx=round(x0+8)
  elif pos=='middle':tx=round(x0+wid/2)
  else:tx=round(x0+wid-8)
  ty=round(y0+hei/2);r['tap']={'x':tx,'y':ty,'field_pos':f['pos'],'field_size':f['size'],'prefill':f.get('value')}
  click_xy(tx,ty);time.sleep(1.0)
  kp=keypad_all(W);r['keypad_keys']=sorted(kp);shot(udid,OUT+f'/{pos}-before-8.jpg')
  if '8' not in kp:raise RuntimeError('8 missing '+repr(kp))
  click_xy(*kp['8']);time.sleep(.55);shot(udid,OUT+f'/{pos}-after-8.jpg')
  # leave via Done; conditional second press only if the first merely dismissed the keyboard
  finish_done(done_xy);time.sleep(.25);shot(udid,OUT+f'/{pos}-after-leaving.jpg')
  r['saved_after_leaving']=amount_val(db)
  open_filings(W);time.sleep(.25);open_form(W,'2551Q');ensure_row_sheet(W);time.sleep(.25)
  fs=simutil.find(W,role='AXTextField');r['shown_after_reopen']=fs[0].get('value') if fs else None
  shot(udid,OUT+f'/{pos}-after-reopen.jpg');r['saved_after_reopen']=amount_val(db)
 except Exception as e:
  r['exception']=repr(e);r['trace']=traceback.format_exc()[-1200:]
  try:shot(udid,OUT+f'/{pos}-exception.jpg')
  except Exception:pass
 log(r);print(json.dumps(r));return r
def run():
 out=[]
 for p in ('left','middle','right'):out.append(one(p))
 print('SUMMARY',json.dumps(out))
if __name__=='__main__':run()
