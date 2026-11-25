#!/usr/bin/env python3
"""Independent PR350 driver: physical-coordinate presses through gpui-agent against a real Linux NSH window."""
import json, os, re, subprocess, sys, time, glob
from pathlib import Path

OUT = Path.home()/"BuwizNsh/proof350/form-review/check/350"
OUT.mkdir(parents=True, exist_ok=True)
ADDR=os.environ.get("CHECK350_ADDR","127.0.0.1:17521")
TOKEN=os.environ.get("GPUI_AGENT_TOKEN","check350local")
ENV=os.environ.copy(); ENV.update({"GPUI_AGENT_ADDR":ADDR,"GPUI_AGENT_TOKEN":TOKEN,"GPUI_AGENT_REPLY_TIMEOUT_MS":"15000"})

def run(args, ok=True, input=None, timeout=20):
    p=subprocess.run(["gpui-agent"]+args, input=input, text=True, capture_output=True, env=ENV, timeout=timeout)
    txt=(p.stdout or "")+(("\nSTDERR:"+p.stderr) if p.stderr else "")
    try: data=json.loads(p.stdout)
    except Exception: data={"ok":p.returncode==0,"raw":txt,"returncode":p.returncode}
    if ok and (p.returncode!=0 or data.get("ok") is False):
        raise RuntimeError(f"gpui-agent {' '.join(args)} failed rc={p.returncode}: {txt[:1000]}")
    return data

def snap():
    return run(["snapshot"])

def flat_tree(data=None):
    data=data or snap(); out=[]
    def rec(ns, depth=0, parent=None):
        for n in ns:
            n['_depth']=depth
            out.append(n); rec(n.get('children',[]), depth+1, n)
    rec(data.get('tree',{}).get('nodes',[]))
    return out,data

def nodes_by_id(ns, id): return [n for n in ns if n.get('id')==id]
def node(ns,id):
    a=nodes_by_id(ns,id)
    return a[0] if a else None

def center(n): return (n['bounds']['x']+n['bounds']['w']/2, n['bounds']['y']+n['bounds']['h']/2)
def press_xy(x,y,required=True):
    return run(["press","--x",str(round(x)),"--y",str(round(y)),"--no-read-back"],ok=required)
def press_node(id):
    ns,_=flat_tree(); n=node(ns,id)
    if not n: raise RuntimeError('no node '+id)
    x,y=center(n); return press_xy(x,y)
def set_value(id,v): return run(["set-value",id,v,"--no-read-back"])
def key(id,k,delivery='virtual'): return run(["key",id,k,"--delivery",delivery,"--no-read-back"],ok=False)
def drag_xy(x,y,dx,dy): return run(["drag","--x",str(round(x)),"--y",str(round(y)),"--dx",str(round(dx)),"--dy",str(round(dy))],ok=False)

def count_text(ns):
    n=node(ns,'tp-forms-count')
    return n.get('name') if n else None

def desc(n):
    out=[]
    def rec(x):
        out.append(x)
        for c in x.get('children',[]): rec(c)
    rec(n); return out

def row_node(ns,code): return node(ns,'tp-form-'+code)
def row_checked(r):
    if not r: return None
    if r.get('checked') is not None: return r.get('checked')
    for c in desc(r):
        if c.get('role')=='checkbox' and c.get('checked') is not None: return c.get('checked')
    return None

def row_checkbox_node(r):
    for c in desc(r):
        if c.get('role')=='checkbox': return c
    return None

def row_accessibility(r):
    ds=desc(r) if r else []
    checks=[{'id':c['id'],'role':c['role'],'name':c.get('name'), 'checked':c.get('checked'), 'enabled':c.get('enabled'), 'states':c.get('states'), 'bounds':c.get('bounds')} for c in ds if c.get('role')=='checkbox']
    return {'row':{k:r.get(k) for k in ('id','role','name','checked','enabled','focused','bounds','states')} if r else None,
            'checkbox_count':len(checks),'checkboxes':checks,'child_count':len(ds)-1}

def state_summary():
    ns,data=flat_tree(); r=row_node(ns,'1601C')
    rows={}
    for n in ns:
        m=re.fullmatch(r'tp-form-([A-Z0-9]+)',n.get('id',''))
        if m: rows[m.group(1)]={'checked':row_checked(n),'role':n.get('role'),'bounds':n.get('bounds'),'enabled':n.get('enabled')}
    return {'count':count_text(ns),'rows':rows,'accessibility1601C':row_accessibility(r) if r else None}

