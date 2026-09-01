# TikTok carousel — camera apps for filmmakers

Seven 1080×1920 slides ranking five iPhone camera apps, with Witness at number
two. Built on the site's own palette and type so the carousel and
witnessrecord.app read as one thing.

`build-slides.py` generates the seven `.dc.html` artboards; `canvas.json` lays
them out and carries the draft caption. `camera-apps-carousel.html` is the
assembled canvas — export each artboard as PNG from its toolbar and post them
in canvas order.

The four third-party icon tiles are placeholders: drop the real icons in as
icon-blackmagic.png, icon-kino.png, icon-filmicpro.png and icon-finalcutcamera.png
and re-run the build, which picks up any icon-<stem>.png it finds.

The Witness slide leads on the one thing no other app here does — footage
leaving the phone mid-record — and states the ProRes limitation and the
authorship conflict on the slide itself, the same way compare.html does.
