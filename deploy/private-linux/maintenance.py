import pathlib,json,urllib.request,subprocess,time,os
r=pathlib.Path.home()/'subboost-private'
def backup():
 out=r/'backups';out.mkdir(mode=0o700,exist_ok=True)
 dump=subprocess.run(['podman','exec','subboost-private-db','pg_dump','-U','subboost','-d','subboost','--format=custom'],capture_output=True,check=True).stdout
 code="const c=require('crypto');let b=[];process.stdin.on('data',x=>b.push(x));process.stdin.on('end',()=>{let iv=c.randomBytes(12),e=c.createCipheriv('aes-256-gcm',Buffer.from(process.env.BACKUP_KEY,'hex'),iv),v=Buffer.concat([e.update(Buffer.concat(b)),e.final()]);process.stdout.write(Buffer.concat([Buffer.from('SBK1'),iv,e.getAuthTag(),v]));});"
 encrypted=subprocess.run(['podman','exec','-i','subboost-private-app','node','-e',code],input=dump,capture_output=True,check=True).stdout
 assert encrypted.startswith(b'SBK1')
 p=out/(time.strftime('%Y%m%d-%H%M%S')+'.pg.aesgcm');p.write_bytes(encrypted);p.chmod(0o600)
 for old in sorted(out.glob('*.pg.aesgcm'))[:-7]:old.unlink()
 print('encrypted backup complete')
if __name__=='__main__':
 import sys
 if len(sys.argv)>1 and sys.argv[1]=='backup':backup()
 else:
  env=dict(l.split('=',1) for l in (r/'app.env').read_text().splitlines())
  req=urllib.request.Request('http://127.0.0.1:13001/api/cron/update-subscriptions',method='POST',headers={'Authorization':'Bearer '+env['CRON_SECRET']})
  with urllib.request.urlopen(req,timeout=300) as x:print('subscription scheduler HTTP',x.status)
