# Docker Stack for Apache2.4 and php7.2 environment

## Summary

A simple Dockerfile for apache 2.4 and php-fpm 7.2

- Based on debian
- With apache 2.4 + php-fpm7.2
- Custom apache 2.4, php7.2 and supervisord configurations

## Usage

### Development

```
docker build -t apache-php-fpm-base --build-arg DEBIAN_IMAGE=debian-base .;
docker run apache-php-fpm -p 80:80;
```

### Debugging

Login:

```
docker exec -it apache-php-fpm-base /bin/bash
```