FROM node:22-slim
RUN npm install -g openclaw@latest
RUN npm install -g grammy
WORKDIR /app
COPY . .
EXPOSE 18789
ENV OPENCLAW_CONFIG_PATH=/app/openclaw.json
CMD ["openclaw", "gateway", "start"]
