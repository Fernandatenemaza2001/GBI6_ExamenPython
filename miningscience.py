from Bio import Entrez
import pandas as pd
import re
def download_pudmed(keyword):
    """Esta funcion busca una palabra clave en PubMed usando el paquete entrez de Biopython
    Para usarlo, se debe especificar download_pudmed(keyword)
    La funcion devuelve un diccionario con los IDs de las publicaciones, un conteo de cuantas publicaciones 
    y demas informacion en un diccionario"""
    Entrez.email = 'A.N.Other@example.com'
    result = Entrez.esearch(db='pubmed',
                            term=keyword, 
                            retmax = 1000, usehistory = 'y')
    data = Entrez.read(result)
    id_list = data['IdList']
    webenv = data['WebEnv']
    query_key = data['QueryKey']
    handle = Entrez.efetch(db = 'pubmed',
                           rettype = 'medline',
                           retmode = 'text', 
                           retmax = 1000, 
                           webenv = webenv, 
                           query_key = query_key)
    texto = handle.read() 
    texto = texto.split('\nPMID- ')
    years = []
    num_autors = []
    paises = []
    for articulo in texto[1:]:
        
        year = re.findall(r'DP\s\s-\s(\d\d\d\d)', articulo)[0]
        num_autor = len(re.findall(r'AU  - ', articulo))
        pais = re.findall(r'PL\s\s-\s(.*)', articulo)[0]
        if pais == 'England':
            pais = 'United Kingdom'
        years.append(year)
        paises.append(pais)
        num_autors.append(num_autor)
    pmtable = pd.DataFrame({'ID':id_list, 
                           'Year':years,
                           'Autores':num_autors,
                           'Pais':paises})
        
    return pmtable
def mining_pugs(tipo, tabla):
    '''Esta funcion extrae columnas especificas deacuerdo al tipo ingresado'''
    if tipo == 'PD':
        return tabla[['ID','Year']]
    elif tipo == 'AU':
        return tabla[['ID','Autores']]
    elif tipo == 'AD':
        return tabla[['Pais','Autores']]