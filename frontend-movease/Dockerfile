FROM node:20 as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:1.19.0-alpine as production
COPY --from=build /app/build /usr/share/nginx/html
# Rename de app.html to index.html
RUN mv /usr/share/nginx/html/app.html /usr/share/nginx/html/index.html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
