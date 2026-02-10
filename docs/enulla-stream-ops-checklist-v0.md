# ExNulla Stream Ops — Setup + Build Checklist (v0)

Owner: James Huson
Workspace: Windows 10 (OBS) + WSL + SSH → DigitalOcean droplet → GitHub (Thesis-Web)  
Primary domains: exnulla.com (Cloudflare)  
Primary stream targets (Phase 1): Kick + Twitch  
Marketing funnels: TikTok / Instagram / Facebook / YouTube (later)

> **Modes**
> - **Design Mode**: docs, requirements, architecture, runbooks.
> - **Code Mode**: shell commands, repo edits, CI, config exports.
> - **Discuss Mode**: tradeoffs, options, decisions.

---

## 0) Decisions to lock before creating the repo

### 0.1 Repo name
Recommended (clean, explicit):  
- **`exnulla-stream-ops`** 

### 0.2 Repo visibility + licensing
- **Public** repo recommended 
- **No secrets** committed. Anything sensitive goes to:
  - private password manager
  - `.env` files (ignored)
  - encrypted vault (if needed)
- License options:
  - If you want maximum reuse: **MIT**
  - If you want to discourage reuse without permission: **All rights reserved** (no OSS license)
  - If you want “share but keep credit”: **CC BY 4.0** for docs (common for non-code)

**Default recommendation:** MIT for code + CC BY 4.0 for docs (if you want clean attribution), but pick one to keep it simple.

---

## 1) Pre-project checklist (platform, infra, accounts, security)

### 1.1 Account baseline (Twitch + Kick)
**Goal:** Get both accounts out of “empty shell” status and into “discoverable”.

For each platform account:
- [ ] Profile photo / avatar
- [ ] Banner / header
- [ ] Bio (short + long variants)
- [ ] About panels / sections (Twitch)
- [ ] Stream category defaults (Software & Game Dev / Just Chatting / etc.)
- [ ] Channel tags / keywords (dev, systems, architecture, infra, etc.)
- [ ] Channel trailer (optional, but high ROI)
- [ ] Schedule (even if “weekly cadence TBD” — set *something*)
- [ ] Moderation settings:
  - [ ] Email verification required (if available)
  - [ ] Phone verification (if available)
  - [ ] AutoMod / blocked terms / link restrictions
- [ ] VOD settings:
  - [ ] Enable VOD storage (Twitch)
  - [ ] Default publish behavior
- [ ] Clip settings:
  - [ ] Who can clip
  - [ ] Clip length defaults



### 1.2 Streaming policy / simulcasting compliance (do early)
- [ ] Confirm your Twitch account’s current simulcast rules you must follow (affiliate/partner vs not).
- [ ] Confirm Kick’s multistream toggle/requirements if any apply to your account status.
- [ ] Record the “rules snapshot” in repo docs so your stream ops are compliant.

*(We’ll document confirmed rules once you capture the exact policy pages or toggles you see.)*

### 1.3 Domain + Cloudflare baseline (exnulla.com)
- [ ] Ensure Cloudflare DNS is authoritative for the zone.
- [ ] DNS records planned:
  - `A` record for `@` → droplet IP (or Cloudflare Tunnel later)
  - `CNAME` for `www` → `@` (or `A` record if you prefer)
- [ ] TLS mode: **Full (strict)** once origin cert/Let’s Encrypt is in place.
- [ ] Enable basic protections:
  - [ ] Always Use HTTPS
  - [ ] Automatic HTTPS Rewrites
  - [ ] WAF baseline rules (optional initially)
  - [ ] Rate limiting (optional)
- [ ] Caching:
  - Keep simple at first; do not cache API endpoints.
- [ ] Email routing (optional): `hello@exnulla.com` forwarding.

### 1.4 DigitalOcean droplet baseline (security + hygiene)
- [ ] OS: Ubuntu 24.04 LTS
- [ ] Non-root deploy user (already)
- [ ] SSH hardening:
  - [ ] SSH keys only (no password auth)
  - [ ] `PermitRootLogin no`
  - [ ] `PasswordAuthentication no`
- [ ] Firewall:
  - [ ] UFW enabled
  - [ ] Allow: 22/tcp, 80/tcp, 443/tcp
- [ ] Fail2ban (optional but recommended)
- [ ] Automatic security updates:
  - [ ] `unattended-upgrades` enabled
- [ ] Backups / snapshots:
  - [ ] DO backups on, or weekly snapshots

### 1.5 Nginx + TLS baseline
- [ ] Nginx site for `exnulla.com` and `www.exnulla.com`
- [ ] HTTP → HTTPS redirect
- [ ] Let’s Encrypt cert via `certbot` (or Cloudflare origin cert if you prefer strict Cloudflare-only)
- [ ] Standard security headers for static site
- [ ] Gzip / Brotli (optional)
- [ ] Log rotation (usually default)

### 1.6 GitHub org baseline (Thesis-Web)
- [ ] Repo created (name chosen above)
- [ ] Branch protection:
  - [ ] Require PR reviews (optional for solo, but professional)
  - [ ] Require status checks (CI)
  - [ ] Prevent force-push to `main` (recommended)
