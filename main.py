from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from pathlib import Path
import pandas as pd
import win32com.client as win32
import os, time

def google_shopping(nav, produto, termos_banidos, preco_minimo, preco_maximo):

    # tratar valores
    lista_resultados_google = []
    termos_banidos = termos_banidos.lower()
    lista_banidos = termos_banidos.split(' ')
    lista_termos = produto.split(' ')
    preco_minimo = float(preco_minimo)
    preco_maximo = float(preco_maximo)

    # entrar no google
    nav.get('https://www.google.com/')

    # pesquisar pelo produto
    nav.find_element(By. XPATH, '//*[@id="APjFqb"]').send_keys(produto)
    nav.find_element(By. XPATH, '//*[@id="APjFqb"]').send_keys(Keys.ENTER)

    # entrar na aba shopping
    while len(nav.find_elements(By.CLASS_NAME, 'hdtb-mitem')) < 1:
        time.sleep(1)   # espera inteligente
    time.sleep(1)

    abas = nav.find_elements(By.CLASS_NAME, 'hdtb-mitem')
    for aba in abas:
        if 'Shopping' in aba.text:
            aba.click()
            break

    # pegar as informações do produto
    while len(nav.find_elements(By.CLASS_NAME, 'i0X6df')) < 1:
        time.sleep(1)  # espera inteligente
    time.sleep(1)

    lista_produtos = nav.find_elements(By.CLASS_NAME, 'i0X6df')

    for produto in lista_produtos:
        nome = produto.find_element(By.CLASS_NAME, 'tAxDx').text
        nome = nome.lower()

        # analisar se o nome do produto NÃO tem algum termo banido

        tem_ban = False
        for palavra in lista_banidos:
            if palavra in nome:
                tem_ban = True

        # analisar se o nome do produto TEM todos os termos da pesquisa

        tem_termos = True
        for palavra in lista_termos:
            if palavra not in nome:
                tem_termos = False

        # selecionar só os elementos que tem_ban = False e tem_termos = True
            if tem_ban == False and tem_termos == True:

                #tratando a variavel preco
                preco = produto.find_element(By.CLASS_NAME, 'a8Pemb').text
                preco = preco.replace('R$', '')
                preco = preco.replace(' ', '')
                preco = preco.replace('.', '')
                preco = preco.replace(',', '.')
                preco = float(preco)

                # verificar se o preco está entre o preçoo minimo e o preço máximo
                if preco_minimo <= preco <= preco_maximo:
                    child_link = produto.find_element(By. CLASS_NAME, 'bONr3b')
                    link = child_link.find_element(By.XPATH, '..').get_attribute('href')
                    lista_resultados_google.append((nome, preco, link))
    return lista_resultados_google
def buscape(nav, produto, termos_banidos, preco_minimo, preco_maximo):

    # tratar valores
    lista_resultados_buscape = []
    termos_banidos = termos_banidos.lower()
    lista_banidos = termos_banidos.split(' ')
    lista_termos = produto.split(' ')
    preco_minimo = float(preco_minimo)
    preco_maximo = float(preco_maximo)

    # entrar no buscape
    nav.get('https://www.buscape.com.br/')

    # pesquisar pelo produto
    nav.find_element(By.XPATH, '//*[@id="new-header"]/div[1]/div/div/div[3]/div/div/div[2]/div/div[1]/input').send_keys(produto)
    nav.find_element(By.XPATH, '//*[@id="new-header"]/div[1]/div/div/div[3]/div/div/div[2]/div/div[1]/input').send_keys(Keys.ENTER)


    # pegar as informações do produto
    while len(nav.find_elements(By.CLASS_NAME, 'SearchFilters_SearchFiltersWrapper__KbKHx')) < 1:
        time.sleep(1)  # espera inteligente
    time.sleep(1)

    lista_produtos = nav.find_elements(By. CLASS_NAME, 'ProductCard_ProductCard_Inner__tsD4M')

    for produto in lista_produtos:
        nome = produto.find_element(By. CLASS_NAME, 'ProductCard_ProductCard_NameWrapper__lOyZM').text
        nome = nome.lower()

        # analisar se o nome do produto NÃO tem algum termo banido

        tem_ban = False
        for palavra in lista_banidos:
            if palavra in nome:
                tem_ban = True

        # analisar se o nome do produto TEM todos os termos da pesquisa

        tem_termos = True
        for palavra in lista_termos:
            if palavra not in nome:
                tem_termos = False

            # selecionar só os elementos que tem_ban = False e tem_termos = True
            if tem_ban == False and tem_termos == True:
                # tratando a variavel preco
                preco = produto.find_element(By.CLASS_NAME, 'Text_MobileHeadingS__Zxam2').text
                preco = preco.replace('R$', '')
                preco = preco.replace(' ', '')
                preco = preco.replace('.', '')
                preco = preco.replace(',', '.')
                preco = float(preco)

                # verificar se o preco está entre o preçoo minimo e o preço máximo
                if preco_minimo <= preco <= preco_maximo:
                    link = produto.get_attribute("href")
                    lista_resultados_buscape.append((nome, preco, link))

    return lista_resultados_buscape

# definir caminho do drive
caminho = os.getcwd()
caminho_driver = Path(caminho + r'\chromedriver.exe')

# criar navegador
service = webdriver.ChromeService(executable_path=caminho_driver)
nav = webdriver.Chrome(service=service)
nav.maximize_window()

# importar a base de dados
df_produtos = pd.read_excel('buscas.xlsx')

# criando tabela de ofertas vazia (inicialmente)
tabela_ofertas = pd.DataFrame()

# percorrendo os produtos da base de dados
for linha in df_produtos.index:

    # incluindo variável para cada valor enquanto roda o for da base de dados
    produto = df_produtos.loc[linha, 'Nome']
    termos_banidos = df_produtos.loc[linha, 'Termos banidos']
    preco_minimo = df_produtos.loc[linha, 'Preço mínimo']
    preco_maximo = df_produtos.loc[linha, 'Preço máximo']

    colunas = ['Produto', 'Preço', 'Link']

    lista_google_shopping = google_shopping(nav, produto, termos_banidos, preco_minimo, preco_maximo)
    # criando a tabela do google shopping caso a lista não esteja vazia e adicionando na tabela de ofertas
    if lista_google_shopping:
        tabela_google_shopping = pd.DataFrame(lista_google_shopping, columns=colunas)
        tabela_ofertas = pd.concat([tabela_ofertas, tabela_google_shopping])

    lista_buscape = buscape(nav, produto, termos_banidos, preco_minimo, preco_maximo)
    # criando a tabela do buscape caso a lista não esteja vazia e adicionando na tabela de ofertas
    if lista_buscape:
        tabela_buscape = pd.DataFrame(lista_buscape, columns=colunas)
        tabela_ofertas = pd.concat([tabela_ofertas, tabela_buscape])

# exportando a tabela de ofertas para excel
tabela_ofertas.drop_duplicates()
tabela_ofertas.to_excel('Ofertas Encontradas.xlsx', index=False)

# enviando e-mail com o resultado da tabela de ofertas
if len(tabela_ofertas) > 0:
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = 'joaofcfreire@gmail.com'
    mail.Subject = 'Produtos encontrados na faixa preço desejada'
    mail.HTMLBody = f"""
    <h2>Prezados,</h2>
    <p>Encontramos alguns produtos em oferta dentro da faixa de preço desejada</p>
    {tabela_ofertas.to_html(index=False)}
    <p>Atenciosamente,</p>
    <p>João Freire</p>
    """
    mail.Send()

nav.quit()

