FROM nginx

COPY assets /usr/share/nginx/html/assets
COPY image /usr/share/nginx/html/image
COPY css /usr/share/nginx/html/css
COPY index.html /usr/share/nginx/html
