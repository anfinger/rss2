FROM centos:centos7.6.1810 AS project-base

# Setup env
ENV LANG en_US.UTF-8
#ENV LANG C.UTF-8
#ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONFAULTHANDLER=1

ARG DATABASE_URL
ARG DEBUG

ENV DATABASE_URL=$DATABASE_URL
ENV DEBUG=$DEBUG

ENV DCKR_PROJECT_WORKDIR=/srv/rss2
RUN mkdir $DCKR_PROJECT_WORKDIR
WORKDIR $DCKR_PROJECT_WORKDIR

RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-* &&\
   sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*

# NOTE: this seems to be the latest available el7 release,
#   but `el7-7` is installed "in production"
#
#RUN curl -sSOL https://dev.mysql.com/get/mysql57-community-release-el7-7.noarch.rpm
RUN curl -sSOL https://dev.mysql.com/get/mysql57-community-release-el7-7.noarch.rpm &&\
   yum --nogpgcheck -y localinstall ./mysql57-community-release-el7-7.noarch.rpm

RUN yum --nogpgcheck -y install epel-release &&\
  # NOTE: exit status of `check-updates` IS NOT 0!
  yum check-updates ||\
  yum --nogpgcheck -y update &&\
  yum --nogpgcheck -y install python python-pip \
    MySQL-python mysql-connector-python \
    libxml2-devel libxslt-devel gcc python-devel     # NOTE: these are all required for `lxml`

COPY requirements.txt .

# see >> https://stackoverflow.com/q/65902444
#
RUN pip --cert /etc/ssl/certs/ca-bundle.crt install --upgrade pip==20.3.4 --no-cache-dir &&\
  pip --cert /etc/ssl/certs/ca-bundle.crt install -r requirements.txt --no-cache-dir

RUN ln -s $DCKR_PROJECT_WORKDIR/home/templates/index/index.html /srv/ &&\
  ln -s $DCKR_PROJECT_WORKDIR/home/templates/index/musicals.html /srv/ &&\
  ln -s $DCKR_PROJECT_WORKDIR/home/templates/index/datenschutz.html /srv/ &&\
  ln -s $DCKR_PROJECT_WORKDIR/home/templates/index/impressum.html /srv/

# MEDIA_ROOT + STATIC_ROOT
#
RUN mkdir --parents /var/www/reiseservice-schwerin/rss2/ &&\
  ln -s $DCKR_PROJECT_WORKDIR/media /var/www/reiseservice-schwerin/rss2/ &&\
  ln -s $DCKR_PROJECT_WORKDIR/static /var/www/reiseservice-schwerin/rss2/

FROM project-base AS dev-app

#RUN pip install pipenv && pipenv install --dev --system

CMD ["python", "-Wd", "./manage.py", "runserver", "0.0.0.0:8000"]
#CMD ["python", "-Wd", "./manage.py", "check"]

# staging / testing / prod (tbd.); managed by helm; currently no volumes or DB containers!
FROM project-base AS prod-app

# NOTE: exit status of `check-updates` IS NOT 0!
RUN yum check-updates ||\
  yum --nogpgcheck -y update &&\
  yum --nogpgcheck -y install httpd httpd-tools httpd-devel \
    apache-commons-lang apache-commons-logging \
    mod_gnutls mod_nss mod_proxy_html mod_proxy_uwsgi \
    mod_session mod_ssl mod_wsgi mod_xsendfile

#COPY . .

#RUN ["./manage.py", "collectstatic",  "--noinput"]

#EXPOSE 8000
EXPOSE 80

# Start the service
CMD ["-D", "FOREGROUND"]
ENTRYPOINT ["/usr/sbin/httpd"]

#CMD ./manage.py check; tail -f /dev/null

#CMD ./manage.py migrate --database "migration";\
#    uvicorn --host 0.0.0.0 --log-level error --use-colors --lifespan off ocean_composer.asgi:application
