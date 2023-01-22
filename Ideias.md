# Variaveis de Interesse


## `candidatos`
- `id_candidato_bd` index
- `ano`
- `genero`
- `sigla_uf_nacimento`
- `sigla_partido` TARGET
- `raca`
- `instrucao`
- `estado_civil`

### Perguntas
Será que isso influencia qual partido a pessoa seria?
- Numero de tentativas;
- Quantas vezes trocou de partido;
- Genero;
- Regial de nacimento;
- Etnia;
- Instrução;
- Estado civil.

## `bens_candidato`
- `id_candidato_bd` index
- `valor_item`
- `ano`

### Perguntas
Será que essas informações também influenciam?
- Pessoas com mais bens determina o partido;

## `Despesas_cadidato`
- `id_candidato_bd` index
- `valor_despesa`
- `tipo_prestacao_contas`
- `nome_partido`
- `sigla_uf`

### Perguntas
Talvez essa tabela fuja da ideia para a analise, pois queriamos saber qual partido a pessoa escolheria. E essa tabela há informações durante a candidatura. Porém, temos algumas perguntas.

- A despesa do candidato é uma cariteristica do partido?
- O candidado de cada partido tem endencia por um tipo de prestação de contas?
- Será esses perguntas tb se relaciona com o local (estado ou região)?