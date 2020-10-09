FROM ubuntu:20.04

# comment this section out if you live outside firewall
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list && \
    apt-get clean && apt-get update
# end F@ck GFW section

RUN echo "Installing deluge, postgresql, etc.."
RUN apt-get -y --force-yes install deluged postgresql postgresql-contrib postgresql-client python libyaml-dev ffmpeg nodejs

USER root
RUN useradd -p albireo -m albireo

USER albireo
WORKDIR /home/albireo
#"Setting up deluge user..."
RUN mkdir .config
RUN mkdir .config/deluge
RUN touch .config/deluge/auth
RUN echo ":deluge:10" >> ~/.config/deluge/auth

ADD . /home/albireo/

#"Installing python dependencies..."
USER root
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip
RUN pip --no-cache-dir install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /home/albireo/requirements.txt --ignore-installed six
RUN chmod -R 777 /home/albireo

RUN echo "Setting up postgresql user and database..."
# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf

# And add ``listen_addresses`` to ``/etc/postgresql/9.3/main/postgresql.conf``
RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf

# Expose the PostgreSQL port
EXPOSE 5432

# http://askubuntu.com/questions/371832/how-can-run-sudo-commands-inside-another-user-or-grant-a-user-the-same-privileg
RUN usermod -a -G sudo postgres
USER postgres
RUN /etc/init.d/postgresql start && sleep 10 && psql -U postgres -d postgres -c "alter role postgres with password '123456';"
RUN /etc/init.d/postgresql start && sleep 10 && createdb -O postgres albireo


USER albireo
RUN echo "Setting up config file..."
RUN echo "Initialing database..."
USER root

EXPOSE 5000

# set up locale
RUN locale-gen "en_US.UTF-8"
ENV LC_ALL en_US.UTF-8

# Add VOLUMEs to allow backup of config, logs and databases
VOLUME  ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

CMD ["bash", "-c", "/etc/init.d/postgresql start && python /home/albireo/server.py"]
# /etc/init.d/postgresql start && python tools.py --db-init && python tools.py --user-add admin 1234 && python tools.py --user-promote admin 3
# docker volume create --name postgres
# docker run -it -v "`pwd`:/albireo" -v postgres:/var/lib/postgresql -p 5000:5000 albireo bash
