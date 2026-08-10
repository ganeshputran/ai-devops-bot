# Changelog

## [v1.2.0] — 2026-06-07
### Added
- Dockerfile — containerised app.py with python:3.11-slim base image
- Dockerfile.metrics — metrics exporter container for Prometheus scraping
- docker-build.yml — automated Docker image build and push to GHCR on every push
- health-check.yml — hourly cloud health check via GitHub Actions with auto-alert issues and auto-close
- Prometheus + Grafana monitoring stack via Docker Compose
- metrics_exporter.py — exposes portfolio health as Prometheus metrics (page_up, response_time, check_total)
- monitoring/docker-compose.yml — Prometheus + Grafana + metrics-exporter stack
- monitoring/prometheus.yml — scrape config aligned to 60s check interval
- monitoring/grafana/ — auto-provisioned datasource and portfolio health dashboard
- CONTRIBUTING.md — feature branch workflow documented
- .gitignore — monitoring/.env excluded from version control
- Branch protection on both repos — PRs required to merge to main
### Changed
- app.py — added duration tracking to check_page results for Prometheus metrics
### Fixed
- Grafana admin password moved to .env file — flagged by AI code reviewer

## [v1.1.0] — 2026-05-27
### Added
- gemini_utils.py — shared Gemini + GitHub utilities
- Cloudflare Worker proxy — all API keys removed from source code
- In-memory caching in Worker — reduces Gemini rate limit hits
- Hourly health check via cron job + log_analyser.py
### Changed
- explain_failure.py — reads from file path, uses gemini_utils
- review_code.py — uses gemini_utils, 8000 char diff limit, error handling
- app.py — portfolio health checker replacing task manager
- test_app.py — 15 tests for health checker using unittest.mock
- Gemini model switched to gemini-2.5-flash-lite (1000 RPD free tier)
- All browser API calls routed through Cloudflare Worker

## [v1.0.0] — 2026-05-26
### Added
- CI pipeline with pytest (15 tests, 80% coverage threshold)
- AI failure explainer on PR comments
- AI code reviewer on every PR
- Live pipeline dashboard on GitHub Pages
- Hobbies page with AI recommendations
- widgets.js centralised functionality layer
- Maintenance page
- Caddy v2 reverse proxy (local WSL)
- Cloudflare Tunnel for public HTTPS
- Caddy JSON access logs and log_analyser.py
- Two-repo architecture (appearance vs functionality)
