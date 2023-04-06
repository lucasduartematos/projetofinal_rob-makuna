import os

import gspread
import requests
import pandas as pd
import telegram
from flask import Flask, request, render_template
from oauth2client.service_account import ServiceAccountCredentials
from tchan import ChannelScraper
from bs4 import BeautifulSoup


TELEGRAM_API_KEY = os.environ["TELEGRAM_API_KEY"]
TELEGRAM_ADMIN_ID = os.environ["TELEGRAM_ADMIN_ID"]
GOOGLE_SHEETS_CREDENTIALS = os.environ["GOOGLE_SHEETS_CREDENTIALS"]
with open("credenciais.json", mode="w") as arquivo:
  arquivo.write(GOOGLE_SHEETS_CREDENTIALS)
conta = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json")
api = gspread.authorize(conta)
planilha_gsheets = api.open_by_key("194kfy5ezKLuREJV7UO5mlEkZSYbUMaUQC2q5hi-XKb4")
sheet = planilha_gsheets.worksheet("robo_lucasduarte_bot")
app = Flask(__name__)

menu = """
<a href="/">Página inicial</a> | <a href="/noticias">Notícias Indígenas</a> | <a href="/sobre">Sobre</a> | <a href="/contato">Contato</a>
<br>
"""

@app.route("/")
def index():
  return menu + "Olá, seja bem-vindo(a) ao site de notícias indígenas do jornalista Lucas Duarte"

@app.route("/sobre")
def sobre():
  return menu + "Robô de notícias indígenas: A análise de dados é uma ferramenta poderosa para a compreensão de tendências e padrões em diversos setores da sociedade. No contexto dos povos indígenas, a análise de notícias diárias pode ajudar a identificar padrões de violação de direitos humanos e a mapear a presença dessas comunidades em diferentes regiões. Nesse sentido, a utilização do método de raspagem em Python pode ser uma ferramenta valiosa para coletar e analisar notícias diárias sobre indígenas."

@app.route("/contato")
def contato():
  return menu + "Mais informações: lucasduartematos@gmail.com"

@app.route("/noticias")
def noticias_indigenas():
    requisicao=requests.get('https://www.cnnbrasil.com.br/tudo-sobre/indigenas/')
    html=BeautifulSoup(requisicao.content)
    manchetes_indigenas=html.findAll('li',{'class':'home__list__item'})
    lista_noticias=[]
    for noticia in manchetes_indigenas:
        manchete=noticia.text
        link=noticia.find('a').get('href') 
        lista_noticias.append([manchete, link])
    df=pd.DataFrame(lista_noticias, columns=['Manchete','Link'])
    df = df.head(5) # seleciona as últimas 5 notícias
    df['Link'] = df['Link'].apply