- [ ] Repo settings:
  - [ ] Issues on
  - [ ] Discussions optional
  - [ ] Dependabot alerts on

---

## 2) Project setup checklist (repo + CI + docs skeleton)

### 2.1 Create repo (GitHub UI)
- [ ] Name: `exnulla-stream-ops`
- [ ] Visibility: Public (or Private if you decide)
- [ ] Initialize:
  - [ ] **Do NOT** add README in UI if you prefer first commit from droplet
  - or add README if you want; we’ll overwrite as needed

### 2.2 Clone to droplet (SSH)
On droplet:
```bash
cd ~/repos
git clone git@github.com-thesisweb:Thesis-Web/exnulla-stream-ops.git
cd exnulla-stream-ops
```

### 2.3 Baseline repo hygiene (P0)
Create these files immediately:
- [ ] `README.md`
- [ ] `LICENSE`
- [ ] `.gitignore`
- [ ] `.editorconfig`
- [ ] `.prettierrc` + `package.json` (if using Prettier for md/json/yaml)
- [ ] `.github/workflows/ci.yml`
- [ ] `docs/` skeleton
- [ ] `configs/` placeholders (empty, documented)

Recommended `.gitignore` items:
- `.env`
- `*.local`
- `.DS_Store`
- `node_modules/` (if you add tooling)
- `configs/**/secrets*` (defense in depth)
- exported OBS configs may include cache/temp — ignore as needed

### 2.4 CI checks (minimum viable)
CI goals:
- prevent broken markdown
- prevent broken links
- enforce formatting

Options:
- Node-based (simple): `prettier`, `markdownlint`, `lychee` link checker
- Or GitHub Actions marketplace actions for markdownlint + lychee

Minimum checks:
- [ ] Markdown lint
- [ ] Link check (tolerate `localhost` and known rate-limited domains)
- [ ] Prettier format check

### 2.5 First commit (from droplet)
- [ ] Add baseline files + docs skeleton
- [ ] Commit message: `chore: initialize stream ops repo`
- [ ] Push to `main`

```bash
git status
git add .
git commit -m "chore: initialize stream ops repo"
git push origin main
```

---

## 3) Project blueprint checklist (what we build and document)

### 3.1 Docs structure (recommended)
```
docs/
  00-vision.md
  10-platforms/
    twitch.md
    kick.md
    youtube.md
    tiktok.md
    instagram.md
    facebook.md
  20-stream-architecture/
    overview.md
    obs-profile-scene-collection.md
    multistreaming.md
    alerts-overlays.md
    chat-bots-moderation.md
    commands-timers.md
  30-brand/
    identity.md
    logo-usage.md
    emotes.md
    panels-bio-copy.md
    seo-keywords.md
  40-growth-funnel/
    pin-comment-and-cta.md
    linkedin-funnel.md
    short-form-clip-workflow.md
    schedule-and-topics.md
  50-music-and-rights/
    policy.md
    audiio-workflow.md
    spotify-workflow.md
    certificate-management.md
  90-runbooks/
    go-live-checklist.md
    end-stream-checklist.md
    incident-response.md
    backup-restore.md
```

### 3.2 Vision + positioning (docs/00-vision.md)
- [ ] One-paragraph statement of purpose
- [ ] Target audience:
  - dev community
  - recruiters/hiring managers
  - founders needing fractional help
  - peers “same boat”
- [ ] Stream pillars (content categories):
  - systems architecture + infra work
  - repo hygiene + CI
  - building public portfolio sites
  - interview prep / case studies
  - real-world troubleshooting sessions
- [ ] “From zero” rules:
  - new accounts
  - build in public
  - publish operational blueprint

### 3.3 Account metadata copy packs (docs/30-brand/panels-bio-copy.md)
Produce copy variants:
- [ ] 1-line bio
- [ ] 2–3 sentence bio
- [ ] Long-form “About”
- [ ] Tag list (keywords)
- [ ] Stream titles templates:
  - “Building X in public — infra/CI/architecture”
  - “Fixing Y — live debugging (postmortem included)”
- [ ] Pinned CTA copy templates:
  - “Connect on LinkedIn: …”
  - “Portfolio hub: …”
  - “Repos: …”

### 3.4 OBS scene collection (docs + versioning plan)
Current OBS: 32.0.4 on Windows 10  
Current devices:
- Display capture (desktop)
- OBSBOT Tiny (camera inset)
- Blue Yeti mic (filters applied)
Existing scenes:
- BRB scene
Needed scenes:
- [ ] Starting Soon
- [ ] Main (desktop + cam inset + lower third)
- [ ] BRB
- [ ] Ending / Thanks
- [ ] “Just Chatting” (cam larger + agenda panel)
- [ ] “Code Focus” (desktop dominant, minimal distractions)
- [ ] “Interview / Call” (capture window + privacy mask)

