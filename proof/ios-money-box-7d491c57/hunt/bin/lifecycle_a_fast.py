import sys,os,time,json,subprocess,traceback
sys.path.insert(0,os.path.dirname(__file__))
from lifelib import *
from navrows import small_scroll,open_row_controlled

def cent(n): return (round(n['pos'][0]+n['size'][0]/2),round(n['pos'][1]+n['size'][1]/2))
def nodeid(ns,id): return next((n for n in ns if n.get('id')==id),None)
def first_textfield(ns): return next((n for n in ns if n.get('role')=='AXTextField' and n.get('value')!='Search returns' and n.get('value')!='Search by code or words'),None)
def find_row(ns): return next((n for n in ns if n.get('id')=='fp-row-drpATC1-0'),None)
def find_return(ns):
 n=nodeid(ns,'return-1')
 if n: return n
 return next((n for n in ns if n.get('role')=='AXButton' and '2551Q Q4 2026' in (n.get('desc') or '')),None)
def setup_fast(W,db):
 # Reach Filings once using the proven robust path, then cache stable navigation coordinates.
 open_filings(W); time.sleep(.3); ns=simutil.nodes(W)
 ret=find_return(ns)
 if not ret: raise RuntimeError('return coordinate missing')
 rc=cent(ret)
 return {'return':rc,'back':None}

def open_sheet_fast(W,nav):
 click_xy(*nav['return']); time.sleep(.65)
 rowxy=None
 for attempt in range(6):
  ns=simutil.nodes(W)
  bk=nodeid(ns,'nb-back') or nodeid(ns,'tb-back')
  if bk: nav['back']=cent(bk)
  row=find_row(ns)
  if row and row.get('pos') and 250<row['pos'][1]<(900 if W==IPHONE else 980):
   rowxy=cent(row); click_xy(*rowxy); time.sleep(.55); break
  # If the return-open click missed or the prior close did not reach Filings, retry the card.
  ret=find_return(ns)
  if ret:
   click_xy(*cent(ret)); time.sleep(.45); continue
  # fallback: collapse return details/expand schedule using visible controls
  p0=nodeid(ns,'fp-part-0-toggle'); p4=nodeid(ns,'fp-part-4-toggle')
  if p0 and any('For the' in (n.get('desc') or n.get('title') or '') for n in ns): click_node(p0,.25)
  elif p4 and not row: click_node(p4,.25)
  else: small_scroll(W,up=True)
 if not rowxy:
  open_row_controlled(W)
  time.sleep(.2)
 for attempt in range(3):
  ns=simutil.nodes(W)
  f=first_textfield(ns)
  if f: return ns,f
  time.sleep(.25)
 raise RuntimeError('fast sheet field missing')

def leave_sheet_to_filings(W,nav,done_xy=None):
 if done_xy: click_xy(*done_xy); time.sleep(.4)
 else:
  ns=simutil.nodes(W); d=nodeid(ns,'fp-table-drpATC1-done'); click_xy(*cent(d)); time.sleep(.4)
 if nav.get('back'): click_xy(*nav['back']); time.sleep(.5)

def close_reopen_validate(W,udid,db,cdir,prefix,nav,db_only=False):
 # Currently on the form page after Done. Close the return, reopen it, open row 1 and read/display saved state.
 if nav.get('back'): click_xy(*nav['back']); time.sleep(.35)
 if db_only:
  click_xy(*nav['return']); time.sleep(.5)
  shot(udid,os.path.join(cdir,prefix+'-after-reopen.jpg'))
  v=amount_val(db)
  if nav.get('back'): click_xy(*nav['back']); time.sleep(.3)
  return {'shown_after_reopen':None,'saved_after_reopen':v}
 ns,f=open_sheet_fast(W,nav)
 shot(udid,os.path.join(cdir,prefix+'-after-reopen.jpg'))
 return {'shown_after_reopen':f.get('value'),'saved_after_reopen':amount_val(db)}

