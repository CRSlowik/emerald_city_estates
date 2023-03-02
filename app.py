# Importando bibliotecas
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import folium
from streamlit_folium import folium_static
import streamlit as st


# Funções
def clean_code(df):
    """Substitui outlier de bedrooms,
    Formata coluna date para datetime,
    Cria coluna de ano de venda,
    Cri coluna de estação do ano,
    retorna df limpo"""

    # Tratando outliers
    df.loc[df['bedrooms'] == 33, 'bedrooms'] = 3  # Substituindo outlier de bedrooms

    # Manipulando os dados
    df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')  # Formatando date para datetime

    df['year'] = df['date'].dt.year  # Coluna ano de venda

    df['month'] = df['date'].dt.month  # Coluna estação do ano
    summer = [6, 7, 8]
    autumn = [9, 10, 11]
    winter = [12, 1, 2]
    spring = [3, 4, 5]
    df.loc[df['month'].isin(summer), 'seasons'] = 'Verão'
    df.loc[df['month'].isin(autumn), 'seasons'] = 'Outono'
    df.loc[df['month'].isin(winter), 'seasons'] = 'Inverno'
    df.loc[df['month'].isin(spring), 'seasons'] = 'Primavera'

    return df


def recomnd_old_houses(df):
    """Calcula a mediana de preço,
    Define os imóveis com mais de 10 anos,
    Remove os imóveis com má condição,
    Remove imóveis acima da mediana de preço,
    retorna imóveis restantes
    """
    # Imóveis recomendados
    # Sem vista
    # Calculando a mediana
    old_houses_median = df.loc[df['yr_built'] <= 2005, 'price'].median()

    # Definindo imóveis com mais de 10 anos
    old_houses = pd.DataFrame(df.loc[df['yr_built'] <= 2005])

    # Removendo imóveis antigos com má condição
    old_houses_remove_cond = old_houses.loc[old_houses['condition'] < 3]
    old_houses = old_houses.drop(old_houses_remove_cond.index)

    # Removendo imóveis antigos com preço acima da mediana
    old_houses_remove_median = old_houses.loc[old_houses['price'] >= old_houses_median]
    old_houses = old_houses.drop(old_houses_remove_median.index)

    # Removendo imóveis antigos com vista para a água
    old_houses_remove_water = old_houses.loc[old_houses['waterfront'] == 1]
    old_houses = old_houses.drop(old_houses_remove_water.index)

    # Removendo imóveis antigos reformados
    old_houses_remove_renov = old_houses.loc[old_houses['yr_renovated'] != 0]
    old_houses = old_houses.drop(old_houses_remove_renov.index)

    # Removendo imóveis antigos com 3 banheiros ou mais
    old_houses_remove_bath = old_houses.loc[old_houses['bathrooms'] >= 3]
    old_houses = old_houses.drop(old_houses_remove_bath.index)

    # Removendo imóveis antigos com 3 quartos ou mais
    old_houses_remove_bed = old_houses.loc[old_houses['bedrooms'] >= 3]
    old_houses = old_houses.drop(old_houses_remove_bed.index)

    # Definindo o lucro
    old_houses['median_price'] = df.loc[df['yr_built'] <= 2005, 'price'].median()
    old_houses['profit'] = old_houses[['price', 'median_price']].apply(lambda x: x['median_price'] - x['price'], axis=1)

    old_houses_buy = old_houses
    return old_houses_buy


