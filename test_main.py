import pytest
import re
from main import (
    get_notebook_cells,
    get_date_from_filename,
    strip_markdown,
    extract_first_image,
    get_post_dict,
    app,
)
from pathlib import Path
import tempfile
import json
from datetime import datetime

from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def client():
    """A TestClient wired to the Air app, shared across all tests in the module."""
    return TestClient(app)


@pytest.fixture(scope="module")
def homepage_html(client):
    """Fetch the homepage once and share the HTML across tests that inspect it."""
    response = client.get("/")
    assert response.status_code == 200
    return response.text


# ---------------------------------------------------------------------------
# Existing tests (get_notebook_cells, get_date_from_filename)
# ---------------------------------------------------------------------------

def test_get_notebook_cells_reads_cells():
    # Create a minimal notebook file
    nb = {
        "cells": [
            {"cell_type": "markdown", "source": ["# Title"], "metadata": {}},
            {"cell_type": "code", "source": ["print('hi')"], "metadata": {}, "outputs": []}
        ]
    }
    with tempfile.NamedTemporaryFile(suffix=".ipynb", mode="w+", delete=False) as f:
        json.dump(nb, f)
        f.flush()
        path = Path(f.name)
        cells = get_notebook_cells(path)
        assert len(cells) == 2
        assert cells[0]["cell_type"] == "markdown"
        assert cells[1]["cell_type"] == "code"
        assert cells[0]["content"] == "# Title"
        assert cells[1]["content"] == "print('hi')"


def test_get_notebook_cells_file_not_found():
    cells = get_notebook_cells(Path("/tmp/doesnotexist.ipynb"))
    assert cells == []


def test_get_date_from_filename_valid():
    fname = "2025-01-12-Get-Date-From-This.ipynb"
    dt = get_date_from_filename(fname)
    assert isinstance(dt, datetime)
    assert dt.year == 2025 and dt.month == 1 and dt.day == 12


def test_get_date_from_filename_invalid():
    fname = "notadate-at-all.ipynb"
    dt = get_date_from_filename(fname)
    assert isinstance(dt, datetime)
    # Should return now, so year should be current year
    assert abs((dt - datetime.now()).total_seconds()) < 5


# ---------------------------------------------------------------------------
# Unit tests: strip_markdown
# ---------------------------------------------------------------------------

class TestStripMarkdown:
    """strip_markdown should remove markdown link and inline-code syntax."""

    def test_strips_link_to_text(self):
        assert strip_markdown("[click here](https://example.com)") == "click here"

    def test_strips_multiple_links(self):
        text = "See [foo](http://foo.com) and [bar](http://bar.com)"
        assert strip_markdown(text) == "See foo and bar"

    def test_strips_inline_code(self):
        assert strip_markdown("Use `print()` to debug") == "Use print() to debug"

    def test_strips_links_and_code_together(self):
        text = "Check [docs](https://docs.pytest.org) for `pytest.fixture`"
        assert strip_markdown(text) == "Check docs for pytest.fixture"

    def test_leaves_plain_text_unchanged(self):
        plain = "Nothing special here."
        assert strip_markdown(plain) == plain

    def test_empty_string(self):
        assert strip_markdown("") == ""


# ---------------------------------------------------------------------------
# Unit tests: extract_first_image
# ---------------------------------------------------------------------------

class TestExtractFirstImage:
    """extract_first_image should return the URL of the first markdown image."""

    def test_extracts_image_url(self):
        text = "![alt text](https://example.com/photo.jpg)"
        assert extract_first_image(text) == "https://example.com/photo.jpg"

    def test_returns_first_when_multiple_images(self):
        text = (
            "![first](https://a.com/1.png)\n"
            "![second](https://b.com/2.png)"
        )
        assert extract_first_image(text) == "https://a.com/1.png"

    def test_returns_empty_string_when_no_image(self):
        assert extract_first_image("No images here.") == ""

    def test_ignores_regular_links(self):
        text = "A [link](https://example.com) but no image."
        assert extract_first_image(text) == ""

    def test_image_with_empty_alt(self):
        text = "![](https://example.com/pic.webp)"
        assert extract_first_image(text) == "https://example.com/pic.webp"


