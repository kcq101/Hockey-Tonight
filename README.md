# Hockey Tonight

Arcade 5-on-5 hockey in the spirit of NHL '94, built for phones. Top-down vertical rink, one-timers, big hits, speed bursts, and an original soundtrack.

## Play

Open the GitHub Pages link on your phone, then:

- **iPhone (Safari):** Share → Add to Home Screen
- **Android (Chrome):** menu → Add to Home screen / Install app

Launching from the home-screen icon runs the game full-screen.

## Controls

Four equal buttons in a diamond at the bottom right, plus the stick on the left.

| Button | Offense | Defense |
|---|---|---|
| Top | Speed burst (hold; uses stamina) | Speed burst, or a body check when an opponent is close |
| Left | Slapshot: hold to wind up, let go to fire | Poke check |
| Right | Wrist shot (swipe off to pick a corner) | Same as top: speed burst, or body check when close |
| Bottom | Pass (tap, or swipe toward a teammate) | Switch player |

On defense the top and right buttons turn red and read "Check" when a body check is available.

### Scoring moves

- **One-timer:** press either shot button while a pass is on its way (both glow "ONE TIMER"). Cross-ice one-timers are hardest to stop.
- **Spin-o-rama:** circle the stick a full turn while carrying. A goalie nearby bites; shoot right after and it goes to the open side.
- **Wraparound:** carry it behind the net and come out the other side. The game pulls you tight to the post; shoot right away to stuff it in.

Tap a teammate on the ice to pass to him.

Keyboard: WASD/arrows; L or Shift = top, U = left, K or Space = right, J = bottom; P pause.

## Project layout

- `index.html` — the whole game (HTML, CSS, JavaScript; no build step)
- `music/` — soundtrack (The Stanley Cup, Arcade Groove, Rink Bounce)
- `img/` — title screen art and the team-select backdrop
- `icons/`, `manifest.webmanifest` — home-screen app setup

## Roadmap

- Feel tuning (skating speed, checking, scoring rate)
- Offsides, icing, penalties
- Online multiplayer against friends
