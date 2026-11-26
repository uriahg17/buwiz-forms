import sys,os,time,json,subprocess,traceback
sys.path.insert(0,'/Users/devin/moneybox-7d491c57/proof/ios-money-box-7d491c57/hunt/bin')
from lifelib import *
from case1 import open_filings,open_form,keypad_all,wait_field
from huntlib import click_xy,ensure_row_sheet
from case3 import launch
from case6valid import expand_schedule,open_row_index
W=IPAD;UDID='41A2AFE3-9E35-4EE8-BEF0-21AA02B68BC3';SEQ='1234.56'
def fast(ev):
 a=[]
 for x,y,d in ev:a += [str(round(x)),str(round(y)),str(max(0,int(d)))]
 return subprocess.run(['/tmp/fastclick35']+a,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=8).stdout
def outlog(x):
 with open(OUT+'/observations.jsonl','a') as f:f.write(json.dumps(x,sort_keys=True)+'\n')
def sheet():return bool(simutil.find(W,idpart='fp-table-drpATC1-done'))
def openrow():
 if sheet():return
 for _ in range(3):
  if open_row_index(W,0):return
 raise RuntimeError('open row failed')
def closerow():
 d=simutil.find(W,idpart='fp-table-drpATC1-done')
 if d:click_node(d[0],.45)
 if sheet():
  c=next((n for n in simutil.find(W,role='AXButton') if (n.get('desc') or '')=='Close' and n.get('pos') and n['pos'][0]>900),None)
  if c:click_node(c,.45)
def controls():
 d=simutil.find(W,idpart='fp-table-drpATC1-done');d=d[0] if d else None
 c=next((n for n in simutil.find(W,role='AXButton') if (n.get('desc') or '')=='Close' and n.get('pos') and n['pos'][0]>900),None)
 return (center(d) if d else None),(center(c) if c else None)
def kpmap():return keypad_all(W)
def sig(kp):return tuple((c,round(kp[c][0]),round(kp[c][1])) for c in '1234567890.' if c in kp)
def detect():
 st=time.monotonic();last=None;stable=0
 while time.monotonic()-st<6:
  kp=kpmap();sg=sig(kp);now=time.monotonic()
  if len(sg)>=11:
   stable=stable+1 if sg==last else 0;last=sg
   if stable>=2:return now,kp
  else:last=None;stable=0
  time.sleep(.01)
 raise RuntimeError('keyboard not shown/stable')
def clear_to_zero(mp):
 openrow();f=wait_field(W,1);click_xy(round(f['pos'][0]+f['size'][0]-12),round(f['pos'][1]+f['size'][1]/2));time.sleep(.45)
 kp=kpmap()
 if 'Delete' in kp:
  x,y=kp['Delete'];fast([(x,y,i*22) for i in range(15)]);time.sleep(.25)
 closerow();time.sleep(.2)
def soft_run(n,delay,mp):
 r={'build':LABEL,'mode':'software','run':n,'delay_target_ms':delay}
 try:
  openrow();done,close=controls();f=wait_field(W,1);fx=round(f['pos'][0]+f['size'][0]-12);fy=round(f['pos'][1]+f['size'][1]/2)
  ft=time.monotonic();click_xy(fx,fy);dt,kp=detect();r['detect_after_focus_ms']=round((dt-ft)*1000,1)
  wait=dt+delay/1000-time.monotonic()
  if wait>0:time.sleep(wait)
  ev=[(kp[c][0],kp[c][1],i*140) for i,c in enumerate(SEQ)]
  inv=time.monotonic();fast(ev);r['first_key_gap_ms']=round((inv-dt)*1000,1);time.sleep(.4)
  fs=simutil.find(W,role='AXTextField');r['shown']=fs[0].get('value') if fs else None
  v=amount_val(DB);r['saved']=v;r['saved_wrong']=v is None or abs(v-1234.56)>.005;r['lost']=(v is None or abs(v-1234.56)>.005)
  time.sleep(1.7);r['saved']=amount_val(DB);r['saved_wrong']=r['saved'] is None or abs(r['saved']-1234.56)>.005
  kp=kpmap()
  if 'Delete' in kp:fast([(kp['Delete'][0],kp['Delete'][1],i*22) for i in range(15)]);time.sleep(.2)
  if done:click_xy(*done);time.sleep(.45)
  r['sheet_closed_by_done']=not sheet()
  if sheet() and close:click_xy(*close);time.sleep(.35)
 except Exception as e:r['exception']=repr(e);r['trace']=traceback.format_exc()[-500:]
 outlog(r);return r
def hw_run(n):
 r={'build':LABEL,'mode':'hardware','run':n,'target_gap_ms':120}
 try:
  set_hardware(W,True);openrow();done,close=controls();f=wait_field(W,1);fx=round(f['pos'][0]+f['size'][0]-12);fy=round(f['pos'][1]+f['size'][1]/2)
  ft=time.monotonic();click_xy(fx,fy);wait=ft+.12-time.monotonic()
  if wait>0:time.sleep(wait)
  inv=time.monotonic();subprocess.run(['cliclick','t:1'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);r['first_key_gap_ms']=round((inv-ft)*1000,1)
  subprocess.run(['cliclick','t:234.56'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.45)
  fs=simutil.find(W,role='AXTextField');r['shown']=fs[0].get('value') if fs else None
  v=amount_val(DB);r['saved']=v;r['saved_wrong']=v is None or abs(v-1234.56)>.005;r['lost']=(v is None or abs(v-1234.56)>.005)
  time.sleep(1.7);r['saved']=amount_val(DB);r['saved_wrong']=r['saved'] is None or abs(r['saved']-1234.56)>.005
  for _ in range(12):subprocess.run(['cliclick','kp:delete'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  if done:click_xy(*done);time.sleep(.45)
  r['sheet_closed_by_done']=not sheet()
  if sheet() and close:click_xy(*close);time.sleep(.35)
 except Exception as e:r['exception']=repr(e);r['trace']=traceback.format_exc()[-500:]
 outlog(r);return r
def matrix(out,label,commit,db):
 global OUT,LABEL,DB;OUT=out;LABEL=label;DB=db;os.makedirs(out,exist_ok=True)
 launch(UDID,db);time.sleep(1.4);set_hardware(W,False);open_filings(W);open_form(W,'2551Q');time.sleep(.5);expand_schedule(W)
 openrow();f=wait_field(W,2);click_xy(round(f['pos'][0]+f['size'][0]-12),round(f['pos'][1]+f['size'][1]/2));time.sleep(.5)
 mp=kpmap();closerow();time.sleep(.2);results=[];n=0
 for d in (0,200,400):
  for i in range(10):
   n+=1
   results.append(soft_run(n,d,mp))
 for i in range(10):
  n+=1;set_hardware(W,False)
  results.append(hw_run(n))
 cnt={d:sum(1 for r in results if r.get('mode')=='software' and r.get('delay_target_ms')==d and r.get('lost')) for d in (0,200,400)}
 hw=sum(1 for r in results if r.get('mode')=='hardware' and r.get('lost'))
 line=f'{label} iPad kb-shown: lost {cnt[0]}/10 at 0, {cnt[200]}/10 at +200, {cnt[400]}/10 at +400; hardware: lost {hw}/10'
 outlog({'case':'summary','line':line});print(line)
if __name__=='__main__':matrix(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
