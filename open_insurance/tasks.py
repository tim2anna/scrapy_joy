from celery.task import task

from dynamic_scraper.utils.task_utils import TaskUtils
from open_insurance.models import InsuranceWebsite, Insurance

@task()
def run_spiders():
    t = TaskUtils()
    t.run_spiders(InsuranceWebsite, 'scraper', 'scraper_runtime', 'loan_spider')
    
@task()
def run_checkers():
    t = TaskUtils()
    t.run_checkers(Insurance, 'loan_website__scraper', 'checker_runtime', 'loan_checker')