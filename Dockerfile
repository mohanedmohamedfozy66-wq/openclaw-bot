FROM node:22-slim

RUN npm install -g openclaw@latest

WORKDIR /app
COPY . .

ENV OPENCLAW_SKIP_ONBOARD=1
ENV NODE_ENV=production

RUN openclaw onboard \
  --provider google \
  --skip-interactive || true

EXPOSE 18789

CMD ["openclaw", "gateway", "start", "--no-daemon"]
