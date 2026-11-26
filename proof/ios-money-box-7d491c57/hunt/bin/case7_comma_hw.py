import sys,os,time,json,subprocess,traceback
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
from lifelib import set_hardware,set_amount,amount_val,focus_window
from case1 import open_filings,open_form,wait_field,keypad_all
from case3 import launch,locale
from navrows import open_row_controlled
W=IPAD;UDID=IPAD_UDID;DB='/tmp/money7d-ipad.db'
OUT=os.path.join(ROOT,'ipad','case7-hardware-comma');os.makedirs(OUT,exist_ok=True)
def ctr(n):return (round(n['pos'][0]+n['size'][0]/2),round(n['pos'][1]+n['size'][1]/2))
def htype(s):
 for c in s:
  subprocess.run(['cliclick','t:'+c],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.13)
def done_node():return (simutil.find(W,idpart='fp-table-drpATC1-done') or [None])[0]
def finish_done(xy):
 click_xy(*xy);time.sleep(.65)
 for _ in range(3):
  d=done_node()
  if not d:break
  click_xy(*ctr(d));time.sleep(.55)
 return done_node() is None
def texts():return [n.get('desc') or '' for n in simutil.nodes(W) if n.get('role')=='AXStaticText']
def run():
 rec={'device':'ipad','case':'case7-hardware-german-comma'}
 try:
  locale(UDID,'de_DE','de');launch(UDID,DB);time.sleep(1.4);set_hardware(W,True)
  open_filings(W);time.sleep(.2);set_amount(DB,0.0);open_form(W,'2551Q');open_row_controlled(W);time.sleep(.3)
  f=wait_field(W,2);d=done_node();done_xy=ctr(d) if d else (1101,1037)
  rec['field_before']={'value':f.get('value'),'pos':f['pos'],'size':f['size']}
  focus_window(W);click_xy(round(f['pos'][0]+f['size'][0]-15),round(f['pos'][1]+f['size'][1]/2));time.sleep(.8)
  shot(UDID,OUT+'/000-zero-focused-hardware.jpg')
  htype('1500,50');time.sleep(.8);shot(UDID,OUT+'/001-after-1500-comma-50.jpg')
  rec['texts_before_tab']=[t for t in texts() if 'amount' in t.lower() or '1500' in t]
  subprocess.run(['cliclick','kp:tab'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.8)
  shot(UDID,OUT+'/002-after-hardware-tab.jpg')
  rec['sentences_after_tab']=[t for t in texts() if 'is not an amount' in t]
  rec['saved_after_tab']=amount_val(DB)
  rec['closed']=finish_done(done_xy);time.sleep(.3);shot(UDID,OUT+'/010-after-leaving.jpg');rec['saved_after_leaving']=amount_val(DB)
  open_filings(W);time.sleep(.25);open_form(W,'2551Q');open_row_controlled(W);time.sleep(.3)
  fs=simutil.find(W,role='AXTextField');rec['shown_after_reopen']=fs[0].get('value') if fs else None;rec['saved_after_reopen']=amount_val(DB);rec['sentences_after_reopen']=[t for t in texts() if 'is not an amount' in t]
  shot(UDID,OUT+'/020-after-reopen.jpg')
  # Inspect the German software decimal pad layout after the hardware test.
  set_hardware(W,False)
  f=wait_field(W,2);click_xy(round(f['pos'][0]+f['size'][0]-15),round(f['pos'][1]+f['size'][1]/2));time.sleep(1.0)
  kp=keypad_all(W);rec['german_software_keypad']=sorted(kp);rec['software_dot_offered']='.' in kp;rec['software_comma_offered']=',' in kp
  labels=[n.get('desc') or '' for n in simutil.nodes(W) if n.get('role')=='AXButton']
  rec['globe_or_layout_labels']=[x for x in labels if 'globe' in x.lower() or 'keyboard' in x.lower() or 'layout' in x.lower()]
  shot(UDID,OUT+'/030-german-software-keypad.jpg')
 except Exception as e:
  rec['exception']=repr(e);rec['trace']=traceback.format_exc()[-1400:]
  try:shot(UDID,OUT+'/099-exception.jpg')
  except Exception:pass
 finally:
  locale(UDID,'en_PH','en')
 with open(OUT+'/result.json','w') as fh:json.dump(rec,fh,indent=1)
 logjson(os.path.join(ROOT,'observations.jsonl'),rec);print(json.dumps(rec))
if __name__=='__main__':run()
