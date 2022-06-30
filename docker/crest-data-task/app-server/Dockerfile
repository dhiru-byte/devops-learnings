###App Server Installation

FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
     apache2 \
     apache2-utils
ENV APACHE_RUN_USER www-data
ENV APACHE_RUN_GROUP www-data
ENV APACHE_LOG_DIR /var/log/apache2
ENV APACHE_RUN_DIR /var/www/html

RUN apt clean
COPY .000-default.conf /etc/apache2/sites-enabled/
COPY .ports.conf /etc/apache2/

ENTRYPOINT ["/usr/sbin/apache2"]
CMD ["-D", "FOREGROUND"]

EXPOSE 80 8080
