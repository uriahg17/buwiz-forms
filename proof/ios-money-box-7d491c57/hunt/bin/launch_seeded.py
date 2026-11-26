#!/usr/bin/env python3
import os,sys,subprocess,time,sqlite3,signal,glob
sys.path.insert(0,os.path.dirname(__file__))
from seedutil import seed_live_db

def db_has_schema(path):
    if not os.path.exists(path): return False
    try:
        con=sqlite3.connect('file:'+path+'?mode=rw',uri=True,timeout=.02)
        row=con.execute("select name from sqlite_master where type='table' and name='taxpayers'").fetchone()
        con.close(); return bool(row)
    except Exception: return False

def launch_seeded(udid,container,seeddb,devserver='ws://127.0.0.1:8790/ws'):
    subprocess.run(['xcrun','simctl','terminate',udid,'com.longbridge.nsh.host'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    time.sleep(.3)
    env=dict(os.environ)
    for k in ['SIMCTL_CHILD_BIR_SFTP_LIVE','BIR_SFTP_LIVE']: env.pop(k,None)
    env.update({'SIMCTL_CHILD_BUWIZ_NO_KEYCHAIN':'1','SIMCTL_CHILD_EBIR_TEST_ENV':'1','SIMCTL_CHILD_BIR_AUTH_BYPASS':'1','SIMCTL_CHILD_BIR_SFTP_DRY_RUN':'1'})
    cp=subprocess.run(['xcrun','simctl','launch',udid,'com.longbridge.nsh.host','--dev-server',devserver],text=True,capture_output=True,env=env)
    print(cp.stdout.strip(),cp.stderr.strip())
    try: pid=int(cp.stdout.split(':')[-1].strip())
    except Exception: raise RuntimeError('no pid '+cp.stdout+cp.stderr)
    # Stop the app immediately, then pulse it only until the door schema exists.
    try: os.kill(pid,signal.SIGSTOP)
    except ProcessLookupError: pass
    base=os.path.join(container,'tmp','ebirforms-door')
    db=os.path.join(base,f'{pid}-0','bir_data.db')
    deadline=time.time()+8; seeded=False
    while time.time()<deadline:
        if db_has_schema(db):
            # The process can be stopped inside its schema transaction. Pulse briefly
            # until the write lock clears, then seed before the UI's first data read.
            for _ in range(100):
                try:
                    seed_live_db(seeddb,db)
                    seeded=True
                    break
                except sqlite3.OperationalError:
                    pass
                try:
                    os.kill(pid,signal.SIGCONT); time.sleep(.006); os.kill(pid,signal.SIGSTOP)
                except ProcessLookupError: break
            break
        try:
            os.kill(pid,signal.SIGCONT)
            time.sleep(.012)
            os.kill(pid,signal.SIGSTOP)
        except ProcessLookupError: break
    try: os.kill(pid,signal.SIGCONT)
    except ProcessLookupError: pass
    time.sleep(3)
    return pid,db,seeded
