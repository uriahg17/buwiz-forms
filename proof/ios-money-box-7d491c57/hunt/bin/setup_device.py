#!/usr/bin/env python3
import sys,os,time,subprocess,sqlite3
sys.path.insert(0,os.path.dirname(__file__))
import simutil

def axset(win,idx,val):
 pid=subprocess.check_output(['pgrep','-x','Simulator'],text=True).splitlines()[0]
 cp=subprocess.run(['/tmp/axset',pid,win,str(idx),val],text=True,capture_output=True)
 if 'ok' not in cp.stdout: raise RuntimeError('axset '+cp.stdout+cp.stderr)
 time.sleep(.25)

def create_taxpayer(win):
 if simutil.find(win,idpart='setup-solo'):
  simutil.click_id(win,'setup-solo',1.0)
 if not simutil.find(win,idpart='new-tp-save'):
  raise RuntimeError('new taxpayer form not found')
 # setup fields only; accessibility value-setting is explicitly allowed for setup
 axset(win,0,'000-123-453')
 axset(win,1,'Juana Santos')
 axset(win,2,'Quezon City')
 simutil.click_id(win,'new-tp-zip_code-trigger',.7)
 for opt in ('new-tp-zip_code-opt-1000','new-tp-zip_code-opt-1100'):
  xs=simutil.find(win,idpart=opt)
  if xs: simutil.click(xs[0],.6); break
 else: raise RuntimeError('zip options missing')
 simutil.click_id(win,'new-tp-rdo_code-trigger',.7)
 xs=simutil.find(win,idpart='new-tp-rdo_code-opt-001')
 if not xs: raise RuntimeError('rdo options missing')
 simutil.click(xs[0],.6)
 simutil.click_id(win,'new-tp-save',1.4)
 if not simutil.find(win,idpart='tp-tabs-forms'):
  raise RuntimeError('taxpayer create did not finish')
 return True