def note_point(r, pred, fallback_dx):
    ds=desc(r)
    cand=[c for c in ds if c.get('role')=='note' and pred(c.get('name','')) and c.get('bounds',{}).get('w',0)>0]
    if cand: return center(cand[0])
    return (r['bounds']['x']+fallback_dx, r['bounds']['y']+r['bounds']['h']/2)

def click_points(r, compact=False):
    b=r['bounds']; y=b['y']+b['h']/2
    codep=note_point(r, lambda s:s=='1601C', 78)
    # the longest note is the form title (not Next:, not the code)
    titlep=note_point(r, lambda s:len(s)>20 and not s.startswith(('Next:','Due ','Every period','Not filed')), 170)
    chipp=note_point(r, lambda s:s in ('No template','Template'), b['w']-(64 if compact else 72))
    return {
      'checkbox':(b['x']+24,y),
      'code':codep,
      'text':titlep,
      'empty':(b['x']+b['w']-8,y),
      'chip':chipp,
    }

def host_pid():
    for p in subprocess.run(['pgrep','-f','nsh-app-nsh-app-ebirforms-linux-host'],text=True,capture_output=True).stdout.split():
        if Path(f'/proc/{p}/root/tmp').exists(): return p
    return None

def capture(dest):
    dest=Path(dest); dest.parent.mkdir(parents=True,exist_ok=True)
    tmp='check350-'+str(time.time_ns())+'.png'
    r=run(['screenshot','--out',tmp])
    inside=r.get('result',{}).get('path','/tmp/gpui-agent-screenshots/'+tmp)
    pid=host_pid(); src=None
    if pid:
        cand=Path('/proc')/pid/'root'/inside.lstrip('/')
        if cand.exists(): src=cand
    if src is None:
        # scan host processes in case pgrep caught threads or wrappers
        for p in subprocess.run(['pgrep','-f','nsh-app'],text=True,capture_output=True).stdout.split():
            cand=Path('/proc')/p/'root'/inside.lstrip('/')
            if cand.exists(): src=cand; break
    if src is None: raise RuntimeError('screenshot not found '+inside)
    dest.write_bytes(src.read_bytes())
    try: src.unlink()
    except Exception: pass
    return str(dest)

def save_json(name,obj):
    (OUT/name).write_text(json.dumps(obj,indent=2,sort_keys=True))

def wait_idle(sec=.45): time.sleep(sec)

def ensure_edit():
    ns,_=flat_tree()
    if node(ns,'tp-forms-edit'):
        press_node('tp-forms-edit'); wait_idle(.8)

def matrix_width(label, reqw, reqh, use_search, results, commit):
    run(['viewport','--width',str(reqw),'--height',str(reqh)])
    wait_idle(1.0)
    ns,_=flat_tree()
    if use_search:
        set_value('tp-forms-search','1601C'); wait_idle(.8)
    else:
        set_value('tp-forms-search',''); wait_idle(.5)
    ns,data=flat_tree()
    save_json(f'snapshot-{commit}-{label}-edit-start.json',data['tree'])
    capture(OUT/f'picker-{commit}-{label}.png')
    ns,_=flat_tree(); r=row_node(ns,'1601C')
    if not r: raise RuntimeError('1601C row not visible '+label)
    pts=click_points(r, compact=(reqw<500))
    widthres={'requested':[reqw,reqh],'actual_root':flat_tree()[0][0]['bounds'] if flat_tree()[0] else None,
              'row_bounds':r['bounds'],'points':pts,'clicks':{},'initial':state_summary()}
    for area in ['text','code','empty','chip','checkbox']:
        x,y=pts[area]; arr=[]
        for nclick in (1,2):
            reply=press_xy(x,y,required=False); wait_idle(.55)
            ns,_=flat_tree(); rr=row_node(ns,'1601C')
            arr.append({'after_click':nclick,'count':count_text(ns),'checked1601C':row_checked(rr),'reply':{k:reply.get(k) for k in ('ok','error','error_code','delivery_status')}})
            if area=='text': capture(OUT/f'rowtext-{commit}-{label}-click{nclick}.png')
        widthres['clicks'][area]=arr
    # two quick presses at the text point (as close as separate CLI requests can make them)
    x,y=pts['text']; press_xy(x,y,False); press_xy(x,y,False); wait_idle(.5)
    ns,_=flat_tree(); widthres['double_press_text']={'count':count_text(ns),'checked1601C':row_checked(row_node(ns,'1601C'))}
    # restore the row to checked if the double press left it off; use the box point, itself part of the matrix
    ns,_=flat_tree()
    if row_checked(row_node(ns,'1601C')) is False:
        press_xy(*pts['checkbox']); wait_idle(.45)
    widthres['after_matrix']=state_summary()
    results['widths'][label]=widthres

