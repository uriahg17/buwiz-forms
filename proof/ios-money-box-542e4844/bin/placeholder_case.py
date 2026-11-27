import sys,os,time,json,traceback
sys.path.insert(0,'/Users/devin/moneybox-542e4844/helpers/bin')
import simutil
from lifelib import *
from lifecycle_a_fast import setup_fast,open_sheet_fast,cent,nodeid
ROOT='/Users/devin/moneybox-542e4844/proof/ios-money-box-542e4844/lifecycle-c-placeholder'
def run(W,udid,db):
 sub=outsub(W);cdir=os.path.join(ROOT,sub);os.makedirs(cdir,exist_ok=True);rec={'device':sub,'case':'zero-placeholder'}
 try:
  nav=setup_fast(W,db);set_amount(db,0.0);ns,f=open_sheet_fast(W,nav)
  rec['unfocused']={'value':f.get('value'),'frame':{'pos':f['pos'],'size':f['size']}};shot(udid,cdir+'/000-zero-unfocused.jpg')
  click_xy(round(f['pos'][0]+f['size'][0]/2),round(f['pos'][1]+f['size'][1]/2));time.sleep(.8)
  fs=simutil.find(W,role='AXTextField');rec['focused_before_key']=fs[0].get('value') if fs else None;shot(udid,cdir+'/001-focused-before-key.jpg')
  kp=keypad(W)
  if '0' not in kp:raise RuntimeError('zero key missing')
  click_xy(*kp['0']);time.sleep(.35);fs=simutil.find(W,role='AXTextField');rec['after_typed_0']=fs[0].get('value') if fs else None;shot(udid,cdir+'/002-after-typed-0.jpg')
  click_xy(*kp['Delete']);time.sleep(.35);fs=simutil.find(W,role='AXTextField');rec['after_delete_0']=fs[0].get('value') if fs else None;shot(udid,cdir+'/003-after-delete-0.jpg')
 except Exception as e:rec['exception']=repr(e);rec['trace']=traceback.format_exc()[-1000:]
 open(cdir+'/result.json','w').write(json.dumps(rec,indent=1));print(json.dumps(rec))
if __name__=='__main__':run(IPHONE if sys.argv[1]=='iphone' else IPAD,IPHONE_UDID if sys.argv[1]=='iphone' else IPAD_UDID,'/tmp/money542-iphone.db' if sys.argv[1]=='iphone' else '/tmp/money542-ipad.db')
