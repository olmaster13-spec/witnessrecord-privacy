# -*- coding: utf-8 -*-
"""Generates the eleven .dc.html artboards for the "why Witness exists" carousel.

Same palette and type as the camera-apps carousel, plus two slide kinds it did
not need: photo slides, where a monochrome press photo bleeds off the top edge
and dissolves into the page, and the opening card, which rebuilds the App Store
listing in the brand's own vocabulary rather than pasting a screenshot."""

BG      = "#08080a"
RAISED  = "#101013"
SURFACE = "#16161a"
LINE    = "#26262c"
LINE_S  = "#34343c"
TEXT    = "#f2f2f3"
TEXT_2  = "#b9b9c0"
TEXT_3  = "#85858f"
RED     = "#e82e3b"
RED_S   = "#ff6b5e"
AMBER   = "#f0b429"

FONT = ("-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text', "
        "'Segoe UI', Roboto, Helvetica, Arial, sans-serif")

TOTAL = 10
BR = chr(10)

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


def kicker(n, over_photo=False):
    """Top rail. Over a photo it needs no scrim of its own — the photo's own
    gradient already darkens the top band."""
    c = TEXT_2 if over_photo else TEXT_3
    return (
        '<div style="display: flex; justify-content: space-between; align-items: baseline; gap: 24px;">\n'
        '  <div style="font-size: 23px; font-weight: 600; letter-spacing: 0.18em; '
        'text-transform: uppercase; color: %s;">Why I built Witness</div>\n'
        '  <div style="font-size: 23px; font-weight: 600; letter-spacing: 0.18em; color: %s;">'
        '<span style="color: %s;">%02d</span>&#8202;/&#8202;%d</div>\n'
        '</div>\n'
        '<div style="height: 1px; background: %s; margin: 28px 0 0;"></div>'
        % (c, c, TEXT, n, TOTAL, 'rgba(255,255,255,0.22)' if over_photo else LINE)
    )


def footer():
    return (
        '<div style="height: 1px; background: %s; margin: 0 0 22px;"></div>\n'
        '<div style="display: flex; align-items: center; gap: 14px;">\n'
        '  <img src="witness-mark.png" alt="" style="width: 34px; height: 34px; display: block;">\n'
        '  <span style="font-size: 23px; font-weight: 600; color: %s;">witnessrecord.app</span>\n'
        '</div>' % (LINE, TEXT_3)
    )


def frame(inner, pad="192px 196px 384px 128px"):
    return ('<div style="width: 1080px; height: 1920px; background: %s; color: %s; '
            'padding: %s; display: flex; flex-direction: column; box-sizing: border-box; '
            'overflow: hidden;">\n%s\n</div>' % (BG, TEXT, pad, inner))


def scene_label(text):
    return ('  <div style="font-size: 23px; font-weight: 600; letter-spacing: 0.18em; '
            'text-transform: uppercase; color: %s; margin-bottom: 22px;">%s</div>' % (RED_S, text))


# --------------------------------------------------------------- slide kinds

def providers():
    """Where the footage actually goes. Only the two logos the repo already
    ships are drawn; Nextcloud has no mark here and WebDAV is a protocol, not a
    brand, so both are named in text rather than approximated."""
    chip = ('    <div style="display: flex; align-items: center; gap: 14px; border: 1px solid %s; '
            'background: %s; border-radius: 999px; padding: 10px 26px 10px 14px;">\n'
            '      <img src="%s" alt="" style="height: 46px; width: auto; display: block;">\n'
            '      <span style="font-size: 28px; font-weight: 600; color: %s;">%s</span>\n'
            '    </div>')
    return (
        '  <div style="display: flex; flex-wrap: wrap; gap: 16px; margin-top: 44px;">\n'
        + chip % (LINE_S, SURFACE, 'logo-google-drive.png', TEXT, 'Google Drive') + '\n'
        + chip % (LINE_S, SURFACE, 'logo-dropbox.png', TEXT, 'Dropbox') + '\n'
        '  </div>\n'
        '  <div style="margin-top: 20px; font-size: 28px; line-height: 1.4; color: %s;">'
        'or any Nextcloud or WebDAV server, including one you host yourself.</div>' % TEXT_3
    )


