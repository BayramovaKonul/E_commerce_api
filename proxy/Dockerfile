FROM nginx:1.25

# clean default nginx configuration
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.prod.conf /etc/nginx/conf.d/
# make it nginix.prod.conf after getting domain