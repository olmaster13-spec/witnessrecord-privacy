# -*- coding: utf-8 -*-
"""Generates the seven .dc.html artboards for the TikTok carousel.
Palette and type are lifted from the site's style.css so the slides and the
site read as one thing."""

import os

BG      = "#08080a"
RAISED  = "#101013"
LINE    = "#26262c"
LINE_S  = "#34343c"
TEXT    = "#f2f2f3"
TEXT_2  = "#b9b9c0"
TEXT_3  = "#85858f"
RED     = "#e82e3b"
RED_S   = "#ff6b5e"
GHOST   = "#2c2c34"
GHOST_T = "#4a4a55"
SURFACE = "#16161a"

FONT = ("-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', "
        "'Segoe UI', Roboto, Helvetica, Arial, sans-serif")

SHELL = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <style>
    body {{ margin: 0; font-family: {font}; -webkit-font-smoothing: antialiased; }}
    a {{ color: {red_s}; }} a:hover {{ color: #ff8f85; }}
  </style>
</helmet>
{body}
</x-dc>
</body>
</html>
"""


def frame(inner):
    return (
        '<div style="width: 1080px; height: 1920px; background: %s; color: %s; '
        'padding: 88px 80px; display: flex; flex-direction: column; '
        'box-sizing: border-box; overflow: hidden;">\n%s\n</div>' % (BG, TEXT, inner)
    )


def kicker(n):
    """Top rail: what this is, and where you are in the stack."""
    return (
        '<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 24px;">\n'
        '  <div style="font-size: 25px; font-weight: 600; letter-spacing: 0.18em; '
        'text-transform: uppercase; color: %s;">Camera apps for filmmakers</div>\n'
        '  <div style="font-size: 25px; font-weight: 600; letter-spacing: 0.18em; color: %s;">'
        '<span style="color: %s;">%02d</span>&#8202;/&#8202;07</div>\n'
        '</div>\n'
        '<div style="height: 1px; background: %s; margin: 28px 0 0;"></div>'
        % (TEXT_3, TEXT_3, TEXT, n, LINE)
    )


def footer(note=None):
    left = (
        '<div style="display: flex; align-items: center; gap: 14px;">\n'
        '    <img src="witness-mark.png" alt="" style="width: 40px; height: 40px; display: block;">\n'
        '    <span style="font-size: 26px; font-weight: 600; color: %s;">witnessrecord.app</span>\n'
        '  </div>' % TEXT_3
    )
    right = ''
    if note:
        right = ('<div style="font-size: 24px; color: %s; text-align: right;">%s</div>' % (TEXT_3, note))
    return (
        '<div style="height: 1px; background: %s; margin: 0 0 26px;"></div>\n'
        '<div style="display: flex; align-items: center; justify-content: space-between; gap: 24px;">\n'
        '  %s\n  %s\n</div>' % (LINE, left, right)
    )


def spec(text):
    """A dash-led supporting line. The dash is a rule, not a glyph, so it
    stays crisp at export size."""
    return (
        '  <div style="display: flex; gap: 24px; align-items: flex-start;">\n'
        '    <div style="width: 26px; height: 2px; background: %s; flex: none; margin-top: 22px;"></div>\n'
        '    <div style="font-size: 34px; line-height: 1.45; color: %s;">%s</div>\n'
        '  </div>' % (RED, TEXT_2, text)
    )


def pill(text, accent=False):
    color = RED_S if accent else TEXT_2
    border = "rgba(232, 46, 59, 0.45)" if accent else LINE_S
    bg = "rgba(232, 46, 59, 0.08)" if accent else "transparent"
    return (
        '  <div style="border: 1px solid %s; background: %s; border-radius: 999px; '
        'padding: 12px 26px; font-size: 27px; font-weight: 600; color: %s;">%s</div>'
        % (border, bg, color, text)
    )


def icon(stem, initials):
    """The app's icon, if we have it. The four third-party icons are not in
    this repo and Apple's endpoints are not reachable from the build box, so
    those render as an obvious placeholder until someone drops the real PNG in
    as icon-<stem>.png and re-runs this script. The icons live on these App
    Store listings:

        Blackmagic  apps.apple.com/us/app/blackmagic-camera/id6449580241
        Kino        apps.apple.com/us/app/kino-pro-video-camera/id6472380172
        FilmicPro   apps.apple.com/us/app/filmic-pro-video-camera/id436577167
        FinalCut    apps.apple.com/us/app/final-cut-camera/id6469552837
    """
    path = 'witness-icon.png' if stem == 'Witness' else 'icon-%s.png' % stem.lower()
    if os.path.exists(path):
        return ('<img src="%s" alt="" style="width: 168px; height: 168px; '
                'border-radius: 38px; display: block; flex: none;">' % path)
    return (
        '<div style="width: 168px; height: 168px; border-radius: 38px; flex: none; '
        'background: %s; border: 2px dashed %s; display: flex; align-items: center; '
        'justify-content: center; font-size: 52px; font-weight: 700; '
        'letter-spacing: -0.02em; color: %s;">%s</div>' % (SURFACE, LINE_S, GHOST_T, initials)
    )


def app_slide(n, rank, name, pills, hook, specs, best_for, stem, initials, disclosure=None):
    rank_color = RED if disclosure else GHOST
    parts = []
    parts.append(kicker(n))
    parts.append('<div style="flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 0;">')
    parts.append(
        '  <div style="display: flex; align-items: center; justify-content: space-between; gap: 32px;">\n'
        '    <div style="font-size: 200px; font-weight: 700; letter-spacing: -0.06em; '
        'line-height: 0.82; color: %s;">%s</div>\n'
        '    %s\n'
        '  </div>' % (rank_color, rank, icon(stem, initials))
    )
    parts.append(
        '  <h2 style="margin: 18px 0 0; font-size: 104px; font-weight: 700; '
        'letter-spacing: -0.035em; line-height: 1.0; color: %s;">%s</h2>' % (TEXT, name)
    )
    parts.append('  <div style="display: flex; flex-wrap: wrap; gap: 14px; margin-top: 30px;">')
    parts.append('\n'.join(pill(p, a) for p, a in pills))
    parts.append('  </div>')
    parts.append(
        '  <p style="margin: 44px 0 0; font-size: 52px; font-weight: 500; line-height: 1.24; '
        'letter-spacing: -0.02em; color: %s; text-wrap: pretty;">%s</p>' % (TEXT, hook)
    )
    parts.append('  <div style="height: 1px; background: %s; margin: 44px 0;"></div>' % LINE)
    parts.append('  <div style="display: flex; flex-direction: column; gap: 22px;">')
    parts.append('\n'.join(spec(s) for s in specs))
    parts.append('  </div>')
    if disclosure:
        parts.append(
            '  <div style="display: flex; gap: 20px; align-items: flex-start; margin-top: 40px; '
            'border-left: 2px solid %s; padding-left: 26px;">\n'
            '    <div style="font-size: 30px; line-height: 1.4; color: %s;">%s</div>\n'
            '  </div>' % (RED, TEXT_3, disclosure)
        )
    parts.append('</div>')
    parts.append(
        '<div style="background: %s; border: 1px solid %s; border-radius: 14px; '
        'padding: 30px 34px; margin-bottom: 34px;">\n'
        '  <div style="font-size: 23px; font-weight: 600; letter-spacing: 0.16em; '
        'text-transform: uppercase; color: %s; margin-bottom: 10px;">Best for</div>\n'
        '  <div style="font-size: 34px; line-height: 1.35; color: %s;">%s</div>\n'
        '</div>' % (RAISED, LINE, TEXT_3, TEXT, best_for)
    )
    parts.append(footer())
    return SHELL.format(font=FONT, red_s=RED_S, body=frame('\n'.join(parts)))


# ---------------------------------------------------------------- slide 1

hook_body = '\n'.join([
    kicker(1),
    '<div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">',
    '  <div style="width: 96px; height: 6px; background: %s; margin-bottom: 56px;"></div>' % RED,
    '  <h1 style="margin: 0; font-size: 118px; font-weight: 700; letter-spacing: -0.045em; '
    'line-height: 0.98; color: %s; text-wrap: balance;">5 camera apps<br>worth the space<br>on a filmmaker&#39;s<br>iPhone</h1>' % TEXT,
    '  <p style="margin: 56px 0 0; font-size: 46px; line-height: 1.35; letter-spacing: -0.015em; '
    'color: %s; max-width: 820px; text-wrap: pretty;">One of them is not a filmmaking '
    'app at all. It is number&nbsp;2, and it might be the one that saves a shoot.</p>' % TEXT_2,
    '</div>',
    '<div style="display: flex; align-items: center; gap: 18px; margin-bottom: 40px;">',
    '  <span style="font-size: 30px; font-weight: 600; letter-spacing: 0.16em; '
    'text-transform: uppercase; color: %s;">Swipe</span>' % RED_S,
    '  <svg width="56" height="24" viewBox="0 0 56 24" fill="none" '
    'stroke="%s" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M2 12h50"></path><path d="M42 3l10 9-10 9"></path></svg>' % RED_S,
    '</div>',
    footer(),
])
slide1 = SHELL.format(font=FONT, red_s=RED_S, body=frame(hook_body))

# ---------------------------------------------------------------- slides 2-6

slide2 = app_slide(
    2, '01', 'Blackmagic<br>Camera',
    [('Manual everything', False)],
    'Pro capture, for nothing, from the people who make the cameras.',
    [
        'Manual ISO, shutter angle, white balance and focus, laid out like a real camera',
        'Apple&nbsp;Log and ProRes, with a LUT preview so Log is watchable on set',
        'Uploads straight to Blackmagic Cloud, so the edit starts before you are home',
    ],
    'Anyone who finishes in DaVinci Resolve.',
    stem='Blackmagic', initials='BM',
)

slide3 = app_slide(
    3, '02', 'Witness',
    [('iOS 17+', True)],
    'It uploads your footage while you are still rolling.',
    [
        'Every ~15 seconds goes to a cloud account <em style="font-style: normal; color: %s;">you own</em>, mid&#8209;record &#8212; Drive, Dropbox or your own server' % TEXT,
        'Films with the screen fully black &#8212; no preview, no glow, nothing to read over your shoulder',
        'Each piece is hashed and timestamped, so the footage holds up when it is challenged',
        'Pro adds 4K, Apple&nbsp;Log and ProRes&nbsp;422 &#8212; ProRes stays on the phone, too big to upload live',
    ],
    'Documentary, protest and field work &#8212; anywhere the phone might not make it back.',
    stem='Witness', initials='W',
    disclosure='Full disclosure: I built this one. The other four are not mine, and they are genuinely good.',
)

slide4 = app_slide(
    4, '03', 'Kino',
    [('From the Halide team', False)],
    'The one you will actually keep opening.',
    [
        'Instant Grade bakes a look into Log as you shoot &#8212; nothing lands flat and grey',
        'AutoMotion holds a cinematic 180&#176; shutter while the light moves',
        'One&#8209;hand controls that are not fighting you at minute forty',
    ],
    'Shooting fast, alone, with no colourist waiting.',
    stem='Kino', initials='K',
)

slide5 = app_slide(
    5, '04', 'Filmic Pro',
    [('Deepest toolbox', False)],
    'Still the most controls of anything on the App Store.',
    [
        'Scripted focus and exposure pulls, waveform, false colour, zebras',
        'LogV3 capture and manual control over every parameter you can name',
        'The lifetime licence became a subscription &#8212; check before you commit',
    ],
    'Controlled shoots where you want every dial.',
    stem='FilmicPro', initials='FP',
)

slide6 = app_slide(
    6, '05', 'Final Cut<br>Camera',
    [('From Apple', False)],
    'Turns the old iPhones in your drawer into a multicam rig.',
    [
        'Live Multicam runs up to four phones from one iPad, focus and exposure included',
        'Each phone still records locally at full quality &#8212; the link is only the monitor',
        'Apple&nbsp;Log in HEVC or ProRes on supported models',
    ],
    'Interviews and two&#8209; or three&#8209;camera setups on no budget.',
    stem='FinalCutCamera', initials='FC',
)

# ---------------------------------------------------------------- slide 7

def recap_row(rank, name, highlight=False):
    color = TEXT if not highlight else RED_S
    return (
        '  <div style="display: flex; align-items: baseline; gap: 28px; padding: 20px 0; '
        'border-bottom: 1px solid %s;">\n'
        '    <div style="font-size: 38px; font-weight: 700; letter-spacing: -0.02em; '
        'color: %s; width: 62px; flex: none;">%s</div>\n'
        '    <div style="font-size: 44px; font-weight: 600; letter-spacing: -0.02em; color: %s;">%s</div>\n'
        '  </div>' % (LINE, RED if highlight else GHOST, rank, color, name)
    )

outro_body = '\n'.join([
    kicker(7),
    '<div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">',
    '  <h2 style="margin: 0 0 44px; font-size: 92px; font-weight: 700; letter-spacing: -0.04em; '
    'line-height: 1.0; color: %s;">Save this before<br>your next shoot.</h2>' % TEXT,
    '  <div style="display: flex; flex-direction: column;">',
    recap_row('01', 'Blackmagic Camera'),
    recap_row('02', 'Witness', highlight=True),
    recap_row('03', 'Kino'),
    recap_row('04', 'Filmic Pro'),
    recap_row('05', 'Final Cut Camera'),
    '  </div>',
    '  <div style="display: flex; align-items: center; gap: 30px; margin-top: 58px;">',
    '    <img src="witness-icon.png" alt="" style="width: 128px; height: 128px; '
    'border-radius: 28px; display: block; flex: none;">',
    '    <div>',
    '      <div style="font-size: 44px; font-weight: 700; letter-spacing: -0.025em; color: %s;">'
    'Witness &#8212; on the App Store</div>' % TEXT,
    '      <div style="font-size: 32px; line-height: 1.4; color: %s; margin-top: 8px;">'
    'Chunked upload, hashing and timestamping, all in the app.</div>' % TEXT_3,
    '    </div>',
    '  </div>',
    '</div>',
    '<div style="background: %s; border: 1px solid %s; border-radius: 14px; '
    'padding: 30px 34px; margin-bottom: 34px;">' % (RAISED, LINE),
    '  <div style="font-size: 32px; line-height: 1.4; color: %s;">'
    'Which one is on your home screen?</div>' % TEXT,
    '</div>',
    footer(),
])
slide7 = SHELL.format(font=FONT, red_s=RED_S, body=frame(outro_body))

# ----------------------------------------------------------------- write

files = {
    'Main.dc.html': slide1,
    'Blackmagic.dc.html': slide2,
    'Witness.dc.html': slide3,
    'Kino.dc.html': slide4,
    'FilmicPro.dc.html': slide5,
    'FinalCutCamera.dc.html': slide6,
    'Outro.dc.html': slide7,
}
for name, src in files.items():
    with open(name, 'w', encoding='utf-8') as fh:
        fh.write(src)
    print('wrote', name, len(src), 'bytes')
