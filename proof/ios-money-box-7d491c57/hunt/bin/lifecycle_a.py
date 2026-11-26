import sys,os,time,json,subprocess,traceback
sys.path.insert(0,os.path.dirname(__file__))
from lifelib import *

def run_device(W,udid,db):
 sub=outsub(W); cdir=os.path.join(LROOT,sub,'case-a'); os.makedirs(cdir,exist_ok=True)
 mp4=os.path.join(cdir,sub+'-a.mp4'); recproc=start_video(udid,mp4)
 results=[]; stopped=False
 try:
  # Ensure another app exists for switcher runs.
  subprocess.run(['xcrun','simctl','launch',udid,'com.apple.Preferences'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  time.sleep(.8); subprocess.run(['xcrun','simctl','launch',udid,'com.longbridge.nsh.host'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
  specs=[('home',1234.56)]*10+[('switcher',1234.56)]*5+[('home',12345678.90)]*2
  for i,(mode,amount) in enumerate(specs,1):
   r={'case':'lifecycle-a','device':sub,'run':i,'mode':mode,'expected_amount':amount}
   try:
    open_amount(W,db,amount)
    focus_amount(W)
    shot(udid,os.path.join(cdir,f'{i:02d}-focused-before-leave.jpg'))
    if mode=='home':
     home(W); time.sleep(5)
     subprocess.run(['xcrun','simctl','launch',udid,'com.longbridge.nsh.host'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    else:
     app_switcher(W); switcher_other(W); time.sleep(2)
     app_switcher(W); switcher_other(W)
    time.sleep(.8)
    shot(udid,os.path.join(cdir,f'{i:02d}-return-before-key.jpg'))
    f=wait_field(W,3); before=f.get('value') if f else None
    r['shown_before_any_key']=before
    if numeric(before) is None or abs(numeric(before)-amount)>.005:
     r['stop_condition']='amount changed without key press'
     stopped=True
     shot(udid,os.path.join(cdir,f'{i:02d}-STOP-changed-without-key.jpg'))
     results.append(r); loglife(r)
     break
    blur_atc(W); time.sleep(.3); r['saved_after_other_box']=amount_val(db)
    fin=finish_reopen(W,udid,db,cdir,f'{i:02d}')
    r.update(fin); results.append(r); loglife(r)
   except Exception as e:
    r['exception']=repr(e); r['trace']=traceback.format_exc()[-1500:]; results.append(r); loglife(r)
    shot(udid,os.path.join(cdir,f'{i:02d}-exception.jpg'))
    break
 finally:
  stop_video(recproc)
 summary={'case':'lifecycle-a-summary','device':sub,'runs':len(results),'changed':sum(1 for r in results if 'stop_condition' in r),'results':results,'mp4':mp4}
 loglife(summary)
 print(json.dumps({'device':sub,'runs':len(results),'changed':summary['changed'],'stopped':stopped}))
if __name__=='__main__':
 W=IPHONE if sys.argv[1]=='iphone' else IPAD
 udid='405F45A9-B471-47B7-A5D9-E545EA624713' if W==IPHONE else '41A2AFE3-9E35-4EE8-BEF0-21AA02B68BC3'
 db='/tmp/money7d-iphone.db' if W==IPHONE else '/tmp/money7d-ipad.db'
 run_device(W,udid,db)
