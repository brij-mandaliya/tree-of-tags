FROM node:20 AS build
WORKDIR /app
COPY tree-of-tags/package.json tree-of-tags/package-lock.json ./
RUN npm install
COPY tree-of-tags/ .
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY tree-of-tags/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
