import sys,os,time,json,traceback
sys.path.insert(0,os.path.dirname(__file__))
from lifelib import *
def run_device(W,udid,db):
 sub=outsub(W); cdir=os.path.join(LROOT,sub,'case-c'); os.makedirs(cdir,exist_ok=True)
 mp4=os.path.join(cdir,sub+'-c.mp4'); vp=start_video(udid,mp4); results=[]
 try:
  open_amount(W,db,1234.56); focus_amount(W); kp=keypad(W); press_done(W); time.sleep(.3)
  for i,posname in enumerate(('left','middle','right'),1):
   r={'case':'lifecycle-c','device':sub,'position':posname}
   try:
    open_amount(W,db,1234.56); f=wait_field(W,2); x0,y,w,h=f['pos'][0],f['pos'][1],f['size'][0],f['size'][1]
    if posname=='left': x=x0+7
    elif posname=='middle': x=x0+w/2
    else: x=x0+w-7
    click_xy(round(x),round(y+h/2)); time.sleep(.35); r['shown_before_8']=wait_field(W,1).get('value')
    shot(udid,os.path.join(cdir,f'{i:02d}-{posname}-before-8.jpg'))
    click_xy(round(kp['8'][0]),round(kp['8'][1])); time.sleep(.4)
    r['shown_after_8']=wait_field(W,1).get('value'); shot(udid,os.path.join(cdir,f'{i:02d}-{posname}-after-8.jpg'))
    press_done(W); time.sleep(.45); r['saved_after_leaving']=amount_val(db)
    open_filings(W); time.sleep(.25); open_form(W,'2551Q'); open_row_controlled(W); time.sleep(.2)
    fs=simutil.find(W,role='AXTextField'); r['shown_after_reopen']=fs[0].get('value') if fs else None; r['saved_after_reopen']=amount_val(db); shot(udid,os.path.join(cdir,f'{i:02d}-{posname}-after-reopen.jpg'))
    results.append(r); loglife(r)
   except Exception as e:
    r['exception']=repr(e); r['trace']=traceback.format_exc()[-1000:]; results.append(r); loglife(r); break
 finally: stop_video(vp[0])
 loglife({'case':'lifecycle-c-summary','device':sub,'results':results,'mp4':mp4}); print(json.dumps({'device':sub,'runs':len(results)}))
if __name__=='__main__':
 W=IPHONE if sys.argv[1]=='iphone' else IPAD
 udid='405F45A9-B471-47B7-A5D9-E545EA624713' if W==IPHONE else '41A2AFE3-9E35-4EE8-BEF0-21AA02B68BC3'
 db='/tmp/money7d-iphone.db' if W==IPHONE else '/tmp/money7d-ipad.db'
 run_device(W,udid,db)
