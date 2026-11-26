#!/usr/bin/env python3
import sys,os,time,json,sqlite3,subprocess,re
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *

def open_filings(W):
    if simutil.find(W,idpart='fp-table-drpATC1-done'):
        press_done(W); time.sleep(.3)
    if simutil.find(W,idpart='nb-back') or simutil.find(W,idpart='tb-back'):
        for bid in ('nb-back','tb-back'):
            xs=simutil.find(W,idpart=bid)
            if xs: click_node(xs[0],.5); break
    for tid in ('tab-filings','nav-filings'):
        xs=simutil.find(W,idpart=tid)
        if xs: click_node(xs[0],.6); break

def open_form(W,code):
    open_filings(W)
    wanted='return-1' if code=='2551Q' else 'return-2'
    for _ in range(16):
        xs=[n for n in simutil.find(W,role='AXButton') if n.get('id')==wanted or code in (n.get('desc') or '')]
        if xs:
            click_node(xs[0],.7); return
        time.sleep(.2)
    raise RuntimeError('form not found '+code)

def update_2551q(db,amount):
    con=sqlite3.connect(db,timeout=2)
    row=con.execute("select id,data_json from form_drafts where form_code='2551Q'").fetchone()
    j=json.loads(row[1]); rows=j.get('schedule_1') or []
    if not rows: rows=[{'atc':'PT010','atc_description':'Persons exempt from VAT under Sec. 109(BB) [Sec. 116]','tax_rate':0.03}]
    rows[0]['taxable_amount']=amount
    rows[0]['tax_due']=round(amount*0.03,2)
    j['schedule_1']=rows; j['total_tax_due']=round(amount*0.03,2)
    con.execute('update form_drafts set data_json=? where id=?',(json.dumps(j),row[0])); con.commit(); con.close()

def keypad_all(W):
    out=keypad(W)
    for n in simutil.find(W,role='AXButton'):
        d=n.get('desc') or ''
        if d==',' and n.get('pos'): out[',']=center(n)
    return out

def wait_field(W,timeout=1.5):
    end=time.time()+timeout
    while time.time()<end:
        fs=simutil.find(W,role='AXTextField')
        if fs: return fs[0]
        time.sleep(.08)
    raise RuntimeError('no field')

def type_keys_real(W,udid,seq,cdir,interval=.16,shots=True):
    rec=[]
    for i,c in enumerate(seq,1):
        kp=keypad_all(W)
        if c not in kp: raise RuntimeError('missing '+c+' keypad '+repr(kp))
        x,y=kp[c]; click_xy(x,y); time.sleep(interval*.55)
        f=wait_field(W)
        fn=os.path.join(cdir,f'key-{i:02d}-{c.replace(".","dot").replace(",","comma")}.jpg')
        if shots: shot(udid,fn)
        rec.append({'key':c,'x':x,'y':y,'shown':f.get('value'),'screenshot':fn if shots else None,'t':time.time()})
    return rec

def fast_keys(W,seq,spacing_ms=50):
    kp=keypad_all(W)
    args=[]
    for c in seq:
        x,y=kp[c]; args += [str(x),str(y),str(spacing_ms)]
    t0=time.time(); cp=subprocess.run(['/tmp/fastclick']+args,text=True,capture_output=True); t1=time.time()
    lines=cp.stdout.splitlines(); clicks=[]
    for line in lines:
        if line.startswith('click '): clicks.append({'at_usec':int(line.split()[1]),'done_usec':int(line.split()[2]),'x':int(line.split()[3]),'y':int(line.split()[4])})
    for j in range(1,len(clicks)): clicks[j]['interval_ms']=(clicks[j]['at_usec']-clicks[j-1]['done_usec'])/1000
    return {'process_ms':(t1-t0)*1000,'stdout':lines,'clicks':clicks,'stderr':cp.stderr,'nominal_spacing_ms':spacing_ms}

def reopen_form(W,code):
    open_filings(W); open_form(W,code)

def money_case1(device,udid,db,fast=False):
    W=device; outsub='iphone' if device==IPHONE else 'ipad'; base=os.path.join(ROOT,outsub,'case1'); os.makedirs(base,exist_ok=True)
    results=[]
    values=(__import__('os').environ.get('CASE1_VALUES','0.50,1234.56,99999.99,100000,1000000.01,12345678.90,99999999.99').split(',')) if not fast else []
    if not fast:
      for val in values:
        cdir=os.path.join(base,'value-'+val.replace('.','p')); os.makedirs(cdir,exist_ok=True)
        open_filings(W); update_2551q(db,0.0); open_form(W,'2551Q'); ensure_row_sheet(W)
        shot(udid,os.path.join(cdir,'000-zero-unfocused.jpg'))
        pre=wait_field(W).get('value')
        focus_amount_end(W); time.sleep(.2)
        keys=type_keys_real(W,udid,val,cdir)
        shot(udid,os.path.join(cdir,'010-after-typing.jpg'))
        press_done(W); time.sleep(.7)
        shot(udid,os.path.join(cdir,'020-after-leaving.jpg'))
        saved=draft_money(db)
        reopen_form(W,'2551Q')
        shot(udid,os.path.join(cdir,'030-after-reopening-return.jpg'))
        ensure_row_sheet(W); time.sleep(.3)
        shown=wait_field(W).get('value')
        shot(udid,os.path.join(cdir,'031-after-reopening-row.jpg'))
        rec={'device':outsub,'case':'case1-value','typed':val,'precondition':pre,'keys':keys,'saved_after_leaving':saved,'shown_after_reopening':shown,'saved_after_reopening':draft_money(db)}
        logjson(os.path.join(ROOT,'observations.jsonl'),rec); results.append(rec)
    else:
      # Fast runs. Reset zero outside form each time; continuous video across all runs.
      video=os.path.join(ROOT,outsub,'case1-fast-ten.mp4'); p,t0,banner=start_video(udid,video)
      try:
       for run in range(1,11):
        cdir=os.path.join(base,f'fast-{run:02d}'); os.makedirs(cdir,exist_ok=True)
        open_filings(W); update_2551q(db,0.0); open_form(W,'2551Q'); ensure_row_sheet(W)
        pre=wait_field(W).get('value'); focus_amount_end(W); time.sleep(.2)
        timing=fast_keys(W,'15000.50',50)
        time.sleep(.3); shown_before=wait_field(W).get('value')
        shot(udid,os.path.join(cdir,'010-after-typing.jpg'))
        press_done(W); time.sleep(.7); shot(udid,os.path.join(cdir,'020-after-leaving.jpg'))
        saved=draft_money(db)
        reopen_form(W,'2551Q'); ensure_row_sheet(W); shown=wait_field(W).get('value')
        shot(udid,os.path.join(cdir,'030-after-reopening-row.jpg'))
        rec={'device':outsub,'case':'case1-fast','run':run,'typed':'15000.50','precondition':pre,'timing':timing,'shown_before_leaving':shown_before,'saved_after_leaving':saved,'shown_after_reopening':shown,'saved_after_reopening':draft_money(db),'misplaced_point':shown_before not in ('15000.50','15,000.50')}
        logjson(os.path.join(ROOT,'observations.jsonl'),rec); results.append(rec)
      finally: stop_video(p)
    return results

if __name__=='__main__':
    device=sys.argv[1]; udid=sys.argv[2]; db=sys.argv[3]; mode=sys.argv[4] if len(sys.argv)>4 else 'slow'
    print(json.dumps(money_case1(device,udid,db,fast=(mode=='fast')),indent=1)[:8000])
