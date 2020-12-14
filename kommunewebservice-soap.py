from __future__ import print_function
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport
from zeep.helpers import serialize_object

'''
Et enkelt script for å gjøre kall mot Kartverkets Kommunewebservice
Se full dokumentasjon på https://www.nd.matrikkel.no/innsynapi_v3/docs/index.html

NB: krever medlemskap i Norge digitalt og avtale om innsyn i matrikkelen

'''

import getpass

def get_user_and_password():
    user=input('Oppgi brukernavn: ')
    password=getpass.getpass('Oppgi passord: ')
    return user,password

def get_matrikkelcontext(sosi_kode):
    return {'sosiKode':sosi_kode,'matrikkelKlientversjon':'3.18.0.25'}


def get_kommuner(wsdl,binding):
    client=Client(wsdl, transport=Transport(session=session))
    service=client.bind(binding)
    response=service.findKommuner(
        matrikkelContext=get_matrikkelcontext(sosi_kode=23))
    kommuner=serialize_object(response)
    print(kommuner)
    return response

def parse_kommuneresponse(ws_reponse):
    kommuner=serialize_object(ws_reponse)
    kommuner = [i for i in kommuner if (i['gyldigTilDato'] is None)]
    return kommuner


wsdl='https://www.nd.matrikkel.no/innsynapi_v3/kommune/KommuneWebService?WSDL'
binding='KommuneWebService'

user,password=get_user_and_password()

session = Session()

session.auth = HTTPBasicAuth(user, password)

kommuner=get_kommuner(wsdl,binding)


