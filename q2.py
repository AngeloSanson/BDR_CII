
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

dfca = pd.read_csv (r'F:\Downloads\casesTON.csv', parse_dates= ['date_ref'],encoding='utf-8-sig')
dfcred = pd.read_csv (r'F:\Downloads\credsTON.csv',parse_dates=["cred_date"], encoding='utf-8-sig')

#filtrando apenas os clientes que se credenciaram e abriram um chamado
dfcred = dfcred.dropna(subset=['accountid'])

dfca = dfca.dropna(subset=['accountid'])

innerjoin = dfca.merge(dfcred, on='accountid')

f=innerjoin.drop_duplicates("Unnamed: 0_x"); 

#filtrando chamados para o mesmo dia de credenciamento
h=f[(f['date_ref']==f['cred_date'])]

#separando o assunto pelo separador :
h[['Categoria', 'SubCategoria', 'Final']]= h["assunto"].str.split(pat=":", n=- 1, expand=True)
 
#obtendo o tamanho da categoria para em seguida somar
count_series = h.groupby(["Categoria", "Final"]).size()

#ajuste
qntchamarec= count_series.to_frame(name = 'size').reset_index()

#soma, media e contagem da "categoria"
acb=qntchamarec.groupby('Categoria')['size'].agg(['sum','count',"mean"])
Total = acb['sum'].sum()

#porcentagem 
acb["perc"] = acb["sum"].div(Total)*100

#fazendo a mesma coisa mas com o total e nao com osclientes do mesmo dia
f[['Categoria', 'SubCategoria', 'Final']]= f["assunto"].str.split(pat=":", n=- 1, expand=True)

count_seriestot = f.groupby(["Categoria", "Final"]).size()
qntchamarectot= count_seriestot.to_frame(name = 'size').reset_index()

acbtot=qntchamarectot.groupby('Categoria')['size'].agg(['sum','count',"mean"])
Total1 = acbtot['sum'].sum()

acbtot["perc"] = acbtot["sum"].div(Total1)*100

#ajustes
acbtot.reset_index(level=0, inplace=True) 
acb.reset_index(level=0, inplace=True) 
acb.replace(r'^\s*$', np.nan, regex=True, inplace = True)
acbtot.replace(r'^\s*$', np.nan, regex=True, inplace = True)
acbtot = acbtot.fillna('Sem Categoria')
acb = acb.fillna('Sem Categoria')

index = acbtot["Categoria"]

y_label=pd.DataFrame(acbtot["perc"])

y_label["percday"] = acb["perc"]

acb=acb.append({'Categoria' : 'Telecom' , 'perc' : 0} , ignore_index=True)

#plotando o grafico
Fams = acbtot["Categoria"]
Fams1 = acb["Categoria"]

plt.figure(figsize=[10, 10])
X = np.arange(len(Fams))
X2 = np.arange(len(Fams1))
plt.barh(X-0.25, acbtot["perc"],color='green', height=0.4)
plt.barh(X2+0.25, acb["perc"],color='black', height=0.4)
plt.xlabel('aaa')
plt.yticks([i for i in range(len(Fams1))],Fams1)
plt.savefig('ABC')
acb["percr"]=acb["perc"].round(3)
acbtot["percr"]=acbtot["perc"].round(3)
for i,j in zip(X, acb["percr"]):
    plt.annotate(float(j),xy=(j,i+0.25), fontsize=6, weight='bold')
for i,j in zip(X, acbtot["percr"]):
     plt.annotate(float(j),xy=(j,i-0.25), fontsize=6, weight='bold')

plt.xlabel('Percentual de Números Chamados Diariamente')
plt.ylabel('Categorias do Suporte')


# subcategorias=qntchamarectot.groupby('Final')['size'].agg(['sum','count',"mean"])
# Totalsubcat = subcategorias['sum'].sum()

# acbtot["perc"] = acbtot["sum"].div(Total1)*100


# subcategorias["perc"] = subcategorias["sum"].div(Total1)*100


# subcategorias.to_excel(r'F:\Chamados_SubCategoria_Total.xlsx', index = True)


# plt.savefig('GrafQ2.jpeg')