def run_device(W,udid,db):
 sub=outsub(W); cdir=os.path.join(LROOT,sub,'case-a'); os.makedirs(cdir,exist_ok=True)
 mp4=os.path.join(cdir,sub+'-a.mp4'); vp=start_video(udid,mp4); results=[]
 try:
  subprocess.run(['xcrun','simctl','launch',udid,'com.apple.Preferences'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.5)
  subprocess.run(['xcrun','simctl','launch',udid,'com.longbridge.nsh.host'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.8)
  nav=setup_fast(W,db)
  specs=[('home',1234.56)]*10+[('switcher',1234.56)]*5+[('home',12345678.90)]*2
  for i,(mode,amount) in enumerate(specs,1):
   r={'case':'lifecycle-a','device':sub,'run':i,'mode':mode,'expected_amount':amount,'fast_version':3}
   try:
    set_amount(db,amount)
    ns,f=open_sheet_fast(W,nav)
    done=nodeid(ns,'fp-table-drpATC1-done'); done_xy=cent(done) if done else None
    x=round(f['pos'][0]+f['size'][0]-12); y=round(f['pos'][1]+f['size'][1]/2); click_xy(x,y); time.sleep(.25)
    shot(udid,os.path.join(cdir,f'{i:02d}-focused-before-leave.jpg'))
    if mode=='home':
     home(W); time.sleep(5)
     subprocess.run(['xcrun','simctl','launch',udid,'com.longbridge.nsh.host'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    else:
     app_switcher(W); switcher_other(W); time.sleep(2)
     app_switcher(W); switcher_other(W)
    time.sleep(.65)
    # If the app-switcher click landed on the wrong card or the switcher is still open, retry the return
    # before judging the field. A missing field is an automation gap, not a product amount change.
    ns=simutil.nodes(W); f=first_textfield(ns)
    for attempt in range(3):
     if f: break
     if any('Hover Typing' in (n.get('desc') or n.get('title') or '') for n in ns): app_switcher(W)
     else: click_xy(180,600) if W==IPHONE else click_xy(1078,734)
     time.sleep(.7); ns=simutil.nodes(W); f=first_textfield(ns)
    shot(udid,os.path.join(cdir,f'{i:02d}-return-before-key.jpg'))
    before=f.get('value') if f else None; r['shown_before_any_key']=before
    if before is None:
     raise RuntimeError('could not return to amount field after lifecycle transition')
    if abs(numeric(before)-amount)>.005:
     r['stop_condition']='amount changed without key press'; shot(udid,os.path.join(cdir,f'{i:02d}-STOP-changed-without-key.jpg')); results.append(r); loglife(r); break
    tr=next((n for n in ns if n.get('id')=='fp-drpATC1-trigger'),None)
    if tr: click_xy(*cent(tr)); time.sleep(.3)
    else:
     # Fallback to the slower proven blur helper if the trigger id is absent.
     blur_atc(W)
    # Close the ATC picker, then read the save caused by that focus transition.
    ns2=simutil.nodes(W); cl=next((n for n in ns2 if n.get('role')=='AXButton' and (n.get('desc') or '')=='Close'),None)
    if cl: click_xy(*cent(cl)); time.sleep(.25)
    r['saved_after_other_box']=amount_val(db)
    dn=nodeid(ns2,'fp-table-drpATC1-done')
    if not dn:
     ns3=simutil.nodes(W); dn=nodeid(ns3,'fp-table-drpATC1-done')
    click_xy(*cent(dn))
    time.sleep(.4); r['saved_after_leaving']=amount_val(db); shot(udid,os.path.join(cdir,f'{i:02d}-after-leaving.jpg'))
    r.update(close_reopen_validate(W,udid,db,cdir,f'{i:02d}',nav,db_only=True))
    results.append(r); loglife(r)
    # Return to Filings so the next run starts from a deterministic place.
    # db-only validation already returned to Filings
   except Exception as e:
    r['exception']=repr(e); r['trace']=traceback.format_exc()[-1500:]; results.append(r); loglife(r); shot(udid,os.path.join(cdir,f'{i:02d}-exception.jpg')); break
 finally: stop_video(vp[0])
 loglife({'case':'lifecycle-a-summary','device':sub,'runs':len(results),'changed':sum(1 for r in results if 'stop_condition' in r),'results':results,'mp4':mp4})
 print(json.dumps({'device':sub,'runs':len(results),'changed':sum(1 for r in results if 'stop_condition' in r)}))
if __name__=='__main__':
 W=IPHONE if sys.argv[1]=='iphone' else IPAD
 udid='405F45A9-B471-47B7-A5D9-E545EA624713' if W==IPHONE else '41A2AFE3-9E35-4EE8-BEF0-21AA02B68BC3'
 db='/tmp/money7d-iphone.db' if W==IPHONE else '/tmp/money7d-ipad.db'
 run_device(W,udid,db)
