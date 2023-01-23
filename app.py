import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster import hierarchy

import streamlit as st

root = os.path.join("data_plot")

df_candidatos = pd.read_csv(os.path.join(root, "num_candidatos.csv"))
df_tentativas = pd.read_csv(os.path.join(root, "tentativas.csv"), index_col=0)
df_genero = pd.read_csv(os.path.join(root, "genero.csv"))
df_etnia = pd.read_csv(os.path.join(root, "etnia.csv"))
df_civil = pd.read_csv(os.path.join(root, "estado_civil.csv"))

st.title("Projeto para ML (CE042)")
st.markdown("""
Projeto para curso de Machine Learning UFPR feito por [Marcio Bulla Jr](https://www.linkedin.com/in/marcio-bulla-junior).

A Ideia do projeto  é responder a pergunta: 
Será que conhecendo as informações e histórico do candidato podemos adivinhar o partido que ele se candidatará?

A fonte das informações está disponível em [BaseDosDados.org](https://basedosdados.org/dataset/br-tse-eleicoes) 
e o código fonte está disposto no [meu GitHub](https://github.com/MarcioBulla/CE042/).

# Metodologia

Notei que para importar os dados usando a API da [base de dados](https://basedosdados.github.io/mais/api_reference_python/) 
realiza a *query* no Google Cloud. Desta forma, farei queries para onde a API retorna um objeto `DataFrame` do Pandas onde podemos realizar as analises, 
pois as tabelas do database tem milhões de linhas. Ou seja, é mais acessível realizar as queries de maneira que retornar os dados para os gráficos. 

Olhando o database como um todo vemos que há "3" tabelas uteis para nossa análise. 
Além disso, por simplicidade avaliaremos dados a partir de $2006$, 
pois os bens do candidato são só informados depois deste ano.

Para mais detalhes do projeto como bibliotecas utilizadas, código fonte, dentre outros 
pormenores está disponível no [meu GitHub](https://github.com/MarcioBulla/CE042/).


# Construindo Análises
Faremos análise por tabelas que temos interesse, lembrando que podemos relacionar as tabelas através da função `JOIN` do SQL.
Isso é de grande valia, pois se a tabela não ter a informação do partido candidatado `id_candidato_bd` e o `ano` podemos dizer qual o partido da pessoa.
Desta forma, listaremos as variáveis de interesse e em seguida faremos algumas perguntas que nossa análise responderá.

## `candidatos`
- `sigla_partido` TARGET
- `id_candidato_bd` index
- `ano`
- `genero`
- `sigla_uf_nacimento`
- `raca`
- `instrucao`
- `estado_civil`

### Perguntas
Será que isso influencia qual partido a pessoa seria?
- Numero de tentativas;
- Quantas vezes trocou de partido;
- Gênero;
- Região de nascimento;
- Etnia;
- Instrução;
- Estado civil.

## `bens_candidato`
- `id_candidato_bd` index
- `valor_item`
- `ano`

### Perguntas
Será que os bens da pessoa determina o partido de escolha?

## `Despesas_cadidato`
- `id_candidato_bd` index
- `ano`
- `valor_despesa`
- `tipo_prestacao_contas`
- `nome_partido`
- `sigla_uf`

### Perguntas
Talvez essa tabela fuja da ideia para a analise, 
pois quero saber qual partido a pessoa escolheria. 
E essa tabela há informações durante a candidatura. 
Porém, temos algumas perguntas.

- A despesa do candidato é uma caraterística do partido?
- O candidato de cada partido tem tendencia por um tipo de prestação de contas?
- Será esses perguntas também estão relacionadas com o local (estado ou região)?

# Análise
""")

list_partidos = df_candidatos.sigla_partido.values

slt_partido = st.multiselect(
    "Selecione os Partidos",
    list_partidos,
    list_partidos[:20],
    label_visibility="hidden"
)

def num_partido():
    global slt_partido, df_candidatos
    if len(slt_partido) == 0:
        return st.warning("Selecione pelo menos um partido", icon="⚠️")

    df = df_candidatos.set_index("sigla_partido").loc[slt_partido,:]
    df.sort_values("candidatos_partido",ascending=False , inplace=True)
    
    fig, ax = plt.subplots()
    
    g = sns.barplot(
        df.reset_index(), 
        y="sigla_partido", x="candidatos_partido", 
        ax=ax, palette="tab20")
    
    sns.despine()
    g.set_xlabel("Numero de candidatos")
    g.set_ylabel("Partido")
    
    st.pyplot(fig)
    
    with st.expander("Dados"):
        st.dataframe(df_candidatos)

