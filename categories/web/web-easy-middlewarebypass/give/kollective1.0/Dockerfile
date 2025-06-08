FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json* ./

RUN npm i
COPY . .
RUN npx prisma generate


EXPOSE 3000
RUN sleep 10
RUN npm run build