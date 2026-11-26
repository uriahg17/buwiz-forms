import sqlite3, os, time

def seed_live_db(src,dst):
    s=sqlite3.connect(src); d=sqlite3.connect(dst)
    tables=['settings','taxpayers','profiles','per_year_forms','form_drafts','year_facts','profile_calendar_events','profile_calendar_links']
    for t in tables:
        try:
            rows=s.execute('select * from '+t).fetchall()
            if not rows: continue
            cols=len(rows[0])
            d.execute('delete from '+t)
            d.executemany('insert or replace into '+t+' values ('+','.join('?'*cols)+')',rows)
        except Exception as e:
            print('skip',t,e)
    d.commit(); d.close(); s.close()

def trigger_reload():
    p='/Users/devin/moneybox-7eacb1d2/buwiz-forms/nsh/moneytools.ipad.seed.test.ts'
    os.utime(p,None)
    time.sleep(1.5)
