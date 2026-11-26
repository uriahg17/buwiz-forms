#!/usr/bin/env python3
import sys,os,time,json
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
WIN=IPHONE; UDID=IPHONE_UDID
DB='/Users/devin/Library/Developer/CoreSimulator/Devices/405F45A9-B471-47B7-A5D9-E545EA624713/data/Containers/Data/Application/0973CEBB-8D01-4458-8873-616214E0F25C/tmp/ebirforms-door/60325-0/bir_data.db'
cdir=os.path.join(ROOT,'iphone','h5'); os.makedirs(cdir,exist_ok=True)
LOG=os.path.join(ROOT,'observations.jsonl')

def key_tap(k):
    kp=keypad(WIN); x,y=kp[k]; click_xy(x,y); time.sleep(.12)

def fieldval():
    try: return amount_field(WIN).get('value')
    except Exception: return None

def reopen_return():
    simutil.click_id(WIN,'nb-back',.5)
    simutil.click_id(WIN,'tab-filings',.5)
    rs=simutil.find(WIN,idpart='return-1')
    click_node(rs[0],.9)

rec={'device':'iphone','case':'h5','sequence':'123 then Home 5s then 4','keys':[]}
ensure_row_sheet(WIN)
# clear whatever amount is there using real keypad delete, then type 123 through real keypad taps
clear_amount_real(WIN)
shot(UDID,os.path.join(cdir,'000-empty-after-real-delete.png'))
for i,k in enumerate('123',1):
    key_tap(k)
    fn=os.path.join(cdir,f'key-{i:02d}-{k}.png'); shot(UDID,fn)
    rec['keys'].append({'key':k,'shown':fieldval(),'screenshot':fn})
# Home through the simulator's own Home button, wait five seconds, return through the visible NshDev icon
home=[x for x in simutil.find(WIN,text='Home',role='AXButton') if x.get('pos') and x['pos'][1]<150][0]
click_node(home,0)
time.sleep(5)
shot(UDID,os.path.join(cdir,'010-home-after-5s.png'))
app=simutil.find(WIN,text='NshDev',role='AXButton')[0]
click_node(app,1.0)
shot(UDID,os.path.join(cdir,'020-resumed-before-4.png'))
rec['shown_after_resume']=fieldval()
key_tap('4')
fn=os.path.join(cdir,'key-04-4.png'); shot(UDID,fn)
rec['keys'].append({'key':'4','shown':fieldval(),'screenshot':fn,'after':'home-resume'})
press_done(WIN); time.sleep(.5)
shot(UDID,os.path.join(cdir,'030-after-leaving-field.png'))
rec['shown_after_leaving_row_texts']=[x.get('desc') or '' for x in simutil.find(WIN,idpart='fp-row-drpATC')]
rec['saved_after_leaving']=draft_money(DB)
reopen_return()
shot(UDID,os.path.join(cdir,'040-after-reopening-return.png'))
ensure_row_sheet(WIN)
shot(UDID,os.path.join(cdir,'041-after-reopening-row-amount.png'))
rec['shown_after_reopening_field']=fieldval()
rec['saved_after_reopening']=draft_money(DB)
logjson(LOG,rec)
print(json.dumps(rec,indent=2))
