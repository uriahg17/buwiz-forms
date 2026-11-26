import sys,os,time,json,sqlite3,subprocess
sys.path.insert(0,'/Users/devin/moneybox-d4f2852a/helpers/bin')
sys.path.insert(0,'/Users/devin/moneybox-d4f2852a/proof/ios-money-box-d4f2852a/bin')
import simutil,b1
from huntlib import *
from case1 import open_filings,open_form
from navrows import small_scroll
ROOTP='/Users/devin/moneybox-d4f2852a/proof/ios-money-box-d4f2852a/b1-strict'
ROWS=[(1000,'PT010'),(2000,'PT040'),(3000,'PT010')]

def setrows(db):
    b1.setrows(db)
    con=sqlite3.connect(db); row=con.execute("select id,data_json from form_drafts where form_code='2551Q'").fetchone(); j=json.loads(row[1])
    total=round(sum(r['tax_due'] for r in j['schedule_1']),2)
    j['total_tax_due']=total; j['tax_payable']=total; j['total_amount_payable']=total
    j['total_tax_credits']=0.0; j['total_penalties']=0.0; j['surcharge']=0.0; j['interest']=0.0; j['compromise']=0.0; j['creditable_tax_withheld']=0.0; j['tax_paid_previous']=0.0; j['other_tax_credit']=0.0; j['penalty_overrides']={}
    con.execute('update form_drafts set data_json=? where id=?',(json.dumps(j),row[0]));con.commit();con.close()

def draft(db):
    return json.loads(sqlite3.connect(db).execute("select data_json from form_drafts where form_code='2551Q'").fetchone()[0])

def rowsdb(db):
    return draft(db).get('schedule_1',[])

def details(db,idx):
    j=draft(db); rows=j.get('schedule_1') or []
    slot=rows[idx] if idx < len(rows) else None
    return {
      'row_count':len(rows),'rows':rows,
      'nonblank_rows':[r for r in rows if r.get('atc')],
      'deleted_slot_index':idx,'deleted_slot_exists':slot is not None,
      'deleted_slot_keys':sorted(slot.keys()) if isinstance(slot,dict) else [],
      'deleted_slot_object':slot,
      'totals':{k:j.get(k) for k in ['total_tax_due','tax_payable','total_tax_credits','total_penalties','total_amount_payable','surcharge','interest','compromise']}
    }

def screen_state(W):
    rownodes=[n for n in simutil.nodes(W) if (n.get('id') or '').startswith('fp-row-drpATC1-')]
    texts=[]
    for n in simutil.nodes(W):
        if n.get('role')=='AXStaticText':
            s=n.get('desc') or n.get('value') or n.get('title') or ''
            if s and n.get('pos') and 300<n['pos'][1]<1000: texts.append({'text':s,'pos':n.get('pos'),'id':n.get('id')})
    return {'row_ids':[(n.get('id'),n.get('pos'),n.get('size')) for n in rownodes], 'texts':texts}

def evaluate(rec):
    idx=rec['row_index']; expected=[1000.0,3000.0] if idx==1 else [1000.0,2000.0]
    rows=rec['draft_after_reopen']['rows']
    nonblank=rec['draft_after_reopen']['nonblank_rows']
    amounts=[r.get('taxable_amount') for r in nonblank]
    # Physical removal (two rows) or a retained blank deleted object with no taxable_amount key both satisfy the draft-side no-amount requirement.
    slotok=len(rows)==2 or (idx < len(rows) and not rows[idx].get('atc') and 'taxable_amount' not in rows[idx])
    total_expected=120.0 if idx==1 else 90.0
    totals=rec['draft_after_reopen']['totals']
    totok=totals.get('total_tax_due')==total_expected and totals.get('tax_payable')==total_expected and totals.get('total_amount_payable')==total_expected
    rec['expected_remaining_amounts']=expected
    rec['nonblank_amounts_after_reopen']=amounts
    rec['draft_rows_ok']=amounts==expected
    rec['deleted_slot_no_amount_ok']=slotok
    rec['totals_ok']=totok
    rec['strict_draft_pass']=rec['draft_rows_ok'] and slotok and totok
    return rec

