from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
import csv


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    with open(settings.BUS_STATION_CSV, 'r', encoding='utf-8') as f:
        data_list = []
        data = csv.reader(f)
        for line in data:
            data_dict = {'Name': line[1], 'Street': line[4], 'District': line[6]}
            data_list.append(data_dict)
        data_list.pop(0)
        page_number = int(request.GET.get("page", 1))
        paginator = Paginator(data_list, 10)
        page = paginator.get_page(page_number)
    context = {
        'bus_stations': page,
        'page': page,
    }
    return render(request, 'stations/index.html', context)