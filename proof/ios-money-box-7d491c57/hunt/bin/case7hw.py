import sys,os,time,json,subprocess
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
from case1 import open_filings,open_form
from case3 import launch
from case6 import setrows
from navrows import open_row_controlled
from lifelib import set_hardware,focus_window

def htype(s):
 for c in s:
  subprocess.run(['cliclick','t:'+c],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.08)
def tab(shift=False):
 if shift: subprocess.run(['cliclick','kd:shift','kp:tab','ku:shift'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 else: subprocess.run(['cliclick','kp:tab'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 time.sleep(.35)
def field(W):
 fs=simutil.find(W,role='AXTextField'); return fs[0] if fs else None
def open_rowfresh(W,udid,db,amt):
 setrows(db,[(amt,'PT010')]); launch(udid,db); open_filings(W);open_form(W,'2551Q');open_row_controlled(W);time.sleep(.4)
def run(W,udid,db):
 cdir=os.path.join(ROOT,'ipad','case7-hardware');os.makedirs(cdir,exist_ok=True); rec={'device':'ipad','case':'case7-hardware-tab-shift-tab'}
 set_hardware(W,True)
 # Tab forward into filled amount from ATC control
 open_rowfresh(W,udid,db,1234.56); focus_window(W); shot(udid,cdir+'/000-row-filled.jpg')
 # Setup focus in the amount, move backward once, then test forward Tab into the filled amount.
 f=field(W)
 if f: click_xy(round(f['pos'][0]+f['size'][0]-15),round(f['pos'][1]+f['size'][1]/2));time.sleep(.3)
 tab(True);time.sleep(.2)
 tab(False); shot(udid,cdir+'/001-after-tab-into-amount.jpg'); f=field(W); rec['tab_after_tab']=f.get('value') if f else None
 htype('15000.50');time.sleep(.3);shot(udid,cdir+'/002-tab-after-1500050.jpg');f=field(W);rec['tab_after_type']=f.get('value') if f else None
 tab(False);time.sleep(.5);rec['tab_saved']=draft_money(db);shot(udid,cdir+'/003-tab-after-blur.jpg')
 # Shift+Tab back into filled amount: focus amount as setup, Tab away, Shift+Tab back
 open_rowfresh(W,udid,db,1234.56); focus_window(W); f=field(W)
 if f: click_xy(round(f['pos'][0]+f['size'][0]-15),round(f['pos'][1]+f['size'][1]/2));time.sleep(.3)
 tab(False);shot(udid,cdir+'/010-setup-tab-away.jpg');tab(True);shot(udid,cdir+'/011-after-shift-tab-into-amount.jpg');f=field(W);rec['shift_after_shift_tab']=f.get('value') if f else None
 htype('15000.50');time.sleep(.3);shot(udid,cdir+'/012-shift-after-1500050.jpg');f=field(W);rec['shift_after_type']=f.get('value') if f else None
 tab(False);time.sleep(.5);rec['shift_saved']=draft_money(db);shot(udid,cdir+'/013-shift-after-blur.jpg')
 # Invalid comma then Tab: sentence after same-session row reopen
 open_rowfresh(W,udid,db,1000.0); focus_window(W); f=field(W)
 if f: click_xy(round(f['pos'][0]+f['size'][0]-15),round(f['pos'][1]+f['size'][1]/2));time.sleep(.3)
 # clear through hardware select-all/backspace setup, then type comma sequence
 subprocess.run(['cliclick','kd:cmd','t:a','ku:cmd'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.1);subprocess.run(['cliclick','kp:delete'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.2)
 htype('1500,50');time.sleep(.3);shot(udid,cdir+'/020-comma-before-tab.jpg');tab(False);time.sleep(.7);rec['comma_saved']=draft_money(db);shot(udid,cdir+'/021-comma-after-tab.jpg')
 open_row_controlled(W);time.sleep(.4);shot(udid,cdir+'/022-comma-row-reopened.jpg')
 texts=[n.get('desc') or '' for n in simutil.nodes(W) if n.get('role')=='AXStaticText'];rec['comma_sentence']=[t for t in texts if 'is not an amount' in t]
 rec['comma_reopen_saved']=draft_money(db);set_hardware(W,False)
 logjson(os.path.join(ROOT,'observations.jsonl'),rec);return rec
if __name__=='__main__': print(json.dumps(run(sys.argv[1],sys.argv[2],sys.argv[3]),indent=1)[:5000])
