"""
Browser-based UI tests using pytest-playwright.

Run with: uv run pytest test_browser.py
Requires: uv sync --group browser-test && uv run playwright install chromium
"""

import pytest
import threading
import uvicorn
from main import app


@pytest.fixture(scope="session")
def live_server():
    """Start the Air app on a background thread for browser tests."""
    config = uvicorn.Config(app, host="127.0.0.1", port=8765, log_level="warning")
    server = uvicorn.Server(config)
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    # Wait for the server to be ready
    import httpx
    for _ in range(50):
        try:
            httpx.get("http://127.0.0.1:8765/", timeout=0.5)
            break
        except httpx.ConnectError:
            import time
            time.sleep(0.1)
    yield "http://127.0.0.1:8765"
    server.should_exit = True


class TestMobileLayout:
    """PR test plan: Check homepage on mobile (375px), verify layout stacks
    correctly and no horizontal overflow."""

    def test_no_horizontal_overflow_at_375px(self, live_server, page):
        page.set_viewport_size({"width": 375, "height": 812})
        page.goto(f"{live_server}/")
        scroll_width = page.evaluate("document.documentElement.scrollWidth")
        assert scroll_width <= 375, (
            f"Horizontal overflow detected: scrollWidth={scroll_width} > viewport=375"
        )

    def test_feed_is_visible(self, live_server, page):
        page.set_viewport_size({"width": 375, "height": 812})
        page.goto(f"{live_server}/")
        feed = page.locator("main.feed")
        assert feed.is_visible()

    def test_sidebar_does_not_sit_beside_feed(self, live_server, page):
        """On mobile the sidebar should stack below the feed, not beside it."""
        page.set_viewport_size({"width": 375, "height": 812})
        page.goto(f"{live_server}/")
        feed_box = page.locator("main.feed").bounding_box()
        sidebar_box = page.locator("aside.sidebar").bounding_box()
        assert sidebar_box["y"] >= feed_box["y"] + feed_box["height"] - 1, (
            "Sidebar should be below the feed on mobile, not beside it"
        )

    def test_post_images_fit_within_viewport(self, live_server, page):
        page.set_viewport_size({"width": 375, "height": 812})
        page.goto(f"{live_server}/")
        images = page.locator(".post-image img")
        count = images.count()
        for i in range(count):
            box = images.nth(i).bounding_box()
            if box:
                assert box["width"] <= 375, (
                    f"Image {i} overflows viewport: width={box['width']}"
                )
