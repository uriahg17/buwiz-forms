#!/usr/bin/env python3
import sys,os,time,json
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *

def keypad_comma(win):
    out=keypad(win)
    for n in simutil.find(win,role='AXButton'):
        d=n.get('desc') or ''
        if d==',' and n.get('pos') and n['pos'][1]>650: out[',']=center(n)
    return out

def run(device,udid,db,outsub):
    WIN=device; croot=os.path.join(ROOT,outsub,'h3'); os.makedirs(croot,exist_ok=True)
    open_row=(lambda: open_row())
    clear_real=(lambda: clear_real())
    if device==IPAD:
        import run_h1h2_ipad as ipadbase
        open_row=(lambda: ipadbase.open_row_sheet())
        clear_real=(lambda: ipadbase.clear_ipad_amount())
    def reopen_return():
        simutil.click_id(WIN,'nb-back' if device==IPHONE else 'tb-back',.5)
        simutil.click_id(WIN,'tab-filings' if device==IPHONE else 'nav-filings',.5)
        rs=simutil.find(WIN,idpart='return-1')
        if not rs: raise RuntimeError('return-1 missing')
        click_node(rs[0],1.0)
    def type_seq(seq,cdir):
        rec=[]
        for i,c in enumerate(seq,1):
            kp=keypad_comma(WIN)
            if c not in kp: raise RuntimeError('missing key '+c+' keys '+repr(kp))
            x,y=kp[c]; click_xy(x,y); time.sleep(.16)
            fn=os.path.join(cdir,f'key-{i:02d}-{c.replace(",","comma").replace(".","dot")}.png'); shot(udid,fn)
            rec.append({'key':c,'shown':amount_field(WIN).get('value'),'screenshot':fn})
        return rec
    def reset_zero():
        open_row()
        clear_real()
        press_done(WIN); time.sleep(.5)
        open_row()
    def perform(name,seq):
        cdir=os.path.join(croot,name); os.makedirs(cdir,exist_ok=True)
        reset_zero()
        shot(udid,os.path.join(cdir,'000-zero-unfocused.png'))
        pre=amount_field(WIN).get('value')
        focus_amount_end(WIN); time.sleep(.15)
        keys=type_seq(seq,cdir)
        shot(udid,os.path.join(cdir,'010-after-typing.png'))
        press_done(WIN); time.sleep(.6)
        shot(udid,os.path.join(cdir,'020-after-leaving.png'))
        saved=draft_money(db)
        reopen_return(); shot(udid,os.path.join(cdir,'030-after-reopening-return.png'))
        open_row(); shot(udid,os.path.join(cdir,'031-after-reopening-row.png'))
        reopenv=amount_field(WIN).get('value')
        return {'case':'h3-'+name,'device':'iphone' if device==IPHONE else 'ipad','sequence':seq,'precondition_field':pre,'keys':keys,'saved_after_leaving':saved,'shown_after_reopening_field':reopenv,'saved_after_reopening':draft_money(db)}
    # enter existing draft and row sheet
    nav='tab-filings' if device==IPHONE else 'nav-filings'
    if simutil.find(WIN,idpart=nav):
        simutil.click_id(WIN,nav,.6)
        rs=simutil.find(WIN,idpart='return-1')
        if rs: click_node(rs[0],1.0)
    open_row()
    focus_amount_end(WIN); time.sleep(.2)
    kp=keypad_comma(WIN)
    kb={d:(n.get('pos')) for n in simutil.find(WIN,role='AXButton') for d in [n.get('desc') or ''] if n.get('pos') and n['pos'][1]>650}
    shot(udid,os.path.join(croot,'000-regional-decimal-pad.png'))
    rec={'case':'h3-keypad','device':'iphone' if device==IPHONE else 'ipad','keyboard_labels':kb,'comma_offered':',' in kp,'dot_offered':'.' in kp}
    logjson(os.path.join(ROOT,'observations.jsonl'),rec)
    results=[rec]
    for name,seq in [('comma-decimal','1500,50'),('lone-comma',',')]:
        r=perform(name,seq); logjson(os.path.join(ROOT,'observations.jsonl'),r); results.append(r)
    # dot grouping sequence is only applicable when both marks are physically offered
    if ',' in kp and '.' in kp:
        r=perform('dot-grouped-comma-decimal','1.234,56'); logjson(os.path.join(ROOT,'observations.jsonl'),r); results.append(r)
    else:
        r={'case':'h3-dot-grouped-comma-decimal','device':'iphone' if device==IPHONE else 'ipad','untested':'dot key not offered on regional decimal pad, so 1.234,56 cannot be typed through the pad'}
        logjson(os.path.join(ROOT,'observations.jsonl'),r); results.append(r)
    print(json.dumps(results,indent=2))
