###Web Server Installation

FROM ubuntu:latest

RUN rm -rf /var/www/html && mkdir -p /var/lock/apache2 /var/run/apache2 /var/log/apache2 /var/www/html && chown -R www-data:www-data /var/lock/apache2 /var/run/apache2 /var/log/apache2 /var/www/html
RUN mv /etc/apache2/apache2.conf /etc/apache2/apache2.conf.dist && rm /etc/apache2/conf-enabled/* /etc/apache2/sites-enabled/*

RUN  apt-get install -y python-pip \
     git \
     wget 

RUN  pip install --upgrade pip \
     && pip install PyMySQL \
     && git clone https://gitlab.com/crest1/devops_test.git \
     && cd devops_test/ \
     chmod +x install.sh

RUN apt-get update && apt-get install -y \
		ca-certificates \
		curl \
		libcurl3 \
		libedit2 \
		libsqlite3-0 \
		libxml2 \
	--no-install-recommends && rm -r /var/lib/apt/lists/*

RUN a2dismod mpm_event && a2enmod mpm_prefork
RUN apt-get update && apt-get install -y apache2 apache2-utils --no-install-recommends && rm -rf /var/lib/apt/lists/*



# ENV APACHE_RUN_USER www-data
# ENV APACHE_RUN_GROUP www-data
# ENV APACHE_LOG_DIR /var/log/apache2
# ENV APACHE_RUN_DIR /var/www/html

COPY .000-default.conf /etc/apache2/sites-enabled/
COPY .ports.conf /etc/apache2/

ENTRYPOINT ["/usr/sbin/apache2"]
CMD ["-D", "FOREGROUND"]

EXPOSE 80
