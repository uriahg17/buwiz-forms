import sys,os,time,json,sqlite3,subprocess
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
from case1 import open_filings,open_form,keypad,wait_field
from navrows import open_row_controlled
from case3 import launch,locale
LROOT='/Users/devin/moneybox-7d491c57/proof/ios-money-box-7d491c57/lifecycle'
def outsub(W): return 'iphone' if W==IPHONE else 'ipad'
def focus_window(W): subprocess.run(['osascript','/tmp/focus_sim.scpt',W],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.25)
def home(W):
 focus_window(W); subprocess.run(['cliclick','kd:cmd,shift','t:h','ku:cmd,shift'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.8)
def app_switcher(W):
 focus_window(W)
 subprocess.run(['osascript','-e','tell application "System Events" to tell process "Simulator" to click menu item "App Switcher" of menu "Device" of menu bar item "Device" of menu bar 1'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 time.sleep(.9)
def switcher_other(W):
 # The other app is the left card in the two-card switcher. Navigation/setup click only.
 x,y=(180,600) if W==IPHONE else (1078,734)
 click_xy(x,y); time.sleep(1.0)
def hardware_state():
 cp=subprocess.run(['osascript','-e','tell application "System Events" to tell process "Simulator" to get value of attribute "AXMenuItemMarkChar" of menu item "Connect Hardware Keyboard" of menu "Keyboard" of menu item "Keyboard" of menu "I/O" of menu bar 1'],text=True,capture_output=True)
 return '✓' in cp.stdout
def set_hardware(W,on):
 focus_window(W)
 cur=hardware_state()
 if cur!=on:
  subprocess.run(['osascript','-e','tell application "System Events" to tell process "Simulator" to click menu item "Connect Hardware Keyboard" of menu "Keyboard" of menu item "Keyboard" of menu "I/O" of menu bar 1'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
  time.sleep(.5)
def set_amount(db,amount):
 con=sqlite3.connect(db,timeout=2); row=con.execute("select id,data_json from form_drafts where form_code='2551Q'").fetchone(); j=json.loads(row[1])
 tax=round(amount*.03,2); j['schedule_1']=[{'atc':'PT010','atc_description':'PERSON EXEMPT FROM VAT UNDER SEC. 109(BB) (SEC. 116)','taxable_amount':amount,'tax_rate':3.0,'tax_due':tax}]
 j['total_taxable_amount']=amount; j['total_tax_due']=tax
 con.execute('update form_drafts set data_json=? where id=?',(json.dumps(j),row[0])); con.commit(); con.close()
def amount_val(db):
 return draft_money(db).get('taxable_amount')
def numeric(s):
 if s in (None,''): return None
 try: return float(str(s).replace(',',''))
 except Exception: return None
def open_amount(W,db,amount):
 open_filings(W); time.sleep(.25); set_amount(db,amount); open_form(W,'2551Q'); open_row_controlled(W); time.sleep(.25)
def focus_amount(W):
 f=wait_field(W,2); x=round(f['pos'][0]+f['size'][0]-12); y=round(f['pos'][1]+f['size'][1]/2); click_xy(x,y); time.sleep(.3); return f
def blur_atc(W):
 tr=simutil.find(W,idpart='fp-drpATC1-trigger')
 if tr: click_node(tr[0],.7)
 else: press_done(W); return
 # Close the picker without changing it; blur/save has already happened.
 time.sleep(.2)
 cls=[n for n in simutil.nodes(W) if n.get('role')=='AXButton' and (n.get('desc') or '')=='Close']
 if cls: click_node(cls[0],.5)
 else: subprocess.run(['cliclick','kp:esc'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.4)
def finish_reopen(W,udid,db,cdir,prefix):
 press_done(W); time.sleep(.4); afterleave=amount_val(db); shot(udid,os.path.join(cdir,prefix+'-after-leaving.jpg'))
 open_filings(W); time.sleep(.15); open_form(W,'2551Q'); open_row_controlled(W); time.sleep(.15); shot(udid,os.path.join(cdir,prefix+'-after-reopen.jpg'))
 fs=simutil.find(W,role='AXTextField'); return {'saved_after_leaving':afterleave,'shown_after_reopen':fs[0].get('value') if fs else None,'saved_after_reopen':amount_val(db)}
def loglife(rec):
 os.makedirs(LROOT,exist_ok=True); logjson(os.path.join(LROOT,'observations.jsonl'),rec)
def reset_english(udid,db):
 locale(udid,'en_PH','en'); launch(udid,db)