def type_slide(n, headline, body, label=None, headline_size=64, accent=None, extra=None):
    """A slide carried entirely by its words."""
    parts = [kicker(n),
             '<div style="flex: 1; display: flex; flex-direction: column; '
             'justify-content: center; padding-bottom: 60px;">']
    if label:
        parts.append(scene_label(label))
    if accent:
        parts.append('  <div style="width: 96px; height: 6px; background: %s; margin-bottom: 48px;"></div>' % RED)
    parts.append('  <h2 style="margin: 0; font-size: %dpx; font-weight: 700; letter-spacing: -0.04em; '
                 'line-height: 1.04; color: %s; text-wrap: pretty;">%s</h2>' % (headline_size, TEXT, headline))
    parts.append('  <p style="margin: 38px 0 0; font-size: 37px; line-height: 1.4; letter-spacing: -0.012em; '
                 'color: %s; max-width: 756px; text-wrap: pretty;">%s</p>' % (TEXT_2, body))
    if extra:
        parts.append(extra)
    parts.append('</div>')
    parts.append(footer())
    return SHELL.format(font=FONT, red_s=RED_S, body=frame('\n'.join(parts)))


def photo_slide(n, photo, label, headline, body, credit=None, band=940, cases=None, headline_size=58):
    """A photo bleeds off the top edge and dissolves into the page, so the text
    below sits on flat black rather than fighting the image for contrast."""
    inner = (
        '<div style="position: absolute; inset: 0 0 auto 0; height: %dpx;">\n'
        '  <img src="%s" alt="" style="width: 1080px; height: %dpx; object-fit: cover; display: block;">\n'
        '  <div style="position: absolute; inset: 0; background: linear-gradient(180deg, '
        'rgba(8,8,10,0.78) 0%%, rgba(8,8,10,0.18) 26%%, rgba(8,8,10,0.20) 46%%, '
        'rgba(8,8,10,0.88) 82%%, %s 100%%);"></div>\n'
        '</div>\n' % (band, photo, band, BG)
    )
    content = [kicker(n, over_photo=True),
               '<div style="flex: 1;"></div>',
               '<div style="padding-bottom: 56px;">']
    content.append(scene_label(label))
    content.append('  <h2 style="margin: 0; font-size: %dpx; font-weight: 700; letter-spacing: -0.038em; '
                   'line-height: 1.06; color: %s; text-wrap: pretty;">%s</h2>' % (headline_size, TEXT, headline))
    if body:
        content.append('  <p style="margin: 32px 0 0; font-size: 34px; line-height: 1.4; '
                       'letter-spacing: -0.012em; color: %s; max-width: 756px; '
                       'text-wrap: pretty;">%s</p>' % (TEXT_2, body))
    if cases:
        content.append('  <div style="display: flex; flex-direction: column; gap: 22px; margin-top: 40px;">')
        for place, line in cases:
            content.append(
                '    <div style="border-left: 2px solid %s; padding-left: 24px;">\n'
                '      <div style="font-size: 23px; font-weight: 600; letter-spacing: 0.16em; '
                'text-transform: uppercase; color: %s; margin-bottom: 6px;">%s</div>\n'
                '      <div style="font-size: 28px; line-height: 1.38; color: %s;">%s</div>\n'
                '    </div>' % (RED, TEXT_3, place, TEXT_2, line))
        content.append('  </div>')
    if credit:
        content.append('  <div style="margin-top: 30px; font-size: 22px; color: #6a6a74;">%s</div>' % credit)
    content.append('</div>')
    content.append(footer())

    body_html = (
        '<div style="position: relative; width: 1080px; height: 1920px; background: %s; '
        'color: %s; box-sizing: border-box; overflow: hidden;">\n%s'
        '  <div style="position: relative; height: 100%%; padding: 192px 196px 384px 128px; display: flex; '
        'flex-direction: column; box-sizing: border-box;">\n%s\n  </div>\n</div>'
        % (BG, TEXT, inner, '\n'.join(content))
    )
    return SHELL.format(font=FONT, red_s=RED_S, body=body_html)


