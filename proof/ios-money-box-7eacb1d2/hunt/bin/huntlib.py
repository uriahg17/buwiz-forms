import json, subprocess, time, os, sys, signal, sqlite3, re, shutil
sys.path.insert(0, os.path.dirname(__file__))
import simutil

ROOT='/Users/devin/moneybox-7eacb1d2/proof/ios-money-box-7eacb1d2/hunt'
IPHONE='iPhone 17 Pro'
IPHONE_UDID='405F45A9-B471-47B7-A5D9-E545EA624713'
IPAD='iPad Pro 13-inch'
IPAD_UDID='41A2AFE3-9E35-4EE8-BEF0-21AA02B68BC3'

def logjson(path,obj):
    os.makedirs(os.path.dirname(path),exist_ok=True)
    with open(path,'a') as f: f.write(json.dumps(obj,sort_keys=True)+'\n')

def shot(udid,path):
    os.makedirs(os.path.dirname(path),exist_ok=True)
    subprocess.run(['xcrun','simctl','io',udid,'screenshot',path],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

def center(n):
    p=n['pos']; s=n['size']; return (round(p[0]+s[0]/2),round(p[1]+s[1]/2))

def click_xy(x,y):
    subprocess.run(['cliclick',f'c:{x},{y}'],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

def click_node(n,wait=0.15):
    x,y=center(n); click_xy(x,y)
    if wait: time.sleep(wait)
    return x,y

def keypad(win):
    out={}
    for n in simutil.find(win,role='AXButton'):
        d=n.get('desc') or ''
        if d in list('1234567890.')+['Delete']:
            out[d]=center(n)
    return out

def amount_field(win):
    # In the row sheet the amount is the lone visible text field. On form pages there may be several;
    # callers use this only while the sheet is open.
    fs=simutil.find(win,role='AXTextField')
    if not fs: raise RuntimeError('no text field')
    return fs[0]

def focus_amount_end(win):
    f=amount_field(win)
    x=round(f['pos'][0]+f['size'][0]-8); y=round(f['pos'][1]+f['size'][1]/2)
    click_xy(x,y); time.sleep(.35)

def clear_amount_real(win,maxdel=14):
    focus_amount_end(win)
    kp=keypad(win)
    if 'Delete' not in kp: raise RuntimeError('no keypad delete')
    x,y=kp['Delete']
    for _ in range(maxdel):
        click_xy(x,y); time.sleep(.055)
    time.sleep(.2)

def press_done(win):
    simutil.click_id(win,'fp-table-drpATC1-done',.8)

def open_row_if_needed(win):
    rows=simutil.find(win,idpart='fp-row-drpATC1-0')
    if not rows: raise RuntimeError('row not visible/available')
    click_node(rows[0],.6)


def drag_scroll(win,up=True):
    # Drag inside the device content. up=True means a finger drag upward, moving content upward.
    x=250 if 'iPhone' in win else 950
    if up:
        subprocess.run(['cliclick',f'dd:{x},850',f'dm:{x},700','w:80',f'du:{x},620'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    else:
        subprocess.run(['cliclick',f'dd:{x},620',f'dm:{x},700','w:80',f'du:{x},850'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    time.sleep(.35)

def close_close_sheet_if_any(win):
    # The all-sections sheet has a lone Close button; close it when it blocks the form.
    cs=[x for x in simutil.find(win,text='Close',role='AXButton') if x.get('pos') and 300<x['pos'][1]<700]
    if cs: click_node(cs[0],.4)

def dismiss_alpha_keyboard(win):
    rs=[x for x in simutil.find(win,role='AXButton') if (x.get('desc') or '')=='return']
    if rs: click_node(rs[0],.4)

def visible_y(n):
    p=n.get('pos')
    return p[1] if p else 9999

def ensure_row_sheet(win,rowid='fp-row-drpATC1-0'):
    # Open the first Schedule-1 row sheet robustly: collapse Return details, expand Schedule 1,
    # scroll until the row is actually visible above the floating to-do pill, then press it.
    if simutil.find(win,idpart='fp-table-drpATC1-done') and simutil.find(win,role='AXTextField'):
        return
    close_close_sheet_if_any(win)
    dismiss_alpha_keyboard(win)
    # Collapse Return details when its month input is present; it pushes Schedule 1 far down.
    if simutil.find(win,idpart='frm2551Qv2018:rtnMonth'):
        try: simutil.click_id(win,'fp-part-0-toggle',.35)
        except Exception: pass
    for attempt in range(14):
        rows=simutil.find(win,idpart=rowid)
        if rows:
            y=visible_y(rows[0])
            if 400 <= y <= 760:
                click_node(rows[0],.7)
                if simutil.find(win,idpart='fp-table-drpATC1-done') and simutil.find(win,role='AXTextField'):
                    return
            elif y > 760:
                drag_scroll(win,up=True)
            else:
                drag_scroll(win,up=False)
            continue
        toggles=simutil.find(win,idpart='fp-part-4-toggle')
        if toggles:
            y=visible_y(toggles[0])
            if 360 <= y <= 850:
                click_node(toggles[0],.45)
            elif y > 850:
                drag_scroll(win,up=True)
            else:
                drag_scroll(win,up=False)
        else:
            drag_scroll(win,up=True)
    raise RuntimeError('could not open row sheet')


def sqlite_values(db):
    con=sqlite3.connect('file:'+db+'?mode=ro',uri=True)
    rows=con.execute('select form_code, taxable_year, quarter, period_key, data_json from form_drafts order by id').fetchall()
    con.close()
    out=[]
    for code,year,q,period,data in rows:
        try: j=json.loads(data)
        except Exception: j={}
        out.append({'form_code':code,'taxable_year':year,'quarter':q,'period_key':period,'data':j})
    return out

def draft_money(db,form='2551Q'):
    for r in sqlite_values(db):
        if r['form_code']==form:
            s=(r['data'].get('schedule_1') or [{}])
            row=s[0] if s else {}
            return {'taxable_amount':row.get('taxable_amount'),'tax_due':row.get('tax_due'),'total_tax_due':r['data'].get('total_tax_due'),'updated_at':r['data'].get('updated_at')}
    return None

def start_video(udid,path):
    os.makedirs(os.path.dirname(path),exist_ok=True)
    if os.path.exists(path): os.unlink(path)
    p=subprocess.Popen(['xcrun','simctl','io',udid,'recordVideo','--force','--codec=h264',path],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True,bufsize=1)
    # Wait for Recording started; first frame is being processed at approximately this instant.
    start=time.perf_counter()
    line=''
    while time.perf_counter()-start<8:
        ch=p.stderr.read(1)
        if not ch: break
        line += ch
        if 'Recording started' in line: break
    t0=time.perf_counter()
    return p,t0,line

def stop_video(p):
    if p.poll() is None:
        p.send_signal(signal.SIGINT)
    try: p.wait(timeout=8)
    except subprocess.TimeoutExpired:
        p.kill(); p.wait()

def extract_frames(video,outdir):
    os.makedirs(outdir,exist_ok=True)
    for x in os.listdir(outdir):
        if x.startswith('frame'): os.unlink(os.path.join(outdir,x))
    subprocess.run(['ffmpeg','-y','-v','error','-i',video,os.path.join(outdir,'frame%04d.png')],check=True)
    # pts times for mapping
    cp=subprocess.run(['ffprobe','-v','error','-select_streams','v:0','-show_entries','frame=pts_time','-of','csv=p=0',video],text=True,capture_output=True)
    pts=[]
    for line in cp.stdout.splitlines():
        try: pts.append(float(line.strip()))
        except: pass
    files=sorted(os.path.join(outdir,x) for x in os.listdir(outdir) if x.startswith('frame') and x.endswith('.png'))
    return list(zip(files,pts))

def crop_frame(src,dst,device='iphone'):
    os.makedirs(os.path.dirname(dst),exist_ok=True)
    if device=='iphone': crop='1206:290:0:700'
    else: crop='1600:350:0:700'
    subprocess.run(['ffmpeg','-y','-v','error','-i',src,'-vf','crop='+crop,dst],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

def ocr_texts(img):
    cp=subprocess.run(['/tmp/ocr',img],text=True,capture_output=True)
    try: return json.loads(cp.stdout)
    except Exception: return []

def amount_ocr(img):
    vals=[]
    for r in ocr_texts(img):
        txt=r.get('text','')
        if any(c.isdigit() for c in txt):
            # Strip caret/bracket/peso noise but keep digits, separators and sign.
            clean=''.join(c for c in txt if c.isdigit() or c in '.,-')
            if clean: vals.append({'raw':txt,'clean':clean,'conf':r.get('conf'),'box':r.get('box')})
    # amount is normally the longest/rightmost numeric OCR object in the crop
    if not vals: return {'raw':'','clean':'','conf':0,'box':[]}
    return sorted(vals,key=lambda x:(len(x['clean']),x['clean'].count('.')),reverse=True)[0]

def type_sequence_real(win,seq,interval_ms=140,progress=None):
    kp=keypad(win)
    missing=[c for c in seq if c not in kp]
    if missing: raise RuntimeError('missing keypad keys '+repr(missing)+' have '+repr(kp))
    times=[]; last=None
    for i,c in enumerate(seq):
        target=(last+interval_ms/1000) if last is not None else time.perf_counter()
        now=time.perf_counter()
        if target>now: time.sleep(target-now)
        x,y=kp[c]
        click_xy(x,y)
        t=time.perf_counter(); times.append({'key':c,'t':t,'x':x,'y':y})
        if progress: progress(i,c,t)
        last=t
    for i in range(1,len(times)): times[i]['interval_after_prev_ms']=round((times[i]['t']-times[i-1]['t'])*1000,2)
    if times: times[0]['interval_after_prev_ms']=None
    return times

def assign_frames_by_time(frames,taps,outdir,case,device='iphone',render_delay=0.03):
    # Copy the first extracted frame at or after tap time + render_delay. Times are relative to video t0 supplied in tap['video_offset'].
    assigned=[]
    for idx,tap in enumerate(taps,1):
        want=tap['video_offset']+render_delay
        candidates=[(f,pts) for f,pts in frames if pts is not None and pts>=want]
        if not candidates: candidates=[frames[-1]] if frames else []
        if not candidates: continue
        f,pts=candidates[0]
        dst=os.path.join(outdir,f'{case}-key-{idx:02d}-{tap["key"].replace(".","dot")}.png')
        shutil.copyfile(f,dst)
        assigned.append({'index':idx,'key':tap['key'],'path':dst,'pts':pts,'wanted_offset':want})
    return assigned
