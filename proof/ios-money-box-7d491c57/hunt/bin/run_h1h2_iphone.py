#!/usr/bin/env python3
import sys,os,time,json,shutil,subprocess
sys.path.insert(0,os.path.dirname(__file__))
import simutil
from huntlib import *

WIN=IPHONE; UDID=IPHONE_UDID
DB='/Users/devin/Library/Developer/CoreSimulator/Devices/405F45A9-B471-47B7-A5D9-E545EA624713/data/Containers/Data/Application/0973CEBB-8D01-4458-8873-616214E0F25C/tmp/ebirforms-door/60325-0/bir_data.db'
OUT=os.path.join(ROOT,'iphone')
LOG=os.path.join(ROOT,'observations.jsonl')
os.makedirs(OUT,exist_ok=True)

def reopen_return():
    simutil.click_id(WIN,'nb-back',.5)
    simutil.click_id(WIN,'tab-filings',.5)
    rs=simutil.find(WIN,idpart='return-1')
    if not rs: raise RuntimeError('return-1 not found in Filings')
    click_node(rs[0],.9)

def reset_zero_and_open():
    # assumes row sheet is open; clear with real keypad taps, settle zero, reopen the row unfocused
    clear_amount_real(WIN)
    press_done(WIN)
    time.sleep(.5)
    z=draft_money(DB)
    ensure_row_sheet(WIN)
    return z

def perform(case,seq,t0):
    cdir=os.path.join(OUT,case); os.makedirs(cdir,exist_ok=True)
    ensure_row_sheet(WIN)
    shot(UDID,os.path.join(cdir,'000-precondition-zero-unfocused.jpg'))
    pre=amount_field(WIN).get('value')
    focus_amount_end(WIN)
    time.sleep(.15)
    taps=type_sequence_real(WIN,seq,interval_ms=140)
    for t in taps: t['video_offset']=round(t['t']-t0,4)
    time.sleep(.45)
    shot(UDID,os.path.join(cdir,'010-after-typing-before-done.jpg'))
    press_done(WIN)
    time.sleep(.6)
    shot(UDID,os.path.join(cdir,'020-after-leaving-field.jpg'))
    rowtexts=[x.get('desc') or '' for x in simutil.find(WIN,idpart='fp-row-drpATC')]
    saved=draft_money(DB)
    reopen_return()
    shot(UDID,os.path.join(cdir,'030-after-reopening-return.jpg'))
    ensure_row_sheet(WIN)
    shot(UDID,os.path.join(cdir,'031-after-reopening-row-amount.jpg'))
    reopen_field=amount_field(WIN).get('value')
    saved_after=draft_money(DB)
    intervals=[x.get('interval_after_prev_ms') for x in taps[1:]]
    return {'device':'iphone','case':case,'sequence':seq,'precondition_field':pre,'tap_times':taps,
      'tap_interval_ms':{'min':min(intervals) if intervals else None,'max':max(intervals) if intervals else None,'mean':sum(intervals)/len(intervals) if intervals else None},
      'shown_after_leaving_row_texts':rowtexts,'saved_after_leaving':saved,
      'shown_after_reopening_field':reopen_field,'saved_after_reopening':saved_after}

def main():
    video=os.path.join(ROOT,'iphone-h1-h2.mp4')
    p,t0,banner=start_video(UDID,video)
    records=[]
    try:
        records.append(perform('h1','15000.50',t0))
        z1=reset_zero_and_open()
        records.append({'device':'iphone','case':'h1-reset-zero-before-h2','saved':z1})
        records.append(perform('h2','15000..50',t0))
    finally:
        stop_video(p)
    # extract frames once from the continuous H1+H2 device video
    for rec in list(records):
        if 'case' not in rec or rec['case'] not in ('h1','h2'): continue
        case=rec['case']; cdir=os.path.join(OUT,case)
        frames=extract_frames(video,os.path.join(cdir,'video-frames'))
        assigned=assign_frames_by_time(frames,rec['tap_times'],cdir,case,'iphone')
        for a in assigned:
            crop=os.path.join(cdir,'crop-'+os.path.basename(a['path']))
            crop_frame(a['path'],crop,'iphone')
            a['ocr']=amount_ocr(crop)
        rec['frames']=assigned
        rec['video']=video
    for rec in records: logjson(LOG,rec)
    print(json.dumps([{k:v for k,v in r.items() if k!='tap_times' and k!='frames'} if 'case' in r else r for r in records],indent=2))
    print('OCR')
    for rec in records:
        if 'frames' in rec: print(rec['case'],[(a['key'],a['ocr']['clean'],a['path']) for a in rec['frames']])

if __name__=='__main__': main()
