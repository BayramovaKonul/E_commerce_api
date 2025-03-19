FROM nginx:1.25

# Clean default Nginx configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy the custom Nginx configuration
COPY nginx/nginx.prod.conf /etc/nginx/conf.d/default.conf

# Expose the ports Nginx will be running on
EXPOSE 80 443