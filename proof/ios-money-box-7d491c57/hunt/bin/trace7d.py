import sys,os,time,json,subprocess,traceback
sys.path.insert(0,'/Users/devin/moneybox-7d491c57/proof/ios-money-box-7d491c57/hunt/bin')
from lifelib import *
from lifecycle_a_fast import setup_fast,open_sheet_fast,cent,nodeid,first_textfield
from lifecycle_b_fast import fast_seq
from case3 import launch
OUT='/Users/devin/moneybox-7d491c57/proof/ios-money-box-7d491c57/lifecycle/trace'
os.makedirs(OUT,exist_ok=True)
SERVERLOG='/Users/devin/moneybox-7d491c57/trace-run.log'
W=IPAD;udid='41A2AFE3-9E35-4EE8-BEF0-21AA02B68BC3';db='/tmp/money7d-ipad.db'
def log(x):
 with open(OUT+'/observations.jsonl','a') as f:f.write(json.dumps(x,sort_keys=True)+'\n')
def segment(path,start):
 try:
  with open(path,'rb') as f:
   f.seek(start); return f.read().decode('utf-8','replace')
 except Exception as e: return 'READ_ERROR '+repr(e)
def one(label,delay,nav,kpmap,done_xy):
 # Try until the requested class is observed, up to four openings. Save only the selected trace file.
 for attempt in range(1,5):
  r={'case':'masked-focus-trace','device':'ipad','label':label,'attempt':attempt,'target_gap_ms':delay}
  try:
   set_amount(db,0.0);ns,f=open_sheet_fast(W,nav)
   fx=round(f['pos'][0]+f['size'][0]-12);fy=round(f['pos'][1]+f['size'][1]/2)
   mark=os.path.getsize(SERVERLOG) if os.path.exists(SERVERLOG) else 0
   ev=[(fx,fy,0),(kpmap['1'][0],kpmap['1'][1],delay-14),(kpmap['2'][0],kpmap['2'][1],220)]
   clicks,raw=fast_seq(ev)
   if len(clicks)>1:r['measured_gap_ms']=round((clicks[1]['before_us']-clicks[0]['before_us'])/1000,3)
   if len(clicks)>2:r['second_digit_gap_ms']=round((clicks[2]['before_us']-clicks[1]['before_us'])/1000,3)
   time.sleep(.45)
   seg=segment(SERVERLOG,mark)
   shot(udid,OUT+f'/{label}-attempt{attempt}-after-second-digit.jpg')
   # Classify by the persisted result after Done. Keep the trace segment itself limited to focus-through-second-digit.
   click_xy(*done_xy);time.sleep(.45);saved=amount_val(db);r['saved_after_done']=saved
   # Two kept digits make 12; first digit lost leaves only 2.
   got='kept' if saved is not None and abs(saved-12)<.005 else 'lost' if saved is not None and abs(saved-2)<.005 else 'other'
   r['observed_class']=got
   r['fastclick_raw']=raw[-1000:]
   if got==label or (label=='lost' and got=='lost') or (label=='kept' and got=='kept'):
    open(OUT+f'/{label}.log','w').write(seg)
    r['trace_file']=OUT+f'/{label}.log';r['trace_line_count']=len([x for x in seg.splitlines() if 'MASKED_TRACE' in x])
    log(r);return r
   log({**r,'trace_file':None,'note':'class mismatch; retrying','segment_tail':seg[-1000:]})
   # Return to filings for next attempt.
   ns2=simutil.nodes(W);bk=nodeid(ns2,'nb-back') or nodeid(ns2,'tb-back')
   if bk:click_xy(*cent(bk));time.sleep(.35)
  except Exception as e:
   r['exception']=repr(e);r['trace']=traceback.format_exc()[-1200:];log(r)
   try: shot(udid,OUT+f'/{label}-attempt{attempt}-exception.jpg')
   except Exception: pass
   time.sleep(.5)
 return {'case':'masked-focus-trace','device':'ipad','label':label,'failed':'no matching run'}
def run():
 launch(udid,db);time.sleep(2)
 nav=setup_fast(W,db)
 set_amount(db,0.0);ns,f=open_sheet_fast(W,nav);done_xy=cent(nodeid(ns,'fp-table-drpATC1-done'))
 x=round(f['pos'][0]+f['size'][0]-12);y=round(f['pos'][1]+f['size'][1]/2);click_xy(x,y);time.sleep(.35)
 kp=keypad(W);kpmap={d:(round(kp[d][0]),round(kp[d][1])) for d in '12'}
 click_xy(*done_xy);time.sleep(.35)
 ns2=simutil.nodes(W);bk=nodeid(ns2,'nb-back') or nodeid(ns2,'tb-back')
 if bk:click_xy(*cent(bk));time.sleep(.4)
 out=[]
 out.append(one('lost',120,nav,kpmap,done_xy))
 out.append(one('kept',900,nav,kpmap,done_xy))
 print(json.dumps(out,indent=1))
if __name__=='__main__':run()
