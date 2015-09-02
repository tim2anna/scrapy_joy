from dynamic_scraper.spiders.django_spider import DjangoSpider
from open_loan.models import LoanWebsite, Loan, LoanItem


class LoanSpider(DjangoSpider):
    
    name = 'loan_spider'

    def __init__(self, *args, **kwargs):
        self._set_ref_object(LoanWebsite, **kwargs)
        self.scraper = self.ref_object.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.scraper_runtime
        self.scraped_obj_class = Loan
        self.scraped_obj_item_class = LoanItem
        super(LoanSpider, self).__init__(self, *args, **kwargs)