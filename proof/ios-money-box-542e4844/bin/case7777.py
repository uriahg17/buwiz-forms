import sys,os,time,json,subprocess
sys.path.insert(0,'/Users/devin/moneybox-542e4844/helpers/bin')
sys.path.insert(0,'/Users/devin/moneybox-542e4844/proof/ios-money-box-542e4844/bin')
import simutil,b1
from huntlib import *
from case1 import open_filings,open_form
ROOTP='/Users/devin/moneybox-542e4844/proof/ios-money-box-542e4844/case7777'

def reset_form(W,db):
 x=simutil.find(W,idpart='fp-table-drpATC1-done')
 if x: click_node(x[0],.5)
 open_filings(W);time.sleep(.4);b1.setrows(db);open_form(W,'2551Q');time.sleep(.8)

def focus_clear_type(W,seq):
 f=simutil.find(W,role='AXTextField')
 if not f: raise RuntimeError('no amount field')
 f=f[0];x=round(f['pos'][0]+f['size'][0]-2);y=round(f['pos'][1]+f['size'][1]/2)
 click_xy(x,y);time.sleep(.9)
 kp=keypad(W)
 if not kp: raise RuntimeError('keyboard not visible')
 for _ in range(9):click_xy(*kp['Delete']);time.sleep(.07)
 time.sleep(.15)
 for i,c in enumerate(seq):
  click_xy(*kp[c]);
  if i<len(seq)-1:time.sleep(.14)
 time.sleep(.05)

def expected(rows):
 try:return rows[0].get('atc','')=='' and rows[0].get('taxable_amount')==0.0 and rows[1].get('atc')=='PT040' and rows[1].get('taxable_amount')==7777.0 and rows[2].get('atc')=='PT010' and rows[2].get('taxable_amount')==3000.0
 except Exception:return False

def runone(W,udid,db,runno):
 sub='iphone' if W==IPHONE else 'ipad';cdir=f'{ROOTP}/{sub}/r{runno:02d}';os.makedirs(cdir,exist_ok=True)
 reset_form(W,db);b1.click_row(W,1);focus_clear_type(W,'7777')
 shot(udid,cdir+'/001-typed-7777-keyboard-up.jpg')
 kp=keypad(W);dn=simutil.find(W,idpart='fp-table-drpATC1-done')
 if not kp or not dn: raise RuntimeError('Done/keyboard missing')
 d=dn[0];above=(d['pos'][1]+d['size'][1]) < (kp['1'][1]-27)
 rec={'device':sub,'run':runno,'keyboard_key1':kp.get('1'),'done_frame':{'pos':d.get('pos'),'size':d.get('size')},'done_above_keyboard':above}
 if not above: raise RuntimeError('Done not hittable above keyboard')
 click_xy(*center(d));time.sleep(1.3);shot(udid,cdir+'/002-after-hittable-done.jpg')
 # open row1 and delete it after row2 was left/saved
 b1.click_row(W,0);time.sleep(.2);kd=simutil.find(W,idpart='fp-table-drpATC1-delete')
 if not kd: raise RuntimeError('row1 Delete missing')
 click_xy(*center(kd[0]));time.sleep(2);shot(udid,cdir+'/003-after-row1-delete.jpg');rec['rows_after_delete']=b1.rowsdb(db)
 open_filings(W);time.sleep(.4);open_form(W,'2551Q');time.sleep(.8);shot(udid,cdir+'/004-after-reopen.jpg');rec['rows_after_reopen']=b1.rowsdb(db);rec['right']=expected(rec['rows_after_reopen'])
 open(cdir+'/result.json','w').write(json.dumps(rec,indent=1));return rec

def main():
 mode=sys.argv[1] if len(sys.argv)>1 else 'iphone'; n=int(sys.argv[2]) if len(sys.argv)>2 else 10
 W,udid,db=(IPHONE,IPHONE_UDID,'/tmp/money542-iphone.db') if mode=='iphone' else (IPAD,IPAD_UDID,'/tmp/money542-ipad.db')
 out=[]
 for r in range(1,n+1): out.append(runone(W,udid,db,r))
 print(json.dumps({'right':sum(1 for x in out if x.get('right')),'n':len(out),'runs':out}))
if __name__=='__main__':main()
