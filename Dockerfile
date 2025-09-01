FROM node:20

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

CMD ["node", "telegram_openai_hook.js"]