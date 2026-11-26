import sys,os,time,json,sqlite3,subprocess,glob
sys.path.insert(0,'/Users/devin/moneybox-d4f2852a/helpers/bin')
sys.path.insert(0,'/Users/devin/moneybox-d4f2852a/proof/ios-money-box-d4f2852a/bin')
import simutil,b1_strict
from huntlib import *
from case1 import open_filings,open_form,keypad_all
from case3 import launch,locale
ROOTP='/Users/devin/moneybox-d4f2852a/proof/ios-money-box-d4f2852a/b2-german-print'
W=IPHONE;UDID=IPHONE_UDID;DB='/tmp/moneyd4-iphone.db'
KEY='frm2551Qv2018:txt20'

def set_surcharge(v):
 con=sqlite3.connect(DB);row=con.execute("select id,data_json from form_drafts where form_code='2551Q'").fetchone();j=json.loads(row[1])
 j.setdefault('penalty_overrides',{})['surcharge']=float(v);j['surcharge']=float(v);j['total_penalties']=float(v);j['total_amount_payable']=round((j.get('total_tax_due') or 0)+float(v),2)
 con.execute('update form_drafts set data_json=? where id=?',(json.dumps(j),row[0]));con.commit();con.close()

def drag_down_visible():
 # Pull the form downward in the visible area above the keyboard; this must not tap another field.
 subprocess.run(['cliclick','dd:250,430','dm:250,500','dm:250,560','du:250,620'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.35)

def drag_up():
 subprocess.run(['cliclick','dd:250,820','dm:250,710','dm:250,650','du:250,590'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(.35)

def field_node():
 xs=simutil.find(W,idpart='fp-'+KEY) or simutil.find(W,idpart=KEY)
 return xs[0] if xs else None

def open_and_find_field():
 # Collapse Return details and open Part III, then scroll until Surcharge (item 20) is visible.
 if simutil.find(W,idpart='frm2551Qv2018:rtnMonth'):
  t=simutil.find(W,idpart='fp-part-0-toggle')
  if t: click_node(t[0],.4)
 opened=False
 for _ in range(28):
  f=field_node()
  if f and f.get('pos') and 330<f['pos'][1]<760:return f
  if not f and not opened:
   t=simutil.find(W,idpart='fp-part-3-toggle')
   if t and t[0].get('pos') and 300<t[0]['pos'][1]<1000:
    click_node(t[0],.45);opened=True
  drag_up()
 raise RuntimeError('surcharge field not reachable')

def run():
 cdir=ROOTP+'/iphone';os.makedirs(cdir,exist_ok=True)
 set_surcharge(2000.0);locale(UDID,'de_DE','de');launch(UDID,DB);time.sleep(1.5)
 open_filings(W);open_form(W,'2551Q');time.sleep(.8)
 f=open_and_find_field();rec={'device':'iphone','field':KEY,'initial_field':{'value':f.get('value'),'pos':f.get('pos'),'size':f.get('size')}}
 x=round(f['pos'][0]+f['size'][0]-2);y=round(f['pos'][1]+f['size'][1]/2);click_xy(x,y);time.sleep(1)
 kp=keypad_all(W);rec['keypad']=kp;rec['comma_offered']=',' in kp;rec['dot_offered']='.' in kp
 if ',' not in kp: raise RuntimeError('German comma key missing '+repr(kp))
 shot(UDID,cdir+'/000-focused-filled-german-keypad.jpg')
 for _ in range(8):click_xy(*kp['Delete']);time.sleep(.07)
 seq='1500,50';typed=[]
 for ch in seq:
  kp=keypad_all(W)
  if ch not in kp: raise RuntimeError('missing key '+ch+' '+repr(kp))
  click_xy(*kp[ch]);time.sleep(.14);typed.append(ch)
 shot(UDID,cdir+'/001-after-1500comma50-still-focused.jpg')
 ff=field_node();rec['after_typing_field']={'value':ff.get('value') if ff else None,'pos':ff.get('pos') if ff else None}
 rec['keyboard_still_visible_after_typing']=bool(keypad_all(W))
 # Still no Done/field change: drag the form back to its header and press Print preview.
 for _ in range(8):drag_down_visible()
 shot(UDID,cdir+'/002-before-print-keyboard-still-up.jpg')
 rec['keyboard_visible_before_print']=bool(keypad_all(W))
 pr=simutil.find(W,idpart='fp-print')
 if not pr: raise RuntimeError('print button not found after scroll')
 rec['print_frame']={'pos':pr[0].get('pos'),'size':pr[0].get('size')}
 click_node(pr[0],.2)
 time.sleep(5)
 shot(UDID,cdir+'/003-print-preview.jpg')
 rec['texts_after_print']=[(n.get('role'),n.get('desc') or n.get('title') or n.get('value') or '',n.get('pos')) for n in simutil.nodes(W) if n.get('role') in ('AXStaticText','AXButton') and (n.get('desc') or n.get('title') or n.get('value'))][:200]
 # database is corroboration only; the screenshot is the preview evidence
 try:
  j=json.loads(sqlite3.connect(DB).execute("select data_json from form_drafts where form_code='2551Q'").fetchone()[0]);rec['saved_surcharge']=j.get('surcharge');rec['saved_penalty_override_surcharge']=(j.get('penalty_overrides') or {}).get('surcharge');rec['saved_total_penalties']=j.get('total_penalties')
 except Exception as e:rec['db_error']=str(e)
 open(cdir+'/result.json','w').write(json.dumps(rec,indent=1));print(json.dumps(rec,indent=1))
if __name__=='__main__':run()
