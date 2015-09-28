# scrapy_joy


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