Checklist to document:
- [ ] Naming conventions (Scenes, Sources)
- [ ] Audio routing conventions
- [ ] Filter settings summary (no secrets)
- [ ] Export procedure (what files, where stored)
- [ ] Sanitization checklist (remove stream keys, cache paths)

### 3.5 Multistream plan (Phase 1: Kick + Twitch)
Document two approaches:
- [ ] Aggregator (Restream or similar)
- [ ] Direct multi-RTMP (plugin-based)

Phase 1 recommended approach:
- [ ] Use aggregator for speed, document constraints
- [ ] Define failover plan: if aggregator fails, go single-platform

### 3.6 Alerts + overlays plan
Baseline:
- [ ] Alerts provider (choose)
- [ ] Overlay layers:
  - alert layer
  - lower third / now playing (later)
  - chat overlay (optional)
- [ ] Browser Sources:
  - resolution standards
  - safe margins
  - performance notes

### 3.7 Moderation + bot plan
Goals:
- stop spam/bots
- automate CTAs
- automate social links
- consistent commands cross-platform

Checklist:
- [ ] Choose one primary bot that supports Kick+Twitch (and later YouTube)
- [ ] Configure:
  - [ ] link posting rules
  - [ ] keyword filters
  - [ ] first-time chatter rules
  - [ ] follower-only / email verification toggles (platform-specific)
- [ ] Commands:
  - `!linkedin`
  - `!site`
  - `!github`
  - `!schedule`
  - `!stack`
  - `!music`
- [ ] Timers:
  - every 10–15 minutes: CTA
  - every 30 minutes: “what we’re building today”

### 3.8 Website hub (exnulla.com) plan
Phase 1 site:
- [ ] Single landing page:
  - headline + positioning
  - link cards: LinkedIn / GitHub / Live channels
  - current focus + “now building”
  - email capture (optional)
- [ ] Hosted as static site behind nginx
- [ ] Cloudflare in front (strict HTTPS)

Phase 2:
- [ ] Blog / changelog
- [ ] Stream schedule integration
- [ ] “Proof of work” page linking repos and streams

### 3.9 Music plan (Spotify now, Audiio later)
Phase 1 (Spotify):
- [ ] Document “risk” clearly (copyright, VOD muting)
- [ ] Keep music on a separable audio channel if possible
- [ ] Editing workflow: remove/duck music for clips if needed

Phase 2 (Audiio):
- [ ] Library structure (tracks + licenses)
- [ ] Certificate retention workflow
- [ ] Document proof pack export
- [ ] Ensure any “license terms” constraints are documented

---

## 4) Runbooks (operational excellence)

### 4.1 Go-live checklist (docs/90-runbooks/go-live-checklist.md)
- [ ] Title + category set correctly
- [ ] Correct scene (Starting Soon)
- [ ] Audio check:
  - mic levels
  - noise gate not clipping
  - desktop audio sane
- [ ] Recording enabled (optional)
- [ ] Bot connected + timers active
- [ ] Pinned message posted (per platform)
- [ ] Stream markers plan (optional)
- [ ] Backup plan if stream drops

### 4.2 End-stream checklist (docs/90-runbooks/end-stream-checklist.md)
- [ ] Switch to Ending scene
- [ ] Thank-you CTA + schedule reminder
- [ ] Stop stream
- [ ] Confirm VOD saved
- [ ] Clip highlights list (timestamps)
- [ ] Post-stream notes (what to fix next)

### 4.3 Incident response (docs/90-runbooks/incident-response.md)
- [ ] Audio failure
- [ ] Dropped frames / encoder overload
- [ ] Bot spam event
- [ ] Account lock / security flags
- [ ] Multistream aggregator outage

---

## 5) Security checklist (secrets and operational safety)
- [ ] Never commit:
  - stream keys
  - webhook URLs
  - bot tokens
  - OAuth client secrets
- [ ] Store secrets:
  - local password manager
  - `.env` (ignored)
- [ ] Rotate keys quarterly (or after any suspected leak)
- [ ] Limit moderator permissions on platforms

---

## 6) Execution order (the “first week” plan)
**Day 1**
- [ ] Create repo
- [ ] Clone to droplet
- [ ] Commit baseline hygiene + docs skeleton + CI

**Day 2**
- [ ] Write 00-vision + platform baseline docs
- [ ] Draft bio/panels copy pack
- [ ] Implement pinned CTA plan + commands list

**Day 3**
- [ ] OBS scene plan documented
- [ ] Export + sanitize scene collection (documented)
- [ ] Choose alerts provider + bot (documented)

**Day 4–5**
- [ ] exnulla.com phase-1 landing page deployed
- [ ] Multistream (Kick + Twitch) approach selected + implemented
- [ ] Runbooks finalized

---

## 7) Notes / assumptions to validate (no guessing policy)
These items are intentionally left as “to confirm”:
- exact Twitch simulcast constraints for your account status
- exact Kick multistream toggle behavior for your account status
- the specific bot you choose and its platform feature parity
- whether Spotify music is acceptable for your risk tolerance for VODs


