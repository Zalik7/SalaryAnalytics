import pandas as pd
import plotly.express as px
import streamlit as st

df = pd.read_excel('SalaryData.xlsx', header= None).T
df.columns = df.iloc[0]
df = df.iloc[1:].rename(columns={'Финансовая деятельность':'Финансы', 
                                 'Здравоохранение и предоставление социальных услуг': 'Здравоохранение' })
df['Год'] = df['Год'].astype('int')

df_inflation = pd.read_excel('InflationData.xlsx')

df = pd.merge(df, df_inflation, on='Год', how='left')

df['Финансы_р'] = (df['Финансы'] - df['Финансы'].shift().fillna(0) * df['Инфляция']/ 100)
df['Образование_р'] = (df['Образование'] - df['Образование'].shift().fillna(0) * df['Инфляция']/ 100)
df['Здравоохранение_р'] = (df['Здравоохранение'] - df['Здравоохранение'].shift().fillna(0) * df['Инфляция']/ 100)

df[['Финансы_р', 'Образование_р', 'Здравоохранение_р', 'Финансы', 'Образование', 'Здравоохранение']] = df[['Финансы_р', 'Образование_р', 'Здравоохранение_р', 'Финансы', 
                                                                                                           'Образование', 'Здравоохранение']].astype('int')

fig = px.line(df, x='Год', y = ['Финансы', 'Образование', 'Здравоохранение'],
             title='Динамика номинальных зарплат в сфере финансов, образования и здравоохранения (в руб.)',
             labels={'value': 'Зарплата', 'variable': 'Отрасль'},
             hover_data={'Год':True, 'variable':True,'value':':.2f'})

fig.update_yaxes(title_text=None)
fig.update_layout(legend_title_text='Отрасль')

fig.show()

fig = px.line(df, x='Год', y = ['Финансы_р', 'Образование_р', 'Здравоохранение_р'],
             title='Динамика реальных зарплат в сфере финансов, образования и здравоохранения (в руб.)',
             labels={'value': 'Зарплата', 'variable': 'Отрасль'},
             hover_data={'Год':True, 'variable':True,'value':':.2f'})

fig.update_yaxes(title_text=None)
fig.update_layout(legend_title_text='Отрасль')

fig.show()