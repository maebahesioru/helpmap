"""Record the HelpMap demo — upload guide -> browse -> quick help -> Q&A.

Prereq: server on :7865, fresh state.
Produces: demo/video/*.webm + demo/marks.json
"""
import json
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).parent.parent / "demo"
OUT.mkdir(exist_ok=True)
VID = OUT / "video"
VID.mkdir(exist_ok=True)
APP = "http://127.0.0.1:7865"
marks: list[dict] = []
t0 = time.time()


def mark(name: str) -> None:
    marks.append({"name": name, "t": round(time.time() - t0, 2)})
    print(f"MARK {name} @ {marks[-1]['t']}s", flush=True)


def slow(page, ms=600):
    page.wait_for_timeout(ms)


with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    ctx = browser.new_context(
        viewport={"width": 1280, "height": 800},
        record_video_dir=str(VID),
        record_video_size={"width": 1280, "height": 800},
    )
    page = ctx.new_page()
    page.on("dialog", lambda d: d.accept())

    page.goto(APP, timeout=60000)
    slow(page, 3500)
    mark("start")

    # upload the guide
    page.set_input_files("#file", [str(OUT.parent / "data/sample_course/community_resources.md")])
    slow(page, 7000)
    mark("uploaded")

    # browse the guide
    page.click("nav button[data-t='timeline']")
    slow(page, 1500)
    page.click("#btnTimeline")
    slow(page, 8000)
    mark("browsed")
    page.evaluate("window.scrollTo(0, 400)")
    slow(page, 4000)
    page.evaluate("window.scrollTo(0, 900)")
    slow(page, 4000)

    # quick help: Food
    page.click("nav button[data-t='tutor']")
    slow(page, 1800)
    page.locator(".qh").first.click()
    slow(page, 26000)
    mark("food_answered")
    try:
        page.locator("#chat .cite a").first.click(timeout=5000)
        slow(page, 4000)
    except Exception:
        pass

    # a second quick help: Shelter
    try:
        page.locator(".qh").nth(2).click()
        slow(page, 24000)
        mark("shelter_answered")
    except Exception:
        pass

    # off-guide refusal
    page.fill("#q", "Can you give me a loan for rent?")
    slow(page, 1200)
    page.click("#btnAsk")
    slow(page, 18000)
    mark("refused")

    page.evaluate("window.scrollTo(0, 0)")
    slow(page, 3500)
    mark("end")

    video = page.video
    ctx.close()
    path = video.path()
    print("VIDEO:", path)
    (OUT / "marks.json").write_text(json.dumps(marks, indent=1))
    print("marks saved")