def forms_list_codes():
    ns,_=flat_tree(); out=[]
    for n in ns:
        m=re.fullmatch(r'tp-form-([A-Z0-9]+)',n.get('id',''))
        if m: out.append((n['bounds']['y'],m.group(1),n))
    return [x[1] for x in sorted(out)]

def save_cancel_flow(results, commit):
    # desktop, full list; 1601C is the controlled row. 2551Q remains checked from the seed.
    run(['viewport','--width','1440','--height','900']); wait_idle(.8)
    set_value('tp-forms-search',''); wait_idle(.5)
    ns,_=flat_tree(); r=row_node(ns,'1601C'); pts=click_points(r)
    # untick 1601C using the physical box position, save, and verify the saved list
    if row_checked(r):
        press_xy(*pts['checkbox']); wait_idle(.5)
    press_node('tp-forms-save'); wait_idle(1.2)
    ns,_=flat_tree(); after_save={'texts':[n.get('name','') for n in ns if n.get('role') in ('note','button')][-30:], 'visible_form_rows':forms_list_codes(), 'editing':bool(node(ns,'tp-forms-search'))}
    capture(OUT/f'saved-{commit}-desktop.png')
    # leave to Templates and return to Forms
    press_node('tp-tabs-templates'); wait_idle(.7); capture(OUT/f'templates-{commit}-desktop.png')
    press_node('tp-tabs-forms'); wait_idle(.9)
    ns,_=flat_tree(); after_reopen={'visible_form_rows':forms_list_codes(),'has1601C':bool(row_node(ns,'1601C')),'has2551Q':bool(row_node(ns,'2551Q'))}
    capture(OUT/f'reopened-{commit}-desktop.png')
    # cancel must not save: enter edit, tick 1601C back on, cancel; saved rows stay as after save
    ensure_edit(); wait_idle(.5); ns,_=flat_tree(); r=row_node(ns,'1601C')
    if r and not row_checked(r): press_xy(*click_points(r)['checkbox']); wait_idle(.5)
    press_node('tp-forms-cancel'); wait_idle(.8)
    ns,_=flat_tree(); after_cancel={'visible_form_rows':forms_list_codes(),'editing':bool(node(ns,'tp-forms-search'))}
    capture(OUT/f'cancelled-{commit}-desktop.png')
    results['save_cancel']={'after_save':after_save,'after_reopen':after_reopen,'after_cancel':after_cancel}

