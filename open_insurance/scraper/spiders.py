from dynamic_scraper.spiders.django_spider import DjangoSpider
from open_insurance.models import InsuranceWebsite, Insurance, InsuranceItem


class InsuranceSpider(DjangoSpider):
    
    name = 'insurance_spider'

    def __init__(self, *args, **kwargs):
        self._set_ref_object(InsuranceWebsite, **kwargs)
        self.scraper = self.ref_object.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.scraper_runtime
        self.scraped_obj_class = Insurance
        self.scraped_obj_item_class = InsuranceItem
        super(InsuranceSpider, self).__init__(self, *args, **kwargs)