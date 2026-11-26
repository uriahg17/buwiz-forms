import sys,os,time,json,traceback
sys.path.insert(0,'/Users/devin/moneybox-7d491c57/proof/ios-money-box-7d491c57/hunt/bin')
from lifelib import *
from case1 import open_filings,open_form,keypad_all,wait_field
from huntlib import ensure_row_sheet
from lifecycle_b_fast import fast_seq
from case3 import launch
OUT='/Users/devin/moneybox-642bfc78/proof/main-bisect-final2';os.makedirs(OUT,exist_ok=True)
W=IPAD;udid='41A2AFE3-9E35-4EE8-BEF0-21AA02B68BC3';db='/tmp/money642-ipad.db'
def log(x):
 with open(OUT+'/observations.jsonl','a') as f:f.write(json.dumps(x,sort_keys=True)+'\n')
def sheet_open():
 return bool(simutil.find(W,idpart='fp-table-drpATC1-done'))
def close_sheet_any():
 if not sheet_open(): return
 ds=simutil.find(W,idpart='fp-table-drpATC1-done')
 if ds: click_node(ds[0],.45)
 if sheet_open():
  cs=[n for n in simutil.find(W,text='Close',role='AXButton') if n.get('pos') and n['pos'][0]>900]
  if cs: click_node(cs[0],.45)
def to_filings():
 close_sheet_any(); open_filings(W); time.sleep(.2)
def sheet_controls():
 ns=simutil.nodes(W)
 done=next((n for n in ns if n.get('id')=='fp-table-drpATC1-done'),None)
 close=next((n for n in ns if n.get('role')=='AXButton' and (n.get('desc') or '')=='Close' and n.get('pos') and n['pos'][0]>900),None)
 return (center(done) if done else None),(center(close) if close else None)
def finish_sheet(done_xy,close_xy,kpmap=None):
 if done_xy: click_xy(*done_xy);time.sleep(.55)
 ns=simutil.nodes(W)
 keys=[n for n in ns if n.get('role')=='AXButton' and (n.get('desc') or '') in list('1234567890.')]
 bad=bool(keys) or bool(simutil.find(W,idpart='fp-table-drpATC1-done'))
 if bad and kpmap and kpmap.get('Delete'):
  # Malformed fast input can disable Done. Clear it with real keypad Delete taps so the sheet/editor returns to a clean zero state.
  for _ in range(15): click_xy(*kpmap['Delete']);time.sleep(.035)
  time.sleep(.2)
  if done_xy: click_xy(*done_xy);time.sleep(.45)
 elif bad and close_xy:
  click_xy(*close_xy);time.sleep(.5)
 return not bad
def calibrate():
 to_filings();set_amount(db,0.0);open_form(W,'2551Q');ensure_row_sheet(W)
 done_xy,close_xy=sheet_controls()
 f=wait_field(W,2);x=round(f['pos'][0]+f['size'][0]-12);y=round(f['pos'][1]+f['size'][1]/2);click_xy(x,y);time.sleep(.6)
 kp=keypad_all(W)
 if not all(c in kp for c in '1234.56'): raise RuntimeError('keypad calibration missing '+repr(kp))
 out={c:(round(kp[c][0]),round(kp[c][1])) for c in '1234.56'}
 if 'Delete' in kp: out['Delete']=(round(kp['Delete'][0]),round(kp['Delete'][1]))
 finish_sheet(done_xy,close_xy,out);time.sleep(.2)
 return out
def one(run,delay,timingrun,kpmap):
 r={'case':'main-bisect-first-digit','commit':'642bfc78221c0a87b318c7c3378c3f5b0b2c9359','device':'ipad','run':run,'timing_run':timingrun,'delay_target_ms':delay,'robust_version':1}
 try:
  to_filings();set_amount(db,0.0);open_form(W,'2551Q');ensure_row_sheet(W)
  done_xy,close_xy=sheet_controls()
  f=wait_field(W,2);fx=round(f['pos'][0]+f['size'][0]-12);fy=round(f['pos'][1]+f['size'][1]/2)
  seq=list('1234.56');ev=[(fx,fy,0),(kpmap['1'][0],kpmap['1'][1],delay-14)]
  for j,c in enumerate(seq[1:]):ev.append((kpmap[c][0],kpmap[c][1],500 if j==0 else 70))
  clicks,raw=fast_seq(ev)
  if len(clicks)>1:r['measured_gap_ms']=round((clicks[1]['before_us']-clicks[0]['before_us'])/1000,3)
  time.sleep(.35);shot(udid,OUT+f'/{run:03d}-{delay}ms-after-typing.jpg')
  fs=simutil.find(W,role='AXTextField');r['shown_after_typing']=fs[0].get('value') if fs else None
  # Leave through Done when valid; if malformed input disables Done, close the sheet with its cached X.
  r['done_left_sheet']=finish_sheet(done_xy,close_xy,kpmap)
  time.sleep(.2);r['saved_after_leaving']=amount_val(db)
  r['first_digit_lost']=(r['saved_after_leaving'] is not None and abs(r['saved_after_leaving']-1234.56)>.005)
  # Leave the form before the next direct-DB reset.
  open_filings(W);time.sleep(.2)
 except Exception as e:
  r['exception']=repr(e);r['trace']=traceback.format_exc()[-1200:]
  try:shot(udid,OUT+f'/{run:03d}-exception.jpg')
  except Exception:pass
 log(r);return r
def runmatrix():
 launch(udid,db);time.sleep(2);set_hardware(W,False)
 kpmap=calibrate();results=[];runno=0
 for delay in (120,200,400):
  made=0;attempt=0
  while made<10 and attempt<15:
   attempt+=1;runno+=1
   r=one(runno,delay,made+1,kpmap)
   # Automation exceptions do not count as one of the 10 product runs.
   if 'exception' not in r:made+=1
   results.append(r)
   if attempt>=15 and made<10:break
 counts={d:sum(1 for r in results if r.get('delay_target_ms')==d and 'exception' not in r and r.get('first_digit_lost')) for d in (120,200,400)}
 valid={d:sum(1 for r in results if r.get('delay_target_ms')==d and 'exception' not in r) for d in (120,200,400)}
 line=f"main 642bfc78 iPad: lost {counts[120]}/10 at 120, {counts[200]}/10 at 200, {counts[400]}/10 at 400 ms"
 summary={'case':'main-bisect-summary','counts':counts,'valid_counts':valid,'required_line':line,'results':results}
 log(summary);print(line);print(json.dumps({'counts':counts,'valid_counts':valid}))
if __name__=='__main__':runmatrix()
