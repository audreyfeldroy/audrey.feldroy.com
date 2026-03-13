# Staticware 0.2.0: The first cut

This is an early release. Staticware does something very satisfyingly today: it serves static files with content-hashed URLs for cache busting. That means when you edit your CSS then redeploy and restart your server, visitors get the latest CSS without forcing a refresh. More will come.

I originally created the code behind Staticware as part of [Air](https://github.com/feldroy/air), building static file handling was built directly into the framework. Extracting it into standalone ASGI middleware meant that anyone building with Starlette, FastAPI, or raw ASGI could use it too, not just Air users. I even started a PR exploring getting it working with Django.

This package is dedicated to the memory of **Michael Ryabushkin** (aka goodwill), who died in 2025. Michael was a Pyramid developer who also helped host and grow the LA Django community. He believed that when you build something useful, you should build it for everyone, not just your own framework's users. He advocated that Python web developers learn to write packages generalized enough for the whole community to benefit. Staticware exists as a standalone ASGI library instead of framework-specific code because that's the kindest way to build it, and Michael was one of the people who made that obvious.

```bash
uv add staticware
```

### What's in this release

**Content-hashed static file serving.** `HashedStatic("static")` scans a directory at startup, computes content hashes, and serves files at URLs like `/static/styles.a1b2c3d4.css`. Hashed URLs get `Cache-Control: public, max-age=31536000, immutable`. Original filenames still work with standard caching, and repeated requests return 304 Not Modified.

**Automatic HTML rewriting.** `StaticRewriteMiddleware` wraps any ASGI app and rewrites static paths in HTML responses to their hashed equivalents. Streaming responses are buffered and rewritten transparently. Non-HTML responses pass through untouched.

**Template URL resolution.** `static.url("styles.css")` returns the cache-busted URL for use in any template engine. Unknown files return the original path with the prefix, so nothing breaks if a file is missing from the directory.

**Aims to work with every ASGI framework.** Tested with Starlette, FastAPI, Air, and raw ASGI. I've started experimental exploration of it with Django in a PR but that's not part of this release yet. Supports `root_path` for mounted sub-applications so cache-busted URLs work correctly behind reverse proxies and path prefixes.

**Security built in.** Path traversal attempts are rejected at both startup (files resolving outside the directory are excluded) and serving time (resolved paths are validated). Files that could escape the static directory never make it into the URL map.

### Contributors

[@audreyfeldroy](https://github.com/audreyfeldroy) (Audrey M. Roy Greenfeld) designed and built staticware: the hashing engine, ASGI serving, HTML rewriting middleware, path traversal protection, 304 support, root_path handling, and the full test suite.

[@pydanny](https://github.com/pydanny) (Daniel Roy Greenfeld) reviewed and merged the middleware return value fix (PR [#2](https://github.com/feldroy/staticware/pull/2)).

Tags: python, open-source
