import sys,os,time,json,traceback
sys.path.insert(0,os.path.dirname(__file__))
from lifelib import *
from lifecycle_a_fast import setup_fast,open_sheet_fast,leave_sheet_to_filings,close_reopen_validate,cent,nodeid,first_textfield

def run_device(W,udid,db):
 sub=outsub(W); cdir=os.path.join(LROOT,sub,'case-c'); os.makedirs(cdir,exist_ok=True)
 mp4=os.path.join(cdir,sub+'-c.mp4'); vp=start_video(udid,mp4); results=[]
 try:
  nav=setup_fast(W,db)
  # calibrate keypad
  set_amount(db,1234.56); ns,f=open_sheet_fast(W,nav)
  click_xy(round(f['pos'][0]+f['size'][0]-12),round(f['pos'][1]+f['size'][1]/2)); time.sleep(.3)
  kp=keypad(W); done_xy=cent(nodeid(ns,'fp-table-drpATC1-done')); click_xy(*done_xy); time.sleep(.3)
  if nav.get('back'): click_xy(*nav['back']); time.sleep(.35)
  for i,posname in enumerate(('left','middle','right'),1):
   r={'case':'lifecycle-c','device':sub,'position':posname,'fast_version':2}
   try:
    set_amount(db,1234.56); ns,f=open_sheet_fast(W,nav)
    x0,y,w,h=f['pos'][0],f['pos'][1],f['size'][0],f['size'][1]
    x=x0+7 if posname=='left' else (x0+w/2 if posname=='middle' else x0+w-7)
    click_xy(round(x),round(y+h/2)); time.sleep(.3)
    nsb=simutil.nodes(W); fb=first_textfield(nsb); r['shown_before_8']=fb.get('value') if fb else None
    shot(udid,os.path.join(cdir,f'{i:02d}-{posname}-before-8.jpg'))
    click_xy(round(kp['8'][0]),round(kp['8'][1])); time.sleep(.3)
    nsa=simutil.nodes(W); fa=first_textfield(nsa); r['shown_after_8']=fa.get('value') if fa else None
    shot(udid,os.path.join(cdir,f'{i:02d}-{posname}-after-8.jpg'))
    click_xy(*done_xy); time.sleep(.35); r['saved_after_leaving']=amount_val(db)
    r.update(close_reopen_validate(W,udid,db,cdir,f'{i:02d}-{posname}',nav))
    results.append(r); loglife(r); leave_sheet_to_filings(W,nav,None)
   except Exception as e:
    r['exception']=repr(e); r['trace']=traceback.format_exc()[-1000:]; results.append(r); loglife(r); break
 finally: stop_video(vp[0])
 loglife({'case':'lifecycle-c-summary','device':sub,'results':results,'mp4':mp4}); print(json.dumps({'device':sub,'runs':len(results)}))
if __name__=='__main__':
 W=IPHONE if sys.argv[1]=='iphone' else IPAD
 udid='405F45A9-B471-47B7-A5D9-E545EA624713' if W==IPHONE else '41A2AFE3-9E35-4EE8-BEF0-21AA02B68BC3'
 db='/tmp/money7d-iphone.db' if W==IPHONE else '/tmp/money7d-ipad.db'
 run_device(W,udid,db)
