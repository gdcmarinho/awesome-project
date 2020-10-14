import pandas as pd

raw_df = pd.read_csv('LINKS.md', sep='\n', names=['column']) # Lê o arquivo

md_titles = list(raw_df[raw_df['column'].str.startswith('##')].index) # Cria lista com os nomes de cada categoria
md_titles.append(len(raw_df)) # Adiciona o index do fim do dataframe 
tuples = [(md_titles[idx], md_titles[idx+1]) for idx in range(len(md_titles)-1)] # Cria tuplas com os intervalos (de cada categoria) a serem ordenados

regex_df = raw_df[~raw_df['column'].str.startswith('##')] # Links da lista
raw_df['regex'] = regex_df['column'].str.extract(r'(?:\*{1}[ ]\[)([\w .,()\-=+&%/:*#$@!?|<>]*)(?:\])') # Regex para extrair somente o que tem dentro de cada []
raw_df['regex'] = raw_df['regex'].str.lower() # Deixa todas as letras minúsculas (para ordenar ignorando as letras maiusculas)

# Escreve no arquivo
with open('LINKS.md', 'w') as f:
    for t in tuples:
        f.write(raw_df.iloc[t[0]]['column'] + '\n') # Escreve nome da categoria
        df = raw_df[t[0]+1 : t[1]] # Seleciona o intervalo
        df = df.sort_values('regex') # Ordena a categoria
        df['column'].apply(lambda x: f.write(x + '\n')) # Escreve as linhas com links
        f.write('\n') # Adiciona uma linha vazia entre cada categoria
