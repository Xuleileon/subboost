# State / 2026-10-05

Deployed source 92dcf02 on home Linux, rootless Podman. App/database/tunnel and backup/refresh timers active. Public host subboost.990203.xyz; administration restricted by Cloudflare Access, subscription download requires a random bearer token. Old public subscription preserved.

NETWORK rule tests 2 passed; full unit run 1688 passed, one Windows shell timeout passed on bounded rerun (6 tests); typecheck/lint/Linux production build passed. Runtime audit zero known vulnerabilities. Public valid token 200, invalid token 404, unauthenticated management 302. Encrypted backup restored to a temporary database and checked, then temporary database dropped.

14 nodes/38 groups retained. Known STUN 13 rules now follow Claude; published YAML equals isolated-tested candidate. 13 existing service routes plus two STUN mock checks passed without accessing AI accounts. Real Nord STUN passed on both VPS. Google entry UDP returned no response in bounded checks; full WebRTC media support is NOT accepted. Arbitrary-port STUN is not guaranteed covered. User explicitly accepts domestic DIRECT probes exposing domestic public IP.

Windows timezone is Taipei Standard Time, Chrome reads Asia/Taipei; UTC+8 unchanged. No browser policies or active Clash profile changes in this work. User still needs import new URL and mobile acceptance. Private connection details and recovery material reside outside Git in protected local handoff folder. No guarantee of platform/GFW non-detection.

Runtime image remains 92dcf02; following commit adds deployment templates and evidence docs only. No PR created.