def gestures(results, commit):
    ensure_edit(); set_value('tp-forms-search',''); wait_idle(.5)
    ns,_=flat_tree(); r=row_node(ns,'1601C'); pts=click_points(r)
    out={}
    # sequence over the first three visible rows, using their title-ish x and center y
    rows=[]
    for n in ns:
        m=re.fullmatch(r'tp-form-([A-Z0-9]+)',n.get('id',''))
        if m and n['bounds']['y']+n['bounds']['h'] < 880: rows.append((n['bounds']['y'],m.group(1),n))
    rows=sorted(rows)[:3]; seq=[]
    before=state_summary()
    for _,code,rw in rows:
        b=rw['bounds']; press_xy(b['x']+170,b['y']+b['h']/2,required=False); wait_idle(.35)
        ns2,_=flat_tree(); seq.append({'code':code,'count':count_text(ns2),'checked':row_checked(row_node(ns2,code))})
    out['sequence_first_rows']={'rows':[c for _,c,_ in rows],'before':before,'steps':seq}
    # restore those rows with the box point when needed to their before states
    for _,code,rw in rows:
        want=before['rows'].get(code,{}).get('checked')
        ns2,_=flat_tree(); rr=row_node(ns2,code)
        if rr and row_checked(rr)!=want:
            press_xy(rr['bounds']['x']+24,rr['bounds']['y']+rr['bounds']['h']/2); wait_idle(.3)
    # Start on a CHECKED 1601C row and end one row lower: no toggle should occur.
    ns,_=flat_tree(); r=row_node(ns,'1601C')
    if r and not row_checked(r):
        press_xy(r['bounds']['x']+24,r['bounds']['y']+r['bounds']['h']/2); wait_idle(.4)
    ns,_=flat_tree(); r=row_node(ns,'1601C'); b=r['bounds']; x=b['x']+170; y=b['y']+b['h']/2
    before_count=count_text(ns); before_checked=row_checked(r)
    d=drag_xy(x,y,0,b['h']+4); wait_idle(.6); ns,_=flat_tree()
    out['press_start_row_end_next']={'reply':{k:d.get(k) for k in ('ok','error','error_code')},'before':[before_count,before_checked],'after':[count_text(ns),row_checked(row_node(ns,'1601C'))]}
    # press-and-drag upward from the row, intended to scroll the long list
    ns,_=flat_tree(); r=row_node(ns,'1601C'); b=r['bounds']; before_y=b['y']; before_count=count_text(ns); before_checked=row_checked(r)
    d=drag_xy(b['x']+170,b['y']+b['h']/2,0,-260); wait_idle(.8); ns,_=flat_tree(); rr=row_node(ns,'1601C')
    out['press_drag_scroll']={'reply':{k:d.get(k) for k in ('ok','error','error_code')},'before_y':before_y,'after_y':rr['bounds']['y'] if rr else None,
        'scrolled':bool(rr and abs(rr['bounds']['y']-before_y)>5),'before':[before_count,before_checked],'after':[count_text(ns),row_checked(rr)]}
    results['gestures']=out

def search_filter_setup(results, commit):
    ensure_edit(); wait_idle(.4)
    out={}
    set_value('tp-forms-search','vat'); wait_idle(.8); ns,_=flat_tree()
    out['vat_filter']={'count':count_text(ns),'rows':sorted([m.group(1) for n in ns for m in [re.fullmatch(r'tp-form-([A-Z0-9]+)',n.get('id',''))] if m]),'has2550Q':bool(row_node(ns,'2550Q')),'has1601C':bool(row_node(ns,'1601C'))}
    capture(OUT/f'search-vat-{commit}-desktop.png')
    r=row_node(ns,'2550Q')
    if r:
        # physical text press first (the behavior under test), then use the box if the row did not select so both commits continue alike
        p=note_point(r,lambda s:len(s)>15 and not s.startswith(('Next:','Not filed')),170)
        before=row_checked(r); text_reply=press_xy(*p,required=False); wait_idle(.5); ns,_=flat_tree(); r=row_node(ns,'2550Q')
        text_after=row_checked(r)
        if text_after==before:
            press_xy(r['bounds']['x']+24,r['bounds']['y']+r['bounds']['h']/2); wait_idle(.5); ns,_=flat_tree(); r=row_node(ns,'2550Q')
        out['select_filtered_2550Q']={'before':before,'text_reply':{k:text_reply.get(k) for k in ('ok','error','error_code','delivery_status')},'after_text_press':text_after,'final':row_checked(r),'count':count_text(ns)}
    for freq in ['Monthly','Quarterly','Annual','As needed','All']:
        press_node('tp-forms-freq-'+freq); wait_idle(.6); ns,_=flat_tree()
        rows=sorted([m.group(1) for n in ns for m in [re.fullmatch(r'tp-form-([A-Z0-9]+)',n.get('id',''))] if m])
        out.setdefault('frequency_steps',[]).append({'freq':freq,'count':count_text(ns),'rows':rows[:20],'row_count':len(rows)})
        if freq=='Quarterly': capture(OUT/f'filter-quarterly-{commit}-desktop.png')
    # set-up button: apply Non-VAT professional and answer Replace if asked
    set_value('tp-forms-search',''); wait_idle(.4); ns,_=flat_tree()
    setup_node=None
    for n in ns:
        if n.get('role')=='button' and n.get('name')=='Non-VAT professional': setup_node=n; break
    if setup_node:
        press_xy(*center(setup_node)); wait_idle(1.0); ns,_=flat_tree()
        replace=node(ns,'tp-replace-yes')
        if replace: press_xy(*center(replace)); wait_idle(1.0); ns,_=flat_tree()
        out['setup_non_vat']={'text_tail':[n.get('name','') for n in ns if n.get('role') in ('note','button')][-35:],'visible_form_rows':forms_list_codes(),'editing':bool(node(ns,'tp-forms-search'))}
        capture(OUT/f'setup-{commit}-desktop.png')
    else: out['setup_non_vat']={'error':'button not found'}
    results['search_filter_setup']=out

