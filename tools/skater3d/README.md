# 3D skater sprite pipeline

`img/sk/atlas3d.webp/json` is rendered from a rigged GLB skater (Meshy, Mixamo skeleton, key-coloured texture:
magenta jersey, cyan stripes, lime helmet/gloves/pants) posed procedurally with two-bone IK and a stick in code.

1. `npm i three@0.160.0 playwright`, put the model at `m.glb` next to `pose.html`, serve the folder (`python3 -m http.server 8810`).
2. Make a jobs list (names `run_<DIR>_<0-7>_<C|L|R>`, `idle_<DIR>`, `accel_<E|S|N>`; DIR in S SE E NE N; `phi` = k*pi/4, `u` = stick side in metres: C .55, L -.05, R 1.0) and run `node render.js "$(cat jobs.json)"` -> `fr3d/*.png` + `meta.json`.
3. `python3 tools/build_3d_sprites.py fr3d img/sk 0.34` packs the atlas (frame = x,y,w,h, footAnchorX, puckX, puckY, footAnchorY).

The game falls back to the 2D atlas for any frame not in the 3D set, and `?classic` in the URL turns the 3D set off.
