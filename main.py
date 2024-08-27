
from selenium import webdriver
from selenium.webdriver.chrome import service
from webdriver_manager.opera import OperaDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
#from senhas import *

def verificar_estrategia(lista):
    for numero in lista[:4]:
        if numero >= 2:
            return False
    return True

webdriver_service = service.Service(OperaDriverManager().install())
webdriver_service.start()
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument('--disable-logging')
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--start-maximized")
options.add_argument('--disable-extensions')
options.add_argument('--disable-popup-blocking')
options.add_argument('--disable-gpu')
options.add_argument('--disable-infobars')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('w3c', True)

driver = webdriver.Remote(webdriver_service.service_url,options=options)

driver.maximize_window()

driver.get('https://estrelabet.com/ptb/bet/main')


sleep(10)
print('Atualizando site...')
driver.refresh()

print('Aguardando botão para aceitar cookies...')

WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH,'//*[@id="cookies-bottom-modal"]/div/div[1]/a'))
    )                                           

sleep(10)

driver.find_element(By.XPATH,'//*[@id="cookies-bottom-modal"]/div/div[1]/a').click()
sleep(3)

print('Botão clicado')
print('iniciando login...')
driver.find_element(By.XPATH,'//*[@id="username"]').send_keys(mario@tmpeml.com)
print('Usuário')
sleep(3)
driver.find_element(By.XPATH,'//*[@id="password-login"]').send_keys(Aviator102030!)
print('Senha')
sleep(3)
driver.find_element(By.XPATH,'//*[@id="header"]/div/div[1]/div/div[2]/app-login/form/div/div/div[2]/button').click()
print('botão de acesso clicado')
sleep(5)

print('Acessando aviator...')
driver.get('https://estrelabet.com/ptb/games/detail/casino/normal/7787')
print('Aguardando Frame...')

WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID,'gm-frm'))
    )
sleep(5)

iframe = driver.find_element(By.ID,'gm-frm')

driver.switch_to.frame(iframe)

sleep(5)

while True: 
    resultados =  [float(n) for n in driver.find_element(
        By.CLASS_NAME,'result-history').text.replace(
            'x','').split('\n')][:10]
    if verificar_estrategia(resultados):
        print(f'estrategia ok -> {resultados[:4]}')
    print(resultados)
    while True:
        verificacao =  [float(n) for n in driver.find_element(
            By.CLASS_NAME,'result-history').text.replace(
                'x','').split('\n')][:10]
        if verificacao != resultados:
            break







bot estrela_bet.py
Exibindo bot estrela_bet.py…
