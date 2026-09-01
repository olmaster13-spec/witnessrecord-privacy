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

TOTAL = 11

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
        '  <div style="font-size: 25px; font-weight: 600; letter-spacing: 0.18em; '
        'text-transform: uppercase; color: %s;">Why I built Witness</div>\n'
        '  <div style="font-size: 25px; font-weight: 600; letter-spacing: 0.18em; color: %s;">'
        '<span style="color: %s;">%02d</span>&#8202;/&#8202;%d</div>\n'
        '</div>\n'
        '<div style="height: 1px; background: %s; margin: 28px 0 0;"></div>'
        % (c, c, TEXT, n, TOTAL, 'rgba(255,255,255,0.22)' if over_photo else LINE)
    )


def footer():
    return (
        '<div style="height: 1px; background: %s; margin: 0 0 26px;"></div>\n'
        '<div style="display: flex; align-items: center; gap: 14px;">\n'
        '  <img src="witness-mark.png" alt="" style="width: 40px; height: 40px; display: block;">\n'
        '  <span style="font-size: 26px; font-weight: 600; color: %s;">witnessrecord.app</span>\n'
        '</div>' % (LINE, TEXT_3)
    )


def frame(inner, pad="88px 80px"):
    return ('<div style="width: 1080px; height: 1920px; background: %s; color: %s; '
            'padding: %s; display: flex; flex-direction: column; box-sizing: border-box; '
            'overflow: hidden;">\n%s\n</div>' % (BG, TEXT, pad, inner))


def scene_label(text):
    return ('  <div style="font-size: 25px; font-weight: 600; letter-spacing: 0.18em; '
            'text-transform: uppercase; color: %s; margin-bottom: 26px;">%s</div>' % (RED_S, text))


# --------------------------------------------------------------- slide kinds

def type_slide(n, headline, body, label=None, headline_size=82, accent=None):
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
    parts.append('  <p style="margin: 44px 0 0; font-size: 42px; line-height: 1.4; letter-spacing: -0.012em; '
                 'color: %s; max-width: 880px; text-wrap: pretty;">%s</p>' % (TEXT_2, body))
    parts.append('</div>')
    parts.append(footer())
    return SHELL.format(font=FONT, red_s=RED_S, body=frame('\n'.join(parts)))


def photo_slide(n, photo, label, headline, body, credit=None):
    """A photo bleeds off the top edge and dissolves into the page, so the text
    below sits on flat black rather than fighting the image for contrast."""
    inner = (
        '<div style="position: absolute; inset: 0 0 auto 0; height: 1120px;">\n'
        '  <img src="%s" alt="" style="width: 1080px; height: 1120px; object-fit: cover; display: block;">\n'
        '  <div style="position: absolute; inset: 0; background: linear-gradient(180deg, '
        'rgba(8,8,10,0.78) 0%%, rgba(8,8,10,0.18) 26%%, rgba(8,8,10,0.20) 46%%, '
        'rgba(8,8,10,0.88) 82%%, %s 100%%);"></div>\n'
        '</div>\n' % (photo, BG)
    )
    content = [kicker(n, over_photo=True),
               '<div style="flex: 1;"></div>',
               '<div style="padding-bottom: 56px;">']
    content.append(scene_label(label))
    content.append('  <h2 style="margin: 0; font-size: 72px; font-weight: 700; letter-spacing: -0.038em; '
                   'line-height: 1.06; color: %s; text-wrap: pretty;">%s</h2>' % (TEXT, headline))
    content.append('  <p style="margin: 36px 0 0; font-size: 38px; line-height: 1.4; letter-spacing: -0.012em; '
                   'color: %s; max-width: 880px; text-wrap: pretty;">%s</p>' % (TEXT_2, body))
    if credit:
        content.append('  <div style="margin-top: 30px; font-size: 22px; color: #6a6a74;">%s</div>' % credit)
    content.append('</div>')
    content.append(footer())

    body_html = (
        '<div style="position: relative; width: 1080px; height: 1920px; background: %s; '
        'color: %s; box-sizing: border-box; overflow: hidden;">\n%s'
        '  <div style="position: relative; height: 100%%; padding: 88px 80px; display: flex; '
        'flex-direction: column; box-sizing: border-box;">\n%s\n  </div>\n</div>'
        % (BG, TEXT, inner, '\n'.join(content))
    )
    return SHELL.format(font=FONT, red_s=RED_S, body=body_html)


def stars(n=5):
    star = ('<svg width="30" height="30" viewBox="0 0 24 24" fill="%s" style="display:block;">'
            '<path d="M12 2.6l2.9 5.9 6.5.95-4.7 4.6 1.1 6.45L12 17.45 6.2 20.5l1.1-6.45L2.6 9.45l6.5-.95z"/>'
            '</svg>' % TEXT_3)
    return ('<div style="display: flex; gap: 4px; align-items: center;">%s</div>' % (star * n))


