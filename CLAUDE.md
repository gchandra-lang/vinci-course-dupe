---
name: lab-workspace-authorization-page
description: React implementation of authorization page gating the Lab Workspaces tab
metadata:
  type: project
  context:
    - design-system
    - authentication
    - tab-navigation
  files:
    - client/src/components/LabAuthPage.tsx
    - client/src/pages/Home.tsx
    - client/src/index.css
---

## Lab Workspace Authorization — Implementation Summary

### Architecture

Invitation-only system. Admin pre-approves emails in `server/allowed_users.json`. Whitelisted users can then set their own access key.

**Flow:**
1. User enters email → `POST /api/auth/status` checks whitelist + whether a password is already set
2. New user (whitelisted, no password) → "Create Access Key" form → `POST /api/auth/register`
3. Returning user (whitelisted, has password) → "Enter Access Key" form → `POST /api/auth/verify`
4. All passwords hashed with per-user salt, stored in the same JSON file

### How to Manage Access

Edit `server/allowed_users.json`:
```json
{
  "users": [
    { "email": "gchandra@vinciai.academy" },
    { "email": "newuser@vinci.ai" }
  ]
}
```
Add a new `{ "email": "..." }` entry to grant access. Remove an entry to revoke. Passwords are set by users themselves on first login and stored inline:
```json
{ "email": "gchandra@vinciai.academy", "passwordHash": "abc...", "salt": "def..." }
```

### Files

| File | Purpose |
|------|---------|
| `server/allowed_users.json` | Whitelist + user-set password hashes |
| `server/index.ts` | Express: `/api/auth/status`, `/register`, `/verify` |
| `vite.config.ts` | Vite dev plugin: same endpoints (reads the same JSON file) |
| `client/src/components/LabAuthPage.tsx` | Multi-step UI: email → create-key or enter-key |
| `client/src/pages/Home.tsx` | Session gating (15-min localStorage session) |

### API Endpoints

| Endpoint | Input | Output |
|----------|-------|--------|
| `POST /api/auth/status` | `{ email }` | `{ whitelisted, hasPassword }` |
| `POST /api/auth/register` | `{ email, password }` | `{ success }` (sets hash + salt) |
| `POST /api/auth/verify` | `{ email, password }` | `{ success }` or `{ needsPassword }` |

### Design Alignment

All design tokens match the Industrial-Editorial system in `auth_page_design/DESIGN.md`:
- Pale Blue-Gray canvas
- Dark Navy text
- Teal-Blue accent
- Cinzel (serif) headings, JetBrains Mono (monospace) labels
- Diagonal watermark
- 1px solid borders, sharp-ish corners
- Semantic status colors (Amber, Green, Teal)

### Verification
- TypeScript: `npx tsc --noEmit` passes cleanly
- Dev server: `npm run dev` → click "Lab Workspaces" → auth page appears
- Auth flow: enter credentials → pending → success → lab workspace loads
- Persistence: refresh page → auth survives (until 15-min expiry)
- Sign out: click sign-out → returns to auth page