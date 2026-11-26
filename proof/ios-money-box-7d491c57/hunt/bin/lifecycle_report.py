import json,os,collections,subprocess
L='/Users/devin/moneybox-7d491c57/proof/ios-money-box-7d491c57/lifecycle/observations.jsonl'
def load():
 rows=[]
 if os.path.exists(L):
  for line in open(L):
   try: rows.append(json.loads(line))
   except Exception: pass
 return rows
def dedupe(rows):
 out={}
 for r in rows:
  if not r.get('case','').startswith('lifecycle-') or r.get('case','').endswith('summary'): continue
  if r.get('case') in ('lifecycle-a','lifecycle-b','lifecycle-c') and r.get('fast_version') not in (2,3): continue
  key=(r.get('case'),r.get('device'),r.get('run'),r.get('mode'),r.get('expected_amount'),r.get('delay_target_ms'),r.get('box_start'),r.get('timing_run'),r.get('position'))
  out[key]=r
 return list(out.values())
def summarize():
 rows=dedupe(load())
 for dev in ('iphone','ipad'):
  aa=[r for r in rows if r.get('case')=='lifecycle-a' and r.get('device')==dev]
  bb=[r for r in rows if r.get('case')=='lifecycle-b' and r.get('device')==dev]
  cc=[r for r in rows if r.get('case')=='lifecycle-c' and r.get('device')==dev]
  print(dev,'a',len(aa),'changed',sum('stop_condition' in r for r in aa),'b',len(bb),'c',len(cc))
  for delay in (100,200,400):
   zz=[r for r in bb if r.get('box_start')=='zero' and r.get('delay_target_ms')==delay]
   print(' zero',delay,len(zz),'lost',sum(1 for r in zz if r.get('first_digit_lost')),'gaps',[r.get('measured_gap_ms') for r in zz])
  print(' filled',[(r.get('delay_target_ms'),r.get('measured_gap_ms'),r.get('shown_after_typing'),r.get('saved_after_leaving')) for r in bb if r.get('box_start')=='filled'])
  print(' c',[(r.get('position'),r.get('shown_before_8'),r.get('shown_after_8'),r.get('saved_after_leaving')) for r in cc])
if __name__=='__main__': summarize()
