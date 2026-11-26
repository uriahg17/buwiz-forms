import sys,os,time,json,traceback
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
from lifelib import set_hardware
from case1 import open_filings,open_form,keypad_all
from case6 import setrows,rowsdb
from case3 import launch
from case6valid import expand_schedule,open_row_index

def ctr(n):return (round(n['pos'][0]+n['size'][0]/2),round(n['pos'][1]+n['size'][1]/2))
def done_node(W):return (simutil.find(W,idpart='fp-table-drpATC1-done') or [None])[0]
def close_sheet_done(W,done_xy):
 # On both devices the first press while the software pad is up may merely dismiss the pad.
 click_xy(*done_xy);time.sleep(.65)
 for _ in range(3):
  d=done_node(W)
  if not d:break
  click_xy(*ctr(d));time.sleep(.6)
 return done_node(W) is None
def close_any_sheet(W):
 for _ in range(3):
  c=next((n for n in simutil.nodes(W) if n.get('role')=='AXButton' and n.get('desc')=='Close'),None)
  if c and simutil.find(W,text='Taxable Amount'):
   click_xy(*ctr(c));time.sleep(.5)
  else:return

def runone(W,udid,db):
 out='iphone' if W==IPHONE else 'ipad';cdir=os.path.join(ROOT,out,'case6-sequential-valid');os.makedirs(cdir,exist_ok=True)
 rec={'device':out,'case':'case6-sequential-valid-row-delete'}
 try:
  launch(udid,db);time.sleep(1.3);set_hardware(W,False)
  open_filings(W);close_any_sheet(W);open_filings(W)
  setrows(db,[(1000.0,'PT010'),(3000.0,'PT040')]);open_form(W,'2551Q');time.sleep(.5)
  rec['rows_initial']=rowsdb(db);rec['expanded']=expand_schedule(W);shot(udid,cdir+'/000-two-rows.jpg')
  rec['opened_row2']=open_row_index(W,1);time.sleep(.3);shot(udid,cdir+'/001-row2-before-type.jpg')
  rec['delete_controls_row2_open']=[(n.get('desc'),n.get('pos')) for n in simutil.nodes(W) if n.get('role')=='AXButton' and 'Delete row' in (n.get('desc') or '')]
  f=(simutil.find(W,role='AXTextField') or [None])[0];d=done_node(W)
  if not f or not d:raise RuntimeError('row2 amount/done missing')
  done_xy=ctr(d);click_xy(round(f['pos'][0]+f['size'][0]-15),round(f['pos'][1]+f['size'][1]/2));time.sleep(1.5)
  kp=keypad_all(W);rec['keypad']=sorted(kp)
  if 'Delete' not in kp:raise RuntimeError('delete keypad missing')
  for _ in range(12):click_xy(*kp['Delete']);time.sleep(.1)
  shot(udid,cdir+'/002-row2-cleared.jpg')
  for ch in '7777':click_xy(*kp[ch]);time.sleep(.3)
  time.sleep(1.2)
  shot(udid,cdir+'/003-row2-7777-before-leaving.jpg')
  rec['closed_row2']=close_sheet_done(W,done_xy);time.sleep(.3)
  rec['rows_after_row2_leave']=rowsdb(db);shot(udid,cdir+'/010-row2-left.jpg')
  rec['opened_row1']=open_row_index(W,0);time.sleep(.35);shot(udid,cdir+'/020-row1-before-delete.jpg')
  b=next((n for n in simutil.nodes(W) if n.get('role')=='AXButton' and 'Delete row' in (n.get('desc') or '')),None)
  rec['delete_button_row1']=bool(b)
  if not b:raise RuntimeError('row1 delete missing')
  click_xy(*ctr(b));time.sleep(.9);shot(udid,cdir+'/021-after-delete-tap.jpg')
  # If a confirmation dialog appears, use its destructive confirmation button.
  texts=[n.get('desc') or n.get('label') or '' for n in simutil.nodes(W) if n.get('role')=='AXButton']
  rec['buttons_after_delete_tap']=texts
  for label in ('Delete','Delete row','Confirm'):
   q=next((n for n in simutil.nodes(W) if n.get('role')=='AXButton' and (n.get('desc')==label or n.get('label')==label)),None)
   if q and 'fp-table' not in (q.get('id') or ''):
    click_xy(*ctr(q));time.sleep(.7);rec['confirmed']=label;shot(udid,cdir+'/022-after-delete-confirm.jpg');break
  rec['rows_after_delete']=rowsdb(db);shot(udid,cdir+'/023-after-delete.jpg')
  # close/reopen the form itself
  open_filings(W);time.sleep(.35);shot(udid,cdir+'/030-back-at-filings.jpg')
  open_form(W,'2551Q');time.sleep(.7);rec['rows_after_reopen']=rowsdb(db);shot(udid,cdir+'/031-after-form-reopen.jpg')
 except Exception as e:
  rec['exception']=repr(e);rec['trace']=traceback.format_exc()[-1500:]
  try:shot(udid,cdir+'/099-exception.jpg')
  except Exception:pass
 logjson(os.path.join(ROOT,'observations.jsonl'),rec)
 with open(cdir+'/result.json','w') as fh:json.dump(rec,fh,indent=1)
 print(json.dumps(rec))
 return rec
if __name__=='__main__':runone(sys.argv[1],sys.argv[2],sys.argv[3])
