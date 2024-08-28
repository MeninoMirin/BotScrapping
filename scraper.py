from requests_html import HTMLSession

def verificar_estrategia(lista):
    for numero in lista[:4]:
        if numero >= 2:
            return False
    return True

def scrape_estrelabet():
    session = HTMLSession()
    
    # Acessando a página principal
    response = session.get('https://estrelabet.com/ptb/bet/main')
    response.html.render(sleep=5)  # Renderiza o JS

    # Aceitando cookies
    accept_cookies = response.html.find('#cookies-bottom-modal a', first=True)
    if accept_cookies:
        accept_cookies.click()
        response.html.render(sleep=2)

    # Simulação de login (se possível, dependendo das restrições do site)
    response = session.get('https://estrelabet.com/ptb/games/detail/casino/normal/7787')
    response.html.render(sleep=5)

    # Extraindo os resultados
    result_history = response.html.find('.result-history', first=True)
    if result_history:
        resultados = [float(n.replace('x', '')) for n in result_history.text.split('\n')[:10]]
        if verificar_estrategia(resultados):
            return f'Estratégia ok -> {resultados[:4]}'
        return resultados
    return 'Nenhum resultado encontrado'

if __name__ == "__main__":
    print(scrape_estrelabet())
