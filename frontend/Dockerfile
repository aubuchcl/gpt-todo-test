FROM node:18 AS build
WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install  # Ensures all dependencies are installed

COPY . .  # Copy the entire project
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]
