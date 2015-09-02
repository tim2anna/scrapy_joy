from dynamic_scraper.spiders.django_checker import DjangoChecker
from open_loan.models import Loan


class LoanChecker(DjangoChecker):
    
    name = 'loan_checker'
    
    def __init__(self, *args, **kwargs):
        self._set_ref_object(Loan, **kwargs)
        self.scraper = self.ref_object.loan_website.scraper
        self.scrape_url = self.ref_object.url
        self.scheduler_runtime = self.ref_object.checker_runtime
        super(LoanChecker, self).__init__(self, *args, **kwargs)