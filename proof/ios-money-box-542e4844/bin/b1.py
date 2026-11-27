import sys,os,time,json,sqlite3,subprocess
sys.path.insert(0,'/Users/devin/moneybox-542e4844/helpers/bin')
import simutil
from huntlib import *
from case1 import open_filings,open_form
from navrows import small_scroll,byid
from case3 import launch
ROOTP='/Users/devin/moneybox-542e4844/proof/ios-money-box-542e4844/b1-fast'
ROWS=[(1000,'PT010'),(2000,'PT040'),(3000,'PT010')]
def setrows(db):
 con=sqlite3.connect(db); row=con.execute("select id,data_json from form_drafts where form_code='2551Q'").fetchone(); j=json.loads(row[1])
 j['schedule_1']=[{'atc':atc,'atc_description':'Persons exempt','taxable_amount':float(amt),'tax_rate':0.03,'tax_due':round(amt*.03,2)} for amt,atc in ROWS]
 con.execute('update form_drafts set data_json=? where id=?',(json.dumps(j),row[0]));con.commit();con.close()
def rowsdb(db):
 try:return json.loads(sqlite3.connect(db).execute("select data_json from form_drafts where form_code='2551Q'").fetchone()[0]).get('schedule_1',[])
 except Exception as e:return {'error':str(e)}
def menu(W,item):
 subprocess.run(['osascript','/tmp/focus_sim.scpt',W],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.15)
 subprocess.run(['osascript','-e',f'tell application "System Events" to tell process "Simulator" to click menu item "{item}" of menu "Keyboard" of menu item "Keyboard" of menu "I/O" of menu bar 1'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.4)
def expand_rows(W):
 if simutil.find(W,idpart='frm2551Qv2018:rtnMonth'):
  t=byid(W,'fp-part-0-toggle')
  if t: click_node(t,.35)
 for _ in range(18):
  rows=[n for n in simutil.nodes(W) if (n.get('id') or '').startswith('fp-row-drpATC1-')]
  if rows: return sorted(rows,key=lambda n:int((n.get('id') or '0').rsplit('-',1)[-1]))
  tog=byid(W,'fp-part-4-toggle')
  if tog and tog.get('pos') and 280<tog['pos'][1]<(1010 if W==IPHONE else 1050): click_node(tog,.4)
  else: small_scroll(W,up=True)
 raise RuntimeError('no rows')
def ensure_kbd(W):
 f=simutil.find(W,role='AXTextField')
 if not f: raise RuntimeError('no amount field')
 x=round(f[0]['pos'][0]+f[0]['size'][0]-2); y=round(f[0]['pos'][1]+f[0]['size'][1]/2)
 for i in range(3):
  click_xy(x,y);time.sleep(.9)
  kp=keypad(W)
  if kp: return kp
  menu(W,'Connect Hardware Keyboard')
 raise RuntimeError('no software keypad')
def clear_type(W,seq):
 kp=ensure_kbd(W)
 # Capture Delete while the keyboard is up and before the final keystroke; its position is verified hittable here.
 kd=simutil.find(W,idpart='fp-table-drpATC1-delete')
 for _ in range(9):
  click_xy(*kp['Delete']);time.sleep(.07)
 time.sleep(.2)
 tlast=None
 for c in seq:
  click_xy(*kp[c]); tlast=time.time()
  if c != seq[-1]: time.sleep(.14)
 return tlast,kp,(kd[0] if kd else None)
def click_row(W,idx):
 row=None
 for _ in range(6):
  rows=expand_rows(W)
  row=next((n for n in rows if (n.get('id') or '').endswith('-'+str(idx))),None)
  if not row: raise RuntimeError('missing row '+str(idx))
  x,y=center(row)
  hi=830 if W==IPHONE else 980
  if y<hi: break
  small_scroll(W,up=True)
 if not row: raise RuntimeError('missing row '+str(idx))
 click_node(row,.8)
 if not simutil.find(W,role='AXTextField'): raise RuntimeError('sheet no field')
def leave_open(W):
 # close form with toolbar back; setup/navigation only
 xs=simutil.find(W,idpart='nb-back') or simutil.find(W,idpart='tb-back')
 if xs: click_node(xs[0],.5)
def runone(W,udid,db,idx,run,control=False,video=False):
 sub='iphone' if W==IPHONE else 'ipad'; cdir=f'{ROOTP}/{sub}/{"control" if control else "row"+str(idx+1)}-r{run}';os.makedirs(cdir,exist_ok=True)
 p=None
 if video:
  p=subprocess.Popen(['xcrun','simctl','io',udid,'recordVideo','--force','--codec=h264',cdir+'/b1.mp4'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
 try:
  setrows(db);launch(udid,db);time.sleep(1.5);open_filings(W);open_form(W,'2551Q');time.sleep(.7);click_row(W,idx)
  tlast,kb,predel=clear_type(W,'500')
  if control:
   dn=simutil.find(W,idpart='fp-table-drpATC1-done')
   if dn: click_node(dn[0],1.2)
   click_row(W,idx)
  kd=(simutil.find(W,idpart='fp-table-drpATC1-delete') if control else ([predel] if predel else []))
  before_rows=None
  rec={'device':sub,'row_index':idx,'run':run,'control':control,'keyboard_visible':bool(kb),'delete_visible':bool(kd),'before_rows':before_rows}
  if not kd: raise RuntimeError('Delete row not exposed/hittable while keyboard up')
  if kd:
   d=kd[0]; rec['delete_frame']={'pos':d.get('pos'),'size':d.get('size')}; rec['keyboard_key1']=kb.get('1')
   # keyboard top estimated from first-row key center less half key height (~27); hittable when delete bottom is above it
   rec['delete_above_keyboard']=(d['pos'][1]+d['size'][1]) < (kb['1'][1]-27) if kb else None
   xy=center(d); tclick=time.time(); click_xy(*xy); tclickdone=time.time(); rec['last_type_to_delete_ms']=round((tclick-tlast)*1000,1); rec['last_type_to_delete_done_ms']=round((tclickdone-tlast)*1000,1); rec['delete_click_xy']=xy; time.sleep(.05); shot(udid,cdir+'/001-just-after-delete-click.jpg')
  time.sleep(2.2);shot(udid,cdir+'/002-after-delete.jpg');rec['rows_after_delete']=rowsdb(db)
  # Reopen by relaunching: on iPad the centered row modal can otherwise keep the form covered.
  launch(udid,db);time.sleep(1.5);open_filings(W);open_form(W,'2551Q');time.sleep(1);shot(udid,cdir+'/003-after-reopen.jpg');rec['rows_after_reopen']=rowsdb(db)
  open(cdir+'/result.json','w').write(json.dumps(rec,indent=1));return rec
 finally:
  if p:
   p.send_signal(2)
   try:p.wait(5)
   except: p.kill()
def main():
 mode=sys.argv[1] if len(sys.argv)>1 else 'all'
 devices=[]
 if mode in ('iphone','all'): devices.append((IPHONE,IPHONE_UDID,'/tmp/money542-iphone.db'))
 if mode in ('ipad','all'): devices.append((IPAD,IPAD_UDID,'/tmp/money542-ipad.db'))
 for W,udid,db in devices:
  out=[]
  if True:
   for idx in [1,2]:
    for r in range(1,4): out.append(runone(W,udid,db,idx,r,video=(idx==1 and r==1)))
   out.append(runone(W,udid,db,1,1,control=True))
  print(json.dumps(out))
if __name__=='__main__': main()
