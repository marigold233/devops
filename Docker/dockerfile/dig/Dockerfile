FROM bitnami/minideb:bookworm
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list \
        && apt update \
        && apt install -y dnsutils \
        && rm -rf /var/lib/apt/lists/*