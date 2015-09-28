from django.db.utils import IntegrityError
from scrapy import log
from scrapy.exceptions import DropItem
from dynamic_scraper.models import SchedulerRuntime

from open_loan.models import LoanScraper
from open_insurance.models import InsuranceWebsite

class DjangoWriterPipeline(object):
    
    def process_item(self, item, spider):
        try:
            if isinstance(spider.ref_object, LoanScraper):
                item['loan_scraper'] = spider.ref_object
            elif isinstance(spider.ref_object, InsuranceWebsite):
                item['insurance_website'] = spider.ref_object
            else:
                item['news_website'] = spider.ref_object
            
            checker_rt = SchedulerRuntime(runtime_type='C')
            checker_rt.save()
            item['checker_runtime'] = checker_rt
            
            item.save()
            spider.action_successful = True
            spider.log("Item saved.", log.INFO)
                
        except IntegrityError, e:
            spider.log(str(e), log.ERROR)
            raise DropItem("Missing attribute.")
                
        return item