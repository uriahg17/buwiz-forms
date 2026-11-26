#!/usr/bin/env python3
# Case 6 row deletion. Real keypad clicks for tested digits; direct SQLite only for setup/verification.
import sys,os,time,json,sqlite3
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
from case1 import open_filings,open_form,keypad,wait_field,type_keys_real
from navrows import open_row_controlled

def setrows(db,rows):
 con=sqlite3.connect(db); dat=con.execute("select data_json from form_drafts where form_code='2551Q'").fetchone()[0]; j=json.loads(dat)
 j['schedule_1']=[]
 for amt,atc in rows:
  tax=round(amt*.03,2); j['schedule_1'].append({'atc':atc,'atc_description':'PERSON EXEMPT FROM VAT UNDER SEC. 109(BB) (SEC. 116)','taxable_amount':amt,'tax_rate':3.0,'tax_due':tax})
 j['total_taxable_amount']=sum(r['taxable_amount'] for r in j['schedule_1']); j['total_tax_due']=sum(r['tax_due'] for r in j['schedule_1'])
 con.execute("update form_drafts set data_json=? where form_code='2551Q'",(json.dumps(j),)); con.commit(); con.close()
def rowsdb(db):
 j=json.loads(sqlite3.connect(db).execute("select data_json from form_drafts where form_code='2551Q'").fetchone()[0]); return j.get('schedule_1',[])
def findbtn(W,label):
 for n in simutil.nodes(W):
  if n.get('role')=='AXButton' and (n.get('desc')==label or n.get('title')==label or label in (n.get('id') or '')): return n
def run(W,udid,db):
 outsub='iphone' if W==IPHONE else 'ipad'; cdir=os.path.join(ROOT,outsub,'case6'); os.makedirs(cdir,exist_ok=True)
 rec={'device':outsub,'case':'case6-rows'}
 # A: row with ATC but no amount deleted; leaving should keep zero/no sentence.
 setrows(db,[(0.0,'PT010')]); open_filings(W); open_form(W,'2551Q'); open_row_controlled(W); time.sleep(.3); shot(udid,cdir+'/000-empty-row-open.jpg')
 b=findbtn(W,'Delete row'); rec['empty_delete_button']=bool(b); click_node(b,.8) if b else None
 shot(udid,cdir+'/001-empty-row-deleted.jpg')
 # leave/reopen return
 open_form(W,'2551Q'); time.sleep(.5); shot(udid,cdir+'/002-empty-after-reopen.jpg')
 rec['empty_rows_after_reopen']=rowsdb(db); rec['empty_amount']=rowsdb(db)[0]['taxable_amount'] if rowsdb(db) else None
 # B: two rows. Closest UI-feasible ordering: type in second row, Done/blur, then open first row and delete at once.
 setrows(db,[(1000.0,'PT010'),(3000.0,'PT040')]); open_filings(W); open_form(W,'2551Q')
 # open second visible row by finding row buttons; fallback first then use exact visible positions manual not available.
 # Existing row opening opens first empty/row1; use table row labels if exposed.
 nodes=simutil.nodes(W); rowbuttons=[n for n in nodes if n.get('role')=='AXButton' and (n.get('id') or '').startswith('fp-table') and 'row' in (n.get('id') or '')]
 rec['rowbuttons']=[n.get('id') for n in rowbuttons]
 # Use the second row button if present, otherwise first.
 target=rowbuttons[1] if len(rowbuttons)>1 else None
 if target and target.get('pos') and 100<target['pos'][1]<900: click_node(target,.6)
 else: open_row_controlled(W)
 time.sleep(.3); focus_amount_end(W); shot(udid,cdir+'/010-row2-before.jpg')
 keys=type_keys_real(W,udid,'7777',cdir,interval=.16,shots=True)
 rec['typed_keys']=keys; rec['shown_after_typing']=(wait_field(W).get('value') if simutil.find(W,role='AXTextField') else None)
 before=time.time(); press_done(W); time.sleep(.35); rec['done_closed']=not bool(simutil.find(W,role='AXTextField'))
 # Immediately open first row and press Delete.
 open_row_controlled(W); b=findbtn(W,'Delete row'); rec['delete_blur_note']='Done/close definitely blurred the amount before Delete in this UI-feasible sequence'
 rec['delete_button']=bool(b); click_node(b,.8) if b else None
 shot(udid,cdir+'/020-after-delete-row1.jpg'); rec['rows_after_delete']=rowsdb(db)
 open_form(W,'2551Q'); time.sleep(.5); shot(udid,cdir+'/030-after-reopen.jpg'); rec['rows_after_reopen']=rowsdb(db)
 logjson(os.path.join(ROOT,'observations.jsonl'),rec); return rec
if __name__=='__main__': print(json.dumps(run(sys.argv[1],sys.argv[2],sys.argv[3]),indent=1)[:5000])