def recomnd_waterview_houses(df):
    """Calcula a mediana do preço,
    Define imóveis com vista para a água,
    Remove imóveis com má condição,
    Remove imóveis com preço acima da mediana,
    Remove imóveis com má vista para a água,
    retorna imóveis restantes
    """
    # Com vista
    # Calculando a mediana dos imóveis com vista para a água
    waterview_houses_median = df.loc[df['waterfront'] == 1, 'price'].median()

    # Definindo imóveis com vista para a água
    waterview_houses = pd.DataFrame(df.loc[df['waterfront'] == 1])

    # Removendo imóveis com vista para a água com má condição
    waterview_houses_remove_cond = waterview_houses.loc[waterview_houses['condition'] < 3]
    waterview_houses = waterview_houses.drop(waterview_houses_remove_cond.index)

    # Removendo imóveis com vista para a água com preço acima da mediana
    waterview_houses_remove_median = waterview_houses.loc[waterview_houses['price'] >= waterview_houses_median]
    waterview_houses = waterview_houses.drop(waterview_houses_remove_median.index)

    # Removendo imóveis com má vista para a água
    waterview_houses_remove_view = waterview_houses.loc[waterview_houses['view'] <= 2]
    waterview_houses = waterview_houses.drop(waterview_houses_remove_view.index)

    # Definindo o lucro
    waterview_houses['median_price'] = df.loc[df['waterfront'] == 1, 'price'].median()
    waterview_houses['profit'] = waterview_houses[['price', 'median_price']].apply(
        lambda x: x['median_price'] - x['price'],
        axis=1)

    waterview_houses_buy = waterview_houses
    return waterview_houses_buy


def graphic_region(df):
    """Cria um df da medéia de preçoa agrupado pelo zipcode,
    plota esse df em um gráfico de barra"""
    price_per_region = df[['price', 'zipcode']].groupby(['zipcode']).mean().reset_index()
    font = {'family': 'serif',
            'color': 'darkred',
            'weight': 'normal',
            'size': 40,
            }
    fig_1 = plt.figure(figsize=(20, 6))
    sns.barplot(x=price_per_region['zipcode'], y=price_per_region['price'], palette='flare')
    plt.title('Preço por região', fontdict=font)
    plt.xticks(rotation=50)
    return fig_1


def graphic_situation(df):
    """Cria um df com casas construidas com antes de 2005,
    Cria outro df com casas construidas depois de 2005,
    Cria um df com casas que foram reformadas,
    Plota em um gráfico de barras os três dfs"""
    new_houses = df.loc[df.yr_built >= 2005, 'price'].mean()
    old_houses = df.loc[df.yr_built <= 2005, 'price'].mean()
    renovated_houses = df.loc[df.yr_renovated != 0, 'price'].mean()
    valores = ['Casas novas', 'Casas velhas', 'Casas reformadas']
    imoveis = [new_houses, old_houses, renovated_houses]

    fig = plt.figure(figsize=(20, 6))
    plt.subplot(1, 2, 2)
    plt.pie(imoveis,
            labels=list(valores),
            colors=["#20B2AA", "#E0FFFF", "#66CDAA"],
            autopct='%1.1f%%',
            labeldistance=1.1,
            explode=[0, 0.1, 0],
            wedgeprops={"ec": "k"},
            textprops={"fontsize": 15},
            )
    plt.axis("equal")
    plt.title("Comparação de preços: novas, velhas e reformadas")
    plt.legend()
    return fig


def graphic_bath(df):
    """Cria um df com casas com 3 banheiros ou mais,
    Cria um df com casas com menos de 3 banheiros,
    Plota esses dfs em um gráfico de pizza"""
    bath_3 = df.loc[df['bathrooms'] >= 3, 'price'].mean()
    bath_2 = df.loc[df['bathrooms'] < 3, 'price'].mean()
    valores_2 = ['3 ou mais', 'menos de 3']
    imoveis_2 = [bath_3, bath_2]

    fig = plt.figure(figsize=(20, 6))
    plt.subplot(1, 2, 2)
    plt.pie(imoveis_2,
            labels=list(valores_2),
            colors=["#2F4F4F", "#8FBC8F"],
            autopct='%1.1f%%',
            labeldistance=1.1,
            explode=[0, 0.1],
            wedgeprops={"ec": "k"},
            textprops={"fontsize": 15},
            )
    plt.axis("equal")
    plt.title("Comparação de preços: banheiros")
    plt.legend()
    return fig


