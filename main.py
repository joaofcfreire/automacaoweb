from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pathlib import Path
import pandas as pd
import os, time

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

    nav.find_element(By. XPATH, '//*[@id="APjFqb"]').send_keys(produto)
    nav.find_element(By. XPATH, '//*[@id="APjFqb"]').send_keys(Keys.ENTER)

    #entrar na aba shopping

    while len(nav.find_elements(By.CLASS_NAME, 'hdtb-mitem')) < 1:
        time.sleep(1)
    time.sleep(1)

    abas = nav.find_elements(By.CLASS_NAME, 'hdtb-mitem')

    for aba in abas:
        if 'Shopping' in aba.text:
            aba.click()
            break

    #pegar as informações do produto

    while len(nav.find_elements(By.CLASS_NAME, 'i0X6df')) < 1:
        time.sleep(1)
    time.sleep(1)

    lista_produtos = nav.find_elements(By.CLASS_NAME, 'i0X6df')

    for produto in lista_produtos:
        preco = produto.find_element(By.CLASS_NAME, 'a8Pemb').text
        nome = produto.find_element(By.CLASS_NAME, 'tAxDx').text
        link = produto.find_element(By.CLASS_NAME, 'shntl').get_attribute('href')

google_shopping(nav, df_produtos)