"""YouTube draft -> unlisted publish — ONE-SHOT script (no reconnects).

Opens the first draft in Studio, answers the wizard via JS clicks, sets
visibility to unlisted and saves — all inside a single CDP session.
"""
from playwright.sync_api import sync_playwright


def log(*a):
    print(*a, flush=True)


def js(pg, code, arg=None):
    return pg.evaluate(code, arg)


with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    ctx = browser.contexts[0]
    pg = ctx.new_page()
    pg.on('dialog', lambda d: d.accept())
    pg.bring_to_front()

    pg.goto('https://studio.youtube.com/channel/UCIBl4qUGee47H4wx96rswNw/videos/upload', timeout=90000)
    pg.wait_for_timeout(12000)
    log('list loaded')

    # open R0 draft editor
    pg.mouse.move(1540, 319)
    pg.wait_for_timeout(700)
    pg.mouse.click(1540, 319)
    log('draft clicked')
    pg.wait_for_timeout(14000)

    def dialog_state():
        return js(pg, """() => {
            const dlg = document.querySelector('ytcp-uploads-dialog');
            if (!dlg) return 'no-dialog';
            const radios = [...dlg.querySelectorAll('tp-yt-paper-radio-button, ytcp-radio-button')]
                .map(e => (e.innerText || '').trim().split('\\n')[0].slice(0, 30) + '=' + (e.getAttribute('aria-checked') || '?'));
            const steps = [...dlg.querySelectorAll('.step-title, [class*="step"]')].map(e => (e.innerText || '').trim().slice(0, 20)).slice(0, 5);
            return 'radios=[' + radios.join(' | ') + '] steps=[' + steps.join(',') + ']';
        }""")

    log('state1:', dialog_state()[:400])

    # answer kids radio if needed
    r = js(pg, """() => {
        const dlg = document.querySelector('ytcp-uploads-dialog');
        if (!dlg) return 'no-dialog';
        for (const rd of dlg.querySelectorAll('tp-yt-paper-radio-button, ytcp-radio-button')) {
            if (/いいえ、子ども向けではありません/.test(rd.innerText || '')) {
                if (rd.getAttribute('aria-checked') === 'true') return 'already';
                rd.click();
                return 'clicked-kids-no';
            }
        }
        return 'radio-nf';
    }""")
    log('kids:', r)
    pg.wait_for_timeout(2500)

    # next x3 with state logging
    for i in range(4):
        st = js(pg, """() => {
            const dlg = document.querySelector('ytcp-uploads-dialog');
            if (!dlg) return 'no-dialog';
            const radios = [...dlg.querySelectorAll('tp-yt-paper-radio-button, ytcp-radio-button')]
                .map(e => (e.innerText || '').trim().split('\\n')[0].slice(0, 26) + '=' + (e.getAttribute('aria-checked') || '?'));
            return 'radios=[' + radios.join(' | ') + ']';
        }""")
        log(f'before next{i+1}:', st[:350])
        r = js(pg, """() => {
            const b = document.querySelector('ytcp-uploads-dialog #next-button');
            if (!b) return 'next-nf';
            b.click();
            return 'next-clicked';
        }""")
        log(f'next{i+1}:', r)
        pg.wait_for_timeout(7000)

    # visibility step: unlisted
    st = js(pg, """() => {
        const dlg = document.querySelector('ytcp-uploads-dialog');
        if (!dlg) return 'no-dialog';
        const radios = [...dlg.querySelectorAll('tp-yt-paper-radio-button, ytcp-radio-button')]
            .map(e => (e.innerText || '').trim().split('\\n')[0].slice(0, 30) + '=' + (e.getAttribute('aria-checked') || '?'));
        return 'final radios=[' + radios.join(' | ') + ']';
    }""")
    log('visibility state:', st[:400])

    r = js(pg, """() => {
        const dlg = document.querySelector('ytcp-uploads-dialog');
        if (!dlg) return 'no-dialog';
        for (const rd of dlg.querySelectorAll('tp-yt-paper-radio-button, ytcp-radio-button')) {
            if (/限定公開/.test(rd.innerText || '')) {
                if (rd.getAttribute('aria-checked') === 'true') return 'already-unlisted';
                rd.click();
                return 'clicked-unlisted';
            }
        }
        return 'unlisted-nf';
    }""")
    log('unlisted:', r)
    pg.wait_for_timeout(2500)

    # final save
    r = js(pg, """() => {
        const dlg = document.querySelector('ytcp-uploads-dialog');
        if (!dlg) return 'no-dialog';
        for (const label of ['保存', '公開']) {
            for (const b of dlg.querySelectorAll('ytcp-button, button')) {
                if ((b.innerText || '').trim() === label) {
                    b.click();
                    return 'clicked-' + label;
                }
            }
        }
        return 'save-nf';
    }""")
    log('save:', r)
    pg.wait_for_timeout(15000)

    # verify
    pg.goto('https://studio.youtube.com/channel/UCIBl4qUGee47H4wx96rswNw/videos/upload', timeout=90000)
    pg.wait_for_timeout(12000)
    rows = js(pg, """() => {
        const out = [];
        document.querySelectorAll('ytcp-video-row').forEach((r, i) => {
            if (i > 1) return;
            const t = (r.innerText || '').replace(/\\n/g, '§');
            out.push('R' + i + ' [' + t.length + ']: ' + t.slice(0, 200));
        });
        return out.join('\\n');
    }""")
    log('ROWS:')
    log(rows)
