#!/usr/bin/env python3
import sys,os,time,json
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *

WIN=IPAD; UDID=IPAD_UDID
DB='/Users/devin/Library/Developer/CoreSimulator/Devices/41A2AFE3-9E35-4EE8-BEF0-21AA02B68BC3/data/Containers/Data/Application/AFAFDA8B-1B88-41B0-8CAB-5B3E0D597490/tmp/ebirforms-door/64572-0/bir_data.db'
OUT=os.path.join(ROOT,'ipad'); LOG=os.path.join(ROOT,'observations.jsonl')
os.makedirs(OUT,exist_ok=True)

def ipad_keypad():
    out={}
    for n in simutil.find(WIN,role='AXButton'):
        d=n.get('desc') or ''
        if d in list('1234567890.'):
            out[d]=center(n)
        elif d.lower()=='delete': out['Delete']=center(n)
    return out

def clear_ipad_amount(maxdel=14):
    focus_amount_end(WIN)
    kp=ipad_keypad()
    if 'Delete' not in kp: raise RuntimeError('no keypad delete '+repr(kp))
    x,y=kp['Delete']
    for _ in range(maxdel): click_xy(x,y); time.sleep(.055)
    time.sleep(.2)

def scroll_content(up=True):
    # iPad content area in real macOS screen coordinates.
    if up:
        subprocess.run(['cliclick','dd:950,880','dm:950,700','w:80','du:950,620'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    else:
        subprocess.run(['cliclick','dd:950,620','dm:950,700','w:80','du:950,880'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    time.sleep(.35)

def open_row_sheet():
    if simutil.find(WIN,idpart='fp-table-drpATC1-done') and simutil.find(WIN,role='AXTextField'):
        return
    # collapse Return details if expanded
    if simutil.find(WIN,idpart='frm2551Qv2018:rtnMonth'):
        try: simutil.click_id(WIN,'fp-part-0-toggle',.35)
        except Exception: pass
    for attempt in range(18):
        rows=simutil.find(WIN,idpart='fp-row-drpATC1-0')
        if rows:
            y=rows[0].get('pos',[0,9999])[1]
            if 450 <= y <= 950:
                click_node(rows[0],.8)
                if simutil.find(WIN,idpart='fp-table-drpATC1-done') and simutil.find(WIN,role='AXTextField'):
                    return
            else:
                scroll_content(up=(y>950))
            continue
        tg=simutil.find(WIN,idpart='fp-part-4-toggle')
        if tg:
            y=tg[0].get('pos',[0,9999])[1]
            if 450 <= y <= 950: click_node(tg[0],.5)
            else: scroll_content(up=(y>950))
        else: scroll_content(up=True)
    raise RuntimeError('could not open row sheet')

def reopen_return():
    simutil.click_id(WIN,'tb-back',.6)
    simutil.click_id(WIN,'nav-filings',.6)
    rs=simutil.find(WIN,idpart='return-1')
    if not rs: raise RuntimeError('return-1 not found')
    click_node(rs[0],1.0)

def type_keys_real_with_shots(seq,cdir):
    taps=[]
    for i,c in enumerate(seq,1):
        kp=ipad_keypad()
        if c not in kp: raise RuntimeError('missing key '+c+' have '+repr(kp))
        x,y=kp[c]; click_xy(x,y); t=time.perf_counter(); time.sleep(.12)
        fn=os.path.join(cdir,f'key-{i:02d}-{c.replace(".","dot")}.png'); shot(UDID,fn)
        val=amount_field(WIN).get('value')
        taps.append({'key':c,'t':t,'x':x,'y':y,'shown':val,'screenshot':fn})
    for i in range(1,len(taps)): taps[i]['interval_after_prev_ms']=round((taps[i]['t']-taps[i-1]['t'])*1000,2)
    if taps: taps[0]['interval_after_prev_ms']=None
    return taps

def reset_zero():
    open_row_sheet()
    clear_ipad_amount()
    press_done(WIN); time.sleep(.5)
    return draft_money(DB)

def perform(case,seq):
    cdir=os.path.join(OUT,case); os.makedirs(cdir,exist_ok=True)
    open_row_sheet()
    clear_ipad_amount()
    press_done(WIN); time.sleep(.5)
    open_row_sheet()
    shot(UDID,os.path.join(cdir,'000-precondition-zero-unfocused.png'))
    pre=amount_field(WIN).get('value')
    focus_amount_end(WIN); time.sleep(.15)
    taps=type_keys_real_with_shots(seq,cdir)
    time.sleep(.35)
    shot(UDID,os.path.join(cdir,'010-after-typing-before-done.png'))
    press_done(WIN); time.sleep(.65)
    shot(UDID,os.path.join(cdir,'020-after-leaving-field.png'))
    saved=draft_money(DB)
    reopen_return(); shot(UDID,os.path.join(cdir,'030-after-reopening-return.png'))
    open_row_sheet(); shot(UDID,os.path.join(cdir,'031-after-reopening-row-amount.png'))
    reopen_field=amount_field(WIN).get('value')
    saved_after=draft_money(DB)
    ints=[x['interval_after_prev_ms'] for x in taps[1:]]
    return {'device':'ipad','case':case,'sequence':seq,'precondition_field':pre,'tap_times':taps,
      'tap_interval_ms':{'min':min(ints) if ints else None,'max':max(ints) if ints else None,'mean':sum(ints)/len(ints) if ints else None},
      'saved_after_leaving':saved,'shown_after_reopening_field':reopen_field,'saved_after_reopening':saved_after}

def main():
    recs=[]
    recs.append(perform('h1','15000.50'))
    recs.append({'device':'ipad','case':'h1-reset-zero-before-h2','saved':reset_zero()})
    recs.append(perform('h2','15000..50'))
    for r in recs: logjson(LOG,r)
    print(json.dumps([{k:v for k,v in r.items() if k!='tap_times'} for r in recs],indent=2))
if __name__=='__main__': main()