def finish(rec,cdir,W,udid,db,idx):
    time.sleep(2.1);shot(udid,cdir+'/002-after-delete.jpg')
    rec['draft_after_delete']=details(db,idx);rec['screen_after_delete']=screen_state(W)
    open_filings(W);time.sleep(.55);open_form(W,'2551Q');time.sleep(.95)
    # make rows visible before the reopening evidence shot when possible
    try: b1.expand_rows(W)
    except Exception: pass
    shot(udid,cdir+'/003-after-reopen.jpg')
    rec['draft_after_reopen']=details(db,idx);rec['screen_after_reopen']=screen_state(W)
    evaluate(rec);open(cdir+'/result.json','w').write(json.dumps(rec,indent=1));return rec

def run_iphone(idx,runno,control=False,video=False):
    W=IPHONE;udid=IPHONE_UDID;db='/tmp/moneyd4-iphone.db'
    sub='iphone';cdir=f'{ROOTP}/{sub}/{"control" if control else "row"+str(idx+1)}-r{runno}';os.makedirs(cdir,exist_ok=True)
    p=None
    if video:
        p=subprocess.Popen(['xcrun','simctl','io',udid,'recordVideo','--force','--codec=h264',cdir+'/b1.mp4'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.8)
    try:
        setrows(db);b1.launch(udid,db);time.sleep(1.5);open_filings(W);open_form(W,'2551Q');time.sleep(.7);b1.click_row(W,idx)
        tlast,kb,predel=b1.clear_type(W,'500')
        if control:
            dn=simutil.find(W,idpart='fp-table-drpATC1-done')
            if not dn: raise RuntimeError('Done missing control')
            click_node(dn[0],1.1);b1.click_row(W,idx)
        kd=(simutil.find(W,idpart='fp-table-drpATC1-delete') if control else ([predel] if predel else []))
        if not kd: raise RuntimeError('Delete row not exposed/hittable while keyboard up')
        d=kd[0]
        rec={'device':sub,'row_index':idx,'run':runno,'control':control,'keyboard_visible':bool(kb),'delete_frame':{'pos':d.get('pos'),'size':d.get('size')},'keyboard_key1':kb.get('1')}
        nowkp=keypad(W)
        rec['keyboard_visible_at_delete']=bool(nowkp)
        rec['delete_above_keyboard']=((d['pos'][1]+d['size'][1]) < (nowkp['1'][1]-27)) if nowkp else True
        if not rec['delete_above_keyboard']: raise RuntimeError('Delete row is not verified above keyboard')
        xy=center(d);t0=time.time();click_xy(*xy);t1=time.time();rec['delete_click_xy']=xy;rec['last_type_to_delete_ms']=round((t0-tlast)*1000,1);rec['last_type_to_delete_done_ms']=round((t1-tlast)*1000,1)
        time.sleep(.05);shot(udid,cdir+'/001-just-after-delete-click.jpg')
        return finish(rec,cdir,W,udid,db,idx)
    finally:
        if p:
            p.send_signal(2)
            try:p.wait(5)
            except: p.kill()

def close_any_sheet(W):
    x=simutil.find(W,idpart='fp-table-drpATC1-done')
    if x: click_node(x[0],.6); return
    c=[n for n in simutil.nodes(W) if n.get('role')=='AXButton' and (n.get('desc') or '')=='Close']
    if c: click_node(c[0],.5)

def reset_ipad():
    W=IPAD;db='/tmp/moneyd4-ipad.db'
    close_any_sheet(W);open_filings(W);time.sleep(.5);setrows(db);open_form(W,'2551Q');time.sleep(.8)

def docked_keypad(W):
    kp=keypad(W)
    return kp if kp and kp.get('1')==(612,861) and 'Delete' in kp else None

def make_docked_if_needed(W):
    kp=keypad(W)
    if kp and kp.get('1')==(1064,718):
        subprocess.run(['cliclick','dd:1015,850','dm:980,890','dm:900,930','dm:800,960','du:700,990'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        time.sleep(.7)
        f=simutil.find(W,role='AXTextField')
        if f:
            x=round(f[0]['pos'][0]+f[0]['size'][0]-2);y=round(f[0]['pos'][1]+f[0]['size'][1]/2);click_xy(x,y);time.sleep(1)

def ipad_focus_type(W,seq):
    f=simutil.find(W,role='AXTextField')
    if not f: raise RuntimeError('no amount field')
    f=f[0];x=round(f['pos'][0]+f['size'][0]-2);y=round(f['pos'][1]+f['size'][1]/2)
    kp=None
    for _ in range(3):
        click_xy(x,y);time.sleep(1);make_docked_if_needed(W);kp=docked_keypad(W)
        if kp: break
    if not kp: raise RuntimeError('docked full-width keypad not visible: '+repr(keypad(W)))
    kd=simutil.find(W,idpart='fp-table-drpATC1-delete')
    done=simutil.find(W,idpart='fp-table-drpATC1-done')
    if not kd: raise RuntimeError('Delete row not exposed with docked keyboard')
    for _ in range(9): click_xy(*kp['Delete']);time.sleep(.07)
    time.sleep(.15);tlast=None
    for i,c in enumerate(seq):
        click_xy(*kp[c]);tlast=time.time()
        if i<len(seq)-1:time.sleep(.14)
    return tlast,kp,kd[0],(done[0] if done else None)

def run_ipad(idx,runno,control=False,video=False):
    W=IPAD;udid=IPAD_UDID;db='/tmp/moneyd4-ipad.db'
    cdir=f'{ROOTP}/ipad/{"control" if control else "row"+str(idx+1)}-r{runno}';os.makedirs(cdir,exist_ok=True)
    p=None
    if video:
        p=subprocess.Popen(['xcrun','simctl','io',udid,'recordVideo','--force','--codec=h264',cdir+'/b1.mp4'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.8)
    try:
        reset_ipad();b1.click_row(W,idx);tlast,kp,delnode,donenode=ipad_focus_type(W,'500')
        rec={'device':'ipad','row_index':idx,'run':runno,'control':control,'docked_keypad':True,'delete_frame':{'pos':delnode.get('pos'),'size':delnode.get('size')},'keyboard_key1':kp.get('1'),'keyboard_delete':kp.get('Delete')}
        nowkp=keypad(W)
        rec['keyboard_visible_at_delete']=bool(nowkp)
        rec['delete_above_keyboard']=((delnode['pos'][1]+delnode['size'][1]) < (nowkp['1'][1]-27)) if nowkp else True
        if not rec['delete_above_keyboard']: raise RuntimeError('Delete row is not verified above docked keyboard')
        if control:
            if not donenode: raise RuntimeError('Done missing control')
            click_node(donenode[0] if isinstance(donenode,list) else donenode,1.1);b1.click_row(W,idx)
            kd=simutil.find(W,idpart='fp-table-drpATC1-delete')
            if not kd: raise RuntimeError('control delete missing after reopen')
            delnode=kd[0]
        xy=center(delnode);t0=time.time();click_xy(*xy);t1=time.time();rec['delete_click_xy']=xy;rec['last_type_to_delete_ms']=round((t0-tlast)*1000,1);rec['last_type_to_delete_done_ms']=round((t1-tlast)*1000,1)
        time.sleep(.05);shot(udid,cdir+'/001-just-after-delete-click.jpg')
        return finish(rec,cdir,W,udid,db,idx)
    finally:
        if p:
            p.send_signal(2)
            try:p.wait(5)
            except: p.kill()

def main():
    mode=sys.argv[1] if len(sys.argv)>1 else 'all'
    out=[]
    if mode in ('iphone','all'):
        for idx in (1,2):
            for r in (1,2,3):out.append(run_iphone(idx,r,video=(idx==1 and r==1)))
        out.append(run_iphone(1,1,control=True))
    if mode in ('ipad','all'):
        for idx in (1,2):
            for r in (1,2,3):out.append(run_ipad(idx,r,video=(idx==1 and r==1)))
        out.append(run_ipad(1,1,control=True))
    print(json.dumps(out))
if __name__=='__main__':main()