def app_card():
    """The App Store listing, rebuilt in the brand's own vocabulary: sharp type
    at 1080px instead of an upscaled screenshot, and it matches the carousel."""
    return (
        '  <div style="border: 1px solid %s; background: %s; border-radius: 26px; '
        'padding: 34px 36px; display: flex; align-items: center; gap: 30px;">\n'
        '    <img src="witness-icon.png" alt="" style="width: 132px; height: 132px; '
        'border-radius: 30px; display: block; flex: none;">\n'
        '    <div style="flex: 1; min-width: 0;">\n'
        '      <div style="font-size: 40px; font-weight: 700; letter-spacing: -0.025em; '
        'color: %s; line-height: 1.15;">Witness: Record Beyond Reach</div>\n'
        '      <div style="font-size: 31px; color: %s; margin-top: 8px;">Evidence That Survives</div>\n'
        '      <div style="display: flex; align-items: center; gap: 14px; margin-top: 16px;">\n'
        '        %s\n'
        '        <span style="font-size: 26px; color: %s;">3</span>\n'
        '        <span style="font-size: 26px; color: %s;">&#183;</span>\n'
        '        <span style="font-size: 26px; color: %s;">Photo &amp; Video</span>\n'
        '      </div>\n'
        '    </div>\n'
        '    <div style="border: 1px solid %s; border-radius: 999px; padding: 14px 38px; '
        'font-size: 30px; font-weight: 700; color: %s; flex: none;">Get</div>\n'
        '  </div>' % (LINE_S, SURFACE, TEXT, TEXT_3, stars(), TEXT_3, TEXT_3, TEXT_3, LINE_S, TEXT)
    )


# -------------------------------------------------------------- the eleven

slides = {}

# 1 — hook, with the listing as a credential rather than a pitch
s1 = [kicker(1),
      '<div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">',
      '  <div style="width: 96px; height: 6px; background: %s; margin-bottom: 52px;"></div>' % RED,
      '  <h1 style="margin: 0; font-size: 112px; font-weight: 700; letter-spacing: -0.045em; '
      'line-height: 0.99; color: %s; text-wrap: balance;">The first move<br>is always<br>the same.<br>'
      '<span style="color: %s;">Take the phone.</span></h1>' % (TEXT, RED_S),
      '  <p style="margin: 48px 0 0; font-size: 42px; line-height: 1.38; color: %s; '
      'max-width: 820px;">Three places with nothing else in common.</p>' % TEXT_2,
      '  <div style="margin-top: 64px;">',
      app_card(),
      '  </div>',
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

slides['WhyThePhone.dc.html'] = type_slide(
    2, 'They go for the phone because filming works.',
    'A recording is the one thing that survives someone else&#8217;s version of events. '
    'Which is exactly why it is not allowed to survive.', accent=True)

slides['Minneapolis.dc.html'] = photo_slide(
    3, 'photo-minneapolis.jpg', 'Minneapolis, 2020',
    'The police statement said &#8220;medical incident during police interaction.&#8221;',
    'A 17-year-old&#8217;s phone said otherwise. The only reason anyone knows is that '
    'the phone made it home.')

slides['Ice.dc.html'] = photo_slide(
    4, 'photo-ice.jpg', 'An unmarked van',
    'When the agents are masked, your video is the only record that exists.',
    'No badge number to write down. No name. Just whatever your phone caught before '
    'someone told you to stop.')

slides['WestBank.dc.html'] = photo_slide(
    5, 'photo-westbank.jpg', 'The occupied West Bank',
    'Cameras get confiscated and broken more often than the footage gets seen.',
    'The settlements are illegal under international law &#8212; the ICJ said so again in 2024. '
    'The people documenting what that looks like keep losing the file.')

slides['Turn.dc.html'] = type_slide(
    6, 'Every one of those recordings existed.<br>Most never made it out.',
    'The footage lives on the one object the other side can take. That is not a filming '
    'problem. It is a storage problem.', headline_size=76, accent=True)

slides['Idea.dc.html'] = type_slide(
    7, 'So I built it backwards.',
    'Not record, then upload. Upload <em style="font-style: normal; color: %s;">while</em> '
    'recording &#8212; roughly 15 seconds at a time, to a cloud account you own, while the '
    'camera is still rolling.' % TEXT, headline_size=96, label='The idea')

slides['Proof.dc.html'] = type_slide(
    8, 'Surviving is not enough.<br>It gets called fake.',
    'Every piece is fingerprinted with SHA-256, and each session is timestamped by an '
    'independent authority. A lawyer, a newsroom or a court can verify it with standard '
    'tools &#8212; without the app, and without me.', headline_size=76)

slides['Means.dc.html'] = type_slide(
    9, 'Take the phone.<br>The footage already left.',
    'Smash it &#8212; already left. It records with the screen fully black, and stopping takes '
    'a triple-tap and a hold, so it does not stop by accident.', headline_size=80)

slides['NoServer.dc.html'] = type_slide(
    10, 'I cannot hold your footage. That is the point.',
    'No server of mine sits in the middle. It goes from your phone to your cloud and nowhere '
    'else. I cannot read it, hand it over, or lose it.', headline_size=76)

# 11 — the ask
s11 = [kicker(11),
       '<div style="flex: 1; display: flex; flex-direction: column; justify-content: center;">',
       scene_label('Before you need it'),
       '  <h2 style="margin: 0; font-size: 88px; font-weight: 700; letter-spacing: -0.042em; '
       'line-height: 1.03; color: %s; text-wrap: pretty;">You cannot download this '
       'while it is happening.</h2>' % TEXT,
       '  <p style="margin: 44px 0 0; font-size: 42px; line-height: 1.4; color: %s; '
       'max-width: 880px;">Two minutes, today: install it, link the cloud account you already '
       'have, put it on your Action Button. Then forget about it.</p>' % TEXT_2,
       '  <div style="margin-top: 62px;">',
       app_card(),
       '  </div>',
       '</div>',
       footer()]
slides['Cta.dc.html'] = SHELL.format(font=FONT, red_s=RED_S, body=frame('\n'.join(s11)))

for name, src in slides.items():
    open(name, 'w', encoding='utf-8').write(src)
    print('wrote', name, len(src), 'bytes')
