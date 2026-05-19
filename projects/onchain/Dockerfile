FROM node:20-bookworm-slim

RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    python3 python3-pip ca-certificates curl jq tini \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev 2>/dev/null || npm install --omit=dev

COPY . .

ENV NODE_OPTIONS=--max-old-space-size=4096
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["bash", "scripts/wallet_v2/watchdog.sh"]
