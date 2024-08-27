# main.py
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import json
import gc
import platform
import logging

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

class Main:
    def __init__(self):
        self.driver = None
        self.config = None
        self.ultimos = []
        self.carregar_valores()
    
    def carregar_valores(self):
        with open('config.json') as configFile:
            config = json.load(configFile)
            self.quantidade_rodadas = config['quantidade_rodadas']
            self.mutiplicador_ausente = config['mutiplicador_ausente']
    
    def start(self):         
        system = platform.system()
        if system == "Windows":
            subprocess.Popen('taskkill /IM chrome.exe /F', shell=True)
            sleep(1)
            subprocess.Popen(
                f'"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --log-level=3 --remote-debugging-port=9222 --disable-popup-blocking', shell=True)
        elif system == "Linux":
            subprocess.Popen('pkill chrome', shell=True)
            sleep(1)
            subprocess.Popen(
                f'/usr/bin/google-chrome --log-level=3 --remote-debugging-port=9222', shell=True)
        
        service = Service(ChromeDriverManager().install())
        self.options = webdriver.ChromeOptions()

        self.options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.options.add_argument("--start-maximized")
        self.options.add_argument("disable-infobars")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--no-sandbox")
        
        sleep(7)
        self.driver = webdriver.Chrome(service=service, options=self.options)
        self.driver.get('https://br.parimatch.com/')
        sleep(10)
        self.entrando_jogo()

    def entrando_jogo(self):        
        self.driver.get('https://br.parimatch.com/pt/casino/instant-games/game/spribe-br-aviator-inst')
        sleep(10)
        iframe = self.driver.find_elements(By.CSS_SELECTOR, 'iframe[title="Aviator"]')[0]
        self.driver.switch_to.frame(iframe)
        sleep(5)

    def ultimos_resultados(self):
        esperar = 0
        while True:
            results = self.driver.find_elements(By.CSS_SELECTOR,'div.payouts-block > app-bubble-multiplier')
            ultimos = []
            esperar+=1
            if esperar > 60: raise Exception('ultimos_resultados -> tempo esgotado')
            for result in results:
                try:
                    ultimos.append(float(result.text.replace('x', '').strip()))
                except: pass
            if len(ultimos): return ultimos

    def processar(self):
        if self.driver is None:
            self.start()
        return self.ultimos_resultados()

    def reset(self):
        if self.driver: self.driver.quit()
        sleep(1)
        del self.driver
        gc.collect()
        self.start()

if __name__ == '__main__':
    main = Main()
    main.start()
