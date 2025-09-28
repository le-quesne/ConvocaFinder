FROM node:20-alpine

WORKDIR /app

# Instala dependencias con caché
COPY package.json package-lock.json ./
RUN npm ci

# Copia el resto del código
COPY . .

# El comando real lo definimos en docker-compose (para forzar 0.0.0.0)
CMD ["npm","run","dev"]
