#docker run --rm --name alpine --log-driver=fluentd --log-opt fluentd-address=128.0.0.1:24224 alpine echo "hello world"
docker run -itd --name httpd --log-driver=fluentd -e TZ="Asia/Shanghai" --log-opt fluentd-address=127.0.0.1:24224 -p 81:80 httpd:latest
