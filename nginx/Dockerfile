FROM nginx:1.27.0-alpine

COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY localhost.crt /etc/nginx/ssl/localhost.crt
COPY localhost.key /etc/nginx/ssl/localhost.key

CMD ["nginx", "-g", "daemon off;"]