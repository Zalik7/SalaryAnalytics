import pandas as pd
import plotly.express as px
import streamlit as st

# Load data
df = pd.read_excel('data/SalaryData.xlsx', header=None).T
df.columns = df.iloc[0]
df = df.iloc[1:].rename(columns={'Финансовая деятельность': 'Финансы', 
                                 'Здравоохранение и предоставление социальных услуг': 'Здравоохранение'})
df['Год'] = df['Год'].astype('int')

df_inflation = pd.read_excel('data/InflationData.xlsx')
df = pd.merge(df, df_inflation, on='Год', how='left')

# Calculate real wages
df['Финансы_р'] = (df['Финансы'] - df['Финансы'].shift().fillna(0) * df['Инфляция'] / 100)
df['Образование_р'] = (df['Образование'] - df['Образование'].shift().fillna(0) * df['Инфляция'] / 100)
df['Здравоохранение_р'] = (df['Здравоохранение'] - df['Здравоохранение'].shift().fillna(0) * df['Инфляция'] / 100)

df[['Финансы_р', 'Образование_р', 'Здравоохранение_р', 'Финансы', 'Образование', 'Здравоохранение']] = \
    df[['Финансы_р', 'Образование_р', 'Здравоохранение_р', 'Финансы', 'Образование', 'Здравоохранение']].astype('int')

# Streamlit App
st.title('Динамика зарплат в различных отраслях')

# Year slicer
years = st.sidebar.slider('Выберите годы', min_value=int(df['Год'].min()), max_value=int(df['Год'].max()), value=(2010, 2020))

# Filter data based on selected years
filtered_df = df[(df['Год'] >= years[0]) & (df['Год'] <= years[1])]

# Visualization for nominal wages
st.header('Динамика номинальных зарплат')
fig_nominal = px.line(filtered_df, x='Год', y=['Финансы', 'Образование', 'Здравоохранение'],
                      title='Динамика номинальных зарплат в сфере финансов, образования и здравоохранения (в руб.)',
                      labels={'value': 'Зарплата', 'variable': 'Отрасль'},
                      hover_data={'Год': True, 'variable': True, 'value': ':.2f'})
fig_nominal.update_yaxes(title_text=None)
fig_nominal.update_layout(legend_title_text='Отрасль')
st.plotly_chart(fig_nominal, use_container_width=True)

# Conclusion text for nominal wages
st.write("""
<div style="width: 100%; text-align: justify;">
    <p><b>Вывод:</b> На графике выше видим, что номинальные зарплаты в сфере финансов кратно превышают номинальные доходы в сфере образования и здравоохранения. И эта разница со временем только увеличивалась в связи с бОльшим темпом роста доходов в финансовой сфере по сравнению с образовательной и медицинской сферами.</p>
    <p>Номинальные зарплаты в сфере здравоохранения незначительно превышают зарплаты в сфере образования. Отрыв увеличился в 2018 году.</p>
</div>
""", unsafe_allow_html=True)



# Visualization for real wages
st.header('Динамика реальных зарплат')
fig_real = px.line(filtered_df, x='Год', y=['Финансы_р', 'Образование_р', 'Здравоохранение_р'],
                   title='Динамика реальных зарплат в сфере финансов, образования и здравоохранения (в руб.)',
                   labels={'value': 'Зарплата', 'variable': 'Отрасль'},
                   hover_data={'Год': True, 'variable': True, 'value': ':.2f'})
fig_real.update_yaxes(title_text=None)
fig_real.update_layout(legend_title_text='Отрасль')
st.plotly_chart(fig_real, use_container_width=True)

# Conclusion text for real wages
st.write("""
<div style="width: 100%; text-align: justify;">
    <p><b>Вывод:</b> Динамика реальных зарплат в целом повторяет динамику номинальных показателей. При этом реальная зарплата в пандемийный 2021 год незначительно снизилась в сфере здравоохранения. В пандемийный период 2020-2022 реальная зарпалата в сфере финансов значительно увеличилась.</p>
</div>
""", unsafe_allow_html=True)
