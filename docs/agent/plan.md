# Private SubBoost / 2026-10-05

- User authorizes star, fork, clone, modify and deploy; keep old subscription running.
- Fork: Xuleileon/subboost; upstream AGPL-3.0 retained.
- Implement NETWORK rule roundtrip in shared core and UI.
- Deployment decision pending: full Node/PostgreSQL container with Cloudflare private entrance, versus Workers adaptation.
- Never commit subscriptions, node credentials, tokens, encryption keys or private backups.
- Owner-only administration; encrypted stored subscription content; separate revocable subscription read credential.
- Validate rules, unauthorized access, subscription rendering and service isolation before delivery.
- No changes to Windows Clash or active gateway routes.
