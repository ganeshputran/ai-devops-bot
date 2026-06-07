# Dockerfile — Portfolio health checker
# Packages app.py into a reproducible container.
# Build:  docker build -t portfolio-health .
# Run:    docker run --rm portfolio-health
# Pull:   docker pull ghcr.io/ganeshputran/ai-devops-bot:latest

# ── BASE IMAGE ──
# python:3.11-slim is the minimal Python image — ~60MB vs ~900MB for full Python.
# slim has no dev tools, compilers, or extra packages — perfect for a script runner.
FROM python:3.11-slim

# ── METADATA ──
# Labels appear in GitHub Packages and Docker Hub listings.
LABEL org.opencontainers.image.title="Portfolio Health Checker"
LABEL org.opencontainers.image.description="Checks all live portfolio URLs and reports HTTP status"
LABEL org.opencontainers.image.author="Ganesh Putran"
LABEL org.opencontainers.image.source="https://github.com/ganeshputran/ai-devops-bot"

# ── WORKING DIRECTORY ──
# All subsequent COPY/RUN commands operate relative to /app.
WORKDIR /app

# ── COPY APP FILES ──
# Copy only what the app needs — .dockerignore excludes the rest.
COPY app.py .

# ── RUNTIME ──
# No pip install needed — app.py uses only Python standard library.
# Non-root user for security best practice — don't run as root inside containers.
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# ── ENTRYPOINT ──
# CMD runs when the container starts with no arguments.
# Can be overridden: docker run portfolio-health python app.py --help
CMD ["python", "app.py"]
