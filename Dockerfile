#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "apply-templates.sh"
#
# PLEASE DO NOT EDIT IT DIRECTLY.
#

FROM python:3.13.2-slim

LABEL org.opencontainers.image.title="KavitaBot"
LABEL org.opencontainers.image.description="A discord bot to allow users to generate their own Kavita invite"
LABEL org.opencontainers.image.vendor="DMTNT"
LABEL org.opencontainers.image.version="0.2.0"
LABEL org.opencontainers.image.created="2025-03-26"
LABEL org.opencontainers.image.url="https://github.com/dmtnt0/kavitabot"
LABEL org.opencontainers.image.documentation="https://github.com/dmtnt0/kavitabot/wiki"
LABEL org.opencontainers.image.licenses="MIT License"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3", "main.py"]
