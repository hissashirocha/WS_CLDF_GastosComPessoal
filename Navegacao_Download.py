# Web scraping de dados de gastos com pessoal da CLDF
# Autor: Luiz Hissashi da Rocha
# Data: 12/2017

# Plano de Execução

# 1 - Acessar link http://www.cl.df.gov.br/web/guest/quadro_demonstrativo_pessoal
# 2 - Ir para a última página disponível
#   2.1 - Buscar <a> com texto "Último"
# 3 - Procurar o último arquivo disponível pela div class "file-entry-list-description"
#   3.1 - Ir no banco e buscar o último dado inserido para testar se há arquivo novo
#   3.2 - Encontrada a div nova, buscar o <a> que a envolve e clicar no link
# 4 - Procurar <a> com id "_110_INSTANCE_seZ5_gezi" e fazer download da planilha XLSX
# 5 - Encontrar arquivo e carregá-lo usando Pandas
# 6 - Subir para o banco de dados

import sys
import time

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


# Define parâmetros de download do Firefox
profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2) # Não irá para a pasta Downloads
profile.set_preference("browser.download.manager.showWhenStarting", False) # Não exibe status do download
profile.set_preference("browser.download.dir", '/home/hissashi/Desktop/Python3/OSBrasilia/') # Local do download
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet") # Não pede permissão para download XLSX

binary = FirefoxBinary('/usr/bin/firefox', log_file=sys.stdout)
driver = webdriver.Firefox(firefox_binary=binary, firefox_profile=profile)

driver.get("http://www.cl.df.gov.br/web/guest/quadro_demonstrativo_pessoal")
driver.find_element_by_xpath("//*[contains(text(),'Último')]").click()
time.sleep(5)
driver.find_element_by_xpath("//*[contains(text(),'outubro/2017')]").click()
time.sleep(5)
driver.find_element_by_id("_110_INSTANCE_seZ5_gezi").click()

