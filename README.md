# Hockey Tonight

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
| Shoot | Tap for a wrister, hold for a slapper, swipe to pick a corner | Check: locks onto the nearest opponent and drives through him |
| Spin / Poke | Spin-o-rama | Poke check: stick reaches out to knock the puck loose |
| Speed | Hold for a burst (uses stamina) | Same |

### Scoring moves

- **One-timer:** press Shoot while a pass is on its way (the button glows "1-TIMER"). Cross-ice one-timers are hardest to stop.
- **Spin-o-rama:** circle the stick a full turn while carrying (or tap Spin). A goalie nearby bites; shoot right after and it goes to the open side.
- **Wraparound:** carry it behind the net and come out the other side. The game pulls you tight to the post; shoot right away to stuff it in.

Tap a teammate on the ice to pass to him.

Keyboard: WASD/arrows, J pass, K shoot, U spin/poke, L or Shift speed, P pause.

## Project layout

- `index.html` — the whole game (HTML, CSS, JavaScript; no build step)
- `music/` — soundtrack (The Stanley Cup, Arcade Groove, Rink Bounce)
- `img/` — title screen art and the team-select backdrop
- `icons/`, `manifest.webmanifest` — home-screen app setup

## Roadmap

- Feel tuning (skating speed, checking, scoring rate)
- Offsides, icing, penalties
- Online multiplayer against friends
