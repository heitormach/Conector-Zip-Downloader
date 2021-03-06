import requests
import json
import csv
import base64
import sys


def downloadZipConector(i, cnpj):
    parametersDownload = {'cnpj': cnpj,
                          'docKey': i['docKey'], 'id': i['id'], 'typeFile': 'zip'}
    # print(parametersDownload)
    responseDownload = requests.get(
        'https://backend.prod.dfeconnector.thomsonreuters.com/api/log/download', parametersDownload)
    if responseDownload.status_code < 400:
        # print(responseDownd.content)
        saveZip(responseDownload.content, i['docKey'] + '.Oracle.Return.zip')


def saveZip(byte, name):
    f = open('arquivos/' + name, "wb")
    f.write(byte)
    f.close()


def __main__(cnpj=sys.argv[1]):
    last_id = 0
    last_doc = 0
    with open('rps.txt', 'r') as f:
        first_column = [row[0] for row in csv.reader(f, delimiter=';')]

    for j in first_column[0:]:
        query = {'cnpj': cnpj, 'docKey': j,
                 'pageNumber': '1', 'pageSize': '10'}
        response = requests.get(
            "https://backend.prod.dfeconnector.thomsonreuters.com/api/log", params=query)
        result = response.json()

        for i in result['content']:
            if i['docKey'][29:34] == j and str(last_doc) != i['docKey']:
                print('Inicio Last Doc: ' + str(last_doc), 'Doc Key: ' +
                      i['docKey'], 'Last ID: ' + str(last_id), 'ID: ' + str(i['id']))
                downloadZipConector(i, cnpj)
            if i['docKey'][29:34] == j and str(last_doc) == i['docKey'] and last_id < i['id']:
                print('Repetido Last Doc: ' + str(last_doc), 'Doc Key: ' +
                      i['docKey'], 'Last ID: ' + str(last_id), 'ID: ' + str(i['id']))
                downloadZipConector(i, cnpj)
            last_doc = i['docKey']
            last_id = i['id']


if __main__():
    __main__(sys.argv)
