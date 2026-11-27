import sys,os,time,json,subprocess
sys.path.insert(0,'/Users/devin/moneybox-542e4844/helpers/bin')
sys.path.insert(0,'/Users/devin/moneybox-542e4844/proof/ios-money-box-542e4844/bin')
import simutil,b1
from huntlib import *
from case1 import open_filings,open_form
ROOTP='/Users/devin/moneybox-542e4844/proof/ios-money-box-542e4844/b1-ipad-docked'
W=IPAD;UDID=IPAD_UDID;DB='/tmp/money542-ipad.db'

def close_any_sheet():
 for idp in ('fp-table-drpATC1-done',):
  x=simutil.find(W,idpart=idp)
  if x: click_node(x[0],.6); return
 c=[n for n in simutil.nodes(W) if n.get('role')=='AXButton' and (n.get('desc') or '')=='Close']
 if c: click_node(c[0],.5)

def reset_form():
 close_any_sheet(); open_filings(W); time.sleep(.5); b1.setrows(DB); open_form(W,'2551Q'); time.sleep(.8)

def docked_keypad():
 kp=keypad(W)
 return kp if kp and kp.get('1')==(612,861) and 'Delete' in kp else None

def make_docked_if_needed():
 kp=keypad(W)
 # Floating 3x4 pad: drag its lower edge down once (this dismisses it), then refocus; iPadOS reopens docked full-width.
 if kp and kp.get('1')==(1064,718):
  subprocess.run(['cliclick','dd:1015,850','dm:980,890','dm:900,930','dm:800,960','du:700,990'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  time.sleep(.7)
  f=simutil.find(W,role='AXTextField')
  if f:
   x=round(f[0]['pos'][0]+f[0]['size'][0]-2);y=round(f[0]['pos'][1]+f[0]['size'][1]/2);click_xy(x,y);time.sleep(1)

def focus_and_type(seq):
 f=simutil.find(W,role='AXTextField')
 if not f: raise RuntimeError('no amount field')
 f=f[0]; x=round(f['pos'][0]+f['size'][0]-2); y=round(f['pos'][1]+f['size'][1]/2)
 kp=None
 for attempt in range(3):
  click_xy(x,y);time.sleep(1)
  make_docked_if_needed()
  kp=docked_keypad()
  if kp: break
 if not kp: raise RuntimeError('docked full-width keypad not visible: '+repr(keypad(W)))
 # Verify Delete row exposure/hittability before typing. With docked keyboard it is above keyboard top.
 kd=simutil.find(W,idpart='fp-table-drpATC1-delete')
 done=simutil.find(W,idpart='fp-table-drpATC1-done')
 if not kd: raise RuntimeError('Delete row not exposed with docked keyboard')
 for _ in range(9): click_xy(*kp['Delete']);time.sleep(.07)
 time.sleep(.15)
 tlast=None
 for i,c in enumerate(seq):
  click_xy(*kp[c]);tlast=time.time()
  if i<len(seq)-1: time.sleep(.14)
 return tlast,kp,kd[0],(done[0] if done else None)

def press_node_fast(n,tlast):
 xy=center(n); t0=time.time(); click_xy(*xy); t1=time.time(); return xy,round((t0-tlast)*1000,1),round((t1-tlast)*1000,1)

def run(idx,runno,control=False,video=False):
 cdir=f'{ROOTP}/{"control" if control else "row"+str(idx+1)}-r{runno}';os.makedirs(cdir,exist_ok=True)
 p=None
 if video:
  p=subprocess.Popen(['xcrun','simctl','io',UDID,'recordVideo','--force','--codec=h264',cdir+'/b1.mp4'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.8)
 try:
  reset_form(); b1.click_row(W,idx)
  tlast,kp,delnode,donenode=focus_and_type('500')
  rec={'device':'ipad','row_index':idx,'run':runno,'control':control,'docked_keypad':True,'delete_frame':{'pos':delnode.get('pos'),'size':delnode.get('size')},'keyboard_key1':kp.get('1'),'keyboard_delete':kp.get('Delete')}
  rec['delete_above_keyboard']=(delnode['pos'][1]+delnode['size'][1]) < (kp['1'][1]-27)
  if control:
   if not donenode: raise RuntimeError('Done missing in control')
   xy=center(donenode);click_xy(*xy);time.sleep(1.2)
   b1.click_row(W,idx)
   kd=simutil.find(W,idpart='fp-table-drpATC1-delete')
   if not kd: raise RuntimeError('control delete missing after reopen')
   delnode=kd[0]
  xy,gap,gapdone=press_node_fast(delnode,tlast);rec['delete_click_xy']=xy;rec['last_type_to_delete_ms']=gap;rec['last_type_to_delete_done_ms']=gapdone
  time.sleep(.05);shot(UDID,cdir+'/001-just-after-delete-click.jpg')
  time.sleep(2);shot(UDID,cdir+'/002-after-delete.jpg');rec['rows_after_delete']=b1.rowsdb(DB)
  # navigate away/back without relaunching, preserving the docked keyboard configuration
  open_filings(W);time.sleep(.5);open_form(W,'2551Q');time.sleep(.9);shot(UDID,cdir+'/003-after-reopen.jpg');rec['rows_after_reopen']=b1.rowsdb(DB)
  open(cdir+'/result.json','w').write(json.dumps(rec,indent=1));return rec
 finally:
  if p:
   p.send_signal(2)
   try:p.wait(5)
   except: p.kill()

def main():
 os.makedirs(ROOTP,exist_ok=True)
 out=[]
 for idx in (1,2):
  for r in (1,2,3): out.append(run(idx,r,video=(idx==1 and r==1)))
 out.append(run(1,1,control=True))
 print(json.dumps(out))
if __name__=='__main__': main()
