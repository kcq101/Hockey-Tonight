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
| Top | Pass (tap, or swipe toward a teammate) | Switch player |
| Left | Slapshot: hold to wind up, let go to fire | Poke check |
| Right | Wrist shot (swipe off to pick a corner) | Speed burst, or a body check when an opponent is close |
| Bottom | Speed burst (hold; uses stamina) | Same as right: speed burst, or body check when close |

On defense the bottom and right buttons turn red and read "Check" when a body check is available.

### Scoring moves

- **One-timer:** press either shot button while a pass is on its way (both glow "ONE TIMER"). Cross-ice one-timers are hardest to stop.
- **Spin-o-rama:** circle the stick a full turn while carrying. A goalie nearby bites; shoot right after and it goes to the open side.
- **Wraparound:** carry it behind the net and come out the other side. The game pulls you tight to the post; shoot right away to stuff it in.

Tap a teammate on the ice to pass to him.

### Fights

Big hits build bad blood. Once a team has taken enough, the next solid hit can start a fight (at most one a period, two a game; never in the last minute of a close third). Play stops, the gear comes off, and the camera cuts to a side-on fight cam:

| Button | In a fight |
|---|---|
| Left | Jab |
| Right | Haymaker (slow, hits hard, steps in; breaks a grab) |
| Bottom | Block (hold) |
| Top | Grab his jersey; press again to pull him off balance for a free shot |

First one out of stamina goes down. After 14 seconds the linesmen step in. Leave the buttons alone and your guy fights on his own.

Keyboard: WASD/arrows; J = top, U = left, K or Space = right, L or Shift = bottom; P pause.

## Project layout

- `index.html` — the whole game (HTML, CSS, JavaScript; no build step)
- `music/` — soundtrack (The Stanley Cup, Arcade Groove, Rink Bounce)
- `img/` — title screen art and the team-select backdrop
- `icons/`, `manifest.webmanifest` — home-screen app setup

## Roadmap

- Feel tuning (skating speed, checking, scoring rate)
- Offsides, icing, penalties
- Online multiplayer against friends

## Player sprites
Players are drawn from `img/sk/atlas.webp` (+ `atlas.json`), built from the key-colour source art in `art/src/`
(magenta = jersey, cyan = stripes, lime = helmet/gloves/pants). The game recolours the atlas for the two teams
at the start of each match. To rebuild after changing the art: `python3 tools/build_sprites.py`
(needs Pillow, NumPy and SciPy). `art/src/` is never loaded by the game.

## Fight sprites
`img/sk/fight.webp/json` is a side-view set rendered from the Meshy fight GLB (same key colours and Mixamo rig; helmetless,
bare fists). The jersey grab is faked with two-bone IK on the lead arm. To rebuild: put the GLB at `m.glb` next to
`tools/fight/fight.html` with three@0.160.0 installed, serve that folder on port 8811, `python3 tools/fight/jobs.py`,
`node tools/fight/rend.js jobs.json fr`, then `python3 tools/build_fight_sprites.py fr img/sk 0.6 90`.
The GLB itself is not in the repo (14 MB); the game only loads the 770 KB atlas, a moment after a match starts.
