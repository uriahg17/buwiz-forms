import sys,os,time,json,sqlite3,traceback
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
from lifelib import set_hardware
from case1 import open_filings,keypad_all
from case3 import launch
from navrows import small_scroll,byid

def ctr(n):return (round(n['pos'][0]+n['size'][0]/2),round(n['pos'][1]+n['size'][1]/2))
def insert1601(db):
 con=sqlite3.connect(db);con.execute("delete from form_drafts where form_code='1601FQ'")
 row={'id':3,'tin':'00012345300000','taxable_year':2026,'quarter':4,'is_amended':False,'any_tax_withheld':True,'number_of_attached_sheets':0,'rdo_code':'039','line_of_business':'','taxpayer_name':'Juana Santos','registered_address':'1 Test Street','zip_code':'1100','contact_number':'09170000000','category':'private','email':'test@example.com','tax_relief':'international_tax_treaty','schedule':[],'total_other_tax_withheld':0.0,'taxes_withheld_regular':0.0,'taxes_withheld_treaty':0.0,'total_taxes_withheld':0.0,'remittance_first_month':0.0,'remittance_second_month':0.0,'tax_remitted_previous':0.0,'total_remittances':0.0,'tax_still_due':0.0,'surcharge':0.0,'interest':0.0,'compromise':0.0,'total_penalties':0.0,'total_amount_due':0.0,'schedule1':[{'treaty_code':'US','atc_code':'WI330','income_payment':0.0,'tax_rate':0.0,'tax_withheld':0.0}]+[{'treaty_code':'NA','atc_code':'NA','income_payment':0.0,'tax_rate':0.0,'tax_withheld':0.0} for _ in range(4)],'schedule1_total':0.0,'penalty_model_version':1,'penalty_overrides':{},'status':'Draft','created_at':'2026-11-26T00:00:00Z','updated_at':'2026-11-26T00:00:00Z','submission_attempts':0}
 con.execute("insert into form_drafts(tin,form_code,taxable_year,quarter,status,data_json,period_key) values(?,?,?,?,?,?,?)",('00012345300000','1601FQ',2026,4,'Draft',json.dumps(row),'Q4'));con.commit();con.close()
def rate_row(db):
 j=json.loads(sqlite3.connect(db).execute("select data_json from form_drafts where form_code='1601FQ'").fetchone()[0]);return j.get('schedule1',[{}])[0]
def open1601(W):
 open_filings(W);time.sleep(.5)
 for _ in range(20):
  b=next((n for n in simutil.nodes(W) if n.get('role')=='AXButton' and '1601FQ' in (n.get('desc') or '')),None)
  if b:click_node(b,.8);time.sleep(.8);return
  time.sleep(.2)
 raise RuntimeError('1601FQ filing row not found')
def ensure_rate_row(W):
 hi=850 if W==IPHONE else 930
 for _ in range(35):
  if simutil.find(W,idpart='fp-table-drpTreatyCode0-done'):return
  row=byid(W,'fp-row-drpTreatyCode0-0')
  if row and row.get('pos'):
   y=row['pos'][1]
   if 250<y<hi:click_node(row,.8);time.sleep(.4);continue
   small_scroll(W,up=(y>hi));continue
  tog=byid(W,'fp-part-3-toggle')
  if tog and tog.get('pos') and 250<tog['pos'][1]<hi:
   click_node(tog,.5);time.sleep(.35);continue
  small_scroll(W,up=True)
 raise RuntimeError('1601FQ schedule row 1 did not open')
def done_node(W):return (simutil.find(W,idpart='fp-table-drpTreatyCode0-done') or [None])[0]
def finish_done(W,xy):
 click_xy(*xy);time.sleep(.7)
 for _ in range(3):
  d=done_node(W)
  if not d:break
  click_xy(*ctr(d));time.sleep(.6)
 return done_node(W) is None
def rate_field(W):
 lab=next((n for n in simutil.nodes(W) if n.get('role')=='AXStaticText' and (n.get('desc') or '')=='Tax Rate (F)'),None)
 fs=simutil.find(W,role='AXTextField')
 if lab:
  y=lab['pos'][1];cand=[n for n in fs if n.get('pos') and 0<n['pos'][1]-y<60]
  if cand:return cand[0]
 return fs[-1] if fs else None
def runone(W,udid,db):
 out='iphone' if W==IPHONE else 'ipad';cdir=os.path.join(ROOT,'percent',out);os.makedirs(cdir,exist_ok=True)
 rec={'device':out,'case':'percent-1601fq-tax-rate'}
 try:
  insert1601(db);launch(udid,db);time.sleep(1.5);set_hardware(W,False);open1601(W)
  rec['initial']=rate_row(db);ensure_rate_row(W);time.sleep(.3);shot(udid,cdir+'/000-row-open-zero.jpg')
  f=rate_field(W);d=done_node(W)
  if not f or not d:raise RuntimeError('tax rate field or done missing')
  rec['field_before']={'value':f.get('value'),'pos':f['pos'],'size':f['size']};done_xy=ctr(d)
  click_xy(round(f['pos'][0]+f['size'][0]-15),round(f['pos'][1]+f['size'][1]/2));time.sleep(1.4)
  kp=keypad_all(W);rec['keypad']=sorted(kp);shot(udid,cdir+'/001-focused-zero.jpg')
  if '4' not in kp or '2' not in kp:raise RuntimeError('missing keypad digits')
  click_xy(*kp['4']);time.sleep(.32);click_xy(*kp['2']);time.sleep(1.2);shot(udid,cdir+'/002-after-42.jpg')
  rec['closed']=finish_done(W,done_xy);time.sleep(.3);shot(udid,cdir+'/010-after-leaving.jpg');rec['saved_after_leaving']=rate_row(db)
  open_filings(W);time.sleep(.35);open1601(W);ensure_rate_row(W);time.sleep(.3)
  f2=rate_field(W);rec['shown_after_reopen']=f2.get('value') if f2 else None;rec['saved_after_reopen']=rate_row(db);shot(udid,cdir+'/020-after-reopen.jpg')
 except Exception as e:
  rec['exception']=repr(e);rec['trace']=traceback.format_exc()[-1200:]
  try:shot(udid,cdir+'/099-exception.jpg')
  except Exception:pass
 with open(cdir+'/result.json','w') as fh:json.dump(rec,fh,indent=1)
 logjson(os.path.join(ROOT,'observations.jsonl'),rec);print(json.dumps(rec));return rec
if __name__=='__main__':runone(sys.argv[1],sys.argv[2],sys.argv[3])