def device(src, width=430, annotate=None):
    """Bezel drawn in CSS, matching .device in the site's style.css, so the
    capture inside stays an unmodified screenshot. `annotate` rings the camera
    indicator and labels it: at feed size a single green pixel on black is
    invisible, and the ring is plainly an overlay rather than a retouch. The
    fractions are measured off the capture, not guessed."""
    DOT_X, DOT_Y = 0.5523, 0.0367
    ring = ''
    if annotate:
        # 11px padding inside the bezel, so the screen starts 11px in.
        sw = width - 22
        cx, cy = 11 + sw * DOT_X, 11 + (sw / 0.4601) * DOT_Y
        ring = (
            '    <div style="position: absolute; left: %.1fpx; top: %.1fpx; width: 54px; height: 54px; '
            'margin: -27px 0 0 -27px; border: 2px solid %s; border-radius: 999px;"></div>\n'
            '    <div style="position: absolute; left: %.1fpx; top: %.1fpx; width: 92px; height: 2px; '
            'background: %s;"></div>\n'
            '    <div style="position: absolute; left: %.1fpx; top: %.1fpx; font-size: 25px; '
            'font-weight: 600; color: %s; white-space: nowrap; transform: translateY(-50%%);">%s</div>\n'
            % (cx, cy, RED, cx + 29, cy - 1, RED, cx + 133, cy, RED_S, annotate)
        )
    return (
        '  <div style="position: relative; width: %dpx; border: 1px solid %s; border-radius: 52px; '
        'padding: 11px; background: linear-gradient(160deg, #202027, #0e0e11); '
        'box-shadow: 0 34px 80px -22px rgba(0,0,0,0.95), inset 0 1px 0 rgba(255,255,255,0.07);">\n'
        '    <img src="%s" alt="" style="width: 100%%; display: block; border-radius: 42px;">\n'
        '%s'
        '  </div>' % (width, LINE_S, src, ring)
    )


def stars(n=5):
    star = ('<svg width="30" height="30" viewBox="0 0 24 24" fill="%s" style="display:block;">'
            '<path d="M12 2.6l2.9 5.9 6.5.95-4.7 4.6 1.1 6.45L12 17.45 6.2 20.5l1.1-6.45L2.6 9.45l6.5-.95z"/>'
            '</svg>' % TEXT_3)
    return ('<div style="display: flex; gap: 4px; align-items: center;">%s</div>' % (star * n))


def app_card():
    """The App Store listing, rebuilt in the brand's own vocabulary: sharp type
    at 1080px instead of an upscaled screenshot, and it matches the carousel."""
    return (
        '  <div style="border: 1px solid %s; background: %s; border-radius: 24px; '
        'padding: 28px 30px; display: flex; align-items: center; gap: 30px;">\n'
        '    <img src="witness-icon.png" alt="" style="width: 112px; height: 112px; '
        'border-radius: 26px; display: block; flex: none;">\n'
        '    <div style="flex: 1; min-width: 0;">\n'
        '      <div style="font-size: 40px; font-weight: 700; letter-spacing: -0.025em; '
        'color: %s; line-height: 1.15;">Witness: Record Beyond Reach</div>\n'
        '      <div style="font-size: 28px; color: %s; margin-top: 7px;">Evidence That Survives</div>\n'
        '      <div style="display: flex; align-items: center; gap: 14px; margin-top: 16px;">\n'
        '        %s\n'
        '        <span style="font-size: 26px; color: %s;">3</span>\n'
        '        <span style="font-size: 26px; color: %s;">&#183;</span>\n'
        '        <span style="font-size: 26px; color: %s;">Photo &amp; Video</span>\n'
        '      </div>\n'
        '    </div>\n'
        '    <div style="border: 1px solid %s; border-radius: 999px; padding: 14px 38px; '
        'font-size: 27px; font-weight: 700; color: %s; flex: none;">Get</div>\n'
        '  </div>' % (LINE_S, SURFACE, TEXT, TEXT_3, stars(), TEXT_3, TEXT_3, TEXT_3, LINE_S, TEXT)
    )


# -------------------------------------------------------------- the eleven

slides = {}

# 1 — hook, illustrated with what recording actually looks like
s1 = [kicker(1),
      '<div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">',
      '  <div style="width: 96px; height: 6px; background: %s; margin-bottom: 44px;"></div>' % RED,
      '  <h1 style="margin: 0; font-size: 53px; font-weight: 700; letter-spacing: -0.035em; '
      'line-height: 1.1; color: %s; text-wrap: pretty;">Why I built an app that lets you '
      'record with your <span style="color: %s;">screen off</span> and backs up the footage '
      '<span style="color: %s;">every 15 seconds</span>.</h1>' % (TEXT, RED_S, RED_S),
      '  <div style="display: flex; justify-content: center; margin-top: 60px; '
      'padding-left: 0;">',
      device('phone-screen.png', 268, annotate='camera indicator'),
      '  </div>',
      '  <div style="margin-top: 26px; text-align: center; font-size: 27px; color: %s;">'
      'This is the app recording. Screen black, nothing to read over your shoulder.</div>' % TEXT_3,
      '</div>',
      '<div style="display: flex; align-items: center; gap: 18px; margin-bottom: 40px;">',
      '  <span style="font-size: 30px; font-weight: 600; letter-spacing: 0.16em; '
      'text-transform: uppercase; color: %s;">Swipe</span>' % RED_S,
      '  <svg width="56" height="24" viewBox="0 0 56 24" fill="none" stroke="%s" stroke-width="2.5" '
      'stroke-linecap="round" stroke-linejoin="round"><path d="M2 12h50"></path>'
      '<path d="M42 3l10 9-10 9"></path></svg>' % RED_S,
      '</div>',
      footer()]
