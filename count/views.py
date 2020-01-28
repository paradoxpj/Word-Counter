from django.http import HttpResponse
from django.shortcuts import render

from bs4 import BeautifulSoup

import requests

from models import FinalData


def home(request):
    return render(request, 'home.html')


def count(request):
    urltext = request.GET['text']
    try:
        p = UrlText.objects.get(urltext=urltext)
    except UrlText.DoesNotExist:
        p = UrlText(urltext=urltext)
        p.save()
        page = requests.get(urltext)
        soup = BeautifulSoup(page.text, 'html.parser')
        data = soup.get_text()
        record = {}
        for word in data.split():
            if word in record:
                record[word]+=1
            else:
                record[word]=1
        sorted_data = sorted(record.items(), key = lambda kv:(kv[1]), reverse=True)
        counter = 0
        for word in sorted_data:
            counter+=1
            if counter>10:
                break
            q = FinalData(query=p, key=word[0], value=word[1])
            q.save()

    context = {}
    query_set = FinalData.objects.filter(query=p).order_by('-value')

    for obj in query_set:
        context[obj.key] = obj.value

    return render(request, 'count.html', context)
