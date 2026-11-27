FROM nginx:1.27-alpine
# Configuración endurecida
RUN rm -f /etc/nginx/conf.d/default.conf && mkdir -p /etc/nginx/snippets
COPY nginx.conf /etc/nginx/conf.d/glysf.conf
COPY seguridad-headers.conf /etc/nginx/snippets/seguridad-headers.conf
# Solo los archivos públicos de la web
COPY index.html privacidad.html aviso-legal.html 404.html styles.css app.js site.js \
     favicon.svg favicon-32.png apple-touch-icon.png og.png robots.txt sitemap.xml /usr/share/nginx/html/
RUN chmod -R a-w /usr/share/nginx/html
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://127.0.0.1/ >/dev/null || exit 1
