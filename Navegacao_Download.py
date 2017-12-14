'''
Web scraping de dados de gastos com pessoal da Câmara Legislativa do Distrito Federal
Observatório Social de Brasília
Data: Dez/2017

Autores:
    + Luiz Hissashi da Rocha - hissashirocha@gmail.com

+++++++++++++++++++++++++
PRÉ-REQUISITOS MÍNIMOS
+ Linux Ubuntu (Debian)
+ Firefox 57.0.1
+ Geckodriver 0.19.0 (deve ser colocado na pasta /usr/local/bin ou em uma pasta que esteja na variável PATH do Linux)
+ Python 3.X
+ Bibliotecas
    - Selenium 3.6.0
    - Pandas 0.21.0
+++++++++++++++++++++++++
'''

import sys
import time
import os
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import pandas as pd

pasta_downloads = '/home/hissashi/Desktop/Python3/OSBrasilia/WS_CLDF_GastosComPessoal/'

# Define parâmetros de download do Firefox
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2) # Não irá para a pasta Downloads
profile.set_preference("browser.download.manager.showWhenStarting", False) # Não exibe status do download
profile.set_preference("browser.download.dir", pasta_downloads) # Local do download
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") # Não pede permissão para o tipo de arquivo especificado

# Faz com que o Firefox rode no mode headless (sem ser exibido)
# Para visualizar a navegação automatizada, basta comentar essa linha
os.environ['MOZ_HEADLESS'] = '1'

#Identificação do arquivo binário do Firefox
binary = FirefoxBinary('/usr/bin/firefox', log_file=sys.stdout)

try:
    driver = webdriver.Firefox(firefox_binary=binary, firefox_profile=profile)
    # Abre o primeiro link para iniciar a navegação
    driver.get("http://www.cl.df.gov.br/web/guest/quadro_demonstrativo_pessoal")

    # Busca o elemento HTML que seu texto seja igual a 'Último'
    driver.find_element_by_xpath("//*[contains(text(),'Último')]").click()
    print("Foi para a útlima página")
    time.sleep(5) # Aguardando 5 segundos para o carregamento da próxima página

    driver.find_element_by_xpath("//*[contains(text(),'outubro/2017')]").click()
    print("Clicou no arquivo de outubro/2017")
    time.sleep(5)

    driver.find_element_by_id("_110_INSTANCE_seZ5_gezi").click()
    print("Fazendo download ...")
    time.sleep(5)

    #Lista todos os arquivos na pasta
    arquivos = os.listdir(pasta_downloads)

    #Lista todos os arquivos xlsx
    arquivos_xlsx = [f for f in arquivos if f[-4:]=='xlsx']

    dados = pd.DataFrame()

    for p in arquivos_xlsx:
        print("Carregando arquivo: ",p)
        dado = pd.read_excel(p,sheet_name=0) # Lê os dados da primeira aba
        dados = dados.append(dado)

    print("CAMPOS: ")
    print(dados.head()) # Apresenta 5 linhas da planilha com os nomes das colunas

    print("ESTATÍSTICAS: ")
    print(dados.describe()) # Apresenta as estatítisticas básicas de cada coluna

finally:
    driver.quit()

