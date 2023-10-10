from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pathlib import Path
import pandas as pd
import os

#definir caminho do drive
caminho = os.getcwd()
caminho_driver = Path(caminho + r'\chromedriver.exe')

#criar navegador
service = webdriver.ChromeService(executable_path=caminho_driver)
nav = webdriver.Chrome(service=service)
nav.maximize_window()

#importar a base de dados
df_produtos = pd.read_excel('buscas.xlsx')
produto = 'iphone 12 64gb'
def google_shopping(nav, df):

    #entrar no google
    nav.get('https://www.google.com/')

    #pesquisar pelo produto
    nav.find_element(By. XPATH, '//*[@id="input"]').send_keys(produto)
    nav.find_element(By. XPATH, '//*[@id="input"]').send_keys(Keys.ENTER)

    #entrar na aba shopping
    #pegar as informações do produto

google_shopping(nav, df_produtos)