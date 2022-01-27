FROM centos:8
RUN yum update -y
RUN yum install git -y
RUN yum -q groupinstall "Development Tools" -y
RUN yum install cmake -y
RUN yum install curl-devel -y
RUN yum install epel-release -y 
RUN yum install pv -y
RUN yum -q install python3 -y
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install pandas requests docker 
RUN ln -sf /usr/bin/python3 /usr/local/bin/python3
WORKDIR /usr/src/local
RUN git clone -b develop-add-docker-backup-restore https://github.com/openfido/cli.git
WORKDIR /usr/src/local/cli
COPY ./install.sh ./install.sh
COPY ./build-aux ./build-aux
# COPY ./build-aux/setup-manual.sh ./build-aux/setup-manual.sh
# COPY ./build-aux/setup-Linux.sh ./build-aux/setup-Linux.sh
# COPY ./build-aux/setup-Linux-centos-8.sh ./build-aux/setup-Linux-centos-8.sh
RUN curl -sL https://raw.githubusercontent.com/openfido/cli/main/install.sh | bash