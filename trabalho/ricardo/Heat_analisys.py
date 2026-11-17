import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

ficheiros = {
    'ABR': 'C:\\Programming\\Redes\\Energy_Consumption_Prediction\\trabalho\\ricardo\\UVTgv_heat_ABR_2019_2020.csv',
    'C': 'C:\\Programming\\Redes\\Energy_Consumption_Prediction\\trabalho\\ricardo\\UVTgv_heat_C_2019_2020.csv',
    'ICSTM': 'C:\\Programming\\Redes\\Energy_Consumption_Prediction\\trabalho\\ricardo\\UVTgv_heat_demand_building_ICSTM_2019.csv',
}

dfs = {}

print('=== 1. CARREGAMENTO E ESTATÍSTICAS DOS DADOS ===\n')

for edificio, arquivo in ficheiros.items():
  df = pd.read_csv(arquivo, sep=';')

  df['datetime_2019'] = pd.date_range(start='2019-01-01', periods=len(df), freq='h')

  dfs[edificio] = df

  print(f'--- Edifício: {edificio} ---')
  print(df.describe())
  print(f"Valores em falta:\n{df.isnull().sum().to_dict()}\n")


plt.style.use('seaborn-v0_8-whitegrid')
fig, axes = plt.subplots(3, 1, figsize=(14, 12))

for edificio, df in dfs.items():
  col_2019 = [c for c in df.columns if '2019' in c][0]
  axes[0].plot(
      df['datetime_2019'],
      df[col_2019],
      label=f'Edifício {edificio}',
      alpha=0.7,
      linewidth=0.8,
  )

axes[0].set_title(
    'Comparação do Consumo Térmico Anual entre Edifícios (2019)',
    fontsize=12,
    weight='bold',
)
axes[0].set_ylabel('Consumo Térmico')
axes[0].legend(loc='upper right')

col_icstm_2019 = 'heat_ICSTM_2019'
sns.histplot(
    dfs['ICSTM'][col_icstm_2019],
    kde=True,
    ax=axes[1],
    color='darkorange',
    bins=50,
)
axes[1].set_title(
    'Distribuição e Variabilidade do Consumo (Edifício ICSTM)',
    fontsize=12,
    weight='bold',
)
axes[1].set_ylabel('Frequência')
axes[1].set_xlabel('Valor de Consumo')

df_icstm = dfs['ICSTM'].copy()
df_icstm['hour'] = df_icstm['datetime_2019'].dt.hour
hourly_mean = df_icstm.groupby('hour')[col_icstm_2019].mean()

axes[2].plot(
    hourly_mean.index,
    hourly_mean.values,
    marker='o',
    color='teal',
    linewidth=2,
)
axes[2].set_title(
    'Padrão Diário Médio - Consumo Térmico por Hora do Dia (ICSTM)',
    fontsize=12,
    weight='bold',
)
axes[2].set_ylabel('Consumo Médio')
axes[2].set_xlabel('Hora do Dia (0-23)')
axes[2].set_xticks(range(0, 24))

plt.tight_layout()

output_image = 'analise_exploratoria_todos_edificios.png'
plt.savefig(output_image, dpi=300)
print(f"Gráfico guardado com sucesso com o nome: '{output_image}'!")

plt.show()