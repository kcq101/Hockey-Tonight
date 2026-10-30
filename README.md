# Hockey Tonight — Blue Line Blitz

Arcade 5-on-5 hockey in the spirit of NHL '94, built for phones. Top-down vertical rink, one-timers, big hits, speed bursts, and an original soundtrack.

## Play

Open the GitHub Pages link on your phone, then:

- **iPhone (Safari):** Share → Add to Home Screen
- **Android (Chrome):** menu → Add to Home screen / Install app

Launching from the home-screen icon runs the game full-screen.

## Controls

| Control | Offense | Defense |
|---|---|---|
| Left stick | Skate | Skate |
| Pass | Tap to pass, swipe to aim at a teammate | Switch player |
| Shoot | Tap for a wrister, hold for a slapper, swipe to pick a corner | Body check |
| Speed | Hold for a burst (uses stamina) | Same |

Press Shoot while a pass is on its way for a one-timer. Tap a teammate on the ice to pass to him.

Keyboard: WASD/arrows, J pass, K shoot, L or Shift speed, P pause.

## Project layout

- `index.html` — the whole game (HTML, CSS, JavaScript; no build step)
- `music/` — soundtrack (The Stanley Cup, Arcade Groove, Rink Bounce)
- `icons/`, `manifest.webmanifest` — home-screen app setup

## Roadmap

- Feel tuning (skating speed, checking, scoring rate)
- Offsides, icing, penalties
- Online multiplayer against friends