# ---------------------------------------------------------------------------
# Unit tests: get_post_dict
# ---------------------------------------------------------------------------

class TestGetPostDict:
    """get_post_dict should extract structured metadata from a markdown file."""

    def test_basic_post(self, tmp_path):
        md = tmp_path / "2025-06-15-My-Great-Post.md"
        md.write_text(
            "# My Great Post\n"
            "\n"
            "This is the tease line.\n"
            "\n"
            "More body content here.\n",
            encoding="utf-8",
        )
        result = get_post_dict(md)

        assert result["title"] == "My Great Post"
        assert "Jun" in result["meta"] and "2025" in result["meta"]
        assert result["tease"] == "This is the tease line."
        assert result["image"] == ""
        assert result["url"] == "/articles/2025-06-15-My-Great-Post"

    def test_post_with_image(self, tmp_path):
        md = tmp_path / "2025-03-01-Photo-Day.md"
        md.write_text(
            "# Photo Day\n"
            "\n"
            "Look at this cool shot.\n"
            "\n"
            "![sunset](https://example.com/sunset.jpg)\n",
            encoding="utf-8",
        )
        result = get_post_dict(md)

        assert result["title"] == "Photo Day"
        assert result["image"] == "https://example.com/sunset.jpg"

    def test_tease_strips_markdown_syntax(self, tmp_path):
        md = tmp_path / "2025-04-10-Linked-Tease.md"
        md.write_text(
            "# Linked Tease\n"
            "\n"
            "Read about [pytest](https://pytest.org) and `fixtures`.\n",
            encoding="utf-8",
        )
        result = get_post_dict(md)

        # The tease should have markdown syntax stripped
        assert "[pytest]" not in result["tease"]
        assert "`fixtures`" not in result["tease"]
        assert "pytest" in result["tease"]
        assert "fixtures" in result["tease"]

    def test_date_extracted_from_filename(self, tmp_path):
        md = tmp_path / "2024-12-25-Christmas.md"
        md.write_text("# Christmas\n\nHappy holidays!\n", encoding="utf-8")
        result = get_post_dict(md)

        assert result["date"].year == 2024
        assert result["date"].month == 12
        assert result["date"].day == 25


# ---------------------------------------------------------------------------
# Homepage integration tests (GET /)
# ---------------------------------------------------------------------------

