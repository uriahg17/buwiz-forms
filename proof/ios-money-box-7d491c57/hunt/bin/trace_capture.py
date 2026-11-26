import sys,os,time,json,traceback
sys.path.insert(0,'/Users/devin/moneybox-7d491c57/proof/ios-money-box-7d491c57/hunt/bin')
from lifelib import *
from case1 import open_filings,open_form,keypad_all,wait_field
from huntlib import ensure_row_sheet
from lifecycle_b_fast import fast_seq
from case3 import launch

def fast_seq35(specs):
 import subprocess
 args=[]
 for x,y,d in specs: args += [str(x),str(y),str(max(0,int(d)))]
 cp=subprocess.run(['/tmp/fastclick35']+args,text=True,capture_output=True,timeout=10)
 clicks=[]
 for line in cp.stdout.splitlines():
  if line.startswith('click '):
   p=line.split(); clicks.append({'before_us':int(p[1]),'after_us':int(p[2]),'x':int(p[3]),'y':int(p[4])})
 return clicks,cp.stdout+cp.stderr
OUT='/Users/devin/moneybox-7d491c57/proof/ios-money-box-7d491c57/lifecycle/trace'
SERVERLOG='/Users/devin/moneybox-7d491c57/trace-run.log'
COORDS='/tmp/tracecoords.json'
W=IPAD;udid='41A2AFE3-9E35-4EE8-BEF0-21AA02B68BC3';db='/tmp/money7d-ipad.db'
os.makedirs(OUT,exist_ok=True)
def logrec(x):
 with open(OUT+'/observations.jsonl','a') as f:f.write(json.dumps(x,sort_keys=True)+'\n')
def ctr(n): return (round(n['pos'][0]+n['size'][0]/2),round(n['pos'][1]+n['size'][1]/2))
def controls():
 ns=simutil.nodes(W)
 done=next((n for n in ns if n.get('id')=='fp-table-drpATC1-done'),None)
 close=next((n for n in ns if n.get('role')=='AXButton' and (n.get('desc') or '')=='Close' and n.get('pos') and n['pos'][0]>900),None)
 return {'done':ctr(done) if done else None,'close':ctr(close) if close else None}
def close_sheet(c=None):
 c=c or {}
 if c.get('done'):click_xy(*c['done']);time.sleep(.45)
 ns=simutil.nodes(W)
 if simutil.find(W,idpart='fp-table-drpATC1-done') and c.get('close'):click_xy(*c['close']);time.sleep(.45)
def to_filings():
 close_sheet();open_filings(W);time.sleep(.25)
def open_zero_row():
 to_filings();set_amount(db,0.0);open_form(W,'2551Q');ensure_row_sheet(W)
 f=wait_field(W,2);c=controls();return f,c
def prepare():
 launch(udid,db);time.sleep(2);set_hardware(W,False)
 f,c=open_zero_row()
 fx=round(f['pos'][0]+f['size'][0]-12);fy=round(f['pos'][1]+f['size'][1]/2)
 click_xy(fx,fy);time.sleep(.7)
 kp=keypad_all(W)
 if not all(x in kp for x in '12'):raise RuntimeError('keypad missing '+repr(kp))
 data={'field':(fx,fy),'done':c['done'],'close':c['close'],'keys':{x:(round(kp[x][0]),round(kp[x][1])) for x in kp},'keypad':kp}
 json.dump(data,open(COORDS,'w'))
 close_sheet(c);open_filings(W);time.sleep(.3)
 print('prepared',json.dumps({k:data[k] for k in ('field','done','close')}),'keys',sorted(data['keys']))
def segment(mark):
 with open(SERVERLOG,'rb') as f:
  f.seek(mark);return f.read().decode('utf-8','replace')
def run(label,delay):
 d=json.load(open(COORDS))
 f,c=open_zero_row()
 # Use current geometry for the focus tap, but calibrated keypad coordinates for the two tested digit taps.
 fx=round(f['pos'][0]+f['size'][0]-12);fy=round(f['pos'][1]+f['size'][1]/2)
 k1=d['keys']['1'];k2=d['keys']['2']
 mark=os.path.getsize(SERVERLOG) if os.path.exists(SERVERLOG) else 0
 ev=[(fx,fy,0),(k1[0],k1[1],int(delay)-14),(k2[0],k2[1],220)]
 clicks,raw=fast_seq35(ev)
 time.sleep(.55)
 seg=segment(mark)
 open(OUT+f'/{label}.log','w').write(seg)
 shot(udid,OUT+f'/{label}-after-second-digit.jpg')
 rec={'case':'masked-focus-trace','label':label,'target_gap_ms':delay,'clicks':clicks,'fastclick_raw':raw[-1000:],'trace_file':OUT+f'/{label}.log','trace_lines':len([x for x in seg.splitlines() if 'MASKED_TRACE' in x])}
 if len(clicks)>1:rec['measured_gap_ms']=round((clicks[1]['before_us']-clicks[0]['before_us'])/1000,3)
 if len(clicks)>2:rec['second_gap_ms']=round((clicks[2]['before_us']-clicks[1]['before_us'])/1000,3)
 logrec(rec);print(json.dumps(rec));return rec
if __name__=='__main__':
 try:
  if sys.argv[1]=='prepare':prepare()
  elif sys.argv[1]=='run':run(sys.argv[2],sys.argv[3])
 except Exception as e:
  print('ERROR',repr(e));traceback.print_exc();shot(udid,OUT+'/error.jpg');raise
