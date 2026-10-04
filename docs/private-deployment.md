# Private deployment and recovery

## Running deployment

Home Linux hosts rootless Podman under the existing user in ~/subboost-private (0700). PostgreSQL 16, app image localhost/subboost-private:92dcf02, cloudflared 2026.9.3 share an isolated slirp4netns pod. Only 127.0.0.1:13001 is published. No public database/app port, no root container bridge, no Xray restart. The home machine must remain online for subscription updates; clients retain their previously downloaded configurations if it is unavailable.

Cloudflare Tunnel sends subboost.990203.xyz to http://127.0.0.1:3000 inside the pod. Access permits only the owner email for administration. The more specific /api/subscriptions/*/config.yaml route bypasses Access but the app requires the unpredictable per-subscription token. A valid download URL is a secret: anyone with it can read node credentials. Remove/recreate a subscription to revoke it. Do not put the URL in Git or public issue reports.

App secrets/configuration are encrypted by upstream AES-256-GCM. Transport is HTTPS. Subscription lookup tokens are not claimed encrypted in PostgreSQL. Host-user access remains a trust boundary. The private entry is defense in depth, not a zero-risk guarantee.

## Reproduce

1. Install rootless Podman and slirp4netns, enable user lingering. Build local/Dockerfile from this source using the lockfile (see upstream self-host instructions). Tag the image to match subboost-app.container.
2. Create ~/subboost-private mode 0700 and secret env files mode 0600. app.env needs DATABASE_URL, ENCRYPTION_KEY, JWT_SECRET, CRON_SECRET, BACKUP_KEY (32 random bytes encoded hex), APP_URL, and TRUST_PROXY_HEADERS=true only behind this trusted loopback/tunnel boundary. db.env needs POSTGRES_DB/USER/PASSWORD. tunnel.env needs TUNNEL_TOKEN. Generate independent random secrets. See upstream env schema for complete required settings; never use sample credentials.
3. Copy deploy/private-linux pod/container/volume files to ~/.config/containers/systemd. Their %h paths resolve per user. The explicit HOSTNAME=0.0.0.0 in Exec is essential: Podman's automatic HOSTNAME otherwise makes Next bind to a pod hostname and the tunnel returns 502.
4. Provision a Cloudflare Tunnel and the two Access policies above with authenticated official cf CLI. Pin/verify image versions before future upgrades. Start user services after daemon-reload. Bootstrap the local admin once, then remove LOCAL_SETUP_TOKEN and recreate only the app container.
5. Import configuration using the authenticated admin API; do not refresh upstream sources unnecessarily. Validate downloaded YAML in an isolated Mihomo instance before switching any client.
6. Copy maintenance.py to ~/subboost-private and service/timer templates to ~/.config/systemd/user; enable timers. Refresh runs at host-local 00:17/12:17, with up to 60 seconds random delay, and each subscription retains a 12-hour interval. Backups run 04:47 host-local. Persistent=false avoids a catch-up fetch at every startup. No long-running Codex scheduler is needed.

## Backup and restore

maintenance.py backup dumps PostgreSQL and encrypts it using BACKUP_KEY from the app environment. Format: SBK1 + 12-byte nonce + 16-byte GCM tag + encrypted pg_dump custom archive. Keep seven copies, 0600. Store encryption keys separately; a database dump alone cannot decrypt stored subscriptions. An encrypted off-host copy and Windows DPAPI-protected env recovery were saved outside Git. DPAPI is tied to that Windows user/machine and is not a portable recovery key.

Restore in an isolated temporary database first: authenticate/decrypt the AES-GCM envelope with BACKUP_KEY, pg_restore the custom archive, verify subscription count and encrypted content, and only then plan production restoration. A restore round trip was verified in this deployment. Before production restore stop the app, preserve current data, restore PostgreSQL and matching encryption keys, then validate downloads and Access behavior. Do not restore a stale DB over a live app without a backup.

Rollback: keep the original hosted subscription and import it if the private deployment is unavailable. Stopping only these five new services/timers does not stop the proxy servers. Do not remove shared Podman resources or other user services.

## Routing and privacy acceptance

The private subscription retains 14 nodes and 38 groups. Thirteen known STUN rules now follow Claude's selected path, not the general Nord selection. Existing YouTube/Netflix/Apple/Google/GitHub rule matches were regression-tested with unreachable local mock proxies, without login/payment/AI requests. Both Nord paths passed real STUN checks. Google paths returned no STUN response: do not claim working WebRTC media or generic UDP support. Known STUN route failure must not be worked around with DIRECT.

This is ordinary split routing. Domestic sites remain DIRECT by explicit user choice, so an arbitrary website can request a domestic probe and learn that public IP. Unknown STUN domains/ports and browser/client variations are outside current proof. A Taiwan timezone does not match an American exit; timezone/IP mismatch alone does not prove account risk. No browser fingerprint spoofing or policy modification was installed.

The new download endpoint returned 200 and matched the isolated-tested YAML. Mobile import and browser post-import acceptance remain for the user. Updating the new source does not silently switch existing clients from the old source.
