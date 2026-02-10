# Exports

This directory is for tool exports that make the stream setup reproducible across machines.

## What belongs here

- `exports/obs/`
  - OBS scene collection exports
  - OBS profile exports
- `exports/streamerbot/`
  - Streamer.bot exports (actions/triggers/config backups)

## What does NOT belong here

- Secrets (keys, tokens, credentials)
- Anything containing private account recovery data
- Machine-specific temp files that churn on every run

## Suggested cadence

- Export and commit after:
  - meaningful scene changes
  - overlay/tooling changes
  - Streamer.bot action/trigger changes
- Keep commits small and descriptive.

## Naming

Prefer timestamped filenames when exporting manually, e.g.:

- `obs-scene-collection-YYYY-MM-DD.json`
- `streamerbot-actions-YYYY-MM-DD.json`
