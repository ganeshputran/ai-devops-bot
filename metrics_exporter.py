# metrics_exporter.py — Prometheus metrics exporter
# Runs app.py health checks on a schedule and exposes results
# as Prometheus metrics on port 8000.
#
# Metrics exposed:
#   portfolio_page_up         — 1 if page returned 200, 0 if not
#   portfolio_response_time   — response time in seconds
#   portfolio_check_total     — total checks run per page
#   portfolio_last_check      — Unix timestamp of last check

import time
import os
from prometheus_client import start_http_server, Gauge, Counter
from app import check_all_pages, PORTFOLIO_PAGES

# ── METRIC DEFINITIONS ──
# Gauge: value that can go up and down (e.g. up/down status)
# Counter: value that only increases (e.g. total checks run)

page_up = Gauge(
    'portfolio_page_up',
    'Whether the portfolio page is returning HTTP 200 (1=up, 0=down)',
    ['page_name', 'url']
)

response_time = Gauge(
    'portfolio_response_time_seconds',
    'Response time of the portfolio page in seconds',
    ['page_name', 'url']
)

check_total = Counter(
    'portfolio_check_total',
    'Total number of health checks run per page',
    ['page_name', 'url']
)

last_check = Gauge(
    'portfolio_last_check_timestamp',
    'Unix timestamp of the last health check',
    ['page_name', 'url']
)

# ── SCRAPE INTERVAL ──
INTERVAL = int(os.environ.get('SCRAPE_INTERVAL', 60))


def run_checks():
    """Run health checks and update all Prometheus metrics.
    Handles failures gracefully — always exposes metrics even if checks fail.
    """
    print(f"Running health checks for {len(PORTFOLIO_PAGES)} pages...")
    try:
        results = check_all_pages()
    except Exception as e:
        # If app.py itself fails, expose error metrics so Prometheus
        # can alert rather than showing stale data
        print(f"❌ Health check failed entirely: {e}")
        for page in PORTFOLIO_PAGES:
            page_up.labels(page_name=page['name'], url=page['url']).set(0)
            last_check.labels(page_name=page['name'], url=page['url']).set(time.time())
        return

    for result in results:
        name = result['name']
        url  = result['url']

        # Update up/down status
        page_up.labels(page_name=name, url=url).set(
            1 if result['ok'] else 0
        )

        # Update response time if available
        if result.get('duration') is not None:
            response_time.labels(page_name=name, url=url).set(
                result['duration']
            )

        # Increment total check counter
        check_total.labels(page_name=name, url=url).inc()

        # Record timestamp of this check
        last_check.labels(page_name=name, url=url).set(time.time())

        status = '✅' if result['ok'] else '❌'
        print(f"  {status} {name} — {'up' if result['ok'] else 'down'}")

    print(f"Next check in {INTERVAL}s\n")


if __name__ == '__main__':
    print(f"Starting metrics exporter on port 8000")
    print(f"Check interval: {INTERVAL}s")

    # Start the Prometheus HTTP server on port 8000
    start_http_server(8000)
    print("Metrics available at http://localhost:8000/metrics\n")

    # Run checks immediately on startup then on schedule
    while True:
        run_checks()
        time.sleep(INTERVAL)
