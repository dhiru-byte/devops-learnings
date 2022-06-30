ARG PHP_APACHE=dhirujackal/test-docker:latest
FROM $PHP_APACHE

# Install Drush
RUN php -r "readfile('https://github.com/drush-ops/drush-launcher/releases/download/0.6.0/drush.phar');" > drush \
    && chmod +x drush \
    && mv drush /usr/bin/
RUN rm -rf /etc/apache2/sites-enabled/000-default.conf

COPY ./docker-utils/apache2/ports.conf /etc/apache2/
COPY ./docker-utils/apache2/sites/*.conf /etc/apache2/sites-available
COPY ./docker-utils/apache2/sites/*.conf /etc/apache2/sites-enabled
RUN mkdir -p /var/www/html/dcg/docroot
COPY ./docroot /var/www/html/dcg/docroot

EXPOSE 81




WORKDIR /var/www/html/dcg/docroot
