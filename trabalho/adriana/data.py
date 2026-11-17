import pandas as pd

# 1. Carregar os datasets originais

pv_geral = pd.read_csv('PV_geral.csv', sep=';')

# 2. Criar a sequência de horas para o ano de 2019 (com base no tamanho de cada um ou 8760 horas)
# Usamos len(pv_01) para garantir que o tamanho corresponde exatamente ao número de linhas do ficheiro
pv_geral['Datetime'] = pd.date_range(start='2019-01-01 00:00:00', periods=len(pv_geral), freq='h')


# 3. Guardar os novos ficheiros CSV (com a coluna Datetime incluída)
# O parâmetro index=False evita que o Pandas guarde o número da linha como uma coluna extra
pv_geral.to_csv('PV_geral_com_data.csv', sep=';', index=False)


print("Ficheiros guardados com sucesso!")