def keyboard_access(results, commit):
    ensure_edit(); set_value('tp-forms-search','1601C'); wait_idle(.7)
    ns,_=flat_tree(); r=row_node(ns,'1601C'); out={'accessibility_before':row_accessibility(r)}
    save_json(f'accessibility-{commit}-row-before.json',out['accessibility_before'])
    # focus through a mouse press is not enough proof; first try direct virtual keys at the row, then physical xdotool Tab probed externally.
    keyresults=[]
    for k in ['Space','Enter','Return']:
        before=row_checked(row_node(flat_tree()[0],'1601C'))
        rr=key('tp-form-1601C',k,'virtual'); wait_idle(.4); ns,_=flat_tree(); after=row_checked(row_node(ns,'1601C'))
        keyresults.append({'key':k,'reply':{x:rr.get(x) for x in ('ok','error','error_code')},'before':before,'after':after,'count':count_text(ns)})
        # restore if it toggled
        if after!=before:
            ns,_=flat_tree(); rrnode=row_node(ns,'1601C'); press_xy(rrnode['bounds']['x']+24,rrnode['bounds']['y']+rrnode['bounds']['h']/2); wait_idle(.3)
    out['direct_virtual_keys']=keyresults
    # inspect focus before/after a click and after Tab sent at the root/window. This records Linux delivery honestly.
    ns,_=flat_tree(); r=row_node(ns,'1601C'); focused_before=[{'id':n['id'],'role':n['role'],'name':n.get('name')} for n in ns if n.get('focused')]
    press_xy(*click_points(r)['checkbox']); wait_idle(.4); press_xy(*click_points(row_node(flat_tree()[0],'1601C'))['checkbox']); wait_idle(.4) # net restore, likely leaves focus
    ns,_=flat_tree(); focused_after_click=[{'id':n['id'],'role':n['role'],'name':n.get('name')} for n in ns if n.get('focused')]
    root=ns[0]['id'] if ns else 'n1'; tabreply=key(root,'Tab','virtual'); wait_idle(.4); ns,_=flat_tree(); focused_after_tab=[{'id':n['id'],'role':n['role'],'name':n.get('name')} for n in ns if n.get('focused')]
    out['focus_probe']={'before':focused_before,'after_row_clicks':focused_after_click,'tab_reply':{x:tabreply.get(x) for x in ('ok','error','error_code')},'after_tab':focused_after_tab}
    ns,_=flat_tree(); out['accessibility_after']=row_accessibility(row_node(ns,'1601C'))
    save_json(f'accessibility-{commit}-row-after.json',out['accessibility_after'])
    results['keyboard_access']=out

