import time,subprocess,sys,os
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import click_node,IPHONE

def small_scroll(W,up=True):
 x=250 if W==IPHONE else 800
 if up: subprocess.run(['cliclick',f'dd:{x},750',f'dm:{x},650',f'du:{x},650'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 else: subprocess.run(['cliclick',f'dd:{x},650',f'dm:{x},750',f'du:{x},750'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 time.sleep(.25)
def byid(W,id): return next((n for n in simutil.nodes(W) if n.get('id')==id),None)
def bring_id(W,id,lo=None,hi=None,steps=20):
 if lo is None: lo=280 if W==IPHONE else 300
 if hi is None: hi=790 if W==IPHONE else 890
 for _ in range(steps):
  n=byid(W,id)
  if n and n.get('pos'):
   y=n['pos'][1]
   if lo<y<hi: return n
   small_scroll(W,up=(y>hi))
  else: small_scroll(W,up=True)
 raise RuntimeError('cannot bring '+id)
def open_row_controlled(W):
 if simutil.find(W,idpart='fp-table-drpATC1-done') and simutil.find(W,role='AXTextField'): return
 # Collapse the expanded return-details card first; this usually puts Schedule 1 in view.
 try:
  import huntlib
  if simutil.find(W,idpart='frm2551Qv2018:rtnMonth'):
   t=byid(W,'fp-part-0-toggle')
   if t: huntlib.click_node(t,.35)
 except Exception: pass
 # Use the row whenever it is already visible; otherwise expand/scroll Schedule 1 with small controlled moves.
 for _ in range(12):
  row=byid(W,'fp-row-drpATC1-0')
  hi=850 if W==IPHONE else 930
  if row and row.get('pos') and 280<row['pos'][1]<hi:
   click_node(row,.55)
   if simutil.find(W,idpart='fp-table-drpATC1-done'): return
  tog=byid(W,'fp-part-4-toggle')
  if not row and tog and tog.get('pos') and 280<tog['pos'][1]<hi:
   click_node(tog,.45)
   continue
  small_scroll(W,up=True)
 raise RuntimeError('row sheet did not open')