slides['Main.dc.html'] = SHELL.format(font=FONT, red_s=RED_S, body=frame('\n'.join(s1)))

slides['Minneapolis.dc.html'] = photo_slide(
    2, 'photo-minneapolis.jpg', 'Minneapolis, 2020',
    'The police statement said &#8220;medical incident during police interaction.&#8221;',
    'A 17-year-old&#8217;s phone said otherwise. The only reason anyone knows is that '
    'the phone made it home.')

slides['Ice.dc.html'] = photo_slide(
    3, 'photo-ice.jpg', 'An unmarked van',
    'When the agents are masked, your video is the only record that exists.',
    'No badge number to write down. No name. Just whatever your phone caught before '
    'someone told you to stop.')

slides['WestBank.dc.html'] = photo_slide(
    4, 'photo-westbank.jpg', 'The occupied West Bank',
    'Cameras get confiscated and broken more often than the footage gets seen.',
    'The settlements are illegal under international law &#8212; the ICJ said so again in 2024. '
    'The people documenting what that looks like keep losing the file.')

slides['Turn.dc.html'] = photo_slide(
    5, 'photo-officer.jpg', 'What happens to the rest',
    'For every recording that makes it out, there is another one that gets '
    'illegally deleted.',
    None, band=640, headline_size=52, cases=[
        ('Baltimore, 2010', 'Officers deleted every video on a man&#8217;s phone after he filmed '
         'an arrest. The city paid $250,000.'),
        ('Des Moines, 2018', 'Police seized a man&#8217;s phone and camera without a warrant and '
         'kept them twelve days. $125,000.'),
        ('Philadelphia, 2021', 'An officer is accused in a lawsuit of deleting a man&#8217;s '
         'recording of his own arrest.'),
    ])

slides['Idea.dc.html'] = type_slide(
    6, 'So I built it backwards.',
    'Not record, then upload. Upload <em style="font-style: normal; color: %s;">while</em> '
    'recording &#8212; roughly 15 seconds at a time, while the camera is still rolling, to a '
    'cloud account <em style="font-style: normal; color: %s;">you</em> own.' % (TEXT, TEXT),
    headline_size=76, label='The idea', extra=providers())

slides['Proof.dc.html'] = type_slide(
    7, 'Surviving is not enough.<br>It gets called fake.',
    'Every piece is fingerprinted with SHA-256, and each session is timestamped by an '
    'independent authority. A lawyer, a newsroom or a court can verify it with standard '
    'tools &#8212; without the app, and without me.', headline_size=60)

slides['Means.dc.html'] = type_slide(
    8, 'Take the phone.<br>The footage already left.',
    'Smash it &#8212; already left. It records with the screen fully black, and stopping takes '
    'a triple-tap and a hold, so it does not stop by accident.', headline_size=62)

slides['NoServer.dc.html'] = type_slide(
    9, 'I cannot hold your footage. That is the point.',
    'No server of mine sits in the middle. It goes from your phone to your cloud and nowhere '
    'else. I cannot read it, hand it over, or lose it.', headline_size=60)

# 10 — the ask
s10 = [kicker(10),
       '<div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">',
       '  <div style="width: 96px; height: 6px; background: %s; margin-bottom: 44px;"></div>' % RED,
       '  <h2 style="margin: 0; font-size: 64px; font-weight: 700; letter-spacing: -0.04em; '
       'line-height: 1.06; color: %s; text-wrap: pretty;">So I built '
       '<span style="color: %s;">Witness: Record Beyond Reach</span>.</h2>' % (TEXT, RED_S),
       '  <p style="margin: 38px 0 0; font-size: 39px; line-height: 1.36; color: %s; '
       'max-width: 756px; text-wrap: pretty;">So that next time you are in trouble, you can '
       'document safely, for free.</p>' % TEXT_2,
       '  <div style="margin-top: 62px;">',
       app_card(),
       '  </div>',
       '</div>',
       footer()]
slides['Cta.dc.html'] = SHELL.format(font=FONT, red_s=RED_S, body=frame(BR.join(s10)))

for name, src in slides.items():
    open(name, 'w', encoding='utf-8').write(src)
    print('wrote', name, len(src), 'bytes')
