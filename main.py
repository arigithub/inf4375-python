#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
__author__ = 'Ariane Pelletier PELA27549006'

from urllib import request
from jsonschema import validate
from io import StringIO
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
import json
import csv
import codecs

schema = {
    "properties" : {
        "FOURNISSEUR" : {"type" : "string"},
        "APPROBATEUR" : {"type" : "string"},
        "DESCRIPTION" : {"type" : "string"},
        "SERVICE" : {"type" : "string"},
        "ACTIVITÉ" : {"type" : "string"},
        "MONTANT" : {"type" : "number"},
        "PORTION À LA CHARGE DE L'AGGLO." : {"type" : "string"},
        "RÉPARTITION" : {"type" : "string"},
        "DIRECTION" : {"type" : "string"},
        "NO DE DOSSIER" : {"type" : "number"},
        "OBJET" : {"type" : "string"},
        "NO DÉCISION" : {"type" : "string"},
        "DATE SIGNATURE" : {"type" : "string"},
    },
}

def getFile(url, jsonFields):
    jsonResults=""
    telechargement = False
    try:
        telechargement = True
        response = request.urlopen(url)
    except request.URLError:
        print("Mauvaise Adresse pour telechargement de contrats.")
        telechargement = False
    except request.HTTPError:
        print("Erreure  de connexion")
        telechargement = False
    jsonResults = ""
    if telechargement:
        decodedResponse= response.read().decode('utf8')
        decodedReponseString = str(decodedResponse)
        responseReaderforReading = StringIO(decodedReponseString)
        reader = csv.DictReader(responseReaderforReading, jsonFields)
        validate(reader, schema)
        jsonResults = reader
    return jsonResults


if __name__ == '__main__':
    index = 0
    while 1:
        urlContratFonctionnaire = "http://donnees.ville.montreal.qc.ca/dataset/74efbfc7-b1bd-488f-be6f-ad122f1ebe8d/resource/a7c221f7-7472-4b01-9783-ed9e847ee8c1/download/contratsfonctionnaires.csv"
        urlContratExecutif      = "http://donnees.ville.montreal.qc.ca/dataset/505f2f9e-8cec-43f9-a83a-465717ef73a5/resource/87a6e535-3a6e-4964-91f5-836cd31099f7/download/contratscomiteexecutif.csv"
        urlContratMunicipal     = "http://donnees.ville.montreal.qc.ca/dataset/6df93670-af44-492e-a644-72643bf58bc0/resource/a6869244-1a4d-4080-9577-b73e09d95ed5/download/contratsconseilmunicipal.csv"
        urlContratAgglomeration = "http://donnees.ville.montreal.qc.ca/dataset/6df93670-af44-492e-a644-72643bf58bc0/resource/35e636c1-9f99-4adf-8898-67c2ea4f8c47/download/contratsconseilagglomeration.csv"

        champsContratFonctionnaire  = ("FOURNISSEUR","NO DE DOSSIER","DATE SIGNATURE","APPROBATEUR","DESCRIPTION","SERVICE","ACTIVITÉ","MONTANT","PORTION À LA CHARGE DE L'AGGLO.")
        champsContrat = ("FOURNISSEUR","RÉPARTITION","SERVICE","DIRECTION","NO DE DOSSIER","OBJET","NO DÉCISION","DATE SIGNATURE","MONTANT","APPROBATEUR","PORTION À LA CHARGE DE L'AGGLO.")

        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

        Fonctionnaires = getFile(urlContratFonctionnaire, champsContratFonctionnaire)
        for row in Fonctionnaires:
            itemCourant = json.dumps(row)
            es.index(index='contrats', doc_type='json', id=index, body=itemCourant, ignore=400, refresh=True)
            index=index+1

        Executif = getFile(urlContratExecutif, champsContrat)
        for row in Executif:
            itemCourant = json.dumps(row)
            es.index(index='contrats', doc_type='json', id=index, body=itemCourant, ignore=400, refresh=True)
            index=index+1

        Municipal = getFile(urlContratMunicipal, champsContrat)
        for row in Municipal:
            itemCourant = json.dumps(row)
            es.index(index='contrats', doc_type='json', id=index, body=itemCourant, ignore=400, refresh=True)
            index=index+1

        Agglomeration = getFile(urlContratAgglomeration, champsContrat)
        for row in Agglomeration:
            itemCourant = json.dumps(row)
            es.index(index='contrats', doc_type='json', id=index, body=itemCourant, ignore=400, refresh=True)
            index=index+1

        tempProchaineMiseAJour = datetime.now() + timedelta(hours=1)
        tempProchaineMiseAJour = int(tempProchaineMiseAJour.strftime('%H'))

        while 1:
            if datetime.now() > datetime.now().replace(hour=tempProchaineMiseAJour, minute=0):
                break




