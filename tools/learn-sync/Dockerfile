# Chromium and its system libraries come baked in, so nothing browser-related
# has to be installed into the LXC itself.
#
# This tag and the playwright pin in requirements.txt MUST match exactly: the
# image ships browser binaries for one specific Playwright version, and a pip
# resolver that picks a newer one fails at launch with "Executable doesn't exist".
FROM mcr.microsoft.com/playwright/python:v1.62.0-jammy

RUN apt-get update && apt-get install -y --no-install-recommends \
        git openssh-client rclone \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python", "-m", "learn_sync.cli"]
CMD ["sync"]
