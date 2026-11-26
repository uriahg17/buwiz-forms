import sys,os,time,json,subprocess
sys.path.insert(0,'/Users/devin/moneybox-d4f2852a/helpers/bin')
sys.path.insert(0,'/Users/devin/moneybox-d4f2852a/proof/ios-money-box-d4f2852a/bin')
import simutil,b1,b1_strict
from huntlib import *
from case1 import open_filings,open_form
ROOTP='/Users/devin/moneybox-d4f2852a/proof/ios-money-box-d4f2852a/b3-plain-delete'

def runone(W,udid,db):
 sub='iphone' if W==IPHONE else 'ipad';cdir=f'{ROOTP}/{sub}';os.makedirs(cdir,exist_ok=True)
 b1_strict.setrows(db);b1.launch(udid,db);time.sleep(1.5);open_filings(W);open_form(W,'2551Q');time.sleep(.8);b1.click_row(W,1)
 # nothing is focused and no keyboard is required/opened; tap only the visible Delete row.
 kd=simutil.find(W,idpart='fp-table-drpATC1-delete')
 if not kd:raise RuntimeError('plain delete Delete row missing')
 rec={'device':sub,'row_index':1,'keyboard_visible':bool(keypad(W)),'delete_frame':{'pos':kd[0].get('pos'),'size':kd[0].get('size')}}
 shot(udid,cdir+'/000-before-plain-delete.jpg')
 click_node(kd[0],.2)
 return b1_strict.finish(rec,cdir,W,udid,db,1)

def main():
 out=[]
 out.append(runone(IPHONE,IPHONE_UDID,'/tmp/moneyd4-iphone.db'))
 out.append(runone(IPAD,IPAD_UDID,'/tmp/moneyd4-ipad.db'))
 print(json.dumps(out))
if __name__=='__main__':main()
