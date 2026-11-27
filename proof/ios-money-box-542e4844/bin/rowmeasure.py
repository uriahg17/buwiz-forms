import sys,os,time,json,subprocess
sys.path.insert(0,'/Users/devin/moneybox-542e4844/helpers/bin')
import simutil
from huntlib import *
from case1 import open_filings,open_form
from navrows import open_row_controlled
ROOT='/Users/devin/moneybox-542e4844/proof/ios-money-box-542e4844/row-sheet-points'
def annotate(img,out,frames,scale,origin):
 # draw boxes/height labels with a small AppKit annotator; ffmpeg here lacks drawtext
 colors=['red','yellow','cyan']; fs=[]
 for i,(name,n) in enumerate(frames.items()):
  x=(n['pos'][0]-origin[0])*scale;y=(n['pos'][1]-origin[1])*scale;w=n['size'][0]*scale;h=n['size'][1]*scale
  fs.append({'x':x,'y':y,'w':w,'h':h,'label':f"{name} {n['size'][1]:.1f}pt",'color':colors[i%3]})
 spec=os.path.join(os.path.dirname(out),'annotate-spec.json')
 open(spec,'w').write(json.dumps({'input':img,'output':out,'frames':fs}))
 subprocess.run(['/tmp/swiftannotate',spec],check=True)

def run(W,udid,db):
 sub='iphone' if W==IPHONE else 'ipad';cdir=os.path.join(ROOT,sub);os.makedirs(cdir,exist_ok=True)
 open_filings(W);open_form(W,'2551Q');open_row_controlled(W);time.sleep(.5)
 ns=simutil.nodes(W)
 f=next((n for n in ns if n.get('role')=='AXTextField' and n.get('pos') and n.get('size')),None)
 d=next((n for n in ns if n.get('id')=='fp-table-drpATC1-delete'),None)
 dn=next((n for n in ns if n.get('id')=='fp-table-drpATC1-done'),None)
 if not(f and d and dn):raise RuntimeError('missing frames '+repr((bool(f),bool(d),bool(dn))))
 rec={'device':sub,'amount':{'pos':f['pos'],'size':f['size'],'height':f['size'][1]},'delete':{'pos':d['pos'],'size':d['size'],'height':d['size'][1]},'done':{'pos':dn['pos'],'size':dn['size'],'height':dn['size'][1]}}
 raw=os.path.join(cdir,'raw.jpg');ann=os.path.join(cdir,'annotated.png');shot(udid,raw)
 # Accessibility frames are absolute macOS window coordinates. Convert them into
 # simulator-screen pixels using the device content group's origin and width.
 win=next((w for w in simutil.windows() if W in w.get('title','')),None)
 group=next((c for c in win.get('children',[]) if c.get('role')=='AXGroup' and c.get('size') and c['size'][0]>300),None)
 sw=float(subprocess.check_output(['sips','-g','pixelWidth',raw],text=True).splitlines()[-1].split()[-1])
 scale=sw/group['size'][0];origin=group['pos']
 annotate(raw,ann,{'amount':f,'Delete row':d,'Done':dn},scale,origin)
 rec['annotation_mapping']={'content_origin_points':origin,'content_width_points':group['size'][0],'screenshot_width_px':sw,'scale':scale}
 rec['screenshot_raw']=raw;rec['screenshot_annotated']=ann
 open(os.path.join(cdir,'result.json'),'w').write(json.dumps(rec,indent=1));print(json.dumps(rec))
if __name__=='__main__':run(IPHONE if sys.argv[1]=='iphone' else IPAD,IPHONE_UDID if sys.argv[1]=='iphone' else IPAD_UDID,'/tmp/money542-iphone.db' if sys.argv[1]=='iphone' else '/tmp/money542-ipad.db')
