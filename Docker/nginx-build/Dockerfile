FROM centos:6.6
WORKDIR /
ADD ./CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo
ADD https://ghproxy.com/https://github.com/benibela/xidel/releases/download/Xidel_0.9.8/xidel-0.9.8.linux64.tar.gz .
RUN yum install -y gcc gcc-c++ make tar perl wget \
    && yum clean all
COPY nginx-builder.sh ./nginx-builder.sh
RUN tar xfv xidel-0.9.8.linux64.tar.gz \
        && chmod u+x /nginx-builder.sh xidel
ENTRYPOINT [ "/nginx-builder.sh" ]
