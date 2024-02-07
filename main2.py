# Importar as bibliotecas que vou utilizar para comparar a Selic com as ações

import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import seaborn as sns

# Criar a função que extrai do Banco Central os dados do retorno mensal da Selic.
def extracao_bcb(codigo, data_inicio, data_fim):
    url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json&dataInicial={}&dataFinal={}'.format(codigo, data_inicio, data_fim)
    df = pd.read_json(url)
    df.set_index('data', inplace=True)
    df.index = pd.to_datetime(df.index, dayfirst=True)
    df.columns = ['SELIC']
    df['SELIC'] = df['SELIC'] / 100
    return df

# Extrair os retornos mensais das ações escolhidas
dados = extracao_bcb(4390, '01/01/2010', '31/12/2023')
ativos = ['ITUB4', 'EMBR3', 'VALE3']
for i in ativos:
    try:
        dados[i] = yf.download(i + '.SA',
                               start='2010-01-01',
                               end='2023-12-31',
                               interval='1mo')['Adj Close'].pct_change()
    except Exception as e:
        print(f"Erro ao baixar os dados de {i}: {e}")

# Vou eliminar a primeira linha, buscando o produto acumulado de cada ativo. Então precisamos partir do 1.
dados = dados.iloc[1:]
dados = dados + 1
dados.head()

# Na primeira análise, busco a comparação do retorno acumulado
acumulado = dados.cumprod()

plt.figure(figsize=(10, 6))
sns.set_style('darkgrid')
sns.set_palette('mako')
plt.title('Ações vs Selic')
sns.lineplot(data=acumulado)
plt.show()

# Por fim, a correção do retorno acumulado de cada ativo

plt.figure(figsize=(8, 6))
plt.title('Correlação do Retorno Acumulado')
sns.heatmap(acumulado.corr(), annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.show()

# fim