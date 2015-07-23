from django.shortcuts import render_to_response
from elasticsearch import Elasticsearch
from django.http import HttpResponse
import json

def index(request):
    return render_to_response('index.html')


def AjaxSearch(request, critere):
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    rechercheEffectue = es.search(index="contrats", q=critere)
    resultat = "["
    for hit in rechercheEffectue['hits']['hits']:
        item = json.dumps(hit['_source'])
        resultat = resultat + item + ","
    resultat += "{}]"
    return HttpResponse(resultat, content_type = "application/json")