class TestHomepage:
    """
    Integration tests for the homepage, covering the PR test plan items:
    - Posts show title + date + tease + image
    - No raw markdown visible in teases
    - Expected page structure (feed header, post articles, sidebar)
    """

    def test_homepage_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200

    def test_homepage_has_feed_header(self, homepage_html):
        assert "feed-header" in homepage_html
        assert "Latest writing" in homepage_html

    def test_homepage_has_post_articles(self, homepage_html):
        # There should be at least one <article class="post ..."> element
        assert '<article class="post' in homepage_html

    def test_homepage_has_sidebar(self, homepage_html):
        assert '<aside class="sidebar">' in homepage_html
        assert "Audrey M. Roy Greenfeld" in homepage_html

    def test_posts_show_titles(self, homepage_html):
        # Every post has an h2.post-title with a link
        assert 'class="post-title"' in homepage_html

    def test_posts_show_dates(self, homepage_html):
        # post-date spans contain formatted dates like "Mon, Jan 9, 2025"
        assert 'class="post-date"' in homepage_html

    def test_posts_show_teases(self, homepage_html):
        assert 'class="post-tease' in homepage_html

    def test_posts_show_continue_reading_links(self, homepage_html):
        assert "Continue reading" in homepage_html
        assert 'class="post-continue"' in homepage_html

    def test_featured_post_exists(self, homepage_html):
        assert 'class="post featured"' in homepage_html
        assert "Featured" in homepage_html

    def test_no_raw_markdown_links_in_teases(self, homepage_html):
        """
        PR test plan: verify no raw markdown [link](url) syntax visible
        in any tease on the homepage.
        """
        # Extract all tease text from <p class="post-tease...">...</p>
        tease_pattern = re.compile(
            r'<p class="post-tease[^"]*">(.*?)</p>', re.DOTALL
        )
        teases = tease_pattern.findall(homepage_html)
        assert len(teases) > 0, "Expected at least one tease on the homepage"
        for tease in teases:
            assert not re.search(r'\[.*?\]\(.*?\)', tease), (
                f"Found raw markdown link in tease: {tease!r}"
            )

    def test_no_raw_code_fences_in_teases(self, homepage_html):
        """
        PR test plan: verify no triple-backtick code fences visible
        in any tease on the homepage.
        """
        tease_pattern = re.compile(
            r'<p class="post-tease[^"]*">(.*?)</p>', re.DOTALL
        )
        teases = tease_pattern.findall(homepage_html)
        for tease in teases:
            assert "```" not in tease, (
                f"Found raw code fence in tease: {tease!r}"
            )

    def test_no_raw_inline_code_in_teases(self, homepage_html):
        """Verify no backtick-wrapped inline code in teases."""
        tease_pattern = re.compile(
            r'<p class="post-tease[^"]*">(.*?)</p>', re.DOTALL
        )
        teases = tease_pattern.findall(homepage_html)
        for tease in teases:
            assert not re.search(r'`[^`]+`', tease), (
                f"Found raw inline code in tease: {tease!r}"
            )

    def test_homepage_total_posts_count(self, homepage_html):
        """The feed header should report the total post count."""
        match = re.search(r'(\d+) total posts', homepage_html)
        assert match, "Expected 'N total posts' in feed header"
        count = int(match.group(1))
        assert count > 0, "Expected at least one post"


# ---------------------------------------------------------------------------
# Article page integration tests (GET /articles/{name})
# ---------------------------------------------------------------------------

class TestArticlePage:
    """
    Integration tests for article detail pages, covering:
    - Article page returns 200 with title and content
    - Nonexistent article returns an error (currently 500 due to air.Response bug)
    """

    def test_article_returns_200(self, client):
        response = client.get(
            "/articles/2025-12-16-Adopting-Idiomatic-PyTest-Code-Review"
        )
        assert response.status_code == 200

    def test_article_contains_title(self, client):
        response = client.get(
            "/articles/2025-12-16-Adopting-Idiomatic-PyTest-Code-Review"
        )
        assert "Adopting Idiomatic PyTest" in response.text

    def test_article_contains_byline(self, client):
        response = client.get(
            "/articles/2025-12-16-Adopting-Idiomatic-PyTest-Code-Review"
        )
        assert "Audrey M. Roy Greenfeld" in response.text

    def test_article_contains_content(self, client):
        response = client.get(
            "/articles/2025-12-16-Adopting-Idiomatic-PyTest-Code-Review"
        )
        # The article body should contain rendered HTML content
        assert "article-content" in response.text

    def test_article_has_date_in_byline(self, client):
        response = client.get(
            "/articles/2025-12-16-Adopting-Idiomatic-PyTest-Code-Review"
        )
        # Dec 16, 2025
        assert "2025" in response.text
        assert "Dec" in response.text

    def test_nonexistent_article_errors(self, client):
        """
        Requesting a nonexistent article should return 404. Currently the app
        raises AttributeError because air.Response does not exist (it should
        be starlette.responses.Response or similar). This test documents the
        existing behavior so the bug is visible.
        """
        with pytest.raises(AttributeError, match="Response"):
            client.get("/articles/this-article-does-not-exist-at-all")
