# Build Integration with Plex Streaming — Handoff

A summary of the full design conversation, from concept to implementation plan.

---

## The goal

Replicate the experience of turning on the TV and a movie already being on — like a TV channel, not a streaming service. You don't choose, you just arrive. The key detail that makes it feel like TV is that the movie is already mid-way through when you get there.

---

## The core mechanic

Treat the Plex library as a virtual channel that's been "broadcasting" since midnight. Based on the current time, calculate what would be playing *right now* and at what offset into the film. Push that to the TV at that exact point — so you join mid-film. Without the mid-movie start, it still feels like choosing. That offset is what sells the illusion.

---

## Setup

- **Plex server:** Running on a PC at home (always on), media on an attached hard drive
- **Clients:** Apple TV on multiple TVs (and possibly Roku — see note below)
- **Library:** Existing Plex movie library

---

## How Plex pushes to a TV

When the Plex app is open on a client (Apple TV, Roku, etc.), it registers itself with the Plex Media Server as an available player on the local network. Via the API, you can send that player a "play this, starting at this point" command. It's not a push in the notification sense — the client is listening for commands from the server, and the script tells the server to issue one.

**The catch:** the Plex app must already be open on the TV for it to be registered and reachable. If the app is closed, the server has no one to talk to.

---

## Why a scheduled task doesn't work

A Windows Task Scheduler approach — run the script at 7pm every evening — was considered and ruled out. If the TV isn't on and the Plex app isn't open at the exact moment the script runs, it fails silently. Timing can't be guaranteed.

---

## The solution: phone button

1. Turn on TV, open Plex app (client registers with server)
2. Tap one button on your phone
3. Movie starts mid-way on the TV

This works reliably because the trigger happens *after* the TV is already ready. One tap from the couch. The mid-movie start does the rest.

**What to build:**
- **Python script** — connects to Plex server via `plexapi`, picks a movie, calculates the live offset, pushes to the TV client
- **Small Flask web server** — runs on the PC, exposes a local endpoint
- **iOS Shortcut** — one button on your phone that hits the server URL over the home network; could also be a Siri command

---

## Letterboxd integration (discussed, not yet built)

Using Letterboxd ratings to inform which movies get picked — so the channel selects films you'd actually like. Two options discussed:
- Share public profile URL (can be fetched directly)
- Export full data as CSV from Letterboxd Settings → Import & Export (richer, includes all ratings and diary)

This was not resolved before the conversation ended.

---

## Note on Roku

A separate conversation (in a Claude Project / Obsidian note titled *Plex Channel Handoff.md*) apparently shifted the client from Apple TV to Roku. That document was not accessible during this session and its contents were not confirmed. **Before building, verify which client(s) are in scope.**

---

## Files in this repo

- `plex-channel.md` — shorter design notes, same project
- `generate.py` — existing Airtable → HTML generator (unrelated, but same repo)

---

## Key dependencies

```
pip install plexapi flask
```

---

## Next steps

1. Confirm client device (Apple TV, Roku, or both)
2. Incorporate contents of *Plex Channel Handoff.md* from Google Drive / Claude Projects
3. Get Plex server local IP and auth token
4. Optionally decide on Letterboxd integration approach
5. Build and test the script
