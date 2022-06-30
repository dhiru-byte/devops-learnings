FROM ubuntu:16.04

MAINTAINER Dhirendra Yadav(dhrnd.ydv@gmail.com)

WORKDIR /var/

# Update cache and install Nginx
RUN apt-get update && apt-get -y install \
   nginx \
   wget \
   curl 

RUN apt-get update && apt-get -y install \
      php-fpm \
       php-common \
       php-mbstring \
       php-xmlrpc \
       php-soap \
       php-gd \
       php-xml \
       php-intl \
       php-mysql \
       php-cli \
       php-mcrypt \
       php-ldap \
       php-tidy \
       php-recode \
       php-zip php-curl



RUN apt-get update && apt-get install -y mariadb-server mariadb-client

RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf

RUN wget https://ftp.drupal.org/files/projects/drupal-8.3.7.tar.gz

RUN tar -zxvf drupal*.gz -C /var/www/html

RUN mv /var/www/html/drupal-8.3.7/ /var/www/html/drupal/

RUN chown -R www-data:www-data /var/www/html/

RUN chmod -R 755 /var/www/html/


# Copy default site conf
COPY default /etc/nginx/sites-available/default

COPY ["start.sh", "/var/start.sh"]
RUN chmod +x start.sh
CMD ["./start.sh"]


# Expose port 80
EXPOSE 80
EXPOSE 443