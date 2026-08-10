# app.py — Portfolio site health checker
# Validates all key portfolio pages with content verification,
# not just HTTP status codes. Checks for expected content in
# each page to ensure the application is truly healthy.

import urllib.request
import urllib.error
from datetime import datetime, timezone

# ── PORTFOLIO PAGES ──
# Each page has optional content_check — a string that must appear
# in the response body to confirm the page is serving real content.
PORTFOLIO_PAGES = [
    {
        "name":          "Portfolio (main)",
        "url":           "https://ganeshputran.github.io",
        "content_check": "Ganesh Putran",   # verify real content is served
    },
    {
        "name":          "Pipeline dashboard",
        "url":           "https://ganeshputran.github.io/ai-devops-bot/",
        "content_check": "AI DevOps Bot",
    },
    {
        "name":          "Hobbies page",
        "url":           "https://ganeshputran.github.io/ai-devops-bot/hobbies.html",
        "content_check": "Hobbies",
    },
    {
        "name":          "Widgets JS",
        "url":           "https://ganeshputran.github.io/ai-devops-bot/widgets.js",
        "content_check": "WORKER_URL",      # verify JS is correctly deployed
    },
    {
        "name":          "Cloudflare Worker",
        "url":           "https://gemini-proxy.ganeshputran.workers.dev/readme?repo=ganeshputran/ai-devops-bot",
        "content_check": None,              # just check it responds
    },
]


def check_page(name: str, url: str, content_check: str = None, timeout: int = 10) -> dict:
    """
    Check a URL for HTTP 200 and optionally verify expected content.

    Args:
        name:          human-readable page name
        url:           URL to check
        content_check: string that must appear in response body (optional)
        timeout:       request timeout in seconds

    Returns dict with name, url, status, ok, duration, error, content_ok fields.
    """
    if not url or not url.startswith("http"):
        raise ValueError(f"Invalid URL: '{url}'")

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "PortfolioHealthChecker/1.0"}
        )
        start = datetime.now(timezone.utc).timestamp()
        with urllib.request.urlopen(req, timeout=timeout) as response:
            duration = round(datetime.now(timezone.utc).timestamp() - start, 3)
            body     = response.read().decode('utf-8', errors='ignore')

            # ── Content verification ──
            content_ok = True
            content_error = None
            if content_check and content_check not in body:
                content_ok    = False
                content_error = f"Expected '{content_check}' not found in response"

            return {
                "name":          name,
                "url":           url,
                "status":        response.status,
                "ok":            response.status == 200 and content_ok,
                "duration":      duration,
                "error":         content_error,
                "content_ok":    content_ok,
                "content_check": content_check,
            }

    except urllib.error.HTTPError as e:
        return {
            "name": name, "url": url, "status": e.code,
            "ok": False, "duration": None,
            "error": f"HTTP {e.code}: {e.reason}",
            "content_ok": False, "content_check": content_check,
        }
    except urllib.error.URLError as e:
        return {
            "name": name, "url": url, "status": None,
            "ok": False, "duration": None,
            "error": f"Connection failed: {e.reason}",
            "content_ok": False, "content_check": content_check,
        }
    except Exception as e:
        return {
            "name": name, "url": url, "status": None,
            "ok": False, "duration": None,
            "error": f"Unexpected error: {str(e)}",
            "content_ok": False, "content_check": content_check,
        }


def check_all_pages(pages: list = None) -> list:
    """Check all portfolio pages. Uses PORTFOLIO_PAGES by default."""
    if pages is None:
        pages = PORTFOLIO_PAGES
    results = []
    for page in pages:
        result = check_page(
            page["name"],
            page["url"],
            page.get("content_check")
        )
        results.append(result)
    return results


def get_summary(results: list) -> dict:
    """Summarise check results."""
    if not results:
        return {"total": 0, "passed": 0, "failed": 0, "healthy": True, "failed_pages": []}
    passed      = sum(1 for r in results if r["ok"])
    failed      = len(results) - passed
    failed_pages = [r["name"] for r in results if not r["ok"]]
    return {
        "total":        len(results),
        "passed":       passed,
        "failed":       failed,
        "healthy":      failed == 0,
        "failed_pages": failed_pages,
    }


def format_report(results: list) -> str:
    """Format check results as a human-readable report."""
    summary = get_summary(results)
    lines   = [
        f"Portfolio Health Report — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}",
        f"{'='*52}",
        f"Total: {summary['total']}  |  Passed: {summary['passed']}  |  Failed: {summary['failed']}",
        ""
    ]

    for r in results:
        icon   = "✅" if r["ok"] else "❌"
        status = str(r["status"]) if r["status"] else "ERR"
        dur    = f" ({r['duration']}s)" if r["duration"] else ""
        lines.append(f"  {icon}  [{status}]  {r['name']}{dur}")
        if r["error"]:
            lines.append(f"         ↳ {r['error']}")
        if r.get("content_check") and not r.get("content_ok"):
            lines.append(f"         ↳ Content check FAILED: '{r['content_check']}' not found")

    lines.append("")
    if summary["healthy"]:
        lines.append("HEALTHY ✓")
    else:
        lines.append(f"UNHEALTHY — failed pages: {', '.join(summary['failed_pages'])}")
    return "\n".join(lines)


if __name__ == "__main__":
    print("Checking portfolio pages...\n")
    results = check_all_pages()
    print(format_report(results))