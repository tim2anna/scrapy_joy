#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date, timedelta, datetime
from django.template import RequestContext
from django.shortcuts import render_to_response

from open_loan.models import Loan, LoanWebsite


def index(request):
    start_date = request.GET.get('start_date')
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    else:
        start_date = date.today() - timedelta(days=7)

    end_date = request.GET.get('end_date')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        end_date = date.today()

    for day in range((end_date-start_date).days):
        print day

    sites = LoanWebsite.objects.all()

    sites = dict([(site.id, {'loans': [], 'site': site, 'category': site.category}) for site in sites])

    loans = Loan.objects.filter(created__range=(start_date, end_date))
    for loan in loans:
        sites[loan.loan_website_id]['loans'].append(loan)

    sites = sites.values()

    return render_to_response('index.html', locals(), context_instance=RequestContext(request))
