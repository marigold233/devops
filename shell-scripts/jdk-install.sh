#!/usr/bin/env bash
set -e
install_file=jdk-8u221-linux-x64.tar.gz
install_dir=/usr/local
untar=$(tar xfv $install_file)
untar_dir=$(basename $(echo $untar | tr ' ' '\n' | head -1))
mv $untar_dir $install_dir

exec >> /etc/profile
export JAVA_HOME=$install_dir/$untar_dir
export JRE_HOME=\${JAVA_HOME}/jre
export CLASSPATH=.:\${JAVA_HOME}/lib:\${JRE_HOME}/lib:\$CLASSPATH
export JAVA_PATH=\${JAVA_HOME}/bin:\${JRE_HOME}/bin
export PATH=\$PATH:\${JAVA_PATH}
exec 1>&-

source /etc/profile
java -version

: '
export JAVA_HOME=/usr/local/jdk1.8.0_221
export JRE_HOME=${JAVA_HOME}/jre
export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib:$CLASSPATH
export JAVA_PATH=${JAVA_HOME}/bin:${JRE_HOME}/bin
export PATH=$PATH:${JAVA_PATH}
'
