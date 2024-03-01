import pandas as pd
import yfinance as yf
# from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

dados_bancarios = yf.download(['ITUB4.SA','BBAS3.SA','SANB4.SA','BBDC4.SA','^BVSP'],start = "2010-01-01", end = '2022-04-30')["Adj Close"]
# dados_bancarios = pdr.get_data_yahoo(['ITUB4.SA','BBAS3.SA','SANB4.SA','BBDC4.SA','^BVSP'],start = "2010-01-01", end = '2022-04-30')["Adj Close"]

lucro_bancos = pd.read_excel("C:/Users/heito/Documents/lucro_bancos_2010_2022.xlsx",index_col = "data")
dados_mercado = dados_bancarios['^BVSP']
#ibovespa = mercado
banco_itau = dados_bancarios['ITUB4.SA']
banco_do_brasil = dados_bancarios['BBAS3.SA']
banco_santander = dados_bancarios['SANB4.SA']
banco_bradesco = dados_bancarios['BBDC4.SA']

def retorno(lista):
    #CALCULO DA COTAÇÃO
    #RETORNO = COTAÇÃO FINAL/ COTAÇÃO INICIAL - 1
    retorno = (lista[-1]/lista[0]) - 1
    return retorno

retorno_itau = retorno(lista = banco_itau)
retorno_mercado = retorno(lista = dados_mercado)
retorno_banco_do_brasil = retorno(lista = banco_do_brasil)
retorno_santander = retorno(lista = banco_santander)
retorno_bradesco = retorno(lista = banco_bradesco)

df_retornos = pd.DataFrame(data = {'retornos': [retorno_itau,retorno_banco_do_brasil,retorno_santander,retorno_bradesco,retorno_mercado]},
index = ['Itau','Banco Do Brasil','Banco Santander','Bando Bradesco','Ibovespa'])
#df_retornos É UM DATAFRAME
print(df_retornos)

print("")

df_retornos['retornos'] = df_retornos['retornos']*100
print(df_retornos)

print("")

df_retornos = df_retornos.sort_values(by = 'retornos', ascending = False)
#sort_values É USADO PARA ORDENAR VALORES DE UM DATAFRAME
#ASCENDING COLOCA A LISTA DO MENOR PRO MAIOR
print(df_retornos)

fig, ax = plt.subplots()
ax.bar(df_retornos.index,df_retornos['retornos'])
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
#COLOCA OS VALORES DO EIXO Y EM PORCENTAGEM
plt.xticks(fontsize = 7)
# ALTERA O TAMANHO DA FONTE DOS VALORES NO EIXO X
plt.title('Retorno dos Bancos')
plt.show()

var_lucro_bancos = lucro_bancos.iloc[-1]/lucro_bancos.iloc[0] - 1
#CALCULA O LUCRO DOS BANCOS
var_lucro_bancos = var_lucro_bancos*100
var_lucro_bancos = var_lucro_bancos.sort_values(ascending = False)

print("")
print(var_lucro_bancos)
print("")

fig, ax = plt.subplots()
ax.bar(var_lucro_bancos.index,var_lucro_bancos)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
plt.xticks(fontsize = 7)
plt.title('Lucro dos Bancos')
plt.show()

def resample_periodo(dado,periodo):
    dado_periodo_novo = dado.resample(f"{periodo}").last()
    dado_periodo_novo = dado_periodo_novo.pct_change()
    dado_periodo_novo = dado_periodo_novo.dropna()
    return dado_periodo_novo

itau_ano_a_ano = resample_periodo(banco_itau,"Y")
ibovespa_ano_a_ano = resample_periodo(dados_mercado,"Y")

itau_mes_a_mes = resample_periodo(banco_itau,"M")
ibovespa_mes_a_mes = resample_periodo(dados_mercado,"M")

print(itau_ano_a_ano)
print("")
print(ibovespa_ano_a_ano)
print("")

outperform_itau = itau_ano_a_ano-ibovespa_ano_a_ano
plt.title('outperform_itau')
plt.plot(outperform_itau)
plt.show()

meses_positivos = sum(outperform_itau > 0)/len(outperform_itau)
print(meses_positivos)

def long_short(long,short,periodo):
    var_long = resample_periodo(long,periodo)
    var_short = resample_periodo(short,periodo)
    outperform = var_long - var_short
    print(outperform)
    plt.title('outperform')
    plt.plot(outperform)
    plt.show()
    
long_short(banco_santander,dados_mercado,"Y")
    
