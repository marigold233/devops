FROM alpine:latest
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories 
RUN apk update \
    && apk add --no-cache --virtual .persistent-deps \
        curl \
        tcpdump \
        iproute2 \
        bind-tools \
        ethtool \
        busybox-extras \
        libressl \
        openssh-client \
        busybox
