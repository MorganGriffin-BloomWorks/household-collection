# Plex Channel — Design Notes

The goal is to replicate the experience of turning on the TV and a movie already being on — like a TV channel, not a streaming service. You don't choose, you just arrive.

---

## The core mechanic

Treat the Plex library as a virtual channel that's been "broadcasting" since midnight. Based on the current time, calculate what would be playing *right now* and at what offset into the film. When triggered, push that movie to the Apple TV at that exact point — so you join mid-film, exactly like TV.

---

## Setup

- **Plex server:** Running on a PC at home (always on), media on an attached hard drive
- **Clients:** Apple TV on multiple TVs
- **Library:** Existing Plex movie library, filtered by rating / not recently watched

---

## How triggering works

**Why not a scheduled task:** The script can only push to an Apple TV if the Plex app is already open on it. If the script runs before the TV is on, it fails silently. So scheduling doesn't work reliably.

**The solution — phone button:**
1. Turn on TV, open Plex on Apple TV (Plex app registers itself with the server as an available client)
2. Tap one button on your phone
3. Movie starts playing mid-way on the TV

One tap, from the couch. The mid-movie start sells the illusion.

---

## What to build

1. **Python script** — connects to Plex server via `plexapi`, picks a movie, calculates live offset, pushes to Apple TV client
2. **Small Flask web server** — runs on the PC, exposes a local endpoint the script listens on
3. **iOS Shortcut** — one button on your phone that hits the local server URL over the home network. Could also be a Siri command.

---

## Key library

```
pip install plexapi flask
```
