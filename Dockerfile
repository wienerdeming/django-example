FROM centos

ENV PROJECT_NAME my_project_name
ENV PROJECT_PATH /var/www/$PROJECT_NAME

##############################
# Install dependency
##############################
RUN yum install -y gcc make zlib-devel openssl-devel \
                   xz-devel groupinstall development \
                   yum-utils wget


##############################
# Install Python
##############################
RUN wget --progress=dot:mega https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tar.xz

RUN tar -xvvf Python-3.6.1.tar.xz > /dev/null
RUN cd Python-3.6.1 && ./configure && make && make install

##############################
# Install gosu
##############################
ENV GOSU_VERSION 1.10
RUN set -ex; \
	\
	yum -y install epel-release; \
	yum -y install wget dpkg; \
	\
	dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"; \
	wget -O /usr/bin/gosu "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch"; \
	wget -O /tmp/gosu.asc "https://github.com/tianon/gosu/releases/download/$GOSU_VERSION/gosu-$dpkgArch.asc"; \
	\
# verify the signature
	export GNUPGHOME="$(mktemp -d)"; \
	gpg --keyserver ha.pool.sks-keyservers.net --recv-keys B42F6819007F00F88E364FD4036A9C25BF357DD4; \
	gpg --batch --verify /tmp/gosu.asc /usr/bin/gosu; \
	rm -r "$GNUPGHOME" /tmp/gosu.asc; \
	\
	chmod +x /usr/bin/gosu; \
# verify that the binary works
	gosu nobody true; \
	\
	yum -y remove wget dpkg; \
	yum clean all

######################################
# Setting Project
######################################
RUN mkdir -p $PROJECT_PATH

# Cd to working directory
WORKDIR $PROJECT_PATH

# Copy requirements for catch
ADD ./requirements.txt $PROJECT_PATH

# Create virtualenv
RUN pip3 install virtualenv

# Create new user for run app
RUN useradd -u 1000 app

# Install dependency
RUN virtualenv .venv
RUN source .venv/bin/activate && pip3 install -r requirements.txt

# Copy project files
COPY --chown=app . $PROJECT_PATH

VOLUME $PROJECT_PATH/media
VOLUME $PROJECT_PATH/static

# Permission project directory
RUN chmod -R 775 $PROJECT_PATH

# Copy entrypoint script to root directory
COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
