from dynamic_scraper.spiders.django_checker import DjangoChecker
from open_insurance.models import Insurance


class InsuranceChecker(DjangoChecker):
    
    name = 'insurance_checker'
    
    def __init__(self, *args, **kwargs):
        self._set_ref_object(Insurance, **kwargs)
        self.scraper = self.ref_object.insurance_website.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.checker_runtime
        super(InsuranceChecker, self).__init__(self, *args, **kwargs)