def graphic_bed(df):
    """Cria um df com casas com 3 quartos ou mais,
        Cria um df com casas com menos de 3 quartos,
        Plota esses dfs em um gráfico de pizza"""
    bed_3 = df.loc[df['bedrooms'] >= 3, 'price'].mean()
    bed_2 = df.loc[df['bedrooms'] < 3, 'price'].mean()
    valores_3 = ['3 ou mais', 'Menos de 3']
    imoveis_3 = [bed_3, bed_2]

    fig = plt.figure(figsize=(20, 6))
    plt.subplot(1, 2, 2)
    plt.pie(imoveis_3,
            labels=list(valores_3),
            colors=["#556B2F", "#BDB76B"],
            autopct='%1.1f%%',
            labeldistance=1.1,
            explode=[0, 0.1],
            wedgeprops={"ec": "k"},
            textprops={"fontsize": 15},
            )
    plt.axis("equal")
    plt.title("Comparação de preços: quartos")
    plt.legend()
    return fig


def graphic_waterview(df):
    """Cria um df com a média de preço de casas com vista para a água,
        Cria um df com a média de preço de casas sem vista para a água,
        Plota esses df em um gráfico de pizza"""
    waterview_1 = df.loc[df['waterfront'] == 1, 'price'].mean()
    waterview_0 = df.loc[df['waterfront'] == 0, 'price'].mean()
    valores_4 = ['Com vista', 'Sem vista']
    imoveis_4 = [waterview_1, waterview_0]

    fig = plt.figure(figsize=(20, 6))
    plt.subplot(1, 2, 2)
    plt.pie(imoveis_4,
            labels=list(valores_4),
            colors=["#66CDAA", "#98FB98"],
            autopct='%1.1f%%',
            labeldistance=1.1,
            explode=[0, 0.1],
            wedgeprops={"ec": "k"},
            textprops={"fontsize": 15},
            )
    plt.axis("equal")
    plt.title("Comparação de preços: vista para à água")
    plt.legend()
    return fig


def graphic_seasons(df):
    """Cria um df para média de preço agrupado pela estação do ano,
    plota um gráfico de linha com o df"""
    price_per_seasons = df[['price', 'seasons']].groupby(['seasons']).mean()
    fig = plt.figure(figsize=(20, 6))
    sns.lineplot(data=price_per_seasons, x="seasons", y="price")
    return fig


def recomend_map(df_lat, df_long, df_id, df_price, df_latw, df_longw, df_idw, df_pricew):
    """Cria uma variável com a função fulium.Map,
    Cria um loop for concatenando 4 df para inserir um marcador para cada item do df adicionando a variavel,
    Cria o mesmo loop para outros 4 df,
    Retorna a variável"""
    maps = folium.Map(location=[47.6063, -122.3323], tiles="Stamen Toner", zoom_start=13)

    for lat, long, id, price in zip(df_lat, df_long, df_id, df_price):
        folium.Marker(location=[lat, long], popup=('sem vista', 'id', id, 'price', price),
                      icon=folium.Icon(color='red')).add_to(maps)

    for lat, long, id, price in zip(df_latw, df_longw, df_idw, df_pricew):
        folium.Marker(location=[lat, long],
                      popup=('com vista', 'id', id, 'price', price),
                      icon=folium.Icon(color='blue', icon='cloud')).add_to(maps)
    return maps


# Extração do arquivo
df = pd.read_csv("dataset/kc_house_data.csv")

df1 = clean_code(df)
df2 = recomnd_old_houses(df1)
df3 = recomnd_waterview_houses(df1)


# Conversão para float
df_lat = df2['lat'].astype(float)
df_long = df2['long'].astype(float)
df_id = df2['id']
df_price = df2['price'].astype(float)

df_latw = df3['lat'].astype(float)
df_longw = df3['long'].astype(float)
df_idw = df3['id']
df_pricew = df3['price'].astype(float)

# App no Streamlit

# Cabeçalho
st.title('Emerald City Estates')
st.markdown("""___""")

# Layout
tab0, tab1, tab2, tab3 = st.tabs(['Página Incial', 'Análise', 'Resultados', 'Mapa'])
with tab0:
    st.markdown('# Boas Vindas')
    st.markdown('Bem-vindo ao nosso Dashboard de Imóveis em Seattle! Aqui, você encontrará um mapa com os'
                ' melhores imóveis da cidade, criteriosamente escolhidos pela nossa equipe especializada da '
                'Emerald City Estates. Com anos de experiência no mercado imobiliário local, nossos especialistas'
                ' realizam análises detalhadas para encontrar as melhores oportunidades de investimento para você.')
    st.markdown('Em nosso Dashboard, oferecemos informações detalhadas sobre a análise realizada, incluindo os'
                ' principais critérios que afetam os preços dos imóveis. Não perca a chance de investir nos melhores'
                ' imóveis de Seattle. Com a ajuda da Emerald City Estates, você pode tomar decisões '
                'informadas e seguras no mercado imobiliário local.')

