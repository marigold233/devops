ARG OS_VERSION="6.6"
FROM centos:${OS_VERSION}}
WORKDIR /
COPY CentOS-Base.repo /etc/yum.repos.d/
RUN yum install -y gcc gcc-c++ make tar perl wget \
        && yum clean all
COPY . .
RUN chmod u+x /nginx-builder.sh xidel
ENTRYPOINT [ "/nginx-builder.sh" ]