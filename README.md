# scrapy_joy

## 部署

* 升级python2.7：
    
        wget https://www.python.org/ftp/python/2.7.9/Python-2.7.9.tgz
        tar -zxvf Python-2.7.9.tgz
        cd Python-2.7.9
        ./configure
        make
        make install
        mv /usr/bin/python /usr/bin/python2.6.6
        ln -s /usr/local/bin/python2.7 /usr/bin/python
        
* 安装easy_install/pip：
        
        wget https://bootstrap.pypa.io/ez_setup.py --no-check-certificate -O - | sudo python
        easy_install pip
        
* 安装uwsgi/virtualenv:
        
        pip install uwsgi
        pip install virtualenv
        
* 创建目录：/root/python-projects

        git clone https://github.com/wanghao524151/scrapy_joy.git
        virtualenv env_scraper
        source env_scraper/bin/activate
        cd scrapy_joy
        pip install -r requirements.txt
        python manage.py syncdb
        python manage.py runserver 0.0.0.0:8000
                
* pip install supervisor

        supervisord -c conf/supervisord.conf
                
        
* python升级导致yum命令无法使用的解决办法:
        
        vim /usr/bin/yum
        #!/usr/bin/python 改为：#!/usr/bin/python2.6
        
* pip install lxml==3.4.4无法安装:
        
        yum install libxslt-devel libxml2-devel
        
* celery root用户无法运行:

        增加环境变量：C_FORCE_ROOT=true
        
* uwsgi静态文件设置：
        
        copy静态文件到项目根目录
        
* 安装redis:

        yum install gcc-c++
        yum install -y tcl
        yum install wget
        
        wget http://download.redis.io/releases/redis-3.0.4.tar.gz
        tar -zxvf redis-3.0.4.tar.gz
        cd redis-3.0.4
        make
        make install
        mkdir -p /etc/redis
        cp redis.conf /etc/redis
        vim /etc/redis/redis.conf
        仅修改： daemonize yes （no-->yes）
        /usr/local/bin/redis-server /etc/redis/redis.conf
        ps -ef|grep redis


## 增加新平台流程

* add 1

* add 2


## 手动运行爬虫

* 激活python虚拟环境:

        source env_kaisa/bin/activate
        
* 进入项目根目录:

        cd cd scrapy_joy/
    
* 运行爬虫命令：id为LoanScraper的id:
    
        scrapy crawl loan_spider -a id=1 -a do_action=yes
