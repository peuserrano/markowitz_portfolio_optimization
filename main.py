import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
from scipy.optimize import minimize
import matplotlib.ticker as mtick

class PortfolioOptimization:
    def __init__(self, lista_acoes, inicio, final):
        self.lista_acoes = lista_acoes
        self.inicio = inicio
        self.final = final
        self.precos = self._baixar_precos()
        self.indice_do_sharpe_maximo = None
        self.tabela_pesos = None

    def _baixar_precos(self):
        lista_acoes = [acao + ".SA" for acao in self.lista_acoes]
        return yf.download(self.lista_acoes, self.inicio, self.final)['Adj Close']

    def calcular_retornos(self):
        retornos = self.precos.pct_change().apply(lambda x: np.log(1 + x)).dropna()
        return retornos

    def calcular_fronteira_eficiente(self, numero_carteiras=100000):
        retornos = self.calcular_retornos()
        media_retornos = retornos.mean()
        matriz_cov = retornos.cov()

        vetor_retornos_esperados = np.zeros(numero_carteiras)
        vetor_volatilidades_esperadas = np.zeros(numero_carteiras)
        vetor_sharpe = np.zeros(numero_carteiras)
        tabela_pesos = np.zeros((numero_carteiras, len(self.lista_acoes)))

        for k in range(numero_carteiras):
            pesos = np.random.random(len(self.lista_acoes))
            pesos = pesos / np.sum(pesos)
            tabela_pesos[k, :] = pesos

            vetor_retornos_esperados[k] = np.sum(media_retornos * pesos * 252)
            vetor_volatilidades_esperadas[k] = np.sqrt(np.dot(pesos.T, np.dot(matriz_cov * 252, pesos)))

            vetor_sharpe[k] = vetor_retornos_esperados[k] / vetor_volatilidades_esperadas[k]

        self.indice_do_sharpe_maximo = vetor_sharpe.argmax()
        self.tabela_pesos = tabela_pesos

        tabela_retornos_esperados_arit = np.exp(vetor_retornos_esperados) - 1

        eixo_y_fronteira_eficiente = np.linspace(tabela_retornos_esperados_arit.min(),
                                                 tabela_retornos_esperados_arit.max(), 50)

        def pegando_retorno(peso_teste):
            peso_teste = np.array(peso_teste)
            retorno = np.sum(media_retornos * peso_teste) * 252
            retorno = np.exp(retorno) - 1
            return retorno

        def checando_soma_pesos(peso_teste):
            return np.sum(peso_teste) - 1

        def pegando_vol(peso_teste):
            peso_teste = np.array(peso_teste)
            vol = np.sqrt(np.dot(peso_teste.T, np.dot(matriz_cov * 252, peso_teste)))
            return vol

        peso_inicial = [1 / len(self.lista_acoes)] * len(self.lista_acoes)
        limites = tuple([(0, 1) for _ in self.lista_acoes])
        eixo_x_fronteira_eficiente = []

        for retorno_possivel in eixo_y_fronteira_eficiente:
            restricoes = ({'type': 'eq', 'fun': checando_soma_pesos},
                          {'type': 'eq', 'fun': lambda w: pegando_retorno(w) - retorno_possivel})

            result = minimize(pegando_vol, peso_inicial, method='SLSQP', bounds=limites,
                              constraints=restricoes)
            eixo_x_fronteira_eficiente.append(result['fun'])

        return vetor_volatilidades_esperadas, tabela_retornos_esperados_arit, vetor_sharpe, \
               eixo_x_fronteira_eficiente, eixo_y_fronteira_eficiente


# Uso da classe
inicio = dt.date(2015, 1, 1)
final = dt.date(2022, 12, 31)
lista_acoes = ["AAPL", "NKE", "GOOGL", "AMZN"]

portifolio = PortfolioOptimization(lista_acoes, inicio, final)
volatilidades, retornos, sharpe, eixo_x, eixo_y = portifolio.calcular_fronteira_eficiente()

# Plotagem dos resultados
fig, ax = plt.subplots()
ax.scatter(volatilidades, retornos, c=sharpe)
ax.scatter(volatilidades[np.argmax(sharpe)], retornos[np.argmax(sharpe)], c="red")
ax.plot(eixo_x, eixo_y)
ax.set_xlabel("Volatilidade esperada", labelpad = 12)
ax.set_ylabel("Retorno esperado", labelpad = 12)
ax.set_title(f'Portfólio Ótimo (Markowitz) - {inicio} a {final}')
ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax.xaxis.set_major_formatter(mtick.PercentFormatter(1.0))
plt.show()

# Após a otimização do portfólio
pesos_optimizados = portifolio.tabela_pesos[portifolio.indice_do_sharpe_maximo]

df_pesos_otimos = pd.DataFrame({'Ação':[acao for acao in lista_acoes],
                         'Peso no Portfólio':[peso for peso in pesos_optimizados]})

df_pesos_otimos

#for acao, peso in zip(lista_acoes, pesos_optimizados):
    #print(f"Ação: {acao}, Peso no portfólio: {peso:.4f}")


