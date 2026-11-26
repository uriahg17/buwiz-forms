import sys,os,time,json,subprocess,traceback
sys.path.insert(0,os.path.dirname(__file__))
from lifelib import *
from lifecycle_a_fast import setup_fast,open_sheet_fast,leave_sheet_to_filings,cent,nodeid,first_textfield

def fast_seq(specs):
 args=[]
 for x,y,d in specs: args += [str(x),str(y),str(max(0,int(d)))]
 cp=subprocess.run(['/tmp/fastclick']+args,text=True,capture_output=True,timeout=10)
 clicks=[]
 for line in cp.stdout.splitlines():
  if line.startswith('click '):
   p=line.split(); clicks.append({'before_us':int(p[1]),'after_us':int(p[2]),'x':int(p[3]),'y':int(p[4])})
 return clicks,cp.stdout+cp.stderr

def close_reopen_db_only(W,nav,db):
 # Close and reopen the return; read the persisted value after that round trip, then go back to Filings.
 if nav.get('back'): click_xy(*nav['back']); time.sleep(.35)
 click_xy(*nav['return']); time.sleep(.55)
 v=amount_val(db)
 if nav.get('back'): click_xy(*nav['back']); time.sleep(.35)
 return v

def run_device(W,udid,db,reps=10):
 sub=outsub(W); cdir=os.path.join(LROOT,sub,'case-b'); os.makedirs(cdir,exist_ok=True)
 mp4=os.path.join(cdir,sub+'-b.mp4'); vp=start_video(udid,mp4); results=[]
 try:
  nav=setup_fast(W,db)
  # Calibrate the software keypad once.
  set_amount(db,0.0); ns,f=open_sheet_fast(W,nav)
  done_xy=cent(nodeid(ns,'fp-table-drpATC1-done'))
  x=round(f['pos'][0]+f['size'][0]-12); y=round(f['pos'][1]+f['size'][1]/2); click_xy(x,y); time.sleep(.3)
  kp=keypad(W); kpmap={d:(round(kp[d][0]),round(kp[d][1])) for d in '1234.56'}
  click_xy(*done_xy); time.sleep(.3)
  if nav.get('back'): click_xy(*nav['back']); time.sleep(.35)
  seq=list('1234.56'); specs=[]
  for delay in (200,400):
   for i in range(reps): specs.append((delay,'zero',0.0,i+1))
  for delay in (100,200,400): specs.append((delay,'filled',1234.56,1))
  for run,(delay,kind,amount,timingrun) in enumerate(specs,1):
   r={'case':'lifecycle-b','device':sub,'run':run,'timing_run':timingrun,'delay_target_ms':delay,'box_start':kind,'expected_amount':amount,'fast_version':2}
   try:
    set_amount(db,amount); ns,f=open_sheet_fast(W,nav)
    fx=round(f['pos'][0]+f['size'][0]-12); fy=round(f['pos'][1]+f['size'][1]/2)
    ev=[(fx,fy,0),(kpmap['1'][0],kpmap['1'][1],delay-14)]
    for j,c in enumerate(seq[1:]): ev.append((kpmap[c][0],kpmap[c][1],500 if j==0 else 70))
    clicks,raw=fast_seq(ev); r['measured_gap_ms']=round((clicks[1]['before_us']-clicks[0]['before_us'])/1000,3) if len(clicks)>1 else None
    time.sleep(.35); shot(udid,os.path.join(cdir,f'{run:03d}-{kind}-{delay}ms-after-typing.jpg'))
    ns=simutil.nodes(W); f=first_textfield(ns); shown=f.get('value') if f else None; r['shown_after_typing']=shown
    r['first_digit_lost']=(kind=='zero' and shown is not None and not str(shown).replace(',','').startswith('1'))
    click_xy(*done_xy); time.sleep(.35)
    r['saved_after_leaving']=amount_val(db); shot(udid,os.path.join(cdir,f'{run:03d}-{kind}-{delay}ms-after-leaving.jpg'))
    if kind=='zero' and shown is None:
     r['first_digit_lost']=(r['saved_after_leaving'] is not None and abs(r['saved_after_leaving']-1234.56)>.005)
    r['saved_after_reopen']=close_reopen_db_only(W,nav,db)
    results.append(r); loglife(r)
   except Exception as e:
    r['exception']=repr(e); r['trace']=traceback.format_exc()[-1200:]; results.append(r); loglife(r); shot(udid,os.path.join(cdir,f'{run:03d}-exception.jpg')); break
 finally: stop_video(vp[0])
 loglife({'case':'lifecycle-b-summary','device':sub,'runs':len(results),'results':results,'mp4':mp4})
 print(json.dumps({'device':sub,'runs':len(results),'lost':sum(1 for r in results if r.get('first_digit_lost'))}))
if __name__=='__main__':
 W=IPHONE if sys.argv[1]=='iphone' else IPAD
 udid='405F45A9-B471-47B7-A5D9-E545EA624713' if W==IPHONE else '41A2AFE3-9E35-4EE8-BEF0-21AA02B68BC3'
 db='/tmp/money7d-iphone.db' if W==IPHONE else '/tmp/money7d-ipad.db'
 run_device(W,udid,db,int(sys.argv[2]) if len(sys.argv)>2 else 10)
