import sys,os,time,json,sqlite3,subprocess,traceback
sys.path.insert(0,'/Users/devin/moneybox-542e4844/helpers/bin')
import simutil
from huntlib import *
from case1 import open_filings,open_form,keypad_all
from navrows import small_scroll

ROOT='/Users/devin/moneybox-542e4844/proof/ios-money-box-542e4844/sheets'
KEY='number_of_attached_sheets'
FIELDID='frm2551Qv2018:txtSheets'

def reset(db):
 con=sqlite3.connect(db,timeout=2); row=con.execute("select id,data_json from form_drafts where form_code='2551Q'").fetchone(); j=json.loads(row[1])
 j.pop(KEY,None)
 con.execute('update form_drafts set data_json=? where id=?',(json.dumps(j),row[0]));con.commit();con.close()

def saved(db):
 con=sqlite3.connect('file:'+db+'?mode=ro',uri=True); row=con.execute("select data_json from form_drafts where form_code='2551Q'").fetchone();con.close()
 return json.loads(row[0]).get(KEY) if row else None

def field(W):
 ns=simutil.nodes(W)
 lab=next((n for n in ns if n.get('role')=='AXStaticText' and (n.get('desc') or n.get('value') or '').startswith('Number of Sheet/s')),None)
 fs=[n for n in ns if n.get('role')=='AXTextField' and n.get('pos') and n.get('size')]
 if lab and lab.get('pos'):
  cand=[f for f in fs if 15<f['pos'][1]-lab['pos'][1]<70 and abs(f['pos'][0]-lab['pos'][0])<100]
  if cand:return sorted(cand,key=lambda f:f['pos'][1]-lab['pos'][1])[0]
 # fallback: the second return-details input on this form is sheets
 return sorted(fs,key=lambda f:f['pos'][1])[1] if len(fs)>1 else (fs[0] if fs else None)

def bring_field(W):
 for _ in range(18):
  f=field(W)
  if f and f.get('pos') and 330<f['pos'][1]<650:return f
  # Return details is normally first/expanded; use small controlled scrolls.
  small_scroll(W,up=True)
 raise RuntimeError('sheets field not reachable')

def stable_keypad(W):
 last=None;same=0;end=time.time()+8
 while time.time()<end:
  kp=keypad_all(W);sig=tuple((k,tuple(v)) for k,v in sorted(kp.items()) if k in list('0123456789,.'))
  if sig and sig==last:same+=1
  else:same=0
  last=sig
  if same>=2 and '4' in kp and '2' in kp:return kp,(time.time(),sig)
  time.sleep(.035)
 raise RuntimeError('keypad not stable')

def fast_seq(specs):
 args=[]
 for x,y,d in specs:args += [str(x),str(y),str(max(0,int(d)))]
 cp=subprocess.run(['/tmp/fastclick']+args,text=True,capture_output=True,timeout=8)
 clicks=[]
 for line in cp.stdout.splitlines():
  if line.startswith('click '):
   p=line.split();clicks.append({'before_us':int(p[1]),'after_us':int(p[2]),'x':int(p[3]),'y':int(p[4])})
 return clicks,cp.stdout+cp.stderr

def close_form(W):
 for bid in ('nb-back','tb-back'):
  xs=simutil.find(W,idpart=bid)
  if xs:click_node(xs[0],.55);return
 raise RuntimeError('back missing')

def leave_field(W):
 # Collapse Return details with a real outside control tap; this is the blur/leave action.
 t=simutil.find(W,idpart='fp-part-0-toggle')
 if t:click_node(t[0],.7);return True
 close_form(W);return False

def run(W,udid,db):
 sub='iphone';cdir=os.path.join(ROOT,sub);os.makedirs(cdir,exist_ok=True)
 mp4=os.path.join(cdir,'sheets-matrix.mp4');vp=start_video(udid,mp4);results=[]
 calib=None
 try:
  for mode in ('tap','shown'):
   for i in range(1,11):
    r={'case':'sheets','device':sub,'mode':mode,'run':i}
    try:
     reset(db);open_filings(W);open_form(W,'2551Q');f=bring_field(W)
     r['precondition_value']=f.get('value');r['field_frame']={'pos':f.get('pos'),'size':f.get('size')}
     if i==1:shot(udid,os.path.join(cdir,f'{mode}-01-before.jpg'))
     fx=round(f['pos'][0]+f['size'][0]/2);fy=round(f['pos'][1]+f['size'][1]/2)
     if mode=='tap':
      if calib is None:
       click_xy(fx,fy);time.sleep(.8);kp,_=stable_keypad(W);calib={k:(round(v[0]),round(v[1])) for k,v in kp.items() if k in '42'}
       # clear this calibration focus before starting the counted run
       leave_field(W);close_form(W);reset(db);open_filings(W);open_form(W,'2551Q');f=bring_field(W);fx=round(f['pos'][0]+f['size'][0]/2);fy=round(f['pos'][1]+f['size'][1]/2)
      ev=[(fx,fy,0),(calib['4'][0],calib['4'][1],0),(calib['2'][0],calib['2'][1],120)]
      clicks,raw=fast_seq(ev);r['clicks']=clicks;r['tap_to_key4_ms']=round((clicks[1]['before_us']-clicks[0]['after_us'])/1000,2) if len(clicks)>1 else None
     else:
      click_xy(fx,fy);kp,det=stable_keypad(W);r['keyboard_detected']=True
      t0=time.perf_counter();click_xy(*kp['4']);time.sleep(.14);click_xy(*kp['2']);r['post_detect_first_key_ms']=round((time.perf_counter()-t0)*1000,2)
     time.sleep(.35)
     f2=field(W);r['shown_after_typing']=f2.get('value') if f2 else None
     if i==1:shot(udid,os.path.join(cdir,f'{mode}-01-after-typing.jpg'))
     r['left_field']=leave_field(W);time.sleep(.4);r['saved_after_leave']=saved(db)
     close_form(W);open_filings(W);open_form(W,'2551Q');f3=bring_field(W)
     r['shown_after_reopen']=f3.get('value') if f3 else None;r['saved_after_reopen']=saved(db)
     if i==1:shot(udid,os.path.join(cdir,f'{mode}-01-after-reopen.jpg'))
     def oknum(x):
      try:return float(x)==42.0
      except Exception:return False
     r['correct']=oknum(r['saved_after_reopen']) and (str(r['shown_after_reopen']).replace(',','') in ('42','42.0','42.00'))
     close_form(W)
    except Exception as e:
     r['exception']=repr(e);r['trace']=traceback.format_exc()[-1200:]
     try:shot(udid,os.path.join(cdir,f'{mode}-{i:02d}-exception.jpg'))
     except Exception:pass
    results.append(r);logjson(os.path.join(cdir,'observations.jsonl'),r)
    if r.get('exception'):break
 finally:stop_video(vp[0])
 summary={'case':'sheets-summary','mp4':mp4,'tap_correct':sum(1 for r in results if r['mode']=='tap' and r.get('correct')),'tap_runs':sum(1 for r in results if r['mode']=='tap'),'shown_correct':sum(1 for r in results if r['mode']=='shown' and r.get('correct')),'shown_runs':sum(1 for r in results if r['mode']=='shown'),'results':results}
 open(os.path.join(cdir,'summary.json'),'w').write(json.dumps(summary,indent=1))
 print(json.dumps({k:summary[k] for k in ['tap_correct','tap_runs','shown_correct','shown_runs']}))
if __name__=='__main__':run(IPHONE,IPHONE_UDID,'/tmp/money542-iphone.db')
