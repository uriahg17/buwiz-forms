import sys,os,time,json
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
from case1 import open_filings,open_form,keypad_all
from case6 import setrows,rowsdb
from navrows import small_scroll,byid

def click_center(n): click_xy(round(n['pos'][0]+n['size'][0]/2),round(n['pos'][1]+n['size'][1]/2))
def expand_schedule(W):
 # close any sheet first
 for _ in range(4):
  d=simutil.find(W,idpart='fp-table-drpATC1-done')
  if not d: break
  click_node(d[0],.4); time.sleep(.5)
 for _ in range(24):
  row=byid(W,'fp-row-drpATC1-0')
  if row and row.get('pos'): return True
  tog=byid(W,'fp-part-4-toggle')
  if tog and tog.get('pos') and 250<tog['pos'][1]<930:
   click_node(tog,.4); time.sleep(.5); continue
  small_scroll(W,up=True)
 return False
def open_row_index(W,idx):
 id='fp-row-drpATC1-'+str(idx)
 for _ in range(25):
  n=byid(W,id)
  hi=880 if W==IPHONE else 990
  if n and n.get('pos') and 280<n['pos'][1]<hi:
   click_center(n); time.sleep(.7)
   if simutil.find(W,idpart='fp-table-drpATC1-done'): return True
  small_scroll(W,up=True)
 raise RuntimeError('cannot open row '+str(idx))
def press_sheet_done(W):
 dl=simutil.find(W,idpart='fp-table-drpATC1-done')
 if dl: click_node(dl[0],.5); time.sleep(.6)
def run(W,udid,db):
 out='iphone' if W==IPHONE else 'ipad'; cdir=os.path.join(ROOT,out,'case6-valid');os.makedirs(cdir,exist_ok=True)
 rec={'device':out,'case':'case6-valid-row-delete'}
 setrows(db,[(1000.0,'PT010'),(3000.0,'PT040')]); open_filings(W)
 # dismiss any stale row sheet left by an earlier failed run
 cl=next((n for n in simutil.nodes(W) if n.get('role')=='AXButton' and n.get('desc')=='Close'),None)
 if cl and simutil.find(W,text='Taxable Amount'): click_node(cl,.5); time.sleep(.5)
 open_form(W,'2551Q');time.sleep(.5)
 rec['expanded']=expand_schedule(W); shot(udid,cdir+'/000-two-rows-expanded.jpg')
 rec['opened_row2']=open_row_index(W,1); time.sleep(.3); shot(udid,cdir+'/001-row2-open-before-type.jpg')
 # record that modal sheet has only its own Delete row control; row1 is behind a scrim and not independently tappable
 rec['delete_controls_while_row2_open']=[(n.get('desc'),n.get('pos')) for n in simutil.nodes(W) if n.get('role')=='AXButton' and 'Delete row' in (n.get('desc') or '')]
 ns=simutil.nodes(W); f=next((n for n in ns if n.get('role')=='AXTextField'),None)
 if not f: raise RuntimeError('amount field not visible')
 dl=simutil.find(W,idpart='fp-table-drpATC1-done'); done=dl[0] if dl else None; done_xy=(round(done['pos'][0]+done['size'][0]/2),round(done['pos'][1]+done['size'][1]/2)) if done else None
 click_xy(round(f['pos'][0]+f['size'][0]-15),round(f['pos'][1]+f['size'][1]/2));time.sleep(.4)
 kp=keypad_all(W); rec['keypad']=sorted(kp)
 # Clear the prefilled 3,000.00 through real keypad Delete taps, then type the tested digits into the empty box.
 for _ in range(12):
  click_xy(*kp['Delete']);time.sleep(.08)
 shot(udid,cdir+'/004-row2-cleared.jpg')
 for i,c in enumerate('7777'):
  click_xy(*kp[c]);time.sleep(.17)
  if i in (0,3): shot(udid,cdir+f'/01{i}-typing-row2.jpg')
 shot(udid,cdir+'/005-row2-7777-before-blur.jpg')
 # feasible valid delete: blur/close row2, open row1, delete it; exact simultaneous row1 Delete is impossible behind modal sheet
 click_xy(*done_xy) if done_xy else press_sheet_done(W)
 time.sleep(.7); rec['rows_after_row2_done']=rowsdb(db);shot(udid,cdir+'/010-after-row2-done.jpg')
 rec['opened_row1']=open_row_index(W,0);time.sleep(.3);shot(udid,cdir+'/020-row1-open-before-delete.jpg')
 b=next((n for n in simutil.nodes(W) if n.get('role')=='AXButton' and 'Delete row' in (n.get('desc') or '')),None)
 rec['delete_button_row1']=bool(b); click_node(b,.7) if b else None; time.sleep(.8);shot(udid,cdir+'/021-after-delete-row1.jpg')
 rec['rows_after_delete']=rowsdb(db)
 open_form(W,'2551Q');time.sleep(.7);shot(udid,cdir+'/030-after-reopen.jpg');rec['rows_after_reopen']=rowsdb(db)
 logjson(os.path.join(ROOT,'observations.jsonl'),rec);return rec
if __name__=='__main__': print(json.dumps(run(sys.argv[1],sys.argv[2],sys.argv[3]),indent=1)[:6000])
