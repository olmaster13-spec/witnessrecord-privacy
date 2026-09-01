# TikTok carousel — camera apps for filmmakers

Seven 1080×1920 slides ranking five iPhone camera apps, with Witness at number
two. Built on the site's own palette and type so the carousel and
witnessrecord.app read as one thing.

`build-slides.py` generates the seven `.dc.html` artboards; `canvas.json` lays
them out and carries the draft caption. `camera-apps-carousel.html` is the
assembled canvas — export each artboard as PNG from its toolbar and post them
in canvas order.

The four third-party icon tiles are placeholders. The build box has no network
egress, so the icons have to be fetched by hand from their App Store listings
and saved into this folder; the build picks up any `icon-<stem>.png` it finds.

| save as | from |
| --- | --- |
| `icon-blackmagic.png` | apps.apple.com/us/app/blackmagic-camera/id6449580241 |
| `icon-kino.png` | apps.apple.com/us/app/kino-pro-video-camera/id6472380172 |
| `icon-filmicpro.png` | apps.apple.com/us/app/filmic-pro-video-camera/id436577167 |
| `icon-finalcutcamera.png` | apps.apple.com/us/app/final-cut-camera/id6469552837 |

The Witness slide leads on the one thing no other app here does — footage
leaving the phone mid-record — and states the ProRes limitation and the
authorship conflict on the slide itself, the same way compare.html does.
