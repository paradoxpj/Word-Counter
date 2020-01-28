from django.http import HttpResponse
from django.shortcuts import render

from bs4 import BeautifulSoup

import urllib3

import re

from .models import FinalData, UrlText


def home(request):
    return render(request, 'home.html')


def count(request):
    urltext = request.GET['text']
    try:
        p = UrlText.objects.get(urltext=urltext)
    except UrlText.DoesNotExist:
        p = UrlText(urltext=urltext)
        p.save()
        req = urllib3.PoolManager()
        res = req.request('GET', urltext)
        soup = BeautifulSoup(res.data, 'html.parser')
        data = soup.get_text()
        record = {}
        for word in data.split():
            if word in record:
                record[word]+=1
            else:
                record[word]=1
        sorted_data = sorted(record.items(), key = lambda kv:(kv[1],kv[0]), reverse=True)
        counter = 0
        file = open('commonwords.txt', 'r')
        string = file.read()
        file.close()
        for word in sorted_data:
            if word[0] in string.split():
                continue
            if re.match("^[A-Za-z]*$", word[0]):
                counter+=1
                q = FinalData(query=p, key=word[0], value=word[1])
                q.save()
            if counter==10:
                break
        found = False
    else:
        found = True

    query_set = FinalData.objects.filter(query=p).order_by('-value')

    context = {
        'query_set': query_set,
        'found': found,
    }

    return render(request, 'count.html', context)
