#!/usr/bin/python
# -*- coding: utf-8 -*-

import xadmin
from xadmin import views

from open_loan.models import Loan


class GlobalSetting(object):
    site_title = u'网贷爬虫'
    site_footer = 'www.kaisagroup.com'

    def get_site_menu(self):
         return (
             {'title': '借款管理', 'perm': self.get_model_perm(Loan, 'change'), 'menus':(
                 {'title': '借款',  'url': self.get_model_url(Loan, 'changelist')},
             )},
         )

xadmin.site.register(views.CommAdminView, GlobalSetting)
