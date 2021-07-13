FROM python:3.9.5
LABEL authors="Biano AI <ai-research@biano.com>"

# ----------------------------------------------------------------------------------------------------
# 1. System Settings
# ----------------------------------------------------------------------------------------------------
ARG PYTHONUNBUFFERED=1
ARG DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-EeuxoC", "pipefail", "-c"]

# ---------------------------------------------------------------------
# 2. Workdir
# ---------------------------------------------------------------------
RUN mkdir -p /app
WORKDIR /app

# ---------------------------------------------------------------------
# 3. Requirements
# ---------------------------------------------------------------------
COPY ./requirements/production.txt /requirements/
RUN pip install --isolated --no-input --compile --exists-action=a --disable-pip-version-check --no-cache-dir -r /requirements/production.txt \
    && rm -rf /requirements/production.txt

COPY ./requirements/base.txt /requirements/
RUN pip install --isolated --no-input --compile --exists-action=a --disable-pip-version-check --no-cache-dir -r /requirements/base.txt \
    && rm -rf /requirements/base.txt

# ---------------------------------------------------------------------
# 4. App sources
# ---------------------------------------------------------------------
COPY ./src /app/src
COPY api.py /app/api.py

# ---------------------------------------------------------------------
# 5. Define process
# ---------------------------------------------------------------------
EXPOSE 8080
CMD ["gunicorn", "api:main", "--worker-tmp-dir=/tmp", "--bind=0.0.0.0:8080", "--workers=2", "--preload", "--chdir=/app", "--worker-class=uvicorn.workers.UvicornWorker", "--log-level=INFO" ]

