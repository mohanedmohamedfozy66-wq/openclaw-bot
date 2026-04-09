FROM node:22-slim

RUN npm install -g openclaw@latest

WORKDIR /app
COPY . .

RUN mkdir -p /root/.openclaw

RUN echo '{"gateway":{"port":18789},"model":{"provider":"google","apiKey":"'$GOOGLE_API_KEY'","model":"gemini-2.0-flash-exp"},"channels":{"telegram":{"enabled":true,"token":"'$TELEGRAM_BOT_TOKEN'"}}}' > /root/.openclaw/config.json

EXPOSE 18789

CMD openclaw gateway start --no-daemon --config /root/.openclaw/config.json
