FROM    centos
RUN     yum install -y epel-release && yum clean all
RUN     yum -y update && yum clean all
RUN     yum -y install supervisor cronie yum-cron && yum clean all
ADD     supervisord.conf /etc/supervisord.conf
ADD     crond.ini /etc/supervisord.d/crond.ini
RUN     chmod 600 /etc/supervisord.conf /etc/supervisord.d/*.ini
RUN     mkdir -p /var/lock/subsys
RUN     touch /var/lock/subsys/yum-cron
RUN     sed -i 's/apply_updates = no/apply_updates = yes/' /etc/yum/yum-cron.conf
RUN     sed -i 's/apply_updates = no/apply_updates = yes/' /etc/yum/yum-cron-hourly.conf
ADD     bashrc.sh /
RUN     cat /bashrc.sh >> /root/.bashrc
RUN     rm /bashrc.sh
ADD     get-pip.py /
RUN     mkdir /build
ADD     gmp-6.0.0a.tar.bz2 /build
RUN     yum -y update
RUN     yum -y install epel-release
RUN     yum install -y gcc-c++
RUN     yum install -y git
RUN     yum install -y make
RUN     yum install -y net-tools
RUN     yum install -y wget
RUN     yum install -y vim
RUN     yum install -y procps
RUN     yum install -y mlocate
RUN     yum install -y links
RUN     yum install -y zlib-devel.x86_64
RUN     yum install -y python-devel
RUN     yum install -y libffi-devel
RUN     python /get-pip.py; rm -f /get-pip.*
RUN     yum upgrade -y
RUN     yum install -y pyOpenSSL.x86_64
RUN     pip install multiprocessing
RUN     pip install gevent
RUN     pip install redis
RUN     pip install msgpack-python
RUN     pip install ujson
RUN     pip install inflection
RUN     pip install python-cjson
RUN     pip install celery
RUN     pip install bcrypt;
RUN     pip install Pygments
RUN     pip install cython git+git://github.com/surfly/gevent.git#egg=gevent
WORKDIR /build/gmp-6.0.0
RUN     yum install -y m4
RUN     ./configure
RUN     make install;
RUN     pip install pycrypto;
RUN     yum install -y tar;
RUN     yum install -y pigz;
RUN     easy_install -U distribute
RUN     pip install autopep8
RUN     pip install docopt
RUN     pip install ecdsa
RUN     pip install future
RUN     pip install gcloud
RUN     pip install gitdb
RUN     pip install GitPython
RUN     pip install httplib2
RUN     pip install ipython
RUN     pip install oauth2client
RUN     pip install paramiko
RUN     pip install pbr
RUN     pip install pep8
RUN     pip install protobuf
RUN     pip install psutil
RUN     pip install pyasn1
RUN     pip install pyasn1-modules
RUN     pip install python-Levenshtein
RUN     pip install python-vagrant
RUN     pip install pytz
RUN     yum install -y libyaml
RUN     yum install -y libyaml-devel
RUN     pip install PyYAML
RUN     pip install requests
RUN     pip install rsa
RUN     pip install schema
RUN     pip install smmap
RUN     pip install ujson
RUN     rm -Rf /build;
RUN     yum -y clean all;
RUN     echo nameserver 8.8.8.8 > /etc/resolv.conf
RUN     updatedb;
RUN     yum remove -y kernel-debug-devel;
RUN     yum remove -y kernel-headers;
RUN     yum -y clean all;
RUN     rpm -qa --queryformat '%10{size} - %-25{name} \t %{version}\n' | sort -n > /installed.txt
RUN     yum -y remove gcc gcc-c++ cmake libyaml-devel gmp-devel binutils-devel boost-devel libmcrypt-devel libmemcached-devel jemalloc-devel libevent-devel sqlite-devel libxslt-devel libicu-devel tbb-devel libzip-devel mysql-devel bzip2-devel openldap-devel readline-devel elfutils-libelf-devel libcap-devel libyaml-devel libedit-devel lz4-devel libvpx-devel unixODBC-devel gmp-devel libpng-devel ImageMagick-devel expat-devel openssl-devel patch make libtool libidn-devel
RUN     rm -Rf /build
WORKDIR /
ADD