def existing_dialog(results, commit):
    # Navigate physically: Form library, search/open 1601C, save sample as January, inspect dialog checkbox line.
    out={}
    run(['viewport','--width','1440','--height','900']); wait_idle(.7)
    ns,_=flat_tree()
    if node(ns,'tp-forms-cancel'):
        press_node('tp-forms-cancel'); wait_idle(.6)
    press_node('nav-library'); wait_idle(1.0)
    set_value('library-search','1601C'); wait_idle(.5)
    # The owned scope is empty after picker setup experiments; search the complete form library.
    ns,_=flat_tree()
    if node(ns,'library-scope-all'):
        press_node('library-scope-all'); wait_idle(.6)
    press_node('library-1601C'); wait_idle(1.4)
    ns,_=flat_tree(); out['opened_sample']={'form_page':bool(node(ns,'form-page')),'sample_note':any('sample' in (n.get('name','').lower()) for n in ns)}
    press_node('fp-save'); wait_idle(.8)
    set_value('sample-period-year',str(time.gmtime().tm_year)); set_value('sample-period-month','1'); wait_idle(.3)
    press_node('sample-period-save'); wait_idle(1.2)
    ns,data=flat_tree(); out['existing_visible']=bool(node(ns,'existing-offer'))
    save_json(f'existing-dialog-{commit}-snapshot.json',data['tree'])
    capture(OUT/f'existing-{commit}-desktop.png')
    cb=node(ns,'existing-fast-lane')
    if cb:
        b=cb['bounds']; y=b['y']+b['h']/2; box=(b['x']+8,y); text=(b['x']+120,y)
        seq=[]
        for area,pt in [('text',text),('text2',text),('box',box),('box2',box)]:
            before=row_checked(cb) if cb.get('checked') is not None else cb.get('checked')
            reply=press_xy(*pt,required=False); wait_idle(.5); ns,_=flat_tree(); cb=node(ns,'existing-fast-lane')
            after=cb.get('checked') if cb else None
            seq.append({'area':area,'before':before,'after':after,'reply':{k:reply.get(k) for k in ('ok','error','error_code','delivery_status')},'bounds':cb.get('bounds') if cb else None,'role':cb.get('role') if cb else None,'name':cb.get('name') if cb else None})
        out['fast_lane_clicks']=seq
        # ensure it ends ON: click box once whenever currently false
        ns,_=flat_tree(); cb=node(ns,'existing-fast-lane')
        if cb and cb.get('checked') is False:
            b=cb['bounds']; press_xy(b['x']+8,b['y']+b['h']/2); wait_idle(.4)
        ns,_=flat_tree(); cb=node(ns,'existing-fast-lane'); out['fast_lane_before_keep']=cb.get('checked') if cb else None
        press_node('existing-keep'); wait_idle(1.0)
        # Same sample session: save as February. With fast lane on it should auto-load without asking again.
        press_node('fp-save'); wait_idle(.7)
        set_value('sample-period-year',str(time.gmtime().tm_year)); set_value('sample-period-month','2'); wait_idle(.2)
        press_node('sample-period-save'); wait_idle(1.5)
        ns,_=flat_tree(); texts=[n.get('name','') for n in ns if n.get('role') in ('note','button')]
        out['second_period']={'existing_offer_shown':bool(node(ns,'existing-offer')),'text_tail':texts[-30:]}
        capture(OUT/f'existing-second-{commit}-desktop.png')
    results['existing_dialog']=out

def main():
    commit=sys.argv[1] if len(sys.argv)>1 else 'unknown'
    phases=set((sys.argv[2] if len(sys.argv)>2 else 'all').split(','))
    results={'commit':commit,'addr':ADDR,'started':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'widths':{}}
    # baseline outside editing: rows are plain rows, text presses do nothing
    run(['viewport','--width','1440','--height','900']); wait_idle(1)
    ns,_=flat_tree()
    results['startup']={'node_count':len(ns),'has_edit':bool(node(ns,'tp-forms-edit')),'initial_rows':forms_list_codes()}
    if node(ns,'tp-forms-edit') and 'all' in phases or 'picker' in phases:
        r=row_node(ns,'1601C'); before={'role':r.get('role') if r else None,'checked':row_checked(r),'access':row_accessibility(r) if r else None}
        if r:
            pts=click_points(r)
            outside_reply=press_xy(*pts['text'],required=False); wait_idle(.35)
            ns2,_=flat_tree(); r2=row_node(ns2,'1601C')
            after={'role':r2.get('role') if r2 else None,'checked':row_checked(r2),'access':row_accessibility(r2) if r2 else None}
        else: after=None
        results['outside_editing']={'before':before,'press_reply':{k:outside_reply.get(k) for k in ('ok','error','error_code','delivery_status')},'after_text_click':after}
        capture(OUT/f'picker-{commit}-desktop-not-editing.png')
    ensure_edit(); wait_idle(.8)
    if 'all' in phases or 'picker' in phases:
        matrix_width('desktop',1440,900,False,results,commit)
        matrix_width('tablet',834,1112,True,results,commit)
        matrix_width('phone',390,844,True,results,commit)
        save_cancel_flow(results,commit)
        gestures(results,commit)
        search_filter_setup(results,commit)
        keyboard_access(results,commit)
    if 'all' in phases or 'dialog' in phases:
        existing_dialog(results,commit)
    rp=OUT/f'results-{commit}.json'
    if rp.exists():
        try:
            old=json.loads(rp.read_text()); old.update(results); results=old
        except Exception: pass
    save_json(Path(f'results-{commit}.json'),results)
    print(json.dumps({'ok':True,'results':str(OUT/f'results-{commit}.json')},indent=2))

if __name__=='__main__':
    main()
