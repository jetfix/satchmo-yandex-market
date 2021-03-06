# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from product.models import Category, Product

from satchmo_yandex_market.models import YandexMarketSite
from product.utils import find_best_auto_discount

def offers(request, site=None):
    u"""Представление для списка товаров Яндекса"""
    site = get_object_or_404(YandexMarketSite, site=Site.objects.get_current())
    categories = Category.objects.filter(is_active=True, site=site)
    products = Product.objects.filter(active=True,
                site = site,
                category__in = categories,
                productvariation__parent__isnull=True)
    sale = find_best_auto_discount(list(products))
    ctx = RequestContext(request, {
            'date' : datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            'categories' : categories,
            'offerproducts' : products,
            'site' : site,
            'sale' : sale,
        })
    return render_to_response('yandex_market/offers.html',
            context_instance=ctx)

