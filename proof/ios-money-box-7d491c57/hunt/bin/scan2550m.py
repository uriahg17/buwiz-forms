#!/usr/bin/env python3
import sys,os,time,json
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *
from case1 import open_filings,open_form
W=sys.argv[1]; udid=sys.argv[2]
out=os.path.join(ROOT,'iphone' if W==IPHONE else 'ipad','case4','scan'); os.makedirs(out,exist_ok=True)
open_filings(W); open_form(W,'2550M')
# expand Part II if its toggle is visible anywhere; AX may expose offscreen nodes, so click only plausible y.
for step in range(16):
 ns=simutil.nodes(W)
 rows=[]
 for n in ns:
  if n.get('role') in ('AXStaticText','AXTextField','AXButton'):
   rows.append({'role':n.get('role'),'text':n.get('desc') or n.get('title') or n.get('value') or '','value':n.get('value'),'pos':n.get('pos'),'size':n.get('size'),'id':n.get('id')})
 json.dump(rows,open(os.path.join(out,f'{step:02d}.json'),'w'),indent=1)
 shot(udid,os.path.join(out,f'{step:02d}.jpg'))
 # click Part II toggle once when visible
 if step==0:
  for n in ns:
   if n.get('id') and 'part' in n.get('id','').lower() and n.get('pos') and 100<n['pos'][1]<1000:
    click_node(n,.5); break
 drag_scroll(W)
print('done')
