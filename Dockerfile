FROM node:22-slim
RUN npm install -g openclaw@latest
WORKDIR /app
COPY . .
EXPOSE 18789
CMD ["openclaw", "gateway", "start", "--no-daemon"]
