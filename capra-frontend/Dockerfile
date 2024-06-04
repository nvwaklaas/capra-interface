FROM node:21-alpine

WORKDIR /app

COPY package.json .

RUN npm install

COPY . .

RUN npm run build

ENV HOST 0.0.0.0

EXPOSE 5173

# Start de Vite dev server
CMD ["npm", "run", "dev"]
