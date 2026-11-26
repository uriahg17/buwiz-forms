#!/usr/bin/env python3
import sys,os,time,json,sqlite3,subprocess
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
from case1 import open_filings,open_form,update_2551q,keypad_all,wait_field,type_keys_real

def launch(udid,db):
 subprocess.run(['xcrun','simctl','terminate',udid,'com.longbridge.nsh.host'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.4)
 env=dict(os.environ); env.update({'SIMCTL_CHILD_BUWIZ_NO_KEYCHAIN':'1','SIMCTL_CHILD_EBIR_TEST_ENV':'1','SIMCTL_CHILD_BIR_AUTH_BYPASS':'1','SIMCTL_CHILD_BIR_SFTP_DRY_RUN':'1','SIMCTL_CHILD_BIR_DATABASE_PATH':db})
 cp=subprocess.run(['xcrun','simctl','launch',udid,'com.longbridge.nsh.host','--dev-server','ws://127.0.0.1:8790/ws'],env=env,text=True,capture_output=True)
 time.sleep(3); return cp.stdout+cp.stderr

def locale(udid,loc,lang):
 subprocess.run(['xcrun','simctl','spawn',udid,'defaults','write','NSGlobalDomain','AppleLocale','-string',loc],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 subprocess.run(['xcrun','simctl','spawn',udid,'defaults','write','NSGlobalDomain','AppleLanguages','-array',lang],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

def software_keyboard():
 subprocess.run(['open','-a','Simulator'],stdout=subprocess.DEVNULL); time.sleep(.3)
 subprocess.run(['cliclick','kd:cmd','t:k','ku:cmd'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(.5)

def static_texts(W):
 return [{'text':n.get('desc') or n.get('title') or n.get('value') or '', 'pos':n.get('pos'),'size':n.get('size')} for n in simutil.nodes(W) if n.get('role')=='AXStaticText']

def perform_seq(W,udid,db,name,seq):
 cdir=os.path.join(ROOT,'iphone' if W==IPHONE else 'ipad','case3',name); os.makedirs(cdir,exist_ok=True)
 open_filings(W); update_2551q(db,0.0); open_form(W,'2551Q'); ensure_row_sheet(W)
 focus_amount_end(W); time.sleep(.2)
 if not keypad_all(W): software_keyboard()
 pre=wait_field(W).get('value')
 keys=type_keys_real(W,udid,seq,cdir,interval=.14,shots=True)
 press_done(W); time.sleep(.7); shot(udid,os.path.join(cdir,'020-after-leaving.jpg'))
 saved=draft_money(db); texts_after=static_texts(W)
 open_form(W,'2551Q'); ensure_row_sheet(W); time.sleep(.3)
 shot(udid,os.path.join(cdir,'030-after-reopening-row.jpg'))
 texts=static_texts(W); shown=wait_field(W).get('value') if simutil.find(W,role='AXTextField') else ''
 rec={'device':'iphone' if W==IPHONE else 'ipad','case':'case3-'+name,'sequence':seq,'precondition':pre,'keys':keys,'saved_after_leaving':saved,'texts_after_leaving':texts_after,'shown_after_reopening':shown,'saved_after_reopening':draft_money(db),'texts_after_reopening':texts}
 logjson(os.path.join(ROOT,'observations.jsonl'),rec); return rec

def run(W,udid,db):
 root=os.path.join(ROOT,'iphone' if W==IPHONE else 'ipad','case3'); os.makedirs(root,exist_ok=True)
 locale(udid,'de_DE','de'); launchout=launch(udid,db)
 open_form(W,'2551Q'); ensure_row_sheet(W); focus_amount_end(W); time.sleep(.3)
 if not keypad_all(W): software_keyboard(); focus_amount_end(W); time.sleep(.2)
 kp=keypad_all(W); labels=[]
 for n in simutil.find(W,role='AXButton'):
  d=n.get('desc') or ''
  if n.get('pos'): labels.append(d)
 shot(udid,os.path.join(root,'000-german-keypad.jpg'))
 rec={'device':'iphone' if W==IPHONE else 'ipad','case':'case3-keypad','locale':'de_DE','keypad':kp,'labels':labels,'comma_offered':',' in kp,'dot_offered':'.' in kp,'launch':launchout}
 logjson(os.path.join(ROOT,'observations.jsonl'),rec)
 out=[rec,perform_seq(W,udid,db,'comma-decimal','1500,50')]
 out.append({'device':rec['device'],'case':'case3-dot-grouped-comma-decimal','untested':'dot key not offered on German decimal pad' if '.' not in kp else 'not run'})
 logjson(os.path.join(ROOT,'observations.jsonl'),out[-1])
 out.append(perform_seq(W,udid,db,'lone-comma',','))
 # valid German-region digits-only control for addition B
 out.append(perform_seq(W,udid,db,'digits-only','1500'))
 locale(udid,'en_PH','en'); launch(udid,db); open_form(W,'2551Q'); ensure_row_sheet(W); focus_amount_end(W); time.sleep(.3)
 if not keypad_all(W): software_keyboard(); focus_amount_end(W); time.sleep(.2)
 shot(udid,os.path.join(root,'900-philippines-keypad-reset.jpg'))
 ph={'device':rec['device'],'case':'case3-philippines-keypad-reset','keypad':keypad_all(W),'dot_offered':'.' in keypad_all(W),'comma_offered':',' in keypad_all(W)}
 logjson(os.path.join(ROOT,'observations.jsonl'),ph); out.append(ph)
 return out
if __name__=='__main__': print(json.dumps(run(sys.argv[1],sys.argv[2],sys.argv[3]),indent=1)[:5000])
