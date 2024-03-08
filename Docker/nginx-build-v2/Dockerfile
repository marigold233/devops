FROM registry.cn-hangzhou.aliyuncs.com/yh-nb/centos-build:6.6
WORKDIR /
COPY . .
RUN chmod u+x /nginx-builder.sh xidel
ENTRYPOINT [ "/nginx-builder.sh" ]