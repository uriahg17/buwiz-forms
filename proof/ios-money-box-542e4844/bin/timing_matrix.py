import sys,os,time,json,subprocess,traceback
sys.path.insert(0,'/Users/devin/moneybox-542e4844/helpers/bin')
from lifelib import *
from lifecycle_a_fast import setup_fast,open_sheet_fast,cent,nodeid,first_textfield
from lifecycle_b_fast import fast_seq,close_reopen_db_only

ROOT='/Users/devin/moneybox-542e4844/proof/ios-money-box-542e4844/lifecycle-b-timing'
SEQ=list('1234.56')

def keypad_stable(W):
 last=None;same=0;end=time.time()+3.5
 while time.time()<end:
  kp=keypad(W);sig=tuple((k,tuple(v)) for k,v in sorted(kp.items()))
  if sig and sig==last:same+=1
  else:same=0
  last=sig
  if same>=2 and all(c in kp for c in SEQ):return kp
  time.sleep(.035)
 raise RuntimeError('keypad not stable')

def keypad_present(W):return bool(keypad(W))

def leave_row_safely(W,trigxy=None,blurxy=None):
 # End editing with an inert in-sheet control, never a cached/covered Done.
 # ATC is deliberately not used: opening its picker can focus a search box and change the keyboard.
 if blurxy is None: blurxy=trigxy or ((700 if W==IPAD else 120),930 if W==IPAD else 650)
 for _ in range(6):
  kp=keypad(W)
  if not kp:break
  live=next((n for n in simutil.nodes(W) if n.get('id')=='fp-txtATCRate1'),None)
  xy=(round(live['pos'][0]+24),round(live['pos'][1]+live['size'][1]/2)) if live and live.get('pos') else blurxy
  click_xy(*xy);time.sleep(.45)
 # Find Done fresh and verify it is not covered.
 for _ in range(10):
  kp=keypad(W);dn=simutil.find(W,idpart='fp-table-drpATC1-done')
  if dn and (not kp or (dn[0]['pos'][1]+dn[0]['size'][1] < min(y for x,y in kp.values())-5)):
   fs=simutil.find(W,role='AXTextField');afterblur=fs[0].get('value') if fs else None
   click_node(dn[0],.45);return {'done_hittable':True,'done_frame':{'pos':dn[0]['pos'],'size':dn[0]['size']},'keyboard_at_done':bool(kp),'value_after_blur':afterblur}
  time.sleep(.25)
 return {'done_hittable':False}

def run_modes(W,udid,db,kb=False):
 sub=outsub(W);mode='kbshown' if kb else 'tapdelay';cdir=os.path.join(ROOT,sub,mode);os.makedirs(cdir,exist_ok=True)
 mp4=os.path.join(cdir,sub+'-'+mode+'.mp4');vp=start_video(udid,mp4);results=[]
 try:
  nav=setup_fast(W,db);set_amount(db,0.0);ns,f=open_sheet_fast(W,nav);trigxy0=cent(nodeid(ns,'fp-drpATC1-trigger'));rate0=nodeid(ns,'fp-txtATCRate1');blurxy0=(round(rate0['pos'][0]+24),round(rate0['pos'][1]+rate0['size'][1]/2)) if rate0 else trigxy0
  fx0=round(f['pos'][0]+f['size'][0]-12);fy0=round(f['pos'][1]+f['size'][1]/2);click_xy(fx0,fy0);time.sleep(.8)
  kp0=keypad_stable(W);kpmap={c:(round(kp0[c][0]),round(kp0[c][1])) for c in SEQ}
  leave_row_safely(W,trigxy0,blurxy0)
  if nav.get('back'):click_xy(*nav['back']);time.sleep(.3)
  delays=(0,200,400) if kb else (120,200,400)
  for delay in delays:
   for trun in range(1,11):
    r={'case':'lifecycle-b-kbshown' if kb else 'lifecycle-b-tapdelay','device':sub,'timing_run':trun,'delay_target_ms':delay}
    try:
     set_amount(db,0.0);ns,f=open_sheet_fast(W,nav);trigxy=cent(nodeid(ns,'fp-drpATC1-trigger'));rate=nodeid(ns,'fp-txtATCRate1');blurxy=(round(rate['pos'][0]+24),round(rate['pos'][1]+rate['size'][1]/2)) if rate else trigxy
     fx=round(f['pos'][0]+f['size'][0]-12);fy=round(f['pos'][1]+f['size'][1]/2)
     if kb:
      click_xy(fx,fy);det0=time.perf_counter();kp=keypad_stable(W);detect_ms=(time.perf_counter()-det0)*1000
      r['detect_after_focus_ms']=round(detect_ms,2)
      if delay:time.sleep(delay/1000)
      tinv=time.perf_counter();click_xy(*kpmap['1']);r['post_detect_first_key_invocation_ms']=round((time.perf_counter()-tinv)*1000,2)
      r['achieved_first_key_after_detect_ms']=delay+r['post_detect_first_key_invocation_ms']
      time.sleep(.18)
      for c in SEQ[1:]:click_xy(*kpmap[c]);time.sleep(.18)
     else:
      ev=[(fx,fy,0),(kpmap['1'][0],kpmap['1'][1],max(0,delay-15))]
      for c in SEQ[1:]:ev.append((kpmap[c][0],kpmap[c][1],180))
      clicks,raw=fast_seq(ev)
      r['clicks']=clicks;r['measured_gap_ms']=round((clicks[1]['before_us']-clicks[0]['before_us'])/1000,2) if len(clicks)>1 else None
     time.sleep(.4)
     fs=simutil.find(W,role='AXTextField');r['shown_after_typing']=fs[0].get('value') if fs else None
     if trun==1:shot(udid,os.path.join(cdir,f'{delay}-r1-after-typing.jpg'))
     r.update({'leave':leave_row_safely(W,trigxy,blurxy)})
     r['saved_after_leaving']=amount_val(db)
     r['saved_after_reopen']=close_reopen_db_only(W,nav,db)
     v=r['saved_after_reopen'];r['correct']=v is not None and abs(v-1234.56)<.005;r['lost_or_not_correct']=not r['correct']
    except Exception as e:
     r['exception']=repr(e);r['trace']=traceback.format_exc()[-1000:]
     try:shot(udid,os.path.join(cdir,f'{delay}-r{trun}-exception.jpg'))
     except Exception:pass
    results.append(r);logjson(os.path.join(cdir,'observations.jsonl'),r)
    if r.get('exception'):break
 finally:stop_video(vp[0])
 summ={'case':mode+'-summary','device':sub,'mp4':mp4,'results':results}
 for d in ((0,200,400) if kb else (120,200,400)):
  rs=[r for r in results if r.get('delay_target_ms')==d];summ[str(d)]={'runs':len(rs),'lost':sum(1 for r in rs if r.get('lost_or_not_correct')),'saved':[r.get('saved_after_reopen') for r in rs]}
 open(os.path.join(cdir,'summary.json'),'w').write(json.dumps(summ,indent=1));print(json.dumps({k:summ[k] for k in ['device','0','200','400','120'] if k in summ}))
if __name__=='__main__':
 W=IPHONE if sys.argv[1]=='iphone' else IPAD;U=IPHONE_UDID if W==IPHONE else IPAD_UDID;db='/tmp/money542-iphone.db' if W==IPHONE else '/tmp/money542-ipad.db';run_modes(W,U,db,kb=(len(sys.argv)>2 and sys.argv[2]=='kb'))
