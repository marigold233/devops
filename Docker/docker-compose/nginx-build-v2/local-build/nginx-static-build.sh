#!/usr/bin/env bash

SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
# 不指定参数默认使用最新的版本进行编译
# ZLIB_VERSION=""; PCRE_VERSION=""; NGINX_VERSION=""; 
# 安装路径。必须指定
NGINX_PREFIX="/data/nginx"

_wget() {
        local unzip_dir=$1
        local download_link=$2
        [ -d $unzip_dir ] || mkdir $unzip_dir
        wget --no-check-certificate -qO- $download_link | tar xzf -  --strip-components=1 -C $unzip_dir
}

zlib_download() {
    zlib_url="http://zlib.net/fossils/"
    all_version=$(./xidel -s $zlib_url  --extract '/html/body/table/tbody/tr[*]/td[2]/a' | grep -vE "Parent|OBSOLETE")
    if [[ "$ZLIB_VERSION" ]]; then
        ret=$(echo "$all_version" | xargs -n1 2>/dev/null| grep -w "$ZLIB_VERSION" | head -1)
        if [[ "$ret" ]]; then
            echo "$ret downloading..."
            _wget zlib "${zlib_url}${ret}"
        else
            echo "zlib version:$ZLIB_VERSION not found."
            exit 1
        fi
    else
        latest_version=$(echo "$all_version" | xargs -n1 2>/dev/null| tail -1)
        echo "$latest_version downloading..."
        _wget zlib "${zlib_url}${latest_version}"
    fi
}

pcre_download(){
    pcre_url="https://sourceforge.net/projects/pcre/files/pcre/"
    all_version=$(./xidel -s $pcre_url  --extract '//*[@id="files_list"]/tbody/tr/@title')
    if [[ "$PCRE_VERSION" ]]; then
        ret=$(echo "$all_version" | xargs -n1 2>/dev/null| grep -w "$PCRE_VERSION")
        if [[ "$ret" ]]; then
            echo "pcre-${ret}.tar.gz downloading..."
            _wget pcre "${pcre_url}${PCRE_VERSION}/pcre-${ret}.tar.gz"
        else
            echo "pcre version:$PCRE_VERSION not found."
            exit 1
        fi
    else
        new_pcre_version=$(echo "$all_version" | xargs -n1 2>/dev/null| head -1)
        echo "pcre-${new_pcre_version}.tar.gz downloading..."
        _wget pcre "${pcre_url}${new_pcre_version}/pcre-${new_pcre_version}.tar.gz"
    fi
}

openssl_download(){
    new_openssl_url="https://mirrors.cloud.tencent.com/openssl/source/"
    old_openssl_url="https://mirrors.cloud.tencent.com/openssl/source/old/"
    if [[ "$OPENSSL_VERSION" ]]; then
        eval $(./xidel -s $new_openssl_url --xpath '//a/@href' --output-format bash)
        for f in ${result[@]}; do
                download_link=$(echo $f | grep -v "beta" | grep "gz$" | xargs -i echo ${new_openssl_url}{})
                ret=$(echo $download_link | grep $OPENSSL_VERSION)
                if [[ $ret ]]; then
                     echo "openssl-${OPENSSL_VERSION}.tar.gz downloading..."
                     _wget openssl $ret
                    return 0
                fi
         done

        eval $(./xidel -s $old_openssl_url  --xpath 'old_version:=//a/@href' --output-format bash)
        unset old_version[0]
        for p in ${old_version[@]}; do
            page=$(echo $p | xargs -i echo ${old_openssl_url}{})
            eval $(./xidel -s "$page" --xpath 'page_ret:=/html/body/pre/a/@href' --output-format bash)
            for f in ${page_ret[@]}; do
                download_link=$(echo $f | grep -v "beta" | grep "gz$" | xargs -i echo ${old_openssl_url}${p}${f})
                ret=$(echo $download_link | grep $OPENSSL_VERSION)
                if [[ $ret ]]; then
                     echo "openssl-${OPENSSL_VERSION}.tar.gz downloading..."
                        _wget openssl $ret
                        return 0
                fi
            done
            unset page_ret
         done
        echo "openssl version:$OPENSSL_VERSION not found."
        exit 1
    else
        latest_version=$( ./xidel -s $new_openssl_url --xpath '//a/@href[5]')
        echo "${latest_version} downloading..."
        _wget openssl ${new_openssl_url}$latest_version
     fi

}

nginx_download() {
        nginx_url="https://repo.huaweicloud.com/nginx/"
        packages=$(./xidel -s $nginx_url  --xpath '//a/@href' | sort -t '.' -k 2 -rn  | grep "gz$")
        if [[ "$NGINX_VERSION" ]]; then
                for f in ${packages[@]}; do
                        download_link=${nginx_url}${f}
                        ret=$(echo "$download_link" | grep -w "$NGINX_VERSION")
                        if [[ "$ret" ]]; then
                                echo "$f downloading..."
                                 _wget nginx $download_link
                                return 0
                        fi
                done
                echo "nginx version:$NGINX_VERSION not found."
                exit 1
        else
                latest_version=$(echo $packages | xargs -n1 2>/dev/null| head -1)
                download_link=${nginx_url}${latest_version}
                echo "$latest_version downloading..."
                _wget nginx $download_link
        fi
}

main() {
        {
                : ${NGINX_PREFIX:?}
                zlib_download
                pcre_download
                openssl_download
                nginx_download
                cd nginx
		./configure \
                        --prefix=${NGINX_PREFIX} \
                        --with-pcre=../pcre \
                        --with-zlib=../zlib \
                        --with-openssl=../openssl \
                        --with-http_ssl_module \
                        --with-http_stub_status_module \
                        --with-http_gzip_static_module \
                        --with-http_realip_module \
                        --with-http_sub_module \
                        --with-stream \
			--with-ld-opt="-static" \
			--with-cc-opt="-O2 -static -static-libgcc" \
			--with-cpu-opt=generic

                proc=$((`grep -c ^processor /proc/cpuinfo` - 1))
                make -j${proc}
                make install
                tar -zcf "$SCRIPT_DIR/nginx-bin.tar.gz" -C "$(dirname $NGINX_PREFIX)" "$(basename $NGINX_PREFIX)"
        } >&2
                [[ $STDOUT ]] && cat "nginx-bin.tar.gz"
}

main
