import sys,os,time,json,sqlite3,subprocess
sys.path.insert(0,'/Users/devin/moneybox-7d491c57/proof/ios-money-box-7d491c57/hunt/bin')
import simutil
from huntlib import *
from case3 import launch
from lifelib import set_hardware
from case4manual import reset2550,vals,open_return2,nav_13a
W=IPAD;UDID='41A2AFE3-9E35-4EE8-BEF0-21AA02B68BC3';DB='/tmp/money7d-ipad.db'
OUT='/Users/devin/moneybox-7d491c57/proof/ios-money-box-7d491c57/ipad-reselect'
LOG=OUT+'/exp-run-current.log'
def fka(v):
 subprocess.run(['xcrun','simctl','spawn',UDID,'defaults','write','com.apple.Accessibility','FullKeyboardAccessEnabled','-bool','true' if v else 'false'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.4)
def field13a():
 st=next((n for n in simutil.nodes(W) if n.get('role')=='AXStaticText' and (n.get('desc') or '')=='13A'),None)
 if not st:raise RuntimeError('13A label missing')
 fs=[n for n in simutil.nodes(W) if n.get('role')=='AXTextField' and n.get('pos') and st['pos'][1]-10<n['pos'][1]<st['pos'][1]+90]
 if fs:return fs[0]
 fs=[n for n in simutil.nodes(W) if n.get('role')=='AXTextField' and n.get('pos') and abs(n['pos'][1]-st['pos'][1])<100]
 if fs:return fs[0]
 raise RuntimeError('13A field missing '+repr([(n.get('value'),n.get('pos')) for n in simutil.nodes(W) if n.get('role')=='AXTextField']))
def type100():
 f=field13a();click_node(f,.7)
 kp=keypad(W)
 if not kp:raise RuntimeError('software keypad missing')
 for ch in '100':click_xy(*kp[ch]);time.sleep(.17)
def run_unmodified():
 reset2550(DB);launch(UDID,DB);time.sleep(1.2);fka(True);set_hardware(W,False)
 open_return2(W);nav_13a(W);shot(UDID,OUT+'/unmodified-000-13a.jpg')
 mark=os.path.getsize(LOG) if os.path.exists(LOG) else 0
 type100();time.sleep(1.0);shot(UDID,OUT+'/unmodified-001-after100.jpg')
 set_hardware(W,True);time.sleep(.4)
 t0=time.time();subprocess.run(['cliclick','kp:tab'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1.0);shot(UDID,OUT+'/unmodified-002-after-tab.jpg')
 subprocess.run(['cliclick','t:5'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.8);shot(UDID,OUT+'/unmodified-003-after5.jpg')
 subprocess.run(['cliclick','kp:tab'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.8)
 time.sleep(1);seg=open(LOG,errors='replace').read()[mark:]
 open(OUT+'/unmodified-trace.log','w').write(seg)
 rec={'fka':True,'vals_end':vals(DB),'trace_lines':[x for x in seg.splitlines() if 'RESELECT_TRACE' in x]}
 open(OUT+'/unmodified-result.json','w').write(json.dumps(rec,indent=1))
 print(json.dumps(rec,indent=1))
if __name__=='__main__':run_unmodified()