with tab1:
    with st.container():
        st.title('Base de dados')
        st.dataframe(df, 1000, 400)
        st.markdown("""___""")

    with st.container():
        st.title('Comparação de preço por região')
        fig_1 = graphic_region(df1)
        st.pyplot(fig_1)
        st.markdown("""___""")

    with st.container():
        st.title('Analisando características')
        col1, col2 = st.columns(2)

        with col1:
            st.markdown('### Situação')
            fig_2 = graphic_situation(df1)
            st.pyplot(fig_2)
            st.markdown('Imóveis reformados são 43,9% mais caros que imóveis velhos')

        with col2:
            st.markdown('### Banheiros')
            fig_3 = graphic_bath(df1)
            st.pyplot(fig_3)
            st.markdown('Imóveis com 3 banheiros ou mais se mostraram 105,6% mais caros do que imóveis'
                        ' com menos de 3 banheiros')

    with st.container():
        col_1, col_2 = st.columns(2)

        with col_1:
            st.markdown('### Quartos')
            fig_4 = graphic_bed(df1)
            st.pyplot(fig_4)
            st.markdown('Imóveis com 3 quartos ou mais se mostraram 42,26% mais caros do que'
                        ' imóveis com menos de 3 quartos')

        with col_2:
            st.markdown('### Vista para água')
            fig_5 = graphic_waterview(df1)
            st.pyplot(fig_5)
            st.markdown('Imóveis com vista para à água são 212,6% mais caros que imóveis sem vista para à água')
        st.markdown("""___""")

    with st.container():
        st.markdown('## Comparação de preço por estação do ano')
        fig_6 = graphic_seasons(df1)
        st.pyplot(fig_6)

        st.markdown('Imóveis vendidos na primavera são 6,5% mais caros que imóveis vendidos no inverno')

with tab2:
    st.markdown('# Resultados')
    st.markdown('Com base nas análises realizadas, verificou-se que o crescimento anual dos imóveis se manteve baixo,'
                ' em torno de 0,5% de aumento. Diante disso, a busca por imóveis com preços abaixo da mediana se'
                ' apresenta como a melhor alternativa para aquisição.')
    st.markdown('Além disso, os imóveis com vista para água se mostraram interessantes, já que apresentam um preço'
                ' médio 212,6% mais alto do que os demais. Apesar de demandarem um maior investimento para aquisição,'
                ' a compra de um imóvel com preço abaixo da mediana e sua revenda por um valor próximo à mediana pode'
                ' gerar grandes lucros. Com base nesse critério, foram selecionados 73 imóveis que podem ser'
                ' comercializados dessa forma, gerando um lucro em torno de 42,4 milhões de dólares.')
    st.markdown('Considerando ainda que imóveis reformados são, em média, 43,9% mais caros que os imóveis com mais'
                ' de 10 anos que não foram reformados, foram selecionados 1660 imóveis abaixo da mediana de preços'
                ' que podem ser reformados. Foi levada em conta também a possibilidade de adicionar mais quartos e'
                ' banheiros, visto que imóveis com 3 ou mais quartos são 42,46% mais caros e imóveis com 3 ou mais'
                ' banheiros são 105,6% mais caros. Os imóveis selecionados apresentam menos de 3 quartos e 3 banheiros.'
                ' A venda desses imóveis pela mediana, sem levar em conta a reforma, pode gerar um lucro em torno de'
                ' 251,2 milhões de dólares.')
    st.markdown('Por fim, considerando que a compra dos imóveis seja realizada no inverno e a venda na primavera,'
                ' é possível obter um aumento de 6,5%.')

with tab3:
    st.title('Localização dos imóveis recomendados')
    maps_1 = recomend_map(df_lat, df_long, df_id, df_price, df_latw, df_longw, df_idw, df_pricew)
    folium_static(maps_1)
