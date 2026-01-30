FROM prom/prometheus:0.16.1

ADD prometheus.yml /etc/prometheus/prometheus.yml
ADD ants.rules /etc/prometheus/ants.rules

RUN mkdir -p /etc/prometheus/targets.d

EXPOSE 9090

ENTRYPOINT [ "/bin/prometheus" ]
CMD        [ "-config.file=/etc/prometheus/prometheus.yml", \
             "-storage.local.path=/prometheus", \
             "-web.console.libraries=/etc/prometheus/console_libraries", \
             "-web.console.templates=/etc/prometheus/consoles", \
             "-web.listen-address=:9090", \
             "-alertmanager.url=http://alertmanager:9093"]
