from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import subprocess
import platform
import logging
import json
import gc


logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

class Main:

    def carregar_valores(self):
        self.ultimos = []
        with open('config.json') as configFile:
            config = json.load(configFile)
            self.quantidade_rodadas = config['quantidade_rodadas']
            self.mutiplicador_ausente = config['mutiplicador_ausente']
            self.telegram.start(config['grupos'])
        
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
        
        service = ChromeService(executable_path=ChromeDriverManager().install())
        self.options = webdriver.ChromeOptions()

        self.options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        self.options.add_argument("--start-maximized")
        self.options.add_argument("disable-infobars")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--no-sandbox")
        
        sleep(7)
        self.driver = webdriver.Chrome(service=service, options=self.options)
        self.config = json.load(open('config.json'))
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
            results = self.driver.find_elements(By.CSS_SELECTOR, 'div.payouts-block > app-bubble-multiplier')
            ultimos = []
            esperar += 1
            if esperar > 60: raise Exception('ultimos_resultados -> tempo esgotado')
            for result in results:
                try:
                    ultimos.append(float(result.text.replace('x', '').strip()))
                except Exception as e:
                    logging.error(f"Erro ao processar resultado: {e}")
            if len(ultimos): return ultimos

    def buscar_alerta(self):
        if not self.ultimos: return True  # Se `self.ultimos` estiver vazio, sempre alerta
        for numero in self.ultimos:
            if numero >= self.mutiplicador_ausente: return False
        return True

    def reset(self):
        if self.driver: self.driver.quit()
        sleep(1)
        del self.driver
        gc.collect()
        self.start()

    def main(self):
        self.carregar_valores()
        self.start()
        while True:
            try:
                ultimos = self.ultimos_resultados()

                if self.ultimos[0:10] == ultimos[0:10]:
                    continue

                if not self.ultimos: self.ultimos = [ultimo for ultimo in ultimos]
                else: self.ultimos.insert(0, ultimos[0])

                while len(self.ultimos) > self.quantidade_rodadas:
                    self.ultimos.pop()

                if self.buscar_alerta():
                    self.telegram.send_alert(self.quantidade_rodadas, self.mutiplicador_ausente)
                    self.ultimos = self.ultimos[0]
                               
            except Exception as error:
                logging.error(f"Erro: {error}", exc_info=True)
                self.reset()

if __name__ == '__main__':
    main = Main()
    main.main()
