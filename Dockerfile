FROM nginx:alpine
COPY index.html privacidad.html favicon.svg /usr/share/nginx/html/
EXPOSE 80
