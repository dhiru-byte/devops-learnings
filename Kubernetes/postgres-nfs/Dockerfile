FROM postgres:12


ENV PGHOST=''
ENV PGPORT='31641'
ENV PGDATABASE='terraform_backend'
ENV PGUSER='amazinguser@terraform_backend'
ENV PGPASSWORD='perfectpassword'

#RUN apk update
#RUN apk add postgresql-12

COPY dumpDatabase.sh .

ENTRYPOINT [ "/bin/sh" ]
CMD [ "./dumpDatabase.sh" ]