num_partido()

st.markdown("""
Vemos que muito partidos tem menos amostras distintas, pelo 
fato de serem novos. O qual é o caso do UP, AGIR, NOVO e outros.

Além disso, provavelmente pessoas que tentaram mais 
vezes são de partido mais antigos, vamos avaliar isso com um dendrograma.


Número de candidatações influencia o partido que está, é claro que essa pergunta 
pode ser influenciada pela idade do partido. Mas podemos visualizar se esse partido 
novos tem pessoas que ja trocaram de partido.
""")


def n_cand():
    global df_tentativas
    
    Z = hierarchy.linkage(df_tentativas, method="centroid")
    
    fig, ax = plt.subplots()
    hierarchy.dendrogram(Z, orientation="left", labels=df_tentativas.index, ax=ax)
    
    ax.set_xticks([])
    ax.set_xticklabels([])
    sns.despine(left=True, bottom=True)
    
    st.pyplot(fig)
    
    with st.expander("Dados"):
        st.dataframe(df_tentativas)

n_cand()

st.markdown("""
Vemos que o candidatos dos partidos em amarelos são mais fieis. 
Observe que os partidos muito novos ou pouco conhecidos se misturam 
como o esperado note que na região verde os partido UNIÃO, PCB, NOVO, 
AGIR, UP e PCO são praticamente iguais, pois esses partido não terão 
tempo de pessoas se candidatarem varias vezes.


### E gênero, etnia e estado civil influencia?
""")


slt_crtc = st.selectbox(
    "Selecione a Característica",
    ('Gênero', 'Etnia', 'Estado Civil'))

slt_partido2 = st.multiselect(
    "Selecione os Partidos",
    list_partidos,
    list_partidos[:20],
    label_visibility="hidden",
    key="partidos2"
)


def crtc():
    global slt_partido2, slt_crtc, df_genero, df_etnia, df_civil
    if len(slt_partido2) == 0:
        return st.warning("Selecione pelo menos um partido", icon="⚠️")

    if slt_crtc == "Gênero":
        df = df_genero
        option = df.columns.tolist()[1:]
        slt_option = st.multiselect(
            "Selecione os Gêneros",
            option,
            option,
            label_visibility="hidden"
            )
    elif slt_crtc == "Etnia":
        df = df_etnia
        df.rename(columns={"nao_informado": "Não Informado"}, inplace=True)

        option = df.columns.tolist()[1:]
        
        slt_option = st.multiselect(
            "Selecione os Gêneros",
            option,
            option[:3],
            label_visibility="hidden"
            )
    else:
        df = df_civil
        df.rename(columns={"nao_informado": "Não Informado"}, inplace=True)

        option = df.columns.tolist()[1:]
        slt_option = st.multiselect(
            "Selecione os Gêneros",
            option,
            option[:2],
            label_visibility="hidden"
            )

    df_bk = df.copy()
    df.set_index("sigla_partido", inplace=True)
    df.drop(columns=list(set(option) - set(slt_option)), inplace=True)
    df = df.loc[slt_partido2,:]
    df_melted = df.melt(ignore_index=False).reset_index()

    ticks = np.arange(0, round(df_melted.value.max(), 1)+.05, .1)
    tickslabel = [f"{int(tick*100)}%" for tick in ticks]

    fig, ax = plt.subplots(figsize=(10,5))

    g = sns.barplot(df_melted,
            y="sigla_partido", hue="variable", x="value",
            palette="tab20", ax=ax)

    g.set_xlabel("Porcentagem")
    g.set_ylabel("Partidos")
    g.set_xticks(ticks)
    g.set_xticklabels(tickslabel)
    sns.despine()
    sns.move_legend(ax, "upper left", bbox_to_anchor=(1, 1))


    st.pyplot(fig)

    with st.expander("Dados"):
        st.dataframe(df_bk)

crtc()

with st.expander("Em Desenvolvimento"):
    st.warning("Infelizmente não consegui concluir, pois estou ocupado em meu TCC", icon="🥲")
    st.write("Pretendo responder todas as perguntas ditas no inicio